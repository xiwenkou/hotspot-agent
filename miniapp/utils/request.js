const app = getApp();

const request = (url, method = 'GET', data = {}) => {
  return new Promise((resolve, reject) => {
    // 这里简单获取全局 URL，也可以直接写死如果还没拿到 app 实例
    const baseUrl = 'http://127.0.0.1:8000/api';
    
    wx.request({
      url: `${baseUrl}${url}`,
      method: method,
      data: data,
      header: {
        'content-type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data.data); // 直接剥离出 data 层
        } else {
          wx.showToast({
            title: '服务器异常',
            icon: 'error'
          });
          reject(res);
        }
      },
      fail: (err) => {
        wx.showToast({
          title: '网络请求失败',
          icon: 'none'
        });
        reject(err);
      }
    });
  });
};

module.exports = {
  request
};
