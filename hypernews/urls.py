"""hypernews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from news.views import MainPageView, ViewNews, ViewHome, CreateNewsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.redirect_view, name="redirect"),
    path('news/', ViewHome.as_view()),
    path('news/create/', CreateNewsView.as_view()),
    re_path(r"news/(?P<blog_id>\d+)/", ViewNews.as_view()),
]
