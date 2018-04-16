//app.js
var config = require("./config")

App({
  onLaunch: function (options) {
    console.log(options)
    this.globalData.options = options
  },
  globalData: {
    userInfo: null,
    options: null
  },
  host: config.service.host
})