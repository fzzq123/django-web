from django.apps import AppConfig

class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'db'
    verbose_name = '产品数据库'