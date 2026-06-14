App({
  onLaunch() {
    console.log('App Launch');
  },
  globalData: {
    // 后端本地接口地址
    // 记得在微信开发者工具勾选 "不校验合法域名"
    apiUrl: 'http://127.0.0.1:8000/api'
  }
})
