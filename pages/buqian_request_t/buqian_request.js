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
            url: 'https://www.physics2.plus/cmpl_excute3',
            data: {
                tea_id: app.globalData.userInfo[0]
            },
            method: "POST",
            success: function (res) {
                _this.setData({
                    complements: res.data,
                    complement_num:res.data.length,
                })
            }
        })
    },
    excute: function (e) {
        var str = e.target.id
        if (str.substring(0, 1) == "t") {
            this.setData({
                ifRefuse: false
            })
        } else {
            this.setData({
                ifRefuse: true
            })
        }
        var index=parseInt(str.substring(1))
        let _this = this
        wx.request({
            url: 'https://www.physics2.plus/cmpl_excute2',
            data: {
                ifRefuse:_this.data.ifRefuse,
                bsgn_id:_this.data.complements[index].bsgn_id
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