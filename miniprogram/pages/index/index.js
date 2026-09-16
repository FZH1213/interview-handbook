// pages/index/index.js
Page({
  data: {},

  goToQuestions() {
    wx.switchTab({
      url: '/pages/questions/index'
    })
  },

  goToSummary() {
    wx.switchTab({
      url: '/pages/summary/index'
    })
  }
})