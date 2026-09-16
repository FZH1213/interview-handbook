// pages/basic/content.js
const app = getApp()

Page({
  data: {
    sections: [],
    currentSection: '',
    searchText: '',
    allQuestions: [],
    displayQuestions: [],
    expandedIndex: -1,
    total: 0,
    loadedCount: 0,
    hasMore: true,
    showBackTop: false,
    currentChunk: 0
  },

  onLoad() {
    this.loadSections()
    this.loadNextChunk()
  },

  onShow() {
    if (this.data.showBackTop) {
      this.setData({ showBackTop: false })
    }
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
    } else if (chunk === 3) {
      questions = require('../data/questions_3.js')
    } else if (chunk === 4) {
      questions = require('../data/questions_4.js')
    } else if (chunk === 5) {
      questions = require('../data/questions_5.js')
    } else if (chunk === 6) {
      questions = require('../data/questions_6.js')
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
      hasMore: this.data.currentChunk + 1 < 7  // 7个数据块
    })
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
      displayQuestions: this.filterQuestions(this.data.allQuestions, section, this.data.searchText),
      expandedIndex: -1
    })
  },

  // 搜索
  onSearch(e) {
    const searchText = e.detail.value.toLowerCase()
    this.setData({
      searchText,
      displayQuestions: this.filterQuestions(this.data.allQuestions, this.data.currentSection, searchText),
      expandedIndex: -1
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

  // 展开/收起问题
  toggleQuestion(e) {
    const index = e.currentTarget.dataset.index
    // 使用全局索引来管理展开状态，避免筛选后索引错乱
    const globalIndex = this.data.displayQuestions[index].index
    this.setData({
      expandedIndex: this.data.expandedIndex === globalIndex ? -1 : globalIndex
    })
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