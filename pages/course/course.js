Page({
    onLoad: function () {
        let _this = this;
        _this.setData({
            ifTeacher: getApp().globalData.ifTeacher,

        });
        wx.request({
            url: 'https://www.physics2.plus/course_get',
            data: {
                "id": getApp().globalData.userInfo[0],
                "ifTeacher": getApp().globalData.ifTeacher
            },
            method: "POST",
            success: function (res) {
                var app = getApp()
                app.globalData.courseInfo = res.data
                var courseData = []
                var ifShow = []
                for (var i = 0; i < res.data.length; i++) {
                    courseData.push({
                        cou_id: res.data[i][0],
                        cou_name: res.data[i][1],
                        tea_id: res.data[i][2],
                        cou_detail: res.data[i][3],
                    })

                }
                _this.setData({
                    courses: courseData,
                })
                console.log(_this.data.courses)
            }
        })
    },

    widgetsToggle: function (e) {
        var id = e.currentTarget.id,
            data = [];
        if (this.data.ifShow[id] == true) {
            for (var i = 0, len = this.data.ifShow.length; i < len; ++i) {
                if (i == id)
                    data[i] = false;
            }
        } else {
            for (var i = 0, len = this.data.ifShow.length; i < len; ++i) {
                if (i == id)
                    data[i] = false;
            }
            data[id] = !this.data[id];
        }


        this.setData({
            ifShow: data
        });
    },

    formInputChange_id: function (e) {
        this.setData({
            cou_id_add: e.detail.value
        })
    },
    formInputChange_name: function (e) {
        this.setData({
            cou_name_add: e.detail.value
        })
    },


    index: function (e) {
        var id = parseInt(e.currentTarget.id.substring(5))

        getApp().globalData.selectedCourse= this.data.courses[id]

        if(this.data.ifTeacher){
            wx.navigateTo({
                url: "/pages/index/index"
            })
        }else{
            wx.navigateTo({
                url: "/pages/index_s/index"
            })
        }

    },


    addCourse: function () {
        // 显示半屏对话框
        this.setData({
            addCourseDialogShow: true
        })

    },
    closeHalfScreenDialog: function () {
        let _this = this
        // 用户id
        var id = getApp().globalData.userInfo[0]
        wx.request({
            url: 'https://www.physics2.plus/course_add',
            data: {
                ifTeacher: _this.data.ifTeacher,
                id: id,
                cou_id: _this.data.cou_id_add,
                cou_name: _this.data.cou_name_add
            },
            method: "POST",
            success(res) {
                console.log(res)
                if (res.statusCode == 200) {
                    // 刷新
                    _this.onLoad()
                    // 对话框消失
                    _this.setData({
                        addCourseDialogShow: false,
                    })
                    // 显示提示
                    var toastInfo=_this.data.ifTeacher?"创建成功":"加入成功"
                    _this.showtoast(toastInfo)

                } else {
                    _this.showTip(res.data,"error")
                }
            }
        })
    },

    showtoast:function(toastinfo){
        this.setData({
            toastShow:true,
            toastInfo:toastinfo
        })
        let _this=this
        
        setTimeout(function(){
            _this.setData({toastShow:false})
        },1000)
    },
    showTip:function(tipMsg,tipType){
        this.setData({
            tipShow:true,
            tipMsg:tipMsg,
            tipType:tipType
        })
    },

    deleteCourse: function (e) {
        var course_index = parseInt(e.target.id.substring(4))

        this.setData({
            dialogShow: true,
            cou_index: course_index,
            cou_target: getApp().globalData.courseInfo[course_index][1]
        })
    },

    closeDialog: function (e) {
        let _this = this

        if (e.target.id == "delete") {
            wx.request({
                url: 'https://www.physics2.plus/course_delete',
                data: {
                    "id": getApp().globalData.userInfo[0],
                    "ifTeacher": _this.data.ifTeacher,
                    "cou_id": _this.data.courses[_this.data.cou_index].cou_id
                },
                method: "POST",
                success: function (res) {
                    var toastInfo=""

                    if(_this.data.ifTeacher){
                        toastInfo="删除成功"
                    }else{
                        toastInfo="退出成功"
                    }
                    if (res.statusCode == 200) {
                        _this.onLoad()
                        _this.setData({dialogShow:false})
                        _this.showtoast(toastInfo)
                    }
                }
            })
        } else {
            this.setData({
                dialogShow: false
            })
        }
    }
})