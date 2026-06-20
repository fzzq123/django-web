from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from pyquery import PyQuery as pq
from db.models import useraccount, MyNew, Ad, Resume
from db.model_forms import UserAccountNewForm, LoginForm, ResumeForm


# ==================== 用户注册 ====================

def registed(request):
    """用户注册（含验证码）"""
    try:
        usrgroup = request.session['group']
    except KeyError:
        usrgroup = ''

    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        acctname = request.POST.get('accountname', '')
        cform = UserAccountNewForm(request.POST)
        if cform.is_valid():
            # 创建 Django 内建用户
            user = User.objects.create_user(username, email, password)
            user.is_active = True
            user.is_staff = True
            user.save()
            # 创建扩展用户账户
            useracc = useraccount()
            useracc.user = user
            useracc.accountname = acctname
            useracc.save()
            message = '帐号申请成功，请登入使用...'
            return render(request, 'OK.html', {'msg': message})
    else:
        cform = UserAccountNewForm()
    return render(request, 'signon.html', {'form': cform})


# ==================== 用户登录 ====================

def login_view(request):
    """用户登录（含验证码）"""
    if request.method == 'POST':
        cForm = LoginForm(request.POST)
        if cForm.is_valid():
            username = cForm.cleaned_data['username']
            password = cForm.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                usracc = get_object_or_404(useraccount, user=user)
                auth.login(request, user)
                request.session['usrid'] = user.id
                request.session['usrName'] = user.username
                rtnurl = '/member/'
                return HttpResponseRedirect(rtnurl)
    else:
        cForm = LoginForm()
    return render(request, 'login.html', {'form': cForm})


# ==================== 用户登出 ====================

def logout_view(request):
    """用户登出"""
    usrgroup = ''
    request.session.flush()
    return render(request, 'logout.html', {'UsrGroup': usrgroup})


# ==================== 会员首页 ====================

def member_home(request):
    """会员中心首页"""
    usrid = request.session.get('usrid')
    if not usrid:
        return HttpResponseRedirect('/login/')
    return render(request, 'member_home.html', {
        'usrName': request.session.get('usrName', ''),
    })


def member_edit(request):
    """编辑会员信息"""
    usrid = request.session.get('usrid')
    if not usrid:
        return HttpResponseRedirect('/login/')
    return render(request, 'member_edit.html')


# ==================== 新闻管理（Froala + PyQuery） ====================

def news_list(request, newType=None):
    """新闻列表页 — 使用 PyQuery 提取纯文本摘要"""
    if newType is None:
        newType = '企业新闻'

    type_map = {
        'company': '企业新闻',
        'industry': '行业新闻',
        'notice': '通知公告',
    }
    newName = type_map.get(newType, '企业新闻')
    newList = MyNew.objects.all().filter(
        newType=newName).order_by('-publishDate')

    # 使用 PyQuery 提取 HTML 中的纯文本摘要
    for mynew in newList:
        html = pq(mynew.description)
        mynew.mytxt = pq(html)('p').text()

    return render(request, 'newsList.html', {
        'active_menu': 'news',
        'newName': newName,
        'newList': newList,
    })


def news_detail(request, id):
    """新闻详情页"""
    mynew = get_object_or_404(MyNew, id=id)
    mynew.views += 1
    mynew.save()
    return render(request, 'newsDetail.html', {
        'mynew': mynew,
    })


# ==================== 人才招聘 ====================

def contact(request):
    """欢迎咨询 — 含百度地图"""
    return render(request, 'contact.html', {
        'active_menu': 'employ',
        'sub_menu': 'contact',
    })


def recruit(request):
    """加入恒达 — 招聘广告 + 简历提交"""
    AdList = Ad.objects.all().order_by('-publishDate')
    if request.method == 'POST':
        resumeForm = ResumeForm(data=request.POST, files=request.FILES)
        if resumeForm.is_valid():
            resumeForm.save()
            msg = "<br><br>成功新增个人简历..."
            return render(request, 'OK.html', {
                'active_menu': 'contactus',
                'sub_menu': 'recruit',
                'msg': msg
            })
    else:
        resumeForm = ResumeForm()
    return render(
        request, 'recruit.html', {
            'active_menu': 'contactus',
            'sub_menu': 'recruit',
            'AdList': AdList,
            'form': resumeForm,
        })
