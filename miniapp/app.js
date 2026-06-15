App({
  onLaunch() {
    console.log('App Launch');
  },
  globalData: {
    // 【第一阶段重构】准备对接云端 URL 或微信云托管环境
    // 请在部署后将此处替换为真实的云托管/服务器 API 域名
    apiUrl: 'https://your-cloud-run-domain.com/api',
    
    // 本地开发备用
    localApiUrl: 'http://127.0.0.1:8000/api'
  }
})
