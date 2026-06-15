const assert = require('node:assert/strict');
const {
  normalizeEvent,
  normalizeEvents,
  isGithubEvent
} = require('../utils/event-normalizer.js');

const normalized = normalizeEvent({
  id: 42,
  title: '  New model release  ',
  platforms: 'GitHub Trending',
  creative_value: '8',
  risk_level: '高'
});

assert.equal(normalized.id, '42');
assert.equal(normalized.title, 'New model release');
assert.deepEqual(normalized.platforms, ['GitHub Trending']);
assert.equal(normalized.creative_value, 8);
assert.equal(normalized.risk_level, '高');
assert.equal(normalized.category, '综合');
assert.equal(normalized.summary, '暂无摘要，建议打开详情查看原始内容。');
assert.equal(isGithubEvent(normalized), true);

assert.deepEqual(normalizeEvents(null), []);
assert.equal(isGithubEvent(normalizeEvent({ platforms: ['微博热搜'] })), false);

console.log('event normalizer tests passed');
