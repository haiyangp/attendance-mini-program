var app = getApp();
Page({
    onLoad: function () {
        this.setData({
            id: app.globalData.userInfo[0],
            name: app.globalData.userInfo[1],
            ifTeacher: app.globalData.ifTeacher,
            userinfo: app.globalData.userProInfo
        })

        // if (this.data.shenfen == "student") {
        //     this.setData({
        //         img_src: "https://www.physics2.plus/imgs/" + this.data.name + "_" + this.data.xuehao + ".jpg"
        //     })
        //     console.log(this.data.img_src)
        // }
    },
})