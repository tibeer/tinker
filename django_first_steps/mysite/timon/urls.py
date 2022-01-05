from django.urls import path
from django.conf.urls import include

from . import views

app_name = 'timon'
urlpatterns = [
    # /
    path('', views.MainView.as_view(), name='main_view'),
    # Deployment
    path('deployment/', views.DeploymentListView.as_view(), name='deployment_list_view'),
    path('deployment/list/', views.DeploymentListView.as_view(), name='deployment_list_view'),
    path('deployment/create/', views.DeploymentCreateView.as_view(), name='deployment_create_view'),
    path('deployment/detail/<int:pk>/', views.DeploymentDetailView.as_view(), name='deployment_detail_view'),
    path('deployment/update/<int:pk>/', views.DeploymentUpdateView.as_view(), name='deployment_update_view'),
    path('deployment/delete/<int:pk>/', views.DeploymentDeleteView.as_view(), name='deployment_delete_view'),
    # TF Modules
    path('module/', views.ModuleListView.as_view(), name='module_list_view'),
    path('module/list/', views.ModuleListView.as_view(), name='module_list_view'),
    path('module/create/', views.ModuleCreateView.as_view(), name='module_create_view'),
    path('module/detail/<int:pk>/', views.ModuleDetailView.as_view(), name='module_detail_view'),
    path('module/update/<int:pk>/', views.ModuleUpdateView.as_view(), name='module_update_view'),
    path('module/delete/<int:pk>/', views.ModuleDeleteView.as_view(), name='module_delete_view'),
]
