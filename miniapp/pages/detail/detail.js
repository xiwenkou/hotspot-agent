const { request } = require('../../utils/request.js');
const { normalizeEvent } = require('../../utils/event-normalizer.js');

Page({
  data: {
    event: null,
    loading: true,
    error: ''
  },

  onLoad(options) {
    if (options.id) {
      this.fetchDetail(options.id);
    } else {
      this.setData({
        loading: false,
        error: '缺少情报 ID，无法加载详情'
      });
    }
  },

  fetchDetail(id) {
    this.setData({ loading: true, error: '' });
    request(`/hot-events/${id}`)
      .then(data => {
        this.setData({
          event: normalizeEvent(data),
          loading: false
        });
      })
      .catch((err) => {
        const message = err && err.message ? err.message : '详情加载失败，请返回后重试';
        this.setData({ loading: false, error: message });
      });
  }
});
