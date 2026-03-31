"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from myapp.views import index, delete_report  # delete_reportを追加
from django.urls import path, include # includeを追加
from myapp.views import index, delete_report, edit_report # edit_reportを追加
from myapp.views import index, delete_report, edit_report, export_csv # export_csvを追加
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # これを追加
    path('', index, name='index'),
    path('delete/<int:report_id>/', delete_report, name='delete_report'), # 削除用のURLを追加
    path('edit/<int:report_id>/', edit_report, name='edit_report'), # これを追加
    path('export/csv/', export_csv, name='export_csv'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # これを追加

