from django.db import models
from django.contrib import auth
from django.utils import timezone
from froala_editor.fields import FroalaField
from datetime import datetime


class Product(models.Model):
    PRODUCTS_CHOICES = (
        ('家用机器人', '家用机器人'),
        ('智能监控', '智能监控'),
        ('人脸识别解决方案', '人脸识别解决方案'),
    )
    title = models.CharField(max_length=50, verbose_name='产品标题')
    description = models.TextField(verbose_name='产品详情描述')
    productType = models.CharField(choices=PRODUCTS_CHOICES,
                                   max_length=50,
                                   verbose_name='产品类型')
    price = models.DecimalField(max_digits=7,
                                decimal_places=1,
                                blank=True,
                                null=True,
                                verbose_name='产品价格')
    publishDate = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'
        ordering = ('-publishDate', )


class ProductImg(models.Model):
    product = models.ForeignKey(Product,
                                related_name='productImgs',
                                verbose_name='产品',
                                on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='Product/',
                              blank=True,
                              verbose_name='产品图片')

    class Meta:
        verbose_name = '产品图片'
        verbose_name_plural = '产品图片'


# ========== 新增模型 ==========

class Students(models.Model):
    """学生数据表"""
    name = models.CharField(max_length=12, verbose_name='姓名')
    address = models.CharField(max_length=60, verbose_name='地址')
    age = models.IntegerField(verbose_name='年龄')
    tel = models.CharField(max_length=14, verbose_name='电话')
    memo = models.TextField(blank=True, verbose_name='备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'


class useraccount(models.Model):
    """扩展Django用户模型"""
    user = models.OneToOneField(auth.get_user_model(), on_delete=models.CASCADE)
    accountname = models.CharField(max_length=20, default='', verbose_name='姓名')

    def __str__(self):
        return self.accountname

    class Meta:
        verbose_name = '用户账户'
        verbose_name_plural = '用户账户'


class MyNew(models.Model):
    """新闻/文章模型，使用 Froala 富文本编辑器"""
    NEWS_TYPE = (
        ('企业新闻', '企业新闻'),
        ('行业新闻', '行业新闻'),
        ('通知公告', '通知公告'),
    )
    title = models.CharField(max_length=100, verbose_name='标题')
    description = FroalaField(verbose_name='内容')
    newType = models.CharField(choices=NEWS_TYPE, max_length=50, verbose_name='新闻类型')
    publishDate = models.DateTimeField(default=timezone.now, verbose_name='发布时间')
    views = models.PositiveIntegerField('浏览量', default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = '新闻'
        ordering = ('-publishDate',)


# ==================== 人才招聘 ====================

class Ad(models.Model):
    """招聘广告"""
    title = models.CharField(max_length=50, verbose_name='招聘岗位')
    description = models.TextField(verbose_name='岗位要求')
    publishDate = models.DateTimeField(max_length=20,
                                       default=datetime.now,
                                       verbose_name='发布时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '招聘广告'
        verbose_name_plural = '招聘广告'
        ordering = ('-publishDate', )


class Resume(models.Model):
    """简历"""
    name = models.CharField(max_length=20, verbose_name='姓名')
    personID = models.CharField(max_length=30, verbose_name='身份证号')
    sex = models.CharField(max_length=5, default='男', verbose_name='性别')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    birth = models.DateField(max_length=20,
                             default=datetime.strftime(datetime.now(), "%Y-%m-%d"),
                             verbose_name='出生日期')
    edu = models.CharField(max_length=5, default='本科', verbose_name='学历')
    school = models.CharField(max_length=40, verbose_name='毕业院校')
    major = models.CharField(max_length=40, verbose_name='专业')
    position = models.CharField(max_length=40, verbose_name='申请职位')
    experience = models.TextField(blank=True,
                                  null=True,
                                  verbose_name='学习或工作经历')
    photo = models.ImageField(upload_to='contact/recruit/%Y_%m_%d',
                              verbose_name='个人照片')
    grade_list = (
        (1, '未审'),
        (2, '通过'),
        (3, '未通过'),
    )
    status = models.IntegerField(choices=grade_list,
                                 default=1,
                                 verbose_name='面试成绩')
    publishDate = models.DateTimeField(max_length=20,
                                       default=datetime.now,
                                       verbose_name='提交时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '简历'
        verbose_name_plural = '简历'
        ordering = ('-status', '-publishDate')


# ==================== 文件下载 ====================

class DLdoc(models.Model):
    """可下载的文件资料"""
    title = models.CharField(max_length=250, verbose_name='资料名称')
    file = models.FileField(upload_to='Service/',
                            blank=True,
                            verbose_name='文件资料')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='发布时间')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publishDate']
        verbose_name = "资料"
        verbose_name_plural = verbose_name