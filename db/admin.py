import os
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.mail import send_mail
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from djangoProject import settings
from .models import Product, ProductImg, useraccount, MyNew, Ad, Resume, DLdoc


class ProductImgInline(admin.StackedInline):
    model = ProductImg
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImgInline, ]


@admin.register(useraccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'accountname')


@admin.register(MyNew)
class MyNewAdmin(admin.ModelAdmin):
    list_display = ('title', 'newType', 'publishDate', 'views')
    search_fields = ('title', 'description')
    list_filter = ('newType',)


# ==================== 人才招聘 Admin ====================

class AdAdmin(admin.ModelAdmin):
    """招聘广告管理"""
    list_display = ('title', 'publishDate')
    search_fields = ('title', 'description')
    list_filter = ('publishDate',)
    date_hierarchy = 'publishDate'


class ResumeAdmin(admin.ModelAdmin):
    """简历审核管理"""
    list_display = ('name', 'status', 'personID', 'birth', 'edu', 'school',
                    'major', 'position', 'image_data', 'publishDate')
    list_filter = ('status', 'edu', 'sex')
    search_fields = ('name', 'personID', 'school', 'major', 'position')
    date_hierarchy = 'publishDate'
    list_editable = ('status',)
    list_per_page = 20
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'sex', 'personID', 'email', 'birth', 'photo')
        }),
        ('教育背景', {
            'fields': ('edu', 'school', 'major')
        }),
        ('求职信息', {
            'fields': ('position', 'experience')
        }),
        ('审核状态', {
            'fields': ('status',),
            'classes': ('wide',)
        }),
    )
    readonly_fields = ('image_preview',)

    def image_data(self, obj):
        """列表页显示缩略图"""
        if obj.photo:
            return mark_safe(
                '<img src="%s" width="80px" style="border-radius:4px;" />' % obj.photo.url
            )
        return '-'

    image_data.short_description = '个人照片'

    def image_preview(self, obj):
        """详情页显示大图"""
        if obj.photo:
            return mark_safe(
                '<img src="%s" width="200px" style="border-radius:6px;border:2px solid #ddd;" />' % obj.photo.url
            )
        return '未上传照片'

    image_preview.short_description = '照片预览'

    def save_model(self, request, obj, form, change):
        """保存简历时，如果状态发生改变则发送邮件通知，同时生成 Word 文档"""
        if change:
            old_obj = Resume.objects.get(pk=obj.pk)
            if old_obj.status != obj.status and obj.status in (2, 3):
                self._send_status_email(obj)
        super().save_model(request, obj, form, change)
        # 保存后生成 Word 简历文档
        self._generate_word_doc(obj)

    def _send_status_email(self, obj):
        """根据审核状态发送邮件"""
        status_map = {2: '通过', 3: '未通过'}
        status_text = status_map.get(obj.status, '未审')

        if obj.status == 2:
            email_title = '通知：恒达科技招聘初试结果'
            email_body = '恭喜您通过本企业初试'
        else:
            email_title = '通知：恒达科技招聘初试结果'
            email_body = '很遗憾，您未通过本企业初试，感谢您的参与'

        try:
            send_status = send_mail(
                email_title,
                email_body,
                settings.EMAIL_FROM,
                [obj.email],
                fail_silently=True,
            )
        except Exception:
            pass

    def _generate_word_doc(self, instance):
        """根据模板生成 Word 简历文档，保存在 media/contact/recruit/ 下"""
        template_path = os.getcwd() + '/media/contact/recruit.docx'
        if not os.path.exists(template_path):
            return

        try:
            template = DocxTemplate(template_path)

            context = {
                'name': instance.name,
                'personID': instance.personID,
                'sex': instance.sex,
                'email': instance.email,
                'birth': instance.birth,
                'edu': instance.edu,
                'school': instance.school,
                'major': instance.major,
                'position': instance.position,
                'experience': instance.experience or '',
            }

            # 如果有照片，作为 InlineImage 嵌入
            if instance.photo and os.path.exists(instance.photo.path):
                context['photo'] = InlineImage(
                    template, instance.photo.path,
                    width=Mm(30), height=Mm(40)
                )
            else:
                context['photo'] = ''

            template.render(context)

            # 输出路径: media/contact/recruit/姓名_id.docx
            output_dir = os.path.join(os.getcwd(), 'media', 'contact', 'recruit')
            os.makedirs(output_dir, exist_ok=True)
            filename = '%s/%s_%d.docx' % (output_dir, instance.name, instance.id)
            template.save(filename)
        except Exception:
            pass


admin.site.register(Ad, AdAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Product, ProductAdmin)


# ==================== 文件下载 Admin ====================

@admin.register(DLdoc)
class DLdocAdmin(admin.ModelAdmin):
    """文件资料管理"""
    list_display = ('title', 'file', 'publishDate')
    search_fields = ('title',)
    list_filter = ('publishDate',)
    date_hierarchy = 'publishDate'