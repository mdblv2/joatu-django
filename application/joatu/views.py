from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import inlineformset_factory

from .models import JoatuUser
from .forms import UserForm, JoatuUserForm

"""Login script. Verify existing user or redirected to signup page if new user. """
@login_required
def profile_edit(request):
    try:
        joatu_user = JoatuUser.objects.get(user=request.user)
    except JoatuUser.DoesNotExist:
        joatu_user = JoatuUser()
        joatu_user.user = request.user
        joatu_user.save()
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=request.user)
        try:
            joatu_user = JoatuUser.objects.get(user=request.user)
        except JoatuUser.DoesNotExist:
            joatu_user = JoatuUser()
            joatu_user.user = request.user
            joatu_user.save()
        joatu_user_form = JoatuUserForm(request.POST, request.FILES, instance=joatu_user)
        if user_form.is_valid() and joatu_user_form.is_valid():
            user_form.save()
            joatu_user_form.save()
            return HttpResponseRedirect('/thanks/')
    else:
        user_form = UserForm(instance=request.user)
        joatu_user_form = JoatuUserForm(instance=joatu_user)
    return render_to_response('profile_edit.html', {
                                'user_form': user_form,
                                'joatu_user_form': joatu_user_form,},
                                context_instance = RequestContext(request))

"""Display signup page for new user"""
@login_required
def profile_redirect(request):
    try:
        joatu_user = JoatuUser.objects.get(user=request.user)
    except JoatuUser.DoesNotExist:
        return HttpResponseRedirect(reverse('profile_create'))
    return HttpResponseRedirect(reverse('profile_detail', kwargs={
                                        'slug': joatu_user.slug, 
                                        }))

class JoatuUserEditView(FormView):
    template_name = 'profile_edit.html'
    success_url = '/success/'


class JoatuUserCreateView(FormView):
    template_name = 'user_create.html'
    form_class = UserCreationForm
    success_url = '/profile/edit/'

    def form_valid(self, form):
        user = form.save()
        joatu_user = JoatuUser()
        joatu_user.user = user
        joatu_user.save()
        return super(JoatuUserCreateView, self).form_valid(form)

