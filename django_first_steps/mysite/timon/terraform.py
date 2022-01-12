
from django.dispatch.dispatcher import receiver
# flake8: noqa
from .models import *
from django.db.models.signals import post_save

@receiver(post_save, sender=TerraformModule)
def tim(sender, instance, **kwargs):
    print("test")
