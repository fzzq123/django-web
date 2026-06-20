# django-web
基于Django开发的网站项目

## 环境依赖
python 3.10+
Django

## 部署
Docker & docker-compose

##运行方式
###本地python运行
1.安装依赖
'''bash
pip install -r requirements.txt

2.迁移数据库
python manage.py by makemigrations
python manage.py by migrate

3.启动服务
python manage.py runserver

4.部署
(位于项目目录)
docker compose up -d
