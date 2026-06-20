import os
import base64
import numpy as np
import cv2
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 人脸检测器路径（使用绝对路径避免运行时工作目录不同导致找不到文件）
face_detector_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'haarcascade_frontalface_default.xml'
)
face_detector = cv2.CascadeClassifier(face_detector_path)  # 生成人脸检测器


def platform(request):
    """人脸识别开放平台页面"""
    submenu = 'platform'
    return render(request, 'platForm.html', {
        'active_menu': 'service',
        'sub_menu': submenu,
    })


def read_image(stream=None):
    """从文件流中读取图像"""
    if stream is not None:
        data_temp = stream.read()
    img = np.asarray(bytearray(data_temp), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img


@csrf_exempt  # 用于规避跨站点请求攻击
def facedetect(request):
    """人脸检测API - 返回人脸坐标"""
    result = {}

    if request.method == "POST":  # 规定客户端使用POST上传图片
        if request.FILES.get("image", None) is not None:  # 读取图像
            img = read_image(stream=request.FILES["image"])
        else:
            result.update({
                "#faceNum": -1,
            })
            return JsonResponse(result)

        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 彩色图像转灰度图像

        # 进行人脸检测
        values = face_detector.detectMultiScale(img,
                                                scaleFactor=1.1,
                                                minNeighbors=5,
                                                minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)

        # 将检测得到的人脸检测关键点坐标封装
        values = [(int(a), int(b), int(a + c), int(b + d))
                  for (a, b, c, d) in values]
        result.update({
            "#faceNum": len(values),
            "faces": values,
        })
    return JsonResponse(result)


@csrf_exempt
def facedetectDemo(request):
    """人脸检测演示 - 返回带检测框的base64图像"""
    result = {}

    if request.method == "POST":
        if request.FILES.get('image') is not None:
            img = read_image(stream=request.FILES["image"])
        else:
            result["#faceNum"] = -1
            return JsonResponse(result)

        if img.shape[2] == 3:
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 彩色图像转灰度图像
        else:
            imgGray = img

        # 进行人脸检测
        values = face_detector.detectMultiScale(imgGray,
                                                scaleFactor=1.1,
                                                minNeighbors=5,
                                                minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE)

        # 将检测得到的人脸检测关键点坐标封装
        values = [(int(a), int(b), int(a + c), int(b + d))
                  for (a, b, c, d) in values]

        # 将检测框显示在原图上
        for (w, x, y, z) in values:
            cv2.rectangle(img, (w, x), (y, z), (0, 255, 0), 3)

        retval, buffer_img = cv2.imencode('.jpg', img)  # 在内存中编码为jpg格式
        img64 = base64.b64encode(buffer_img)  # base64编码用于网络传输
        img64 = str(img64, encoding='utf-8')  # bytes转换为str类型
        result["img64"] = img64  # json封装
    return JsonResponse(result)
