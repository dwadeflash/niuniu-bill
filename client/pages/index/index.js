//index.js
//获取应用实例
const app = getApp()
var config = require("../../config")
var types = ['default', 'primary', 'warn']

Page({
  data: {
    motto: '欢迎大妞妞！',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo')
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
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
                  wx.redirectTo({
                    url: '/pages/list/list',
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
  onLoad: function () {
    var that = this;
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
      this.login(app.globalData.userInfo)
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
          this.login(res.userInfo)
        }
      })
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
          this.login(res.userInfo)
        }
      })
    }
  },
  getUserInfo: function (e) {
    console.log(e)
    var that = this;
    wx.request({
      url: app.host,
      data: {
        userInfo: e.detail.userInfo
      },
      success: function (res) {
        app.globalData.userInfo = e.detail.userInfo
        that.setData({
          userInfo: e.detail.userInfo,
          motto: res.data,
          hasUserInfo: true
        })
      }
    })
  }
})
