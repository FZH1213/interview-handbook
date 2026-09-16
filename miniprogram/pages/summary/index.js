// pages/summary/index.js
Page({
  data: {
    userInfo: null,
    hasUserInfo: false,
    mastered: 0,
    toImprove: 0
  },

  onLoad() {
    this.loadUserData()
  },

  onShow() {
    this.loadUserData()
  },

  loadUserData() {
    // 从本地存储加载用户数据
    const userInfo = wx.getStorageSync('userInfo')
    const mastered = wx.getStorageSync('masteredCount') || 0
    const toImprove = wx.getStorageSync('toImproveCount') || 0

    this.setData({
      userInfo,
      hasUserInfo: !!userInfo,
      mastered,
      toImprove
    })
  },

  // 获取用户信息
  getUserProfile() {
    wx.getUserProfile({
      desc: '用于展示用户信息',
      success: (res) => {
        const userInfo = res.userInfo
        wx.setStorageSync('userInfo', userInfo)
        this.setData({
          userInfo,
          hasUserInfo: true
        })
      }
    })
  },

  // 跳转到已摸清列表
  goToMastered() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  },

  // 跳转到待加强列表
  goToToImprove() {
    wx.showToast({
      title: '功能开发中',
      icon: 'none'
    })
  }
})