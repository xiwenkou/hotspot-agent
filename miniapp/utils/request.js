const app = getApp();

const request = (url, method = 'GET', data = {}) => {
  return new Promise((resolve, reject) => {
    const baseUrl = (app.globalData && app.globalData.apiUrl) || '';
    
    wx.request({
      url: `${baseUrl}${url}`,
      method: method,
      data: data,
      header: {
        'content-type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode === 200) {
          const responseData = res.data;
          if (responseData && responseData.code && Number(responseData.code) !== 200) {
            wx.showToast({
              title: responseData.message || '服务返回异常',
              icon: 'none'
            });
            reject(responseData);
          } else if (responseData && responseData.data !== undefined) {
            resolve(responseData.data);
          } else {
            resolve(responseData || null);
          }
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
