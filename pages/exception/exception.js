var app = getApp()


Page({
    onLoad: function () {
        let _this = this
        this.setData({
            course: app.globalData.selectedCourse,

        })
        this.getComplements()
        this.setData({
            dialogShow:true
        })
    },
    getComplements:function(){
        let _this = this
        wx.request({
            url: 'https://www.physics2.plus/expt_get2',
            data: {
                tea_id: app.globalData.userInfo[0]
            },
            method: "POST",
            success: function (res) {
                console.log(res.data)
                _this.setData({
                    exceptions: res.data,
                    exception_num:res.data.length,
                })
            }
        })
    },
    excute: function (e) {
        var str = e.target.id

        var index=parseInt(str.substring(1))
        let _this = this
        wx.request({
            url: 'https://www.physics2.plus/expt_excute',
            data: {
                excp_id:_this.data.exceptions[index].excp_id
            },
            method: "POST",
            success: function (res) {
                _this.setData({
                    toastShow:true,
                })
                setTimeout(function () {
                    _this.setData({
                        toastShow: false
                    })
                    _this.getComplements()
                }, 500)
            }
        })

    },
    close: function () {
        this.setData({
            dialogShow: false
        })
    }
})