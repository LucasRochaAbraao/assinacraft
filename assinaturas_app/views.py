from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from assinaturas_app.models import Assinatura
import json


class CustomLoginView(LoginView):
    template_name = 'assinaturas_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('assinaturas')

class AssinaturaList(LoginRequiredMixin, ListView):
    model = Assinatura
    context_object_name = 'assinaturas'


class AssinaturaDetail(LoginRequiredMixin, DetailView):
    model = Assinatura
    context_object_name = 'assinatura'
    template_name = 'assinaturas_app/assinatura.html'


class AssinaturaCreate(LoginRequiredMixin, CreateView):
    model = Assinatura
    fields = ['nome', 'setor', 'telefone', 'email']
    success_url = reverse_lazy('assinaturas')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AssinaturaCreate, self).form_valid(form)


class AssinaturaUpdate(LoginRequiredMixin, UpdateView):
    model = Assinatura
    fields = ['nome', 'setor', 'telefone', 'email']
    success_url = reverse_lazy('assinaturas')


class CustomDeleteView(LoginRequiredMixin, DeleteView):
    model = Assinatura
    context_object_name = 'assinatura'
    success_url = reverse_lazy('assinaturas')
