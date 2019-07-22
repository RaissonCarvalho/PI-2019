from django.shortcuts import render
from perfis.models import Perfil, Convite, Post, TimeLine
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from perfis.forms import ProfilePhotoForm, NovoPostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


@login_required()
def index(request):
    storage = messages.get_messages(request)
    perfil_logado = request.user.perfil
    timeline_my_posts = perfil_logado.my_timeline.exibicao()
    page = request.GET.get('page', 1)

    paginator = Paginator(timeline_my_posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html',{'perfis' : Perfil.objects.all(), 'perfil_logado' : perfil_logado, 'posts': posts, 'messages': storage})


@login_required()
def exibir_perfil(request, perfil_id):
    user_logado = request.user

    perfil = Perfil.objects.get(id=perfil_id)
    user_perfil = perfil.usuario

    perfil_logado = get_perfil_logado(request)
    ja_eh_contato = perfil_logado.ja_eh_contato(perfil)

    tem_convite = perfil.tem_convite(perfil_logado)

    perfil_posts = perfil.get_perfil_posts()
    page = request.GET.get('page', 1)

    paginator = Paginator(perfil_posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'perfil.html', {'perfil' : perfil,
                                           'perfil_logado' : perfil_logado,
                                           'ja_eh_contato': ja_eh_contato,
                                           'tem_convite': tem_convite,
                                           'posts': posts,
                                           'user_logado': user_logado,
                                           'user_perfil': user_perfil})


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
        messages.success(request, 'Nova foto de perfil salva')
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
        messages.success(request, 'Post adicionado com sucesso')
        return redirect('index')

    return render(request, 'novo_post.html', {'form': form, 'perfil_logado': perfil_logado})


@login_required()
@transaction.atomic()
def excluir_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.excluir_post()
    messages.success(request, 'Post deletado com sucesso')
    return redirect('index')


@login_required()
@transaction.atomic()
def make_superuser(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    user = perfil.usuario

    user.is_superuser = True
    user.save()
    messages.success(request, 'Novo superusuário cadastrado')
    return redirect('index')


@login_required()
def listar_perfis(request):
    termo_busca = request.GET.get('username', None)

    if termo_busca:
        perfis = Perfil.objects.all()
        perfis = perfis.filter(nome=termo_busca)
    else:
        perfis = Perfil.objects.all()


    perfil_logado = get_perfil_logado(request)

    return render(request, 'perfis_list.html', {'perfis': perfis,
                                                'perfil_logado': perfil_logado})

@login_required()
@transaction.atomic()
def cancelar_solicitacao(request, perfil_id):
    perfil_convidado = Perfil.objects.get(id=perfil_id)
    convite = Convite.objects.get(solicitante=get_perfil_logado(request), convidado=perfil_convidado)
    convite.delete()

    return redirect('index')


@login_required()
@transaction.atomic()
def bloquear_contato(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)

    perfil_logado = get_perfil_logado(request)
    perfil_logado.bloquear_contato(perfil)

    return redirect('index')