from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.views.decorators.http import require_POST

from .forms import EscritorioForm, RegistroForm, ContactoForm, CheckoutForm
from .models import Escritorio, MensajeContacto, Carrito, ItemCarrito, Pedido, ItemPedido


def obtener_o_crear_carrito(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        carrito, _ = Carrito.objects.get_or_create(session_key=request.session.session_key)
    return carrito


def inicio(request):
    return render(request, 'store/inicio.html')


def lista_escritorios(request):
    query = request.GET.get('q')
    if query:
        escritorios = Escritorio.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )
    else:
        escritorios = Escritorio.objects.all()
    return render(request, 'store/lista_escritorios.html', {'escritorios': escritorios})


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})


def detalle_escritorio(request, id):
    escritorio = get_object_or_404(Escritorio, id=id)
    return render(request, 'store/detalle_escritorio.html', {'escritorio': escritorio})


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'store/contacto_exito.html')
    else:
        form = ContactoForm()
    return render(request, 'store/contacto.html', {'form': form})


@require_POST
def agregar_al_carrito(request):
    escritorio = get_object_or_404(Escritorio, id=request.POST.get('escritorio_id'))
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = obtener_o_crear_carrito(request)

    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        escritorio=escritorio,
        defaults={'cantidad': cantidad}
    )

    if not creado:
        item.cantidad += cantidad
        item.save()

    return redirect('detalle_escritorio', id=escritorio.id)


def ver_carrito(request):
    carrito = obtener_o_crear_carrito(request)

    if request.method == 'POST':
        item = get_object_or_404(ItemCarrito, id=request.POST.get('item_id'), carrito=carrito)
        if request.POST.get('action') == 'update':
            cantidad = int(request.POST.get('cantidad', 1))
            if cantidad > 0:
                item.cantidad = cantidad
                item.save()
        elif request.POST.get('action') == 'remove':
            item.delete()
        return redirect('ver_carrito')

    items = ItemCarrito.objects.filter(carrito=carrito)
    total_carrito = sum(item.subtotal() for item in items)

    return render(request, 'store/carrito.html', {
        'carrito': carrito,
        'items': items,
        'total_carrito': total_carrito
    })


def checkout(request):
    carrito = obtener_o_crear_carrito(request)
    items = ItemCarrito.objects.filter(carrito=carrito)

    if not items.exists():
        return redirect('ver_carrito')

    total_carrito = sum(item.subtotal() for item in items)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.user = request.user if request.user.is_authenticated else None
            pedido.total_final = total_carrito
            pedido.completo = True
            pedido.save()

            for item in items:
                ItemPedido.objects.create(
                    pedido=pedido,
                    escritorio=item.escritorio,
                    cantidad=item.cantidad,
                    precio_al_momento=item.escritorio.precio
                )

            items.delete()
            return redirect('confirmacion_pedido', pedido_id=pedido.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email
            initial['nombre_completo'] = f"{request.user.first_name} {request.user.last_name}".strip()
        form = CheckoutForm(initial=initial)

    return render(request, 'store/checkout.html', {
        'items': items,
        'total_carrito': total_carrito,
        'form': form
    })


def confirmacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'store/confirmacion_pedido.html', {'pedido': pedido})


def es_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(es_admin)
def dashboard(request):
    escritorios = Escritorio.objects.all()
    return render(request, 'store/dashboard.html', {'escritorios': escritorios})


@user_passes_test(es_admin)
def lista_mensajes(request):
    mensajes = MensajeContacto.objects.all().order_by('-fecha_envio')
    return render(request, 'store/lista_mensajes.html', {'mensajes': mensajes})


@user_passes_test(es_admin)
def crear_escritorio(request):
    if request.method == 'POST':
        form = EscritorioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EscritorioForm()
    return render(request, 'store/form_escritorio.html', {'form': form, 'titulo': 'Nuevo Escritorio'})


@user_passes_test(es_admin)
def editar_escritorio(request, id):
    escritorio = get_object_or_404(Escritorio, id=id)
    if request.method == 'POST':
        form = EscritorioForm(request.POST, request.FILES, instance=escritorio)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = EscritorioForm(instance=escritorio)
    return render(request, 'store/form_escritorio.html', {'form': form, 'titulo': 'Editar Escritorio'})


@user_passes_test(es_admin)
def eliminar_escritorio(request, id):
    escritorio = get_object_or_404(Escritorio, id=id)
    escritorio.delete()
    return redirect('dashboard')


@user_passes_test(es_admin)
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    return render(request, 'store/lista_pedidos.html', {'pedidos': pedidos})


@user_passes_test(es_admin)
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    items = ItemPedido.objects.filter(pedido=pedido)
    return render(request, 'store/detalle_pedido.html', {'pedido': pedido, 'items': items})
