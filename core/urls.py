from django.urls import path
from .views.index import index, dashboard, edit_profile_pic
from .views.authentication import signup, signin, signout, check_username_email

urlpatterns = [
    path('', index, name="index"),
    path('signup/', signup, name="signup"),
    path('api/validate_email_username/', check_username_email, name="validate_email_username"),
    path('signin/', signin , name="signin"),
    path('signout/', signout , name="signout"),
    path('dashboard/', dashboard, name="dashboard"),
    path('edit_profile_pic/', edit_profile_pic, name="edit_profile_pic"),
]