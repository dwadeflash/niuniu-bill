var app = getApp()
var sliderWidth = 96;
Page({
  data: {
    tabs: ["申请列表", "提交申请"],
    activeIndex: 0,
    sliderOffset: 0,
    sliderLeft: 0,
    approveList: [],
    amount: '',
    memo: '',
    memoTip: '0/200',
    amountValid: true
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
    if (app.globalData.options.scene == 1007) {
      if (app.globalData.options.query.applicantId) {
        wx.request({
          url: app.host + '/acceptrelation',
          method: "POST",
          data: {
            "applicantId": app.globalData.options.query.applicantId
          },
          header: {
            "sessionId": wx.getStorageSync("sessionId")
          },
          success: function (result) {

          }
        })
      }
    }
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
  onPullDownRefresh: function() {
    console.log("onPullDownRefresh")
    this.getApproveList()
    wx.stopPullDownRefresh()
  },
  approve: function(event) {
    console.log(event)
    var dataset = event.currentTarget.dataset
    if(dataset.status != 1) {
      return;
    }
    if(dataset.applicantid == app.globalData.userInfo.id) {
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
              "approveId" : dataset.id,
              "status": res.tapIndex + 2,
              "memo": "",
              "amount": dataset.amount
            },
            header: {
              "sessionId" : wx.getStorageSync("sessionId")
            },
            success: function(result) {
              console.log(result)
              if(!result.data.success) {
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
  submitApprove: function() {
    var amount = this.data.amount
    if(undefined == amount || amount == '' || isNaN(amount) || amount <=0 ) {
      this.setData({
        amountValid: false
      })
      return
    }
    var that = this
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
      success: function(res) {
        if(res.data.success) {
          /*wx.showToast({
            title: '提交成功',
            icon: 'success',
            duration: 1500
          })*/
          wx.showShareMenu({

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
      fail: function(res) {},
      complete: function(res) {}
    })
  },
  bindAmountInput: function(e) {
    var amount = e.detail.value
    this.setData({
      amount: amount
    })
    if (undefined == amount || amount == '' || isNaN(amount)|| amount <= 0) {
      this.setData({
        amountValid: false
      })
    } else {
      this.setData({
        amountValid: true
      })
    }
  },
  bindMemoInput: function (e) {
    this.setData({
      memo: e.detail.value,
      memoTip: e.detail.value.length + '/200'
    })
  },
  onShareAppMessage: function(e) {
    var that = this
    return {
      title: '我提交了一个啪啪啪的申请',
      path: '/pages/list/list?applicantId' + app.globalData.userInfo.id,
      success: function (res) {
        that.setData({
          amount: '',
          memo: '',
          sliderOffset: 0,
          activeIndex: 0,
          memoTip:'0/200'
        })
      },
      fail: function (res) {
        // 转发失败
      }
    }
  }
})