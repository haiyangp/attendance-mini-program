var app=getApp();
Page({
    onLoad:function(){
        this.setData({
            course: app.globalData.selectedCourse,
            textNum:0
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
    buqian:function(){
        let _this = this

        wx.request({
            url: 'https://www.physics2.plus/cmpl_send',
            data: {
                stu_id: _this.data.stu_id,
                sign_index: _this.data.sign_index,
                cou_id: _this.data.course.cou_id,
                bsgn_reason:_this.data.bsgn_reason
            },
            method: "POST",
            success: function (res) {
                if(res.statusCode==200){
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

            }
        })
    },
    excepInput: function (e) {
        this.setData({
            bsgn_reason: e.detail.value,
            textNum: e.detail.value.length
        })
    }
})