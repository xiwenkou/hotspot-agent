const { request } = require('../../utils/request.js');
const {
  normalizeEvents,
  isGithubEvent
} = require('../../utils/event-normalizer.js');

Page({
  data: {
    hotEvents: [],
    filteredEvents: [],
    activeTab: 'news', // 'news' or 'github'
    loading: true,
    error: '',
    lastUpdated: '',
    subtitleText: '正在同步今日热点'
  },

  onLoad() {
    this.fetchHotEvents();
  },

  onPullDownRefresh() {
    this.fetchHotEvents().then(() => {
      wx.stopPullDownRefresh();
    });
  },

  switchTab(e) {
    const tab = e.currentTarget.dataset.tab;
    this.setData({ activeTab: tab });
    this.filterData();
  },

  filterData() {
    const all = this.data.hotEvents || [];
    let filtered = [];
    if (this.data.activeTab === 'news') {
      filtered = all.filter(e => !isGithubEvent(e));
    } else {
      filtered = all.filter(isGithubEvent);
    }
    this.setData({
      filteredEvents: filtered,
      subtitleText: this.data.loading ? '正在同步今日热点' : `已呈现 ${filtered.length} 条高价值信息`
    });
  },

  fetchHotEvents() {
    this.setData({
      loading: true,
      error: '',
      subtitleText: '正在同步今日热点'
    });
    return request('/hot-events/today')
      .then(data => {
        const events = normalizeEvents(data);
        this.setData({
          hotEvents: events,
          loading: false,
          lastUpdated: this.formatTime(new Date())
        });
        this.filterData();
      })
      .catch((err) => {
        const message = err && err.message ? err.message : '暂时无法获取热点情报，请稍后重试';
        this.setData({ loading: false, error: message, filteredEvents: [] });
      });
  },

  retryFetch() {
    this.fetchHotEvents();
  },

  formatTime(date) {
    const pad = value => String(value).padStart(2, '0');
    return `${pad(date.getHours())}:${pad(date.getMinutes())}`;
  }
});
