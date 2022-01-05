from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# flake8: noqa
from .models import *
# flake8: noqa
from .forms import *


class MainView(ListView):
    model = Deployment
    template_name = 'timon/main_view.html'


# Deployments
class DeploymentListView(ListView):
    model = Deployment
    template_name = 'timon/deployment_list.html'
    context_object_name = 'terraform_deployment_list'

    def get_queryset(self):
        return Deployment.objects.order_by('-apply_date')


class DeploymentCreateView(CreateView):
    model = Deployment
    fields = ['name', 'comment', 'terraform_module_id']
    success_url = reverse_lazy('timon:deployment_list_view')

    def form_valid(self, form):
        form.instance.username = "tibeer"
        return super().form_valid(form)


class DeploymentDetailView(DetailView):
    model = Deployment
    
    def get_overview(self, id):
        object = Deployment.objects.get(pk=id)
        overview = []
        overview.append({'field': "Terraform Module ID", 'value': object.terraform_module_id})
        overview.append({'field': "Deployment Name", 'value': object.name})
        overview.append({'field': "Comment", 'value': object.comment})
        overview.append({'field': "Apply Date", 'value': object.apply_date})
        overview.append({'field': "Destroy Date", 'value': object.destroy_date})
        overview.append({'field': "Username", 'value': object.username})
        return overview

    def get_details(self, id):
        details = []
        details_list = DeploymentParam.objects.filter(deployment_id=id)
        for i in details_list:
            details.append({'field': i.terraform_param_id, 'value': i.value})
        return details

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['overview'] = self.get_overview(self.kwargs['pk'])
        context['details'] = self.get_details(self.kwargs['pk'])
        return context


class DeploymentUpdateView(UpdateView):
    model = Deployment
    fields = ['name', 'comment']

    def get_success_url(self, **kwargs):
        return reverse("timon:deployment_detail_view", args = (self.object.id,))


class DeploymentDeleteView(DeleteView):
    model = Deployment
    success_url = reverse_lazy('timon:deployment_list_view')

# Modules
class ModuleListView(ListView):
    model = TerraformModule
    template_name = 'timon/terraformmodule_list.html'
    context_object_name = 'terraform_module_list'

    def get_queryset(self):
        return TerraformModule.objects.order_by('name')


class ModuleCreateView(CreateView):
    model = TerraformModule
    fields = ['name', 'path', 'is_useable']
    success_url = reverse_lazy('timon:module_list_view')

    def form_valid(self, form):
        return super().form_valid(form)


class ModuleDetailView(DetailView):
    model = TerraformModule
    
    def get_overview(self, id):
        object = TerraformModule.objects.get(pk=id)
        overview = []
        overview.append({'field': "Name", 'value': object.name})
        overview.append({'field': "Path", 'value': object.path})
        overview.append({'field': "Creation Date", 'value': object.creation_date})
        overview.append({'field': "Deletion Date", 'value': object.deletion_date})
        overview.append({'field': "Useable", 'value': object.is_useable})
        return overview

    def get_parameters(self, id):
        parameters = []
        parameters_list = TerraformParamToModuleAssociation.objects.filter(module_id=id)
        for i in parameters_list:
            parameters.append({'field': i.terraform_param_id, 'value': i.value})
        return parameters

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['overview'] = self.get_overview(self.kwargs['pk'])
        context['parameters'] = self.get_parameters(self.kwargs['pk'])
        return context


class ModuleUpdateView(UpdateView):
    model = TerraformModule
    fields = ['name', 'path', 'is_useable']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs() 
        print(kwargs)
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse("timon:module_detail_view", args = (self.object.id,))


class ModuleDeleteView(DeleteView):
    model = TerraformModule
    success_url = reverse_lazy('timon:module_list_view')