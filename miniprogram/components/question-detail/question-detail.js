// components/question-detail/question-detail.js
Component({
  properties: {
    show: {
      type: Boolean,
      value: false
    },
    question: {
      type: Object,
      value: {}
    }
  },

  data: {
    isMastered: false,
    isToImprove: false
  },

  observers: {
    'question.index': function(index) {
      if (index) {
        const mastered = wx.getStorageSync('masteredQuestions') || {}
        const toImprove = wx.getStorageSync('toImproveQuestions') || {}
        this.setData({
          isMastered: !!mastered[index],
          isToImprove: !!toImprove[index]
        })
      }
    }
  },

  methods: {
    onClose() {
      this.triggerEvent('close')
    },

    toggleMastered() {
      const question = this.data.question
      const index = question.index
      const mastered = wx.getStorageSync('masteredQuestions') || {}

      mastered[index] = {
        index,
        title: question.title,
        summary: question.summary,
        followUp: question.followUp,
        section: question.section,
        timestamp: Date.now()
      }

      wx.setStorageSync('masteredQuestions', mastered)

      const toImprove = wx.getStorageSync('toImproveQuestions') || {}
      delete toImprove[index]
      wx.setStorageSync('toImproveQuestions', toImprove)

      this.setData({
        isMastered: true,
        isToImprove: false
      })

      this.updateSummaryCount()
    },

    toggleToImprove() {
      const question = this.data.question
      const index = question.index
      const toImprove = wx.getStorageSync('toImproveQuestions') || {}

      toImprove[index] = {
        index,
        title: question.title,
        summary: question.summary,
        followUp: question.followUp,
        section: question.section,
        timestamp: Date.now()
      }

      wx.setStorageSync('toImproveQuestions', toImprove)

      const mastered = wx.getStorageSync('masteredQuestions') || {}
      delete mastered[index]
      wx.setStorageSync('masteredQuestions', mastered)

      this.setData({
        isMastered: false,
        isToImprove: true
      })

      this.updateSummaryCount()
    },

    updateSummaryCount() {
      const mastered = wx.getStorageSync('masteredQuestions') || {}
      const toImprove = wx.getStorageSync('toImproveQuestions') || {}
      wx.setStorageSync('masteredCount', Object.keys(mastered).length)
      wx.setStorageSync('toImproveCount', Object.keys(toImprove).length)
    }
  }
})