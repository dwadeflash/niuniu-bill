//index.js
//获取应用实例
const app = getApp()
var config = require("../../config")
var types = ['default', 'primary', 'warn']
var sliderWidth = 96;

Page({
  data: {
    motto: '欢迎大妞妞！',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    tabs: ["申请列表", "提交申请"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0,
    amount: '',
    memo: '',
    memoTip: '0/200'
  },
  //事件处理函数
  bindViewTap: function () {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        motto: "老婆，来一发？",
        hasUserInfo: true
      })
    } else if (this.data.canIUse) {
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          motto: "老婆，来一发？",
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
    wx.hideShareMenu()
  },
  getUserInfo: function (e) {
    console.log(e)
    var that = this;
    wx.request({
      url: app.host + '/login',
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
  },
  getApproveList: function () {
    var that = this
    wx.request({
      url: app.host + '/list',
      method: 'GET',
      data: {},
      header: {
        'content-type': 'application/json'
      },
      header: {
        "sessionId": wx.getStorageSync("sessionId")
      },
      success: function (res) {
        that.setData({
          approveList: res.data.data
        });
      }
    })
  },
  onLoad: function (options) {
    var that = this;
    wx.getSystemInfo({
      success: function (res) {
        that.setData({
          sliderLeft: sliderWidth / 2,
          sliderOffset: res.windowWidth / that.data.tabs.length * that.data.activeIndex
        });
      }
    });
    this.getApproveList()
  },
  tabClick: function (e) {
    this.setData({
      sliderOffset: e.currentTarget.offsetLeft,
      activeIndex: e.currentTarget.id
    });
  },
  onPullDownRefresh: function () {
    console.log("onPullDownRefresh")
    this.getApproveList()
    wx.stopPullDownRefresh()
  },
  approve: function (event) {
    console.log(event)
    var dataset = event.currentTarget.dataset
    if (dataset.status != 1) {
      return;
    }
    if (dataset.applicantid == app.globalData.userInfo.id) {
      return;
    }
    wx.showActionSheet({
      itemList: ['同意', '不同意'],
      success: function (res) {
        console.log(res)
        if (!res.cancel) {
          console.log(res.tapIndex)
          wx.request({
            url: app.host + '/approve',
            method: "POST",
            data: {
              "approveId": dataset.id,
              "status": res.tapIndex + 2,
              "memo": "",
              "amount": dataset.amount
            },
            header: {
              "sessionId": wx.getStorageSync("sessionId")
            },
            success: function (result) {
              console.log(result)
              if (!result.data.success) {
                /*wx.navigateTo({
                  url: '/pages/msg/msg_fail'
                })*/
                wx.showToast({
                  title: '操作失败！',
                  icon: 'none',
                  duration: 1500
                });
              } else {
                wx.showToast({
                  title: '已完成',
                  icon: 'success',
                  duration: 1500
                });
                wx.startPullDownRefresh();
              }
            }
          })
        }
      }
    });
  },
  submitApprove: function (e) {
    var that = this
    /*
    wx.request({
      url: app.host + '/create',
      data: {
        'amount': that.data.amount,
        'memo': that.data.memo
      },
      header: {
        'sessionId': wx.getStorageSync("sessionId")
      },
      method: 'POST',
      success: function (res) {
        if (res.data.success == "true") {
          that.setData({
            amount: '',
            memo: '',
            sliderOffset: 0,
            activeIndex: 0
          })
          wx.showToast({
            title: '提交成功',
            icon: 'success',
            duration: 1500
          })
          wx.startPullDownRefresh()
        } else {
          wx.showToast({
            title: res.data.errorMsg,
            icon: 'none',
            duration: 1500
          });
        }
      },
      fail: function (res) { },
      complete: function (res) { }
    })*/
    wx.showShareMenu({
      withShareTicket: true
    })
  },
  bindAmountInput: function (e) {
    this.setData({
      amount: e.detail.value
    })
  },
  bindMemoInput: function (e) {
    this.setData({
      memo: e.detail.value,
      memoTip: e.detail.value.length + '/200'
    })
  },
  onShareAppMessage: function (res) {
    var that = this
    if (res.from === 'button') {
      // 来自页面内转发按钮
      console.log(res.target)
    }
    return {
      title: '我提交了一个花钱申请',
      path: '/pages/list/list?applicantId=' + app.globalUserInfo,
      success: function (res) {
        // 转发成功
        console.log(res)

      }
    }
  }
})
