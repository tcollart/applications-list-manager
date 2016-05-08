from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView

from .models import Application


class ApplicationListView(ListView):
    model = Application

    def get_queryset(self):
        """ An application appears in the list if it's public or
        if the author is the current logged in user"""
        queryset = Q(is_private=False)
        if self.request.user.is_authenticated():
            queryset |= Q(author=self.request.user)
        return Application.objects.filter(queryset).order_by('-id')


class ApplicationCreateView(CreateView):
    model = Application
    fields = ('description', 'zip_file', 'is_private',)
    success_url = "/"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/signin/')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ApplicationUpdateView(UpdateView):
    model = Application
    fields = ('description', 'zip_file', 'is_private',)
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        """ Only authors can update their application(s)
        http://stackoverflow.com/a/18172770/3170948 """
        obj = self.get_object()
        if obj.author != self.request.user:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


def signin(request, **kwargs):
    if request.user.is_authenticated():
        return redirect("/")
    else:
        return login(request, **kwargs)


class SignUp(CreateView):
    template_name = 'app/signup.html'
    form_class = UserCreationForm
    success_url = '/signin/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return super().get(request, *args, **kwargs)
