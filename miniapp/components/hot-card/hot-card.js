Component({
  properties: {
    item: {
      type: Object,
      value: {}
    }
  },
  methods: {
    onTap() {
      wx.navigateTo({
        url: `/pages/detail/detail?id=${this.data.item.id}`
      });
    }
  }
})
