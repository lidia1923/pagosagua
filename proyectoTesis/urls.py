"""proyectoTesis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from appAgua.views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='vista_login'),
    path('login/', login_view, name='vista_login'),
    path('inicio/', inicio_view, name='vista_inicio'),
    path('logout/', logout_view, name='vista_logout'),

    path('crearUsuario/', registrarUsuario_view, name='crearUsuario'),
    path('listar_usuario/',login_required(ListadoUsuarios.as_view()), name='listar_usuario'),
    path('modificarUsuario/<int:idUsuario>/', actualizarUsuario_view, name='modificarUsuario'),
    
    path('crearTesorero/', crearTesorero_view, name='vista_crearTesorero'),
    path('listarTesoreros/',login_required(ListadoTesoreros.as_view()), name='listarTesoreros'),
    path('editarTesorero/<int:id>/',actualizarTesorero_view, name='vista_editarTesorero'),
    
    path('listarServicios/',login_required(ListadoServicios.as_view()), name='vista_listarServicios'),
    path('nuevoServicio/',nuevoServicioAgua_view, name='vista_nuevoServicioAgua'),
    path('activarServicio/<int:pk>/',login_required(ActivarServicio.as_view()), name='vista_activarServicio'),
    path('suspenderServicio/<int:id>/',SuspenderServicio, name='suspenderServicio'),

    path('listarPagos/',login_required(ListadoPagos.as_view()), name='listarPagos'),
    path('crearPago/',crearPago_view, name='vista_crearPago'),

    path('consultar/<int:pk>/',login_required(ConsultaPagos.as_view()), name='vista_consultarInformacion'),
    path('recibo/<int:pk>/', login_required(ReciboPdf.as_view()), name="recibo"),

    path('historial/',login_required(Historial.as_view()),name='historial'),
]

admin.site.site_header = 'SISTEMA DE PAGOS DE AGUA'
