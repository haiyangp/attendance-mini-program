var app = getApp()
var catch2 = function (e1, e2) {
    console.log(e1 + e2)
    return String(e1) + String(e2)
}

Page({
    onLoad: function () {
        this.setData({
            course: app.globalData.selectedCourse,
            textNum: 0
        })
        let _this = this

        wx.request({
            url: 'https://www.physics2.plus/sign_get',
            data: {
                cou_id: _this.data.course.cou_id,
            },
            method: "POST",
            success: function (res) {
                console.log(res.data)
                _this.setData({
                    objectArray: [
                        JSON.parse(res.data[2]),
                    ],
                    roomtype: 0,
                    sign_data: res.data
                })
                _this.drawRoom()
            }
        })
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

    sendSigning: function () {
        console.log("send")
        let _this = this

        wx.uploadFile({
            url: "https://www.physics2.plus/sign_send",
            filePath: _this.data.img_src,
            name: 'editormd-image-file',
            header: {
                "Content-Transfer-Encoding": "binary",
                "Content-Type": "application/octet-stream",
                "Content-Disposition": "form-data"
            },
            formData: {
                'token': wx.getStorageSync('userData').token,
                sgn_id: _this.data.sign_data[0],
                seat_x: _this.data.seat[0],
                seat_y: _this.data.seat[1],
                stu_id: getApp().globalData.userInfo[0],
            },
            success: function (res) {
                if (res.statusCode == 200) {
                    _this.setData({
                        dialogShow1: true,
                        dialogInfo1: "签到成功"
                    })
                } else {
                    _this.setData({
                        dialogShow2: true,
                        dialogInfo2: res.data
                    })
                }
            },
            fail: function (e) {
                wx.showToast({
                    title: '上传失败',
                    icon: 'none'
                })
            },
            complete: function () {
                wx.hideToast(); //隐藏Toast
            }
        })
    },

    bindcatchtap: function (e) {
        var str = e.target.id

        var i_index = parseInt(str.split(',')[0])
        var j_index = parseInt(str.split(',')[1])

        this.setData({
            seat: [i_index, j_index],
            usableBtn: true
        })
    },


    takePhoto: function () {
        let _this = this;
        wx.chooseImage({
            count: 1,
            sizeType: ['original', 'compressed'],
            sourceType: ["camera"],
            success(res) {
                _this.setData({
                    img_src: res.tempFilePaths[0],
                    haveTakenPhoto: true
                })
            }
        })
    },
    closeDialog1: function () {
        this.setData({
            dialogShow1: false
        })
        wx.navigateBack({
            delta: 0,
        })
    },
    closeDialog2: function () {
        this.setData({
            dialogShow2: false,
            seat: [-1, -1],
            img_src: "",
            haveTakenPhoto: false,
            haveChosenSeat: false,
            usableBtn: false
        })
    },
    closeDialog3: function () {
        this.setData({
            dialogShow3: true,
            dialogShow2: false,
        })
    },
    excepInput: function (e) {
        this.setData({
            excepInfo: e.detail.value,
            textNum: e.detail.value.length
        })
    },

    sendExcept: function () {
        let _this = this
        wx.request({
            url: 'https://www.physics2.plus/excep_send',
            data: {
                excp_describe:_this.data.excepInfo,
                stu_id:getApp().globalData.userInfo[0],
                sgn_id:_this.data.sign_data[0]
            },
            method: "POST",
            success: function (res) {
                _this.setData({
                    dialogShow3:false,
                    dialogShow1:true,
                    dialogInfo1:"发送成功"
                })
            }
        })

    }
})