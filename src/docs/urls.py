"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.urls import path
from .views import DocsHomePage, CategoryPage, ArticlePage

urlpatterns = [
    path('', DocsHomePage.as_view(), name='docs_home'),
    path('<slug:category_name>', CategoryPage.as_view(), name='docs_category'),
    path('<slug:category_name>/<slug:article_name>', ArticlePage.as_view(), name='docs_article'),
    # path('<slug:category_name>', None, name='docs_search')
]
