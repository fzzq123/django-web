from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from db.models import Product

# include separate file for different functions
from .faceDetect import *
def home(request):
    return render(request, 'index.html')

def calculator(request):
    return render(request, 'calculator.html')

def dance(request):
    return render(request, 'dance.html')

def slider(request):
    return render(request, 'slider.html')

def products(request, productName):
    # 1. 转换 URL 参数为中文产品类型
    submenu = productName
    if productName == 'robot':
        productName = '家用机器人'
    elif productName == 'monitor':
        productName = '智能监控'
    else:
        productName = '人脸识别解决方案'

    # 2. 查询该产品类型的所有产品
    productList = Product.objects.all().filter(
        productType=productName).order_by('-publishDate')

    # 3. 分页核心代码
    paginator = Paginator(productList, 4)        # 每页显示 4 个产品
    page_number = request.GET.get('page')        # 获取 URL 中的 ?page=参数
    page_obj = paginator.get_page(page_number)   # 获取当前页的数据

    return render(
        request, 'productList.html', {
            'active_menu': 'products',
            'sub_menu': submenu,
            'productName': productName,
            'page_obj': page_obj,        # 传给模板的是 page_obj，不是 productList
        })


def productDetail(request, id):
    product = get_object_or_404(Product, id=id)
    product.views += 1
    product.save()

    # 根据产品类型确定返回的 URL 参数
    type_map = {
        '家用机器人': 'robot',
        '智能监控': 'monitor',
        '人脸识别解决方案': 'face',
    }
    back_type = type_map.get(product.productType, 'robot')

    return render(request, 'productDetail.html', {
        'active_menu': 'products',
        'product': product,
        'back_type': back_type,  # 新增
    })