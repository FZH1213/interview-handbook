// pages/summary/index.js
Page({
  data: {
    userInfo: null,
    hasUserInfo: false,
    mastered: 0,
    toImprove: 0,
    donationList: [],
    currentDonation: 0,
    donationVisible: true
  },

  onLoad() {
    this.loadUserData()
    this.initDonationList()
    this.startDonationAnimation()
  },

  onShow() {
    this.loadUserData()
  },

  onUnload() {
    if (this.donationTimer) {
      clearInterval(this.donationTimer)
    }
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

  // 初始化模拟打赏数据
  initDonationList() {
    const donationList = [
      { name: '老徐**', amount: '3.33' },
      { name: '3号**', amount: '6.66' },
      { name: 'sh**', amount: '8.88' },
      { name: '阿s**', amount: '5.20' },
      { name: '远在**', amount: '0.99' },
      { name: '林在**', amount: '1.88' }
    ]
    this.setData({ donationList })
  },

  // 开始打赏动画
  startDonationAnimation() {
    this.donationTimer = setInterval(() => {
      let next = this.data.currentDonation + 1
      if (next >= this.data.donationList.length) {
        next = 0
      }
      // 先隐藏，切换数据，再显示
      this.setData({ donationVisible: false })
      setTimeout(() => {
        this.setData({
          currentDonation: next,
          donationVisible: true
        })
      }, 300)
    }, 5000)
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