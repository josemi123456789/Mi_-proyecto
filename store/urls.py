from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # =========================================================
    # RUTAS PÚBLICAS Y DE NAVEGACIÓN
    # =========================================================
    path('', views.inicio, name='inicio'),
    path('catalogo/', views.lista_escritorios, name='lista_escritorios'),
    path('escritorio/<int:id>/', views.detalle_escritorio, name='detalle_escritorio'),
    path('contacto/', views.contacto, name='contacto'),

    # =========================================================
    # RUTAS DE AUTENTICACIÓN
    # =========================================================
    path('registro/', views.registro, name='registro'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    # Al hacer logout, redirige al inicio
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),

    # =========================================================
    # RUTAS DE CARRITO Y CHECKOUT (MANUAL)
    # =========================================================
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    # Esta ruta permite añadir items usando el ID del escritorio
    path('carrito/agregar/<int:escritorio_id>/', views.agregar_al_carrito, name='agregar_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido, name='confirmacion_pedido'),

    # =========================================================
    # RUTAS DE PAGO (STRIPE) - ¡NUEVAS!
    # =========================================================
    # Esta ruta procesa el inicio del pago y redirige a Stripe
    path('create-checkout-session/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    # Estas rutas manejan el retorno desde Stripe
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-cancelado/', views.pago_cancelado, name='pago_cancelado'),

    # =========================================================
    # PANEL ADMINISTRATIVO (Dashboard)
    # =========================================================
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gestión de Productos (CRUD)
    path('dashboard/productos/nuevo/', views.crear_escritorio, name='crear_escritorio'),
    path('dashboard/productos/editar/<int:id>/', views.editar_escritorio, name='editar_escritorio'),
    path('dashboard/productos/eliminar/<int:id>/', views.eliminar_escritorio, name='eliminar_escritorio'),

    # Gestión de Mensajes y Pedidos
    path('dashboard/mensajes/', views.lista_mensajes, name='lista_mensajes'),
    path('dashboard/pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('dashboard/pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]

# Configuración para servir archivos MEDIA (imágenes) en desarrollo (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)