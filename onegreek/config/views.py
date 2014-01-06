# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

# view imports
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model

# Only authenticated users can access views using this.
from braces.views import LoginRequiredMixin

# Import the form from users/forms.py
from django.views.generic.edit import FormMixin
from django.contrib import messages


# Import the customized User model
User = get_user_model() # use this function for swapping user model
from django.contrib.auth.models import Group

from django.http import HttpResponseRedirect


def home_view(request):
        user = request.user
        redirect_url = reverse('account_login')
        # is user anon?
        if not user.is_authenticated():
            if not request.GET.get('guest'):
                return redirect(redirect_url)

        return render_to_response('pages/home.html', context_instance=RequestContext(request))
