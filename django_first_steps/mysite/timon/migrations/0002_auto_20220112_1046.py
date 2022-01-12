# Generated by Django 3.2.9 on 2022-01-12 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timon', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='terraformmodule',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='terraformparam',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='deploymentparam',
            unique_together={('deployment_id', 'terraform_param_id')},
        ),
        migrations.AlterUniqueTogether(
            name='terraformparamtomoduleassociation',
            unique_together={('terraform_module_id', 'terraform_param_id')},
        ),
    ]
