var app = getApp()


Page({
    onLoad: function () {
        let _this=this
        this.setData({
            course:app.globalData.selectedCourse
        })
        wx.request({
            url: 'https://www.physics2.plus/sign_record_s',
            data: {
                cou_id:app.globalData.selectedCourse["cou_id"],
                stu_id:app.globalData.userInfo[0]
            },
            method:"POST",
            success:function(res){
                console.log(res.data)
                _this.setData({
                    sign_records:res.data
                })
            }
        })
    }
})