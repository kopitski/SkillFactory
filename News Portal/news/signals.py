from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from .tasks import new_post_mail

from .models import Post, Category, PostCategory


@receiver(m2m_changed, sender=PostCategory)
def send_mail_to_subs(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_mail(instance)
