var app = getApp();
Page({
    onLoad: function () {
        this.setData({
            course: app.globalData.selectedCourse
        })
    },
    fromInputName: function (e) {
        this.setData({
            stu_name: e.detail.value
        })
    },
    fromInputId: function (e) {
        this.setData({
            stu_id: e.detail.value
        })
    },
    fromInputIndex: function (e) {
        this.setData({
            sign_index: e.detail.value
        })
    },
    buqian: function () {
        let _this = this

        wx.request({
            url: 'https://www.physics2.plus/cmpl_add',
            data: {
                stu_id: _this.data.stu_id,
                stu_name: _this.data.stu_name,
                sign_index: _this.data.sign_index,
                cou_id: _this.data.course.cou_id
            },
            method: "POST",
            success: function (res) {
                _this.setData({
                    toastShow: true
                })
                setTimeout(function () {
                    _this.setData({
                        toastShow: false
                    })
                    wx.navigateBack({
                        delta: 0,
                    })
                }, 500)
            }
        })

    }
})