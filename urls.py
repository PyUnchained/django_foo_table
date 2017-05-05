from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

import views

urlpatterns = [
    url(r'^table_foo/export_to_excel/(\w+)/$', views.export_to_excel,
        name = 'export_foo_table_excel'),
] 