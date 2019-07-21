"""connectedin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from perfis import views as perfis_views
from usuarios import views as usuarios_views
from django.contrib.auth import views as v
from usuarios.views import RegistrarUsuarioView
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', perfis_views.index,name='index'),
    path('perfil/<int:perfil_id>', perfis_views.exibir_perfil, name='exibir'),
    path('perfil/<int:perfil_id>/convidar',perfis_views.convidar, name='convidar'),
    path('convite/<int:convite_id>/aceitar',perfis_views.aceitar, name='aceitar'),
    path('convite/<int:convite_id>/recusar',perfis_views.recusar, name='recusar'),
    path('perfil/<int:perfil_id>/desfazer', perfis_views.desfazer_amizade, name='desfazer_amizade'),
    path('registrar/', RegistrarUsuarioView.as_view(), name = 'registrar'),
    path('login/', v.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('desativar_perfil/',perfis_views.desativar_perfil, name='desativar'),
    path('update_photo/', perfis_views.MudarFotoPerfil, name='update_photo'),
    path('change_password', usuarios_views.ChangePassword, name='change_password'),
    path('novo_post/', perfis_views.novo_post, name='novo_post'),
    path('excluir_post/<int:post_id>', perfis_views.excluir_post, name='exluir_post'),
    path('make_superuser/perfil/<int:perfil_id>', perfis_views.make_superuser, name='make_superuser'),
    path('listar_perfis/', perfis_views.listar_perfis, name='listar_perfis'),
    path('cancelar_solicitacao/<int:perfil_id>', perfis_views.cancelar_solicitacao, name='cancelar_solicitacao'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

