# django-web
基于Django开发的网站项目

## 环境依赖
- python 3.10+
- Docker

## 本质大学生作品，项目内存在冗余代码和文件，仅作为记录，存在不当请即刻联系:fzzq123@foxmail.com

## 已经针对包含隐私的地方修改为"！"，不进行修改可能导致功能缺失或无法部署

## 需修改地方

### config/nginx/local.conf
#### 第8行
修改为服务器地址
```bash
server_name ! localhost;
```

### djangoProject/settings.py
#### 第23行
根据自己django项目密钥修改
```bash
SECRET_KEY = "！"
```

### djangoProject/settings.py
#### 第28行
修改为服务器地址
```bash
ALLOWED_HOSTS = ['!']
```

### djangoProject/settings.py
#### 第31行
修改为的服务器地址
```bash
ALLOWED_ORIGINS = ['!']
```

### djangoProject/settings.py
#### 第141~146行
根据QQ邮箱的SMTP服务以及自己的设置进行修改
```bash
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '!'             # 修改为自己邮箱
EMAIL_HOST_PASSWORD = '!'         # 授权码（需替换为实际授权码）
EMAIL_USE_TLS = True
EMAIL_FROM = '!'                  #修改此处则修改收件时看到的发送方
```

### templates/contact.html
#### 第27行
代码后面'ak=！'处需要将！修改为自己申请的api
```bash
<script type="text/javascript" src="https://api.map.baidu.com/api?v=1.0&&type=webgl&ak=！">
```

### docker-compose.yml
#### 第19行
将！修改为服务器提供的端口号，？修改为容器内部监听端口
```bash
      - !:?
```

### Dockerfile
#### 第13行
需要将'！'修改为服务器提供的端口号
```bash
EXPOSE !
```
### Dockerfile
#### 第16行
需要将'！'修改为服务器提供的端口号
```bash
CMD ["gunicorn", "--chdir", "djangoProject", "--bind", "0.0.0.0:！", "djangoProject.wsgi:application", "--reload"]
```

### 实现步骤(可能有误)
#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 创建超级管理员
```bash
python manage.py createsuperuser
```

#### 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 运行
```bash
python manage.py runserver
```

#### 运行后检查无误
#### 更新依赖
```bash
pip freeze > requirements.txt
```
#### 静态文件收集
```bash
python manage.py collectstatic
```

#### 将项目文件压缩成压缩包并上传到要部署的服务器(以本地Windows操作系统，Docker平台Linux操作系统为例)
```bash
scp 本地文件路径 用户名@服务器IP:远程存放目录

例：本地文件：D:/test/project.zip，传到服务器 /home/upload/ 目录
scp D:/test/project.zip root@5.13.123.23:/home/upload/

若服务器带端口
scp -P 2222 D:/test/project.zip root@5.13.123.23:/home/upload/
```

#### 进行部署
```bash
检查是否报错
docker compose up

后台运行
docker compose up -d
```


### 已实现功能
- 可以编辑产品的标题、描述、价格、发布时间、浏览量统计，可以展示产品图片，可以分页
- 可以使用Froala(免费版，无法上传图片只能使用文字相关功能)发布新闻/文章
- 可以根据新闻/文章的题目或内容搜索到对应的新闻/文章
- 可以通过经纬度显示定位(需要百度api)
- 可以通过简历提交功能发送电邮到指定邮箱(需在填写简历的时候写想要收到邮件的邮箱)
- 可以文件下载(可在后台上传文件)
- 可以上传人脸照片并检测人脸
- 简单的计算机
- 神秘的可爱卡通人跳舞页面

### 未完成功能(且存在于项目中)
- 登入、登出、注册、验证码部分还需完善
- 简历导出自动生成word文档仍待完善
