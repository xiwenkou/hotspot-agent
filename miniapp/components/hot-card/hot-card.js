Component({
  properties: {
    item: {
      type: Object,
      value: {}
    }
  },
  methods: {
    onTap() {
      if (!this.data.item || !this.data.item.id) {
        wx.showToast({
          title: '缺少情报详情',
          icon: 'none'
        });
        return;
      }
      wx.navigateTo({
        url: `/pages/detail/detail?id=${this.data.item.id}`
      });
    }
  }
})
