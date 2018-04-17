//app.js
var config = require("./config")

App({
  onLaunch: function (options) {
    console.log(options)
    this.globalData.options = options
  },
  onShow: function(options) {
    console.log(options)
    this.globalData.options = options
  },
  login: function (userInfo) {
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
              // 可以将 res 发送给后台解码出 unionId
              app.globalData.userInfo = userInfo
              wx.request({
                url: config.service.host + '/login',
                data: {
                  code: res1.code,
                  userInfo: userInfo
                },
                success: res => {
                  console.log('host login result:' + res.data)
                  app.globalData.userInfo.id = res.data.id
                  wx.setStorageSync('sessionId', res.data.sessionId)
                  wx.request({
                    url: app.host + '/queryrelation',
                    header: {
                      'sessionId': wx.getStorageSync("sessionId")
                    },
                    method: 'GET',
                    success: function (res) {
                      if (res.data.success) {
                        wx.redirectTo({
                          url: '/pages/list/list',
                        })
                      }
                    }
                  })
                }
              })
              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res3)
              }
            }
          }
        })
      }
    })
  },
  globalData: {
    userInfo: null,
    options: null
  },
  host: config.service.host
})