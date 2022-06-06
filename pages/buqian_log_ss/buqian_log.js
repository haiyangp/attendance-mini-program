var app = getApp()
Page({

    onLoad: function () {
        let _this = this
        this.setData({
            course: app.globalData.selectedCourse
        })
        wx.request({
            url: 'https://www.physics2.plus/cmpl_get3',
            data: {
                stu_id: app.globalData.userInfo[0]
            },
            method: "POST",
            success: function (res) {
                console.log(res.data)
                _this.setData({
                    complements: res.data,
                    complement_num:res.data.length,
                    dialogShow: true
                })
            }
        })
    },
    close: function () {
        this.setData({
            dialogShow: false
        })
    }
})