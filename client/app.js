//app.js
var config = require("./config")

App({
  onLaunch: function () {
    var that = this;
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res1 => {
        console.log('login result:' + res1)
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
        // 获取用户信息
        wx.getSetting({
          success: res2 => {
            if (res2.authSetting['scope.userInfo']) {
              // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
              wx.getUserInfo({
                success: res3 => {
                  // 可以将 res 发送给后台解码出 unionId
                  this.globalData.userInfo = res3.userInfo
                  wx.request({
                    url: config.service.host + '/login',
                    data: {
                      code: res1.code,
                      userInfo: res3.userInfo
                    },
                    success: res => {
                      console.log('host login result:' + res)
                    }
                  })
                  // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
                  // 所以此处加入 callback 以防止这种情况
                  if (this.userInfoReadyCallback) {
                    this.userInfoReadyCallback(res3)
                  }
                }
              })
            }
          }
        })
      }
    })
  },
  globalData: {
    userInfo: null
  },
  host: config.service.host
})