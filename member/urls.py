from django.urls import path
from db.views import member_home, member_edit

urlpatterns = [
    path('', member_home, name='member_home'),
    path('edit/', member_edit, name='member_edit'),
]
