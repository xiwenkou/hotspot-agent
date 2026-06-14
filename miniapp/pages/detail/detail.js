const { request } = require('../../utils/request.js');

Page({
  data: {
    event: null,
    loading: true
  },

  onLoad(options) {
    if (options.id) {
      this.fetchDetail(options.id);
    }
  },

  fetchDetail(id) {
    request(`/hot-events/${id}`)
      .then(data => {
        this.setData({
          event: data,
          loading: false
        });
      })
      .catch(() => {
        this.setData({ loading: false });
      });
  }
});
