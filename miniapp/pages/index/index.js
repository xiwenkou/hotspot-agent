const { request } = require('../../utils/request.js');

Page({
  data: {
    hotEvents: [],
    loading: true
  },

  onLoad() {
    this.fetchHotEvents();
  },

  onPullDownRefresh() {
    this.fetchHotEvents().then(() => {
      wx.stopPullDownRefresh();
    });
  },

  fetchHotEvents() {
    this.setData({ loading: true });
    return request('/hot-events/today')
      .then(data => {
        // 由于我们在模型里标签是 JSON string 或者 array，如果后端返回有变化可以在这里 format
        // 但我们在后端直接用 JSON 存了，返回的应该就是对象
        this.setData({
          hotEvents: data || [],
          loading: false
        });
      })
      .catch(() => {
        this.setData({ loading: false });
      });
  }
});
