// pages/questions/index.js
Page({
  data: {
    modules: [
      {
        id: 'basic',
        title: '基础面试题',
        desc: 'HTML、CSS、JavaScript等基础知识',
        icon: '/assets/basic.png',
        path: '/packageBasic/pages/content'
      },
      {
        id: 'advanced',
        title: '进阶面试题',
        desc: '框架、工程化、性能优化等进阶知识',
        icon: '/assets/advanced.png',
        path: '/packageAdvanced/pages/content'
      }
    ]
  },

  navigateToModule(e) {
    const path = e.currentTarget.dataset.path
    wx.navigateTo({
      url: path
    })
  }
})