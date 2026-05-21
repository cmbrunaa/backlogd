from django.shortcuts import render, redirect, get_object_or_404
from .models import Game
from .forms import GameForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .services.rawg_service import buscar_jogos, buscar_detalhes_jogo


@login_required
def home(request):
    filtro = request.GET.get('status')

    games = Game.objects.filter(usuario=request.user)

    if filtro == 'favoritos':
        games = games.filter(favorito=True)
    elif filtro:
        games = games.filter(status=filtro)

    games = games.order_by('-favorito', '-id')

    return render(request, 'games/home.html', {
        'games': games,
        'filtro': filtro
    })


@login_required
def buscar(request):
    jogos = []
    termo = request.GET.get('q')

    if termo:
        jogos = buscar_jogos(termo)

    return render(request, 'games/buscar.html', {
        'jogos': jogos
    })


@login_required
def adicionar_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)

        if form.is_valid():
            game = form.save(commit=False)
            game.usuario = request.user
            game.save()

            return redirect('home')

    else:
        nome = request.GET.get('nome')
        imagem_url = request.GET.get('imagem_url')
        rawg_id = request.GET.get('rawg_id')

        descricao = ''

        if rawg_id:
            detalhes = buscar_detalhes_jogo(rawg_id)

            if detalhes:
                descricao = detalhes.get(
    'descricao_traduzida',
    ''
)

        form = GameForm(initial={
            'nome': nome,
            'imagem_url': imagem_url,
            'rawg_id': rawg_id,
            'descricao': descricao,
        })

    return render(request, 'games/form.html', {
        'form': form,
        'titulo': 'Adicionar jogo'
    })


@login_required
def editar_game(request, id):
    game = get_object_or_404(
        Game,
        id=id,
        usuario=request.user
    )

    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = GameForm(instance=game)

    return render(request, 'games/form.html', {
        'form': form,
        'titulo': 'Editar jogo'
    })


@login_required
def deletar_game(request, id):
    game = get_object_or_404(
        Game,
        id=id,
        usuario=request.user
    )

    if request.method == 'POST':
        game.delete()
        return redirect('home')

    return render(request, 'games/confirmar_delete.html', {
        'game': game
    })


@login_required
def detalhes_game(request, id):
    game = get_object_or_404(
        Game,
        id=id,
        usuario=request.user
    )

    return render(request, 'games/detalhes.html', {
        'game': game
    })


def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            return redirect('home')

    return render(request, 'games/login.html')


def cadastro_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            usuario = User.objects.create_user(
                username=username,
                password=password
            )

            login(request, usuario)
            return redirect('home')

    return render(request, 'games/cadastro.html')


def logout_usuario(request):
    logout(request)
    return redirect('login')