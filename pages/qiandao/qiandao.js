const _ = require("../../miniprogram_npm/weui-miniprogram/_commons/0")

var app = getApp()
var catch2 = function (e1, e2) {
    console.log(e1 + e2)
    return String(e1) + String(e2)
}

Page({
    onLoad: function () {
        this.setData({
            course: app.globalData.selectedCourse,
            array: ['3 X 3', '4 X 2'],
            objectArray: [
                [3, 3],
                [4, 2]
            ],
            roomtype: 0,
            excepNum: 0
        })
        this.drawRoom()
    },
    catch: function (e1, e2) {
        console.log(e1 + e2)
        return String(e1) + String(e2)
    },
    drawRoom: function () {
        const m = this.data.objectArray[this.data.roomtype][0];
        const n = this.data.objectArray[this.data.roomtype][1];

        let arr = new Array(m); // create an empty array of length n
        for (var i = 0; i < m; i++) {
            arr[i] = new Array(n); // make each element an array
        }

        for (var i = 0; i < m; i++) {
            for (var j = 0; j < n; j++) {
                arr[i][j] = [i + 1, j + 1]
            }
        }
        this.setData({
            arr: arr,
            arrSize: [m, n],
        })
    },
    finishChooseRoomType: function () {
        this.setData({
            haveChosenRoomType: true
        })
        this.showtoast("选择教室类型完成")
    },
    startSigning: function () {
        this.setData({
            dialogShow1: true
        })
    },
    stopSigning: function () {
        this.setData({
            dialogShow2: true
        })
    },

    exit: function () {
        let _this = this

        wx.request({
            url: 'https://www.physics2.plus/expt_get',
            data: {
                sgn_id: _this.data.sgn_id
            },
            method: "POST",
            success: function (res) {
                _this.setData({
                    excepNum: res.data,
                })
            }
        })

        this.setData({
            excepShow: true
        })

    },

    bindPickerChange: function (e) {
        this.setData({
            roomtype: e.detail.value
        })
        this.drawRoom()
    },

    bindcatchtap: function (e) {
        let _this = this
        var str = e.target.id
        // str=str.substring(0,str.length)

        var i_index = parseInt(str.split(',')[0])
        var j_index = parseInt(str.split(',')[1])
        if (this.data.sign_result[i_index][j_index] == "") return
        this.setData({
            dialogShow4: true,
            sign_info: _this.data.sign_result[i_index][j_index],
        })
    },
    close: function () {
        this.setData({
            dialogShow4: false
        })
    },
    showtoast: function (toastinfo) {
        this.setData({
            toastShow: true,
            toastInfo: toastinfo
        })
        let _this = this

        setTimeout(function () {
            _this.setData({
                toastShow: false
            })
        }, 1000)
    },


    closeDialog: function () {
        this.setData({
            dialogShow1: false,
            dialogShow2: false
        })
    },
    closeDialog1: function () {
        let _this = this
        wx.getLocation({
            type: "wgs84",
            success(res) {
                var latitude = res.latitude
                var longitude = res.longitude

                wx.request({
                    url: 'https://www.physics2.plus/sign_start',
                    data: {
                        cou_id: _this.data.course.cou_id,
                        latitude: latitude,
                        longitude: longitude,
                        roomtype: _this.data.objectArray[_this.data.roomtype]
                    },
                    method: "POST",
                    success: function (res) {
                        _this.showtoast("发起签到成功")
                        _this.setData({
                            haveStartedSigning: true,
                            sgn_id: res.data,
                            dialogShow1: false,
                        })

                        const m = _this.data.objectArray[_this.data.roomtype][0];
                        const n = _this.data.objectArray[_this.data.roomtype][1];

                        let ifShow = new Array(m); // create an empty array of length n
                        let sign_result = new Array(m);
                        for (var i = 0; i < m; i++) {
                            ifShow[i] = new Array(n); // make each element an array
                            sign_result[i] = new Array(n)
                        }

                        for (var i = 0; i < m; i++) {
                            for (var j = 0; j < n; j++) {
                                ifShow[i][j] = false
                                sign_result[i][j] = ""
                            }
                        }
                        _this.setData({
                            ifShow: ifShow,
                            sign_result: sign_result
                        })

                        var interval = setInterval(function () {
                            wx.request({
                                url: 'https://www.physics2.plus/sign_result',
                                data: {
                                    sgn_id: res.data
                                },
                                method: "POST",
                                success: function (res) {
                                    var ifShow = _this.data.ifShow
                                    for (var i = 0; i < res.data.length; i++) {

                                        var seat = JSON.parse(res.data[i][0])
                                        seat[0] = _this.data.objectArray[_this.data.roomtype][0] - 1 - seat[0]
                                        seat[1] = _this.data.objectArray[_this.data.roomtype][1] - 1 - seat[1]
                                        ifShow[seat[0]][seat[1]] = true
                                        _this.data.sign_result[seat[0]][seat[1]] = res.data[i][1] + " " + res.data[i][2]
                                    }
                                    _this.setData({
                                        ifShow: ifShow
                                    })
                                }
                            })
                        }, 1000)

                        _this.setData({
                            interval: interval
                        })
                    }
                })
            }
        })
    },
    closeDialog2: function () {
        let _this = this
        wx.request({
            url: 'https://www.physics2.plus/sign_stop',
            data: {
                sgn_id: _this.data.sgn_id
            },
            method: "POST",
            success: function (res) {
                _this.showtoast("结束签到成功")
                _this.setData({
                    haveStopedSigning: true,
                    dialogShow2: false
                })
                clearInterval(_this.data.interval)
            }
        })

        // 得到签到结果*************
    },
    closeDialog3: function () {
        this.setData({
            excepShow: false
        })

        wx.navigateBack({
            delta: 0,
        })
    }
})