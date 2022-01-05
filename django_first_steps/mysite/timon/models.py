from django.db import models
from django.utils import timezone
from django.urls import reverse


class ActionLog(models.Model):
    timestamp = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def set_action(self):
        return timezone.now()


class TerraformModule(models.Model):
    name = models.CharField(max_length=255)
    path = models.FilePathField(path='/')
    creation_date = models.DateTimeField(auto_now_add=True)
    deletion_date = models.DateTimeField(auto_now_add=True)
    is_useable = models.BooleanField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('timon:module_detail_view', kwargs={'pk': self.pk})


class TerraformParam(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # bool, string, number, list, touple, map, object, null
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TerraformParamToModuleAssociation(models.Model):
    terraform_module_id = models.ForeignKey(TerraformModule, on_delete=models.CASCADE)
    terraform_param_id = models.ForeignKey(TerraformParam, on_delete=models.CASCADE)


class Deployment(models.Model):
    terraform_module_id = models.ForeignKey(TerraformModule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    comment = models.TextField()
    apply_date = models.DateTimeField(auto_now_add=True)
    destroy_date = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('timon:deployment_detail_view', kwargs={'pk': self.pk})


class DeploymentParam(models.Model):
    deployment_id = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    terraform_param_id = models.ForeignKey(TerraformParam, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
