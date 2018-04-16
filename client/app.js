//app.js
var config = require("./config")

App({
  onLaunch: function () {
    
  },
  globalData: {
    userInfo: null
  },
  host: config.service.host
})