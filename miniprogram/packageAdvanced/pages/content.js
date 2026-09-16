// pages/advanced/content.js
const app = getApp()

Page({
  data: {
    sections: [],
    currentSection: '',
    searchText: '',
    allQuestions: [],
    displayQuestions: [],
    total: 0,
    loadedCount: 0,
    hasMore: true,
    showBackTop: false,
    currentChunk: 0,
    showDetail: false,
    currentQuestion: {}
  },

  onLoad() {
    this.loadSections()
    this.loadNextChunk()
    this.loadMarks()
  },

  onShow() {
    if (this.data.showBackTop) {
      this.setData({ showBackTop: false })
    }
    this.loadMarks()
  },

  // 加载标记数据
  loadMarks() {
    const mastered = wx.getStorageSync('masteredQuestions') || {}
    const toImprove = wx.getStorageSync('toImproveQuestions') || {}

    // 更新显示的问题列表中的标记状态
    const displayQuestions = this.data.displayQuestions.map(q => ({
      ...q,
      isMastered: !!mastered[q.index],
      isToImprove: !!toImprove[q.index]
    }))

    this.setData({ displayQuestions })
  },

  // 加载章节索引
  loadSections() {
    const sectionsData = require('../data/sections.js')
    // 为每个章节添加唯一索引
    const sections = sectionsData.sections.map((s, idx) => ({
      ...s,
      id: idx
    }))
    this.setData({
      sections,
      total: sectionsData.total
    })
  },

  // 加载下一个数据块
  loadNextChunk() {
    const chunk = this.data.currentChunk
    let questions = null

    // 直接require，不能使用动态路径
    if (chunk === 0) {
      questions = require('../data/questions_0.js')
    } else if (chunk === 1) {
      questions = require('../data/questions_1.js')
    } else if (chunk === 2) {
      questions = require('../data/questions_2.js')
    } else {
      this.setData({ hasMore: false })
      return
    }

    // 添加序号并转换简化字段名
    const allQuestions = [...this.data.allQuestions]
    questions.questions.forEach((q, idx) => {
      q.index = questions.startIndex + idx + 1
      q.section = q.s
      q.title = q.t
      q.summary = q.m
      q.followUp = q.f.map(f => ({
        question: f.q,
        answer: f.a
      }))
    })

    allQuestions.push(...questions.questions)

    this.setData({
      allQuestions,
      displayQuestions: this.filterQuestions(allQuestions, this.data.currentSection, this.data.searchText),
      loadedCount: allQuestions.length,
      currentChunk: this.data.currentChunk + 1,
      hasMore: this.data.currentChunk + 1 < 3  // 3个数据块
    })

    // 加载标记状态
    this.loadMarks()
  },

  // 显示题目详情
  showQuestionDetail(e) {
    const index = e.currentTarget.dataset.index
    const question = this.data.displayQuestions[index]
    this.setData({
      showDetail: true,
      currentQuestion: question
    })
  },

  // 关闭题目详情
  closeQuestionDetail() {
    this.setData({
      showDetail: false,
      currentQuestion: {}
    })
    // 刷新标记状态
    this.loadMarks()
  },

  // 加载更多
  loadMore() {
    this.loadNextChunk()
  },

  // 选择章节
  selectSection(e) {
    const section = e.currentTarget.dataset.section
    this.setData({
      currentSection: section,
      displayQuestions: this.filterQuestions(this.data.allQuestions, section, this.data.searchText)
    })
  },

  // 搜索
  onSearch(e) {
    const searchText = e.detail.value.toLowerCase()
    this.setData({
      searchText,
      displayQuestions: this.filterQuestions(this.data.allQuestions, this.data.currentSection, searchText)
    })
  },

  // 过滤问题
  filterQuestions(questions, section, searchText) {
    let result = questions

    if (section) {
      result = result.filter(q => q.section === section)
    }

    if (searchText) {
      result = result.filter(q =>
        q.title.toLowerCase().includes(searchText) ||
        (q.summary && q.summary.toLowerCase().includes(searchText))
      )
    }

    return result
  },

  // 回到顶部
  backToTop() {
    wx.pageScrollTo({
      scrollTop: 0,
      duration: 300
    })
  },

  // 监听页面滚动
  onPageScroll(e) {
    this.setData({
      showBackTop: e.scrollTop > 500
    })
  }
})