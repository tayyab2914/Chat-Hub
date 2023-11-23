from django.urls import path
from .views import *

urlpatterns = [
    path('<key>', chat, name="chat"),
    path('create/', create, name="create"),
    path('created-rooms/', created_rooms, name="created-rooms"),
    path('join/', join, name="join"),
    path('languages/', language_list, name="languages"),
    path('translate/<key>/', get_translated_text, name="translate")
]
