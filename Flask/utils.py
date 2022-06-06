import cv2
import numpy as np
import os
# from . import yolo

#生成标签集
def generateLabels(dir):
    fileNameList=os.listdir(dir)
    labels=[]
    for fileName in fileNameList:
        label=fileName.replace('.jpg','')
        label=int(label)
        labels.append(label)
    labels=np.array(labels)#以学号作为标签
    return labels

#生成训练图片集
def generateTrains(dir):
    fileNameList=os.listdir(dir)
    trains=[]
    for fileName in fileNameList:
        fileDir=dir+'/'+fileName
        image = cv2.imread(fileDir, cv2.IMREAD_GRAYSCALE)#以灰度图形式读取图片
        imageR = cv2.resize(image,(250,250),interpolation=cv2.INTER_NEAREST)#裁剪大小
        trains.append(imageR)
    return trains

#预测
def predict(bytesImage):
    dir='C:/Users/ASUS/Desktop/backend/faces'
    labels=generateLabels(dir)
    trains=generateTrains(dir)
    #调用yolo模型进行人脸检测并裁剪图片

    net=cv2.dnn.readNetFromONNX("model.onnx")
    net.setInput(cv2.dnn.blobFromImage(cv2.imread(bytesImage),size=(640,640)))
    output=net.forward()

    # cropBytesImage = yolo.detect_image(bytesImage, crop = True, count=False)
    #转换预测图片格式
    nparrImage = np.frombuffer(output, dtype=np.uint8)
    image = cv2.imdecode(nparrImage, cv2.IMREAD_GRAYSCALE)
    imageR = cv2.resize(image,(250,250),interpolation=cv2.INTER_NEAREST)
    #创建识别器，训练模型
    # recoginer = cv2.face.EigenFaceRecognizer_create()
    recoginer = cv2.face.LBPHFaceRecognizer_create()
    recoginer.train(trains, labels)
    #预测
    label, confidence = recoginer.predict(imageR)
    predictRes={'label':label,'confidence':confidence}
    return predictRes
