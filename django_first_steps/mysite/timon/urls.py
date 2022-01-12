from django.urls import path
# from django.conf.urls import include

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
    # TF Params
    path('param/', views.ParamListView.as_view(), name='param_list_view'),
    path('param/list/', views.ParamListView.as_view(), name='param_list_view'),
    path('param/create/', views.ParamCreateView.as_view(), name='param_create_view'),
    path('param/detail/<int:pk>/', views.ParamDetailView.as_view(), name='param_detail_view'),
    path('param/update/<int:pk>/', views.ParamUpdateView.as_view(), name='param_update_view'),
    path('param/delete/<int:pk>/', views.ParamDeleteView.as_view(), name='param_delete_view'),
    # Deploy Params
    path('deployparam/', views.DeployParamListView.as_view(), name='deployparam_list_view'),
    path('deployparam/list/', views.DeployParamListView.as_view(), name='deployparam_list_view'),
    path('deployparam/create/', views.DeployParamCreateView.as_view(), name='deployparam_create_view'),
    path('deployparam/detail/<int:pk>/', views.DeployParamDetailView.as_view(), name='deployparam_detail_view'),
    path('deployparam/update/<int:pk>/', views.DeployParamUpdateView.as_view(), name='deployparam_update_view'),
    path('deployparam/delete/<int:pk>/', views.DeployParamDeleteView.as_view(), name='deployparam_delete_view'),
    # TF Param to TF Module Association
    path('moduleparam/', views.ModuleParamListView.as_view(), name='moduleparam_list_view'),
    path('moduleparam/list/', views.ModuleParamListView.as_view(), name='moduleparam_list_view'),
    path('moduleparam/create/', views.ModuleParamCreateView.as_view(), name='moduleparam_create_view'),
    path('moduleparam/detail/<int:pk>/', views.ModuleParamDetailView.as_view(), name='moduleparam_detail_view'),
    # path('moduleparam/update/<int:pk>/', views.ModuleParamUpdateView.as_view(), name='moduleparam_update_view'),
    path('moduleparam/delete/<int:pk>/', views.ModuleParamDeleteView.as_view(), name='moduleparam_delete_view'),
    # Provider
    path('provider/', views.ProviderListView.as_view(), name='provider_list_view'),
    path('provider/list/', views.ProviderListView.as_view(), name='provider_list_view'),
    path('provider/create/', views.ProviderCreateView.as_view(), name='provider_create_view'),
    path('provider/detail/<int:pk>/', views.ProviderDetailView.as_view(), name='provider_detail_view'),
    path('provider/update/<int:pk>/', views.ProviderUpdateView.as_view(), name='provider_update_view'),
    path('provider/delete/<int:pk>/', views.ProviderDeleteView.as_view(), name='provider_delete_view'),
]
