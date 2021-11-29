from django.urls import path
from rango.templatetags import views

# from django.contrib import admin

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.about, name='contact'),
    path('usimu-admin/', views.usimuAdmin, name='usimuAdmin'),
    path('submissions/', views.submission, name='submissions'),
    path('submissions/upload-code/', views.upload_code, name='uploadCode'),
    path('submissions/<int:submission_id>/', views.submission_detail, name='submission_detail'),
    path('ajax/load-cpus/', views.load_cpu, name='ajax_load_cpus'),
    path('ajax/load-simulation-results/', views.load_result, name='ajax_load_results')
    # path('django-admin/', admin.site.urls, name='djangoAdmin'),
    # path('category/<slug:category_name_slug>/',
    #      views.show_category, name='show_category'),
    # path('add_category/', views.add_category, name='add_category'),
    # path('category/<slug:category_name_slug>/add_page/',
    #      views.add_page, name='add_page'),
    # path('restricted/', views.restricted, name='restricted'),

]
