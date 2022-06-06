var app = getApp()
Page({
    onLoad: function () {
        let _this = this
        this.setData({
            course: app.globalData.selectedCourse
        })
        wx.request({
            url: 'https://www.physics2.plus/sign_record_ss',
            data: {
                stu_id: app.globalData.userInfo[0]
            },
            method: "POST",
            success: function (res) {
                console.log(res.data)
                _this.setData({
                    signs: res.data,
                    signs_num: res.data.length,
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