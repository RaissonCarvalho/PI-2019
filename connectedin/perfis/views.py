from django.shortcuts import render
from perfis.models import Perfil, Convite, Post, TimeLine
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from perfis.forms import ProfilePhotoForm, NovoPostForm


@login_required()
def index(request):
    perfil_logado = request.user.perfil
    timeline_my_posts = perfil_logado.my_timeline.exibicao()

    return render(request, 'index.html',{'perfis' : Perfil.objects.all(), 'perfil_logado' : perfil_logado, 'timeline_my_posts': timeline_my_posts})


@login_required()
def exibir_perfil(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil_logado.ja_eh_contato(perfil)

    tem_convite = perfil.tem_convite(perfil_logado)

    return render(request, 'perfil.html', {'perfil' : perfil,
                                           'perfil_logado' : perfil_logado,
                                           'ja_eh_contato': ja_eh_contato,
                                           'tem_convite': tem_convite})


@transaction.atomic()
@login_required()
def convidar(request,perfil_id):
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request)
    perfil_logado.convidar(perfil_a_convidar)

    return  redirect('index')


@login_required()
def get_perfil_logado(request):
    return request.user.perfil


@transaction.atomic()
@login_required()
def aceitar(request, convite_id):
    convite = Convite.objects.get(id = convite_id)
    convite.aceitar()

    return redirect('index')


@transaction.atomic()
@login_required()
def desfazer_amizade(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    perfil.desfazer_amizade(get_perfil_logado(request))

    return redirect('index')


@transaction.atomic()
@login_required()
def recusar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.recusar()

    return redirect('index')


@login_required()
@transaction.atomic()
def desativar_perfil(request):
    usuario = request.user
    usuario.is_active = False
    usuario.save()

    return redirect('login')


@login_required()
@transaction.atomic
def MudarFotoPerfil(request):
    perfil = request.user.perfil
    form = ProfilePhotoForm(request.POST or None, request.FILES or None, instance=perfil)
    if form.is_valid():
        form.save()
        return redirect('index')

    return render(request, 'update_foto_perfil.html', {'form':form})


@login_required()
@transaction.atomic()
def novo_post(request):
    perfil_logado = request.user.perfil
    form = NovoPostForm(request.POST or None, request.FILES or None, instance=perfil_logado)
    if form.is_valid():
        dados_form = form.cleaned_data
        post = Post(texto=dados_form['texto'],
                    perfil=perfil_logado,
                    foto=dados_form['foto'])
        post.save()
        return redirect('index')

    return render(request, 'novo_post.html', {'form': form, 'perfil_logado': perfil_logado})