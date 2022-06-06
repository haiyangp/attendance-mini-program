Page({
    data: {
        img_src: "/image/demo.jpg",
        disableBtn: true
    },
    formInputChange_xingming: function (e) {
        this.setData({
            name: e.detail.value
        })
        this.checkBtn()
    },
    formInputChange_xuehao: function (e) {
        this.setData({
            xuehao: e.detail.value
        })
        this.checkBtn()
    },
    // 选择上传图片的方式
    chooseImageTap() {
        let _this = this;
        wx.showActionSheet({
            itemList: ['从相册中选择', '拍一张'],
            itemColor: "#000000",
            success(res) {
                if (!res.cancel) {
                    if (res.tapIndex == 0) {
                        // 从相册中选择
                        _this.chooseWxImage('album')
                    } else if (res.tapIndex == 1) {
                        // 使用相机
                        _this.chooseWxImage('camera')
                    }
                }
            }
        })
    },
    // 选择图片
    chooseWxImage(type) {
        let _this = this;
        wx.chooseImage({
            count: 1,
            sizeType: ['original', 'compressed'],
            sourceType: [type],
            success(res) {
                console.log(res.tempFilePaths[0])
                _this.setData({
                    img_src: res.tempFilePaths[0]
                })
                _this.checkBtn()
            }
        })
    },
    //上传图片到服务器
    upload: function () {
        let _this = this
        let src = this.data.img_src

        // console.log(_this.data)
        wx.showToast({
            icon: "loading",
            title: "正在上传"
        })

        //将本地资源上传到服务器
        wx.uploadFile({
            url: "https://www.physics2.plus/register", // 开发者服务器地址
            filePath: src, // 要上传文件资源的路径 (本地路径)
            name: 'editormd-image-file', // 文件对应的 key，开发者在服务端可以通过这个 key 获取文件的二进制内容
            header: {

                "Content-Transfer-Encoding": "binary",
                "Content-Type": "application/octet-stream",
                "Content-Disposition": "form-data"
            },
            formData: {

                'token': wx.getStorageSync('userData').token,
                'name': _this.data.name,
                'xuehao': _this.data.xuehao,
                'openid': getApp().globalData.openid
            },
            success: function (res) {
                if (res.statusCode == 240) {
                    _this.setData({
                        tipShow: true,
                        tipType: "error",
                        tipMsg: "该学号已经注册"
                    })

                } else if (res.statusCode == 200) {
                    getApp().globalData.userInfo = JSON.parse(res.data)[0]
                    wx.switchTab({
                        url: '/pages/course/course',
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

    checkBtn: function () {
        let _this = this;
        let src = _this.data.img_src;

        if (!_this.data.name) {
            return
        }
        if (!_this.data.xuehao) {

            return
        }

        if (src == "/image/demo.jpg") {
            return
        }

        _this.setData({
            disableBtn: false
        })
    }
})