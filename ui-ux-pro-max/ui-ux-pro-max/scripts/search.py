#!/usr/bin/env python3
import argparse
import sys
import csv
import re
from pathlib import Path

# Built-in knowledge base for various domains
DOMAINS = {
    "product": [
        "SaaS: Optimized for information hierarchy, workflow efficiency, and responsive grid layouts.",
        "Fintech: High-density data grids, strict tabular number styling, and reassuring security visual indicators.",
        "E-commerce: Focus on product-grid clarity, easy-to-tap filters, responsive imagery, and seamless checkout flows.",
        "Healthcare: Calm color palettes (teals/blues), clear type scaling for accessibility, and simple navigation paths.",
        "Beauty/Spa/Wellness: Elegant Serif typography, warm tones, high-quality images, and minimal decorative borders."
    ],
    "style": [
        "Glassmorphism: Uses translucent card layers with backdrop-blur, thin borders, and vibrant backing gradients to create depth.",
        "Claymorphism: 3D pastel shapes, inner shadows, and soft ambient drop shadows to look friendly and playful.",
        "Minimalism: Focuses on whitespace, crisp type, strict grid alignments, and high text contrast.",
        "Brutalism: High contrast borders, bold primary colors, raw layout grids, and oversized typography.",
        "Neumorphism: Soft extruded shapes created by combining dual drop shadows (light source top-left, shadow bottom-right).",
        "Bento Grid: Grid of multi-sized cards representing individual features, highly readable and popular for SaaS."
    ],
    "typography": [
        "Elegant Serif: Playfair Display for headers, Outfit/Inter for body. Best for luxury, spa, and beauty brands.",
        "Modern Sans: Inter for headers, Inter/Roboto for body. High readability, best for SaaS, admin tools, and utilities.",
        "Playful Sans: Quicksand for headers, Open Sans for body. Friendly, rounded corners, best for education and children.",
        "Technical Monospace: JetBrains Mono for headers/body. Best for code editors, developer tools, and fintech charts."
    ],
    "color": [
        "Warm Ochre & Warm Sand: HSL(24, 45%, 45%) with HSL(34, 30%, 96%). Soft, premium wellness theme.",
        "Deep Slate & Tech Blue: HSL(222, 47%, 11%) with HSL(217, 91%, 60%). Trustworthy fintech theme.",
        "Classic Navy & Emerald: HSL(215, 60%, 16%) with HSL(150, 60%, 40%). Professional corporate/e-commerce theme.",
        "Electric Neon & Cyber Dark: HSL(280, 85%, 60%) with HSL(220, 20%, 3%). Social and entertainment theme."
    ],
    "landing": [
        "Hero-centric with Live Chart: Places the product core visual (like an interactive chart or form) above the fold.",
        "Hero with Large Media & Social Proof: Big warm hero image, followed immediately by testimonials and client logos.",
        "Feature Grid: Layout of key features arranged in a 3-column grid or Bento box design with micro-animations.",
        "Pricing Matrix: Clean tables contrasting plans, emphasizing the 'Most Popular' with visual indicators (e.g. badges)."
    ],
    "chart": [
        "Trend Line: Simple line chart with subtle area under the curve; avoid heavy shadow grids, use locale-aware formatted axis.",
        "Comparison Bar: Horizontal bar chart for small mobile viewports, vertical for desktop.",
        "Proportion Donut: Use only if categories <= 5, otherwise fallback to comparison bar."
    ],
    "ux": [
        "color-contrast: Minimum 4.5:1 ratio for normal text (WCAG AA) to ensure accessibility. Never use gray-on-gray.",
        "touch-target-size: Interactive area must be >= 44x44pt on iOS / 48x48dp on Android. Use hitSlop to improve touch accessibility.",
        "reduced-motion: Respect media query prefers-reduced-motion to disable animations for accessibility.",
        "layout-shift-avoid: Keep aspect-ratio on images, reserve space for async loaders to prevent CLS.",
        "inline-validation: Validate form fields on blur, not on active keystrokes."
    ],
    "google-fonts": [
        "Inter: High-performance variable sans-serif font designed for screens.",
        "Playfair Display: Elegant serif font with high contrast strokes.",
        "Outfit: Geometric, friendly sans-serif font ideal for headers.",
        "JetBrains Mono: Developer-friendly monospaced font with great number readability."
    ],
    "react": [
        "Minimize re-renders: Use React.memo, useMemo, and useCallback for computationally expensive children.",
        "Virtualize list: Virtualize datasets with 50+ items using packages like FlashList or FlatList on mobile.",
        "Suspense: Split heavy routes/components with lazy loading, wrapping them in Suspense with a skeleton placeholder."
    ],
    "web": [
        "Use viewport meta: width=device-width, initial-scale=1 (never disable zoom).",
        "Semantic HTML: Leverage <main>, <nav>, <section>, and <article> tags for native screen reader parsing.",
        "Aria labels: Use aria-label on icon-only buttons to ensure screen reader accessibility."
    ],
    "prompt": [
        "Minimalist CSS prompt: 'Use absolute layout symmetry, generous whitespace, Inter typography, slate-900 text, and white surfaces.'",
        "Vibrant theme prompt: 'Electric purple accent, deep slate backdrop, cyber glassmorphism overlays, and neon micro-glows.'"
    ]
}

STACK_RN = [
    "Touch Targets: Keep buttons and Pressables >= 44x44pt. Use hitSlop={{top: 10, bottom: 10, left: 10, right: 10}} to expand touch hit area.",
    "Lists: Use FlatList with getItemLayout, or Shopify FlashList, for smooth scrolling. Set removeClippedSubviews=true.",
    "Safe Areas: Wrap screens in SafeAreaView from react-native-safe-area-context to clear notches and home indicators.",
    "Animations: Leverage Animated API with useNativeDriver=true, or use Reanimated for 60fps performance on main-thread-free UI.",
    "Typography: Support system font scaling with dynamic size calculations; avoid hardcoded container heights that clip large text."
]

DEFAULT_RECOMMENDATION = {
    "ProductType": "General SaaS / Web App",
    "Style": "Minimalism / Clean UI",
    "ColorPalette": "Deep Slate & Cool Gray",
    "Typography": "Modern Sans (Inter / Roboto)",
    "LandingStructure": "Feature Grid & Pricing Matrix",
    "Effects": "Soft elevations & Clean borders",
    "AntiPatterns": "Excessive layout shifts, Redundant animations, Low text contrast"
}


def load_reasoning_rules(csv_path: Path):
    rules = []
    if not csv_path.exists():
        return rules
    try:
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rules.append(row)
    except Exception as e:
        print(f"Warning: Failed to load CSV data: {e}", file=sys.stderr)
    return rules


def match_design_system(query: str, rules: list) -> dict:
    if not query:
        return DEFAULT_RECOMMENDATION
    
    query_lower = query.lower()
    for rule in rules:
        keyword = rule.get("Keyword", "").strip().lower()
        if keyword and keyword in query_lower:
            return rule
            
    # Sub-matching
    words = re.findall(r'\w+', query_lower)
    for word in words:
        for rule in rules:
            keyword = rule.get("Keyword", "").strip().lower()
            if keyword and word == keyword:
                return rule
                
    return DEFAULT_RECOMMENDATION


def render_ascii_box(title: str, recommendation: dict) -> str:
    lines = [
        f"DESIGN SYSTEM RECOMMENDATION: {title}",
        "-" * 60,
        f"Product Type     : {recommendation.get('ProductType')}",
        f"Design Style     : {recommendation.get('Style')}",
        f"Color Palette    : {recommendation.get('ColorPalette')}",
        f"Typography Pairing: {recommendation.get('Typography')}",
        f"Landing Structure: {recommendation.get('LandingStructure')}",
        f"Visual Effects   : {recommendation.get('Effects')}",
        f"Anti-Patterns    : {recommendation.get('AntiPatterns')}"
    ]
    
    max_len = max(len(line) for line in lines)
    box_width = max_len + 4
    
    output = []
    output.append("+" + "-" * (box_width - 2) + "+")
    for line in lines:
        if line == "-" * 60:
            output.append("+" + "-" * (box_width - 2) + "+")
        else:
            padding = box_width - len(line) - 4
            output.append(f"| {line}" + " " * padding + " |")
    output.append("+" + "-" * (box_width - 2) + "+")
    
    return "\n".join(output)


def render_markdown(title: str, recommendation: dict) -> str:
    md = [
        f"# Design System: {title}",
        "",
        f"- **Product Type**: {recommendation.get('ProductType')}",
        f"- **Style**: {recommendation.get('Style')}",
        f"- **Color Palette**: {recommendation.get('ColorPalette')}",
        f"- **Typography**: {recommendation.get('Typography')}",
        f"- **Landing Structure**: {recommendation.get('LandingStructure')}",
        f"- **Effects**: {recommendation.get('Effects')}",
        f"- **Anti-Patterns to Avoid**: {recommendation.get('AntiPatterns')}",
        ""
    ]
    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="UI/UX Design Intelligence Search CLI")
    parser.add_argument("query", nargs="?", default="", help="Search keywords or product descriptors")
    parser.add_argument("--design-system", action="store_true", help="Generate a comprehensive design system")
    parser.add_argument("-p", "--project", default="Project Name", help="Project name for design system header")
    parser.add_argument("-f", "--format", choices=["ascii", "markdown"], default="ascii", help="Output layout format")
    parser.add_argument("--persist", action="store_true", help="Save the output design system to local files")
    parser.add_argument("--page", help="Save output for a specific page name instead of MASTER.md")
    parser.add_argument("--domain", choices=list(DOMAINS.keys()), help="Perform a detailed search on a design domain")
    parser.add_argument("--stack", help="Filter rules for a specific technical stack (e.g. react-native)")
    parser.add_argument("-n", "--limit", type=int, default=10, help="Max number of search results to return")

    args = parser.parse_args()

    # Load custom rules
    script_dir = Path(__file__).parent
    csv_path = script_dir.parent / "data" / "ui-reasoning.csv"
    rules = load_reasoning_rules(csv_path)

    # 1. Design System Generation
    if args.design_system:
        recommendation = match_design_system(args.query, rules)
        
        if args.format == "ascii":
            output = render_ascii_box(args.project, recommendation)
        else:
            output = render_markdown(args.project, recommendation)
            
        print(output)
        
        if args.persist:
            md_output = render_markdown(args.project, recommendation)
            dest_dir = Path("design-system")
            if args.page:
                dest_dir = dest_dir / "pages"
                dest_file = dest_dir / f"{args.page.lower()}.md"
            else:
                dest_file = dest_dir / "MASTER.md"
                
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file.write_text(md_output, encoding="utf-8")
            print(f"\n[Success] Design system persisted to: {dest_file}")
        return

    # 2. Domain Detailed Search
    if args.domain:
        print(f"=== Domain Search Results: [{args.domain}] ===")
        kb = DOMAINS[args.domain]
        query = args.query.lower()
        
        matched = []
        for item in kb:
            if not query or query in item.lower():
                matched.append(item)
                
        for i, item in enumerate(matched[:args.limit], 1):
            print(f"{i}. {item}")
            
        if not matched:
            print("No matching design patterns found.")
        return

    # 3. Stack Guidelines
    if args.stack:
        stack_normalized = args.stack.lower().replace("_", "-")
        if stack_normalized == "react-native":
            print("=== React Native UI/UX Guidelines ===")
            query = args.query.lower()
            matched = []
            for item in STACK_RN:
                if not query or query in item.lower():
                    matched.append(item)
            for i, item in enumerate(matched[:args.limit], 1):
                print(f"{i}. {item}")
            if not matched:
                print("No matching stack guidelines found.")
        else:
            print(f"Notice: Stack '{args.stack}' is currently using generic guidelines.")
            # Fallback to general advice
            for i, item in enumerate(DOMAINS["react"][:args.limit], 1):
                print(f"{i}. {item}")
        return

    # 4. Fallback search (Global Keyword Search across all domains)
    if args.query:
        print(f"=== Global Search Results for: '{args.query}' ===")
        found = False
        query_lower = args.query.lower()
        for dom_name, items in DOMAINS.items():
            domain_matches = [it for it in items if query_lower in it.lower()]
            if domain_matches:
                found = True
                print(f"\n[{dom_name.upper()}]:")
                for it in domain_matches[:args.limit]:
                    print(f"  - {it}")
        if not found:
            print("No matches found across any domain. Try different keywords.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
