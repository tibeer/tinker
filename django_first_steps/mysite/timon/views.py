from distutils.util import strtobool
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
# flake8: noqa
from .models import *
# föale8: noqa
from .forms import *


class MainView(ListView):
    model = Deployment
    template_name = 'timon/main_view.html'


class DeploymentListView(ListView):
    model = Deployment
    template_name = 'timon/deployment_list.html'
    context_object_name = 'terraform_deployment_list'

    def get_queryset(self):
        return Deployment.objects.order_by('-apply_date')


class DeploymentCreateView(CreateView):
    model = Deployment
    fields = ['name', 'comment', 'terraform_module_id', 'provider']
    success_url = reverse_lazy('timon:deployment_list_view')

    def form_valid(self, form):
        timestamp = timezone.now()
        form.instance.username = "osism"
        form.instance.apply_date = timestamp
        form.instance.destroy_date = timestamp
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


class DeploymentDeleteView(DeleteView):
    model = Deployment
    success_url = reverse_lazy('timon:deployment_list_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.destroy_date=timezone.now()
        self.object.save()
        return super().delete(request, *args, **kwargs) 


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
        timestamp = timezone.now()
        form.instance.creation_date = timestamp
        form.instance.deletion_date = timestamp
        return super().form_valid(form)


class ModuleDetailView(DetailView):
    model = TerraformModule
    
    def get_overview(self, id):
        object = TerraformModule.objects.get(pk=id)
        overview = []
        print(object.creation_date)
        print(object.deletion_date)
        overview.append({'field': "Name", 'value': object.name})
        overview.append({'field': "Path", 'value': object.path})
        overview.append({'field': "Creation Date", 'value': object.creation_date})
        overview.append({'field': "Deletion Date", 'value': object.deletion_date})
        overview.append({'field': "Useable", 'value': object.is_useable})
        return overview

    def get_parameters(self, id):
        parameters = []
        parameters_list = TerraformParamToModuleAssociation.objects.filter(terraform_module_id=id)
        for i in parameters_list:
            description = TerraformParam.objects.get(pk=i.terraform_param_id.pk).description
            parameters.append({'field': i.terraform_param_id, 'value': description})
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
        return kwargs


class ModuleDeleteView(DeleteView):
    model = TerraformModule
    success_url = reverse_lazy('timon:module_list_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deletion_date = timezone.now()
        self.object.is_useable = False
        self.object.save()
        return super().delete(request, *args, **kwargs) 

class ParamListView(ListView):
    model = TerraformParam
    template_name = 'timon/terraformparam_list.html'
    context_object_name = 'terraform_param_list'

    def get_queryset(self):
        return TerraformParam.objects.order_by('name')


class ParamCreateView(CreateView):
    model = TerraformParam
    fields = ['name', 'description', 'type']
    success_url = reverse_lazy('timon:param_list_view')

    def form_valid(self, form):
        return super().form_valid(form)


class ParamDetailView(DetailView):
    model = TerraformParam
    
    def get_overview(self, id):
        object = TerraformParam.objects.get(pk=id)
        overview = []
        overview.append({'field': "Name", 'value': object.name})
        overview.append({'field': "Description", 'value': object.description})
        overview.append({'field': "Type", 'value': object.type})
        return overview

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['overview'] = self.get_overview(self.kwargs['pk'])
        return context


class ParamUpdateView(UpdateView):
    model = TerraformParam
    fields = ['name', 'description', 'type']

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs() 
        return kwargs


class ParamDeleteView(DeleteView):
    model = TerraformParam
    success_url = reverse_lazy('timon:param_list_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Abort if referenced TerraformParamToModuleAssociation or DeploymentParam exists
        if TerraformParamToModuleAssociation.objects.filter(terraform_param_id=self.object.pk).count() != 0:
            messages.add_message(request, messages.ERROR, 'Can not delete: referenced TerraformParamToModuleAssociation exists!')
            return HttpResponseRedirect(reverse_lazy('timon:param_detail_view', args=(self.object.pk,)))
        if DeploymentParam.objects.filter(terraform_param_id=self.object.pk).count() != 0:
            messages.add_message(request, messages.ERROR, 'Can not delete: referenced DeploymentParam exists!')
            return HttpResponseRedirect(reverse_lazy('timon:param_detail_view', args=(self.object.pk,)))
        return super().delete(request, *args, **kwargs) 


class DeployParamListView(ListView):
    model = DeploymentParam
    template_name = 'timon/deploymentparam_list.html'
    context_object_name = 'deployment_param_list'

    def get_queryset(self):
        return DeploymentParam.objects.order_by('deployment_id')


class DeployParamCreateView(CreateView):
    model = DeploymentParam
    fields = ['deployment_id', 'terraform_param_id', 'value']
    success_url = reverse_lazy('timon:deployparam_list_view')

    def form_valid(self, form):
        desired_type = TerraformParam.objects.get(pk=form.instance.terraform_param_id.pk).type
        if check_data_type_DeployParam(form.cleaned_data['value'], desired_type):
            return super().form_valid(form)
        else:
            form.add_error('value', 'data type not matching desired [%s]' % desired_type)
            return super().form_invalid(form)


class DeployParamDetailView(DetailView):
    model = DeploymentParam
    
    def get_overview(self, id):
        object = DeploymentParam.objects.get(pk=id)
        overview = []
        overview.append({'field': "Deployment", 'value': object.deployment_id})
        overview.append({'field': "Parameter", 'value': object.terraform_param_id})
        overview.append({'field': "Value", 'value': object.value})
        return overview

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['overview'] = self.get_overview(self.kwargs['pk'])
        return context


class DeployParamUpdateView(UpdateView):
    model = DeploymentParam
    fields = ['value']

    def form_valid(self, form):
        desired_type = TerraformParam.objects.get(pk=form.instance.terraform_param_id.pk).type
        if check_data_type_DeployParam(form.cleaned_data['value'], desired_type):
            return super().form_valid(form)
        else:
            form.add_error('value', 'data type not matching desired [%s]' % desired_type)
            return super().form_invalid(form)


class DeployParamDeleteView(DeleteView):
    model = DeploymentParam
    success_url = reverse_lazy('timon:deployparam_list_view')


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Abort if referenced Deployment exists
        if Deployment.objects.filter(pk=self.object.deployment_id.pk).count() != 0:
            messages.add_message(request, messages.ERROR, 'Can not delete: referenced Deployment exists!')
            return HttpResponseRedirect(reverse_lazy('timon:deployparam_detail_view', args=(self.object.pk,)))
        return super().delete(request, *args, **kwargs) 


class ModuleParamListView(ListView):
    model = TerraformParamToModuleAssociation
    template_name = 'timon/terraformparamtomoduleassociation_list.html'
    context_object_name = 'module_param_list'

    def get_queryset(self):
        print(TerraformParamToModuleAssociation.objects)
        return TerraformParamToModuleAssociation.objects.order_by('terraform_module_id')


class ModuleParamCreateView(CreateView):
    model = TerraformParamToModuleAssociation
    fields = ['terraform_module_id', 'terraform_param_id']
    success_url = reverse_lazy('timon:moduleparam_list_view')

    def form_valid(self, form):
        return super().form_valid(form)


class ModuleParamDetailView(DetailView):
    model = TerraformParamToModuleAssociation
    
    def get_overview(self, id):
        object = TerraformParamToModuleAssociation.objects.get(pk=id)
        overview = []
        overview.append({'field': "Module", 'value': object.terraform_module_id})
        overview.append({'field': "Parameter", 'value': object.terraform_param_id})
        return overview

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['overview'] = self.get_overview(self.kwargs['pk'])
        return context


# Since updates would break most likely something, don't even offer them
#class ModuleParamUpdateView(UpdateView):
#    model = TerraformParamToModuleAssociation
#    fields = ['']


class ModuleParamDeleteView(DeleteView):
    model = TerraformParamToModuleAssociation
    success_url = reverse_lazy('timon:moduleparam_list_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Abort if refereced DeploymentParam exist
        if DeploymentParam.objects.filter(terraform_param_id=self.object.terraform_param_id).count() != 0:
            messages.add_message(request, messages.ERROR, 'Can not delete: referenced TerraformModule exists!')
            return HttpResponseRedirect(reverse_lazy('timon:moduleparam_detail_view', args=(self.object.pk,)))
        return super().delete(request, *args, **kwargs) 


class ProviderListView(ListView):
    model = Provider
    template_name = 'timon/provider_list.html'
    context_object_name = 'tf_provider_list'

    def get_queryset(self):
        return Provider.objects.order_by('name')


class ProviderCreateView(CreateView):
    model = Provider
    success_url = reverse_lazy('timon:provider_list_view')
    form_class = ProviderCreateForm

    def form_valid(self, form):
        return super().form_valid(form)


class ProviderDetailView(DetailView):
    model = Provider
    
    def get_overview(self, id):
        object = Provider.objects.get(pk=id)
        overview = []
        overview.append({'field': "Name", 'value': object.name})
        overview.append({'field': "Username", 'value': object.username})
        #overview.append({'field': "Password", 'value': object.password})
        overview.append({'field': "Password", 'value': '*****'})
        return overview

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['overview'] = self.get_overview(self.kwargs['pk'])
        return context


class ProviderUpdateView(UpdateView):
    model = Provider
    form_class = ProviderUpdateForm


class ProviderDeleteView(DeleteView):
    model = Provider
    success_url = reverse_lazy('timon:provider_list_view')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Abort if referenced Deployment exists
        if Deployment.objects.filter(provider=self.object.pk).count() != 0:
            messages.add_message(request, messages.ERROR, 'Can not delete: referenced Deployment exists!')
            return HttpResponseRedirect(reverse_lazy('timon:provider_detail_view', args=(self.object.pk,)))
        return super().delete(request, *args, **kwargs)  


def check_data_type_DeployParam(value, desired_type):
    if desired_type == "BOOL":
        try:
            casted_value = bool(strtobool(value))
        except ValueError:
            return False
        return isinstance(type(casted_value), bool)
    elif desired_type == "NUMBER":
        success_state = False
        # try casting int
        try:
            casted_value = int(value)
        except ValueError:
            print("Cannot cast [%s] to int" % value)
        else:
            success_state = isinstance(casted_value, int)
        # try casting float
        try:
            casted_value = float(value)
        except ValueError:
            print("Cannot cast [%s] to float" % value)
        else:
            success_state = isinstance(casted_value, float)
        # try casting complex
        try:
            casted_value = complex(value)
        except ValueError:
            print("Cannot cast [%s] to complex" % value)
        else:
            success_state = isinstance(casted_value, complex)
        # return
        return success_state
    # you cannot validate if it's actually a tuple just from casting
    elif desired_type == "TUPLE" or desired_type == "LIST":
        try:
            casted_value = list(value)
        except ValueError:
            return False
        return isinstance(type(casted_value), list)
    # you cannot validate if it's actually an object just from casting
    elif desired_type == "MAP" or desired_type == "OBJECT":
        try:
            casted_value = dict(value)
        except ValueError:
            return False
        return isinstance(type(casted_value), dict)
    elif desired_type == "NULL":
        return (value == "null")
    elif desired_type == "STRING":
        # no casting required, since the field is already a string
        return isinstance(type(value), str)
    else:
        return False
