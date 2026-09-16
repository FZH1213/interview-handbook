// pages/marked/list.js
Page({
  data: {
    type: '',
    title: '',
    questions: [],
    showDetail: false,
    currentQuestion: {}
  },

  onLoad(options) {
    const type = options.type || 'mastered'
    this.setData({
      type,
      title: type === 'mastered' ? '已摸清' : '待加强'
    })
    this.loadQuestions()
  },

  onShow() {
    this.loadQuestions()
  },

  loadQuestions() {
    const storageKey = this.data.type === 'mastered' ? 'masteredQuestions' : 'toImproveQuestions'
    const questions = wx.getStorageSync(storageKey) || {}

    // 转换为数组并按时间倒序排序
    const questionList = Object.values(questions).sort((a, b) => b.timestamp - a.timestamp)

    this.setData({
      questions: questionList
    })
  },

  // 删除标记
  removeQuestion(e) {
    const index = e.currentTarget.dataset.index
    const storageKey = this.data.type === 'mastered' ? 'masteredQuestions' : 'toImproveQuestions'
    const questions = wx.getStorageSync(storageKey) || {}

    delete questions[index]

    wx.setStorageSync(storageKey, questions)

    // 更新计数
    this.updateSummaryCount()

    // 刷新列表
    this.loadQuestions()
  },

  // 更新总结页面的数量
  updateSummaryCount() {
    const mastered = wx.getStorageSync('masteredQuestions') || {}
    const toImprove = wx.getStorageSync('toImproveQuestions') || {}
    wx.setStorageSync('masteredCount', Object.keys(mastered).length)
    wx.setStorageSync('toImproveCount', Object.keys(toImprove).length)
  },

  // 显示题目详情
  showQuestionDetail(e) {
    const index = e.currentTarget.dataset.index
    const question = this.data.questions.find(q => q.index === index)
    if (question) {
      this.setData({
        showDetail: true,
        currentQuestion: question
      })
    }
  },

  // 关闭题目详情
  closeQuestionDetail() {
    this.setData({
      showDetail: false,
      currentQuestion: {}
    })
    // 刷新列表
    this.loadQuestions()
  }
})