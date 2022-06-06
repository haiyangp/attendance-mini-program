var app = getApp();
Page({
    onLoad: function () {
        this.setData({
            course:app.globalData.selectedCourse
        })
    },
})