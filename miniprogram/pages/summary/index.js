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
    const userInfo = wx.getStorageSync('userInfo') || {}
    const mastered = wx.getStorageSync('masteredCount') || 0
    const toImprove = wx.getStorageSync('toImproveCount') || 0

    this.setData({
      userInfo,
      hasUserInfo: !!userInfo.avatarUrl,
      mastered,
      toImprove
    })
  },

  // 选择头像
  onChooseAvatar(e) {
    const { avatarUrl } = e.detail
    const userInfo = this.data.userInfo || {}
    userInfo.avatarUrl = avatarUrl
    wx.setStorageSync('userInfo', userInfo)
    this.setData({
      userInfo,
      hasUserInfo: true
    })
  },

  // 获取昵称
  onNicknameChange(e) {
    const nickname = e.detail.value
    const userInfo = this.data.userInfo || {}
    userInfo.nickName = nickname
    wx.setStorageSync('userInfo', userInfo)
    this.setData({
      userInfo
    })
  },

  // 跳转到已摸清列表
  goToMastered() {
    wx.navigateTo({
      url: '/pages/marked/list?type=mastered'
    })
  },

  // 跳转到待加强列表
  goToToImprove() {
    wx.navigateTo({
      url: '/pages/marked/list?type=toImprove'
    })
  }
})