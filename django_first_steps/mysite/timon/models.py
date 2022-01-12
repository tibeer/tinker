from django.db import models
from django.utils import timezone
from django.urls import reverse


# missing
class ActionLog(models.Model):
    timestamp = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def set_action(self):
        return timezone.now()
# end


class TerraformModule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    path = models.FilePathField(path='/', allow_folders=True, allow_files=False)
    creation_date = models.DateTimeField(null=True)
    deletion_date = models.DateTimeField(null=True)
    is_useable = models.BooleanField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('timon:module_detail_view', kwargs={'pk': self.pk})


class TerraformParam(models.Model):
    TF_BOOL = "BOOL"
    TF_STRING = "STRING"
    TF_NUMBER = "NUMBER"
    TF_LIST = "LIST"
    TF_TUPLE = "TOUPLE"
    TF_MAP = "MAP"
    TF_OBJECT = "OBJECT"
    TF_NULL = "NULL"

    TYPE_CHOICES = (
        (TF_BOOL, 'Boolean'),
        (TF_STRING, 'String'),
        (TF_NUMBER, 'Number'),
        (TF_LIST, 'List'),
        (TF_TUPLE, 'Tuple'),
        (TF_MAP, 'Map'),
        (TF_OBJECT, 'Object'),
        (TF_NULL, 'Null'),
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    # bool, string, number, list, touple, map, object, null
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default=TF_STRING)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('timon:param_detail_view', kwargs={'pk': self.pk})


class TerraformParamToModuleAssociation(models.Model):
    terraform_module_id = models.ForeignKey(TerraformModule, on_delete=models.CASCADE)
    terraform_param_id = models.ForeignKey(TerraformParam, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('terraform_module_id', 'terraform_param_id',)

    def get_absolute_url(self):
        return reverse('timon:moduleparam_detail_view', kwargs={'pk': self.pk})


class Provider(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('timon:provider_detail_view', kwargs={'pk': self.pk})


class Deployment(models.Model):
    terraform_module_id = models.ForeignKey(TerraformModule, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    comment = models.TextField()
    apply_date = models.DateTimeField(null=True)
    destroy_date = models.DateTimeField(null=True)
    username = models.CharField(max_length=255)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('timon:deployment_detail_view', kwargs={'pk': self.pk})


class DeploymentParam(models.Model):
    deployment_id = models.ForeignKey(Deployment, on_delete=models.CASCADE)
    terraform_param_id = models.ForeignKey(TerraformParam, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        unique_together = ('deployment_id', 'terraform_param_id',)

    def __str__(self):
        return self.pk

    def get_absolute_url(self):
        return reverse('timon:deployparam_detail_view', kwargs={'pk': self.pk})
