from django import forms
from captcha.fields import CaptchaField
from db.models import useraccount, Resume


# ==================== 用户注册表单（含验证码） ====================

class UserAccountNewForm(forms.ModelForm):
    username = forms.CharField(max_length=20, label='帐号',
                               help_text='请不要用中文、空白及特殊符号&#@%')
    accountname = forms.CharField(max_length=20, label='姓名')
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, label='密码')
    email = forms.EmailField(required=False, label='电邮信箱')
    user = forms.IntegerField(required=False)
    captcha = CaptchaField(label='验证码', required=True)

    class Meta:
        model = useraccount
        fields = '__all__'


# ==================== 登录表单（含验证码） ====================

class LoginForm(forms.ModelForm):
    username = forms.CharField(
        required=True,
        max_length=20,
        label='帐号',
        widget=forms.TextInput(attrs={'size': '12', 'class': 'inputText'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput, max_length=12, label='密码'
    )
    captcha = CaptchaField(label='验证码', required=True)

    class Meta:
        model = useraccount
        fields = ['username', 'password']


# ==================== 简历表单 ====================

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('name', 'sex', 'personID', 'email', 'birth', 'edu', 'school',
                  'major', 'experience', 'position', 'photo')
        sex_list = (
            ('男', '男'),
            ('女', '女'),
        )
        edu_list = (
            ('大专', '大专'),
            ('本科', '本科'),
            ('硕士', '硕士'),
            ('博士', '博士'),
            ('其它', '其它'),
        )
        widgets = {
            'sex': forms.Select(choices=sex_list),
            'edu': forms.Select(choices=edu_list),
            'photo': forms.FileInput(),
        }
