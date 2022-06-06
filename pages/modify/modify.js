var app = getApp()
Page({
    onLoad: function () {
        this.setData({
            img_src: "https://www.physics2.plus/imgs/" + app.globalData.userInfo[1] + "_" + app.globalData.userInfo[0] + ".jpg"
        })

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
            }
        })
    },
    upload: function () {
        let _this = this;

        let src = _this.data.img_src;
        wx.showToast({
                icon: "loading",
                title: "正在上传"
            }),

            //将本地资源上传到服务器
            wx.uploadFile({
                url: "https://www.physics2.plus/modify", // 开发者服务器地址
                filePath: src, // 要上传文件资源的路径 (本地路径)
                name: 'editormd-image-file', // 文件对应的 key，开发者在服务端可以通过这个 key 获取文件的二进制内容
                header: {
                    // HTTP 请求 Header，Header 中不能设置 Referer
                    "Content-Transfer-Encoding": "binary",
                    "Content-Type": "application/octet-stream",
                    "Content-Disposition": "form-data"
                },
                formData: {
                    //和服务器约定的token, 一般也可以放在header中
                    'token': wx.getStorageSync('userData').token,
                    'name': app.globalData.userInfo[1],
                    'xuehao': app.globalData.userInfo[0],
                    'openid': app.globalData.userInfo[2]
                },
                success: function (res) {
                    console.log(res.data)
                    if (res.statusCode == 270) {
                        _this.setData({
                            errorShow: true,
                            errorMsg: "修改失败"
                        })

                    } else if (res.statusCode == 200) {
                        _this.onLoad()
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
})