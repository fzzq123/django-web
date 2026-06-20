"""
URL configuration for djangoProject project.
"""
from djangoProject.views import *
from django.conf.urls.static import static
from djangoProject import settings
from django.contrib import admin
from django.urls import path, include
from db.views import (
    registed, login_view, logout_view,
    news_list, news_detail,
    contact, recruit,
)
from db.fileDownload import download, getDoc

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', home, name='home'),
    path('calcu/', calculator, name='calcu'),
    path('dance/', dance, name='dance'),
    path('products/<str:productName>/', products, name='products'),
    path('productDetail/<int:id>/', productDetail, name='productDetail'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signon/', registed, name='signon'),
    path('captcha/', include('captcha.urls')),
    path('froala_editor/', include('froala_editor.urls')),
    path('news/', news_list, name='newsList'),
    path('news/<str:newType>/', news_list, name='newsType'),
    path('newsDetail/<int:id>/', news_detail, name='newsDetail'),
    path('search/', include('haystack.urls')),
    path('contact/', contact, name='contact'),    # 欢迎咨询
    path('recruit/', recruit, name='recruit'),    # 加入恒达
    path('download/', download, name='download'), # 资料下载
    path('getDoc/<int:id>/', getDoc, name='getDoc'), # 单项资料下载
    path('platform/', platform, name='platform'),  # 人脸识别开放平台
    path('facedetect/', facedetect, name='facedetect'),         # 人脸检测API
    path('facedetectDemo/', facedetectDemo, name='facedetectDemo'),  # 人脸检测演示
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)