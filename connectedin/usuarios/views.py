from django.shortcuts import render, redirect
from usuarios.forms import RegistrarUsuarioForm
from django.contrib.auth.models import User
from perfis.models import Perfil, TimeLine
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages


class RegistrarUsuarioView(View):

    template_name = 'registrar.html'

    def get(self, request):
        return render(request, self.template_name)


    @transaction.atomic()
    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['nome'],
                                               email=dados_form['email'],
                                               password=dados_form['senha'])

            perfil = Perfil(nome=dados_form['nome'],
                            telefone=dados_form['telefone'],
                            nome_empresa=dados_form['nome_empresa'],
                            usuario=usuario)
            perfil.save()

            timeline = TimeLine(perfil_id=perfil.id)
            timeline.save()

            return redirect('index')

        return render(request, self.template_name, {'form':form})


@login_required()
@transaction.atomic()
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Nova senha cadastrada')
            return redirect('index')

    if request.method == 'GET':
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}

        return render(request, 'change_password.html', args)