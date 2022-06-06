var app = getApp()

Page({

    onLoad: function () {
        this.setData({
            hasUserProInfo: app.globalData.hasUserProInfo,
            errShow: false,
            maskHidden: true,
            ifTeacher: false
        })
    },
    data: {
        errorInfo: '未检测到用户信息',
        errShow: false,
        dialogShow: false
    },
    register: function () {
        wx.navigateTo({
            url: '../register/register'
        })
    },

    login: function () {
        let that = this
        wx.login({
            success: function (res) {
                wx.request({
                    url: 'https://www.physics2.plus/login',
                    data: {
                        "code": res.code,
                        "ifTeacher": that.data.ifTeacher
                    },
                    method: "POST",
                    success: function (res) {
                        var currentPage = getCurrentPages()[getCurrentPages().length - 1]

                        app.globalData.ifTeacher = currentPage.data.ifTeacher //设置身份信息

                        if (res.statusCode == 200) {
                            //登录成功
                            app.globalData.userInfo = res.data[0] //设置用户信息


                            //跳出提示
                            currentPage.setData({
                                tipMsg: "登录成功",
                                tipType: "success",
                                tipShow: true,

                                loading: true,
                                hideLoading: false,
                                maskHidden: false,
                                loadingInfo: "正在加载课程信息"
                            })
                            setTimeout(() => {

                                currentPage.setData({
                                    loading: false,
                                    hideLoading: true,
                                    maskHidden: true
                                });
                                //进入课程主界面
                                wx.switchTab({
                                    url: '/pages/course/course'
                                })
                            }, 1000);
                        } else if (res.statusCode == 250) {
                            //教师登录失败 弹出提示
                            currentPage.setData({
                                tipMsg: "登录失败",
                                tipType: "error",
                                tipShow: true
                            })
                        } else if (res.statusCode == 260) {

                            getApp().globalData.openid = res.data

                            //学生登录失败
                            currentPage.setData({
                                tipMsg: "登录失败",
                                tipType: "error",
                                tipShow: true,

                                loading: true,
                                hideLoading: false,
                                maskHidden: false,
                                loadingInfo: "正在进入注册"
                            })

                            setTimeout(() => {
                                // 弹出提示
                                currentPage.setData({
                                    loading: false,
                                    hideLoading: true,
                                    maskHidden: true
                                });

                                // 进入注册
                                wx.navigateTo({
                                    url: '/pages/register/register',
                                })
                            }, 1000);
                        }
                    }
                })
            }
        })

    },


    getUserProfile: function (e) {
        let _this = this
        wx.getUserProfile({
            desc: '用于完善用户主页',
            success: (res) => {
                app.globalData.userProInfo = res.userInfo;
                app.globalData.hasUserProInfo = true;
                _this.setData({
                    hasUserProInfo: true,
                    ifTeacher: false
                })
            }
        })
    },
    switch1Change: function (e) {
        this.setData({
            ifTeacher: e.detail.value
        })
    }
})