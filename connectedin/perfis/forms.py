from django.forms import ModelForm
from perfis.models import Perfil, Post
from django import forms
from perfis.models import *

class ProfilePhotoForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['photo']


class NovoPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['texto', 'foto']


class AtivarContaForm(forms.Form):
    nome = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def is_valid(self):
        valid = True
        if not super(AtivarContaForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False

        user_exists = User.objects.filter(username=self.cleaned_data['nome']).exists()
        if not user_exists:
            self.adiciona_erro('Nome de usuário inexistente')
            valid = False

        else:
            usuario = User.objects.get(username=self.cleaned_data['nome'])
            if not usuario.check_password(self.cleaned_data['password']):
                self.adiciona_erro('Usuário e/ou senha incorreto')
                valid = False

        return valid

    def adiciona_erro(self, message):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(message)