// pages/index/index.js
Page({
  data: {},

  goToBasic() {
    wx.switchTab({
      url: '/pages/basic/content'
    })
  },

  goToAdvanced() {
    wx.switchTab({
      url: '/pages/advanced/content'
    })
  }
})