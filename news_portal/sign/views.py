from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class MyView(PermissionRequiredMixin):
    permission_required = ('news.add_post',
                           'news.change_post')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')