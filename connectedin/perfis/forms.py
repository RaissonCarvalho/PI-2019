from django.forms import ModelForm
from perfis.models import Perfil, Post

class ProfilePhotoForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['photo']


class NovoPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['texto', 'foto']