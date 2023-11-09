from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import UpdateView

from .forms import AccountForm


class Account(LoginRequiredMixin, UpdateView):
    form_class = AccountForm
    model = User
    template_name = 'account_form.html'
    context_object_name = 'user'

    def get_object(self, *args, **kwargs):
        obj = super(Account, self).get_object(*args, **kwargs)
        if not obj.id == self.request.user.id:
            raise Http404
        return obj
