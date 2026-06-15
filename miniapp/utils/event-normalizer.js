const DEFAULT_SUMMARY = '暂无摘要，建议打开详情查看原始内容。';

const toText = (value, fallback = '') => {
  if (value === null || value === undefined) return fallback;
  const text = String(value).trim();
  return text || fallback;
};

const toNumber = (value, fallback = 0) => {
  const number = Number(value);
  return Number.isFinite(number) ? number : fallback;
};

const toPlatforms = (platforms) => {
  if (Array.isArray(platforms)) {
    return platforms.map(item => toText(item)).filter(Boolean);
  }
  const platform = toText(platforms);
  return platform ? [platform] : [];
};

const normalizeEvent = (event = {}) => {
  const platforms = toPlatforms(event.platforms);

  return {
    ...event,
    id: toText(event.id || event.event_id || event.title),
    title: toText(event.title, '未命名情报'),
    summary: toText(event.summary || event.content, DEFAULT_SUMMARY),
    category: toText(event.category, '综合'),
    platforms,
    credibility: toText(event.credibility, '待观察'),
    risk_level: toText(event.risk_level, '低'),
    creative_value: toNumber(event.creative_value),
    max_rank: toNumber(event.max_rank || event.rank),
    angles: Array.isArray(event.angles) ? event.angles.filter(Boolean) : [],
    suggestion: toText(event.suggestion)
  };
};

const normalizeEvents = (events) => {
  return Array.isArray(events) ? events.map(normalizeEvent) : [];
};

const isGithubEvent = (event = {}) => {
  return toPlatforms(event.platforms).includes('GitHub Trending');
};

module.exports = {
  normalizeEvent,
  normalizeEvents,
  isGithubEvent
};
