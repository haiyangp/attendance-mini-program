var app = getApp()


Page({
    onLoad: function () {
        let _this=this
        this.setData({
            course:app.globalData.selectedCourse
        })
        wx.request({
            url: 'https://www.physics2.plus/sign_record',
            data: {
                cou_id:app.globalData.selectedCourse["cou_id"]
            },
            method:"POST",
            success:function(res){
                _this.setData({
                    sign_records:res.data
                })
            }
        })

    }
})