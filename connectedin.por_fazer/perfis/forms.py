from django.forms import ModelForm
from perfis.models import Perfil

class ProfilePhotoForm(ModelForm):
    class Meta:
        model = Perfil
        fields = ['photo']