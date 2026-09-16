// pages/index/index.js
Page({
  data: {
    code0: '',
    code1: '',
    code2: '',
    code3: '',
    errorMsg: '',
    focusIndex: 0
  },

  onLoad() {
    this.checkInviteCode()
  },

  onShow() {
    this.checkInviteCode()
  },

  // 检查本地是否已验证过邀请码
  checkInviteCode() {
    const verifiedCode = wx.getStorageSync('inviteCode')
    if (verifiedCode === '9527') {
      // 已验证，直接跳转到 tabBar
      wx.switchTab({
        url: '/pages/questions/index'
      })
    }
  },

  // 输入邀请码
  onCodeInput(e) {
    const index = parseInt(e.currentTarget.dataset.index)
    const value = e.detail.value

    // 更新对应的输入框
    this.setData({
      [`code${index}`]: value
    })

    // 如果输入了数字，自动聚焦到下一个输入框
    if (value && index < 3) {
      // 使用 setTimeout 确保在下一个事件循环中设置焦点
      setTimeout(() => {
        this.setData({
          focusIndex: index + 1
        })
      }, 50)
    }

    // 自动验证：当输入第四位后
    if (index === 3 && value) {
      setTimeout(() => {
        this.verifyInviteCode()
      }, 100)
    }
  },

  // 验证邀请码
  verifyInviteCode() {
    const { code0, code1, code2, code3 } = this.data
    const inviteCode = code0 + code1 + code2 + code3
    const validCode = '9527'

    if (inviteCode.length !== 4) {
      return
    }

    if (inviteCode === validCode) {
      // 验证通过，显示提示
      wx.showToast({
        title: '验证通过',
        icon: 'success',
        duration: 1500
      })

      // 保存到本地
      wx.setStorageSync('inviteCode', inviteCode)

      // 延迟跳转到 tabBar
      setTimeout(() => {
        wx.switchTab({
          url: '/pages/questions/index'
        })
      }, 1500)
    } else {
      this.setData({
        errorMsg: '邀请码错误，请重试',
        code0: '',
        code1: '',
        code2: '',
        code3: '',
        focusIndex: 0
      })
    }
  }
})