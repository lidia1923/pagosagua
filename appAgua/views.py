from django.shortcuts import render, redirect
from io import BytesIO
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import *
import json
from django.db.models import Count, Q
#import matplotlib.pyplot as plt
from xhtml2pdf import pisa
from django.template.loader import get_template

class MixinFormInvalid:
    def form_invalid(self, form):
            response = super().form_invalid(form)
            if self.request.is_ajax():
                return JsonResponse(form.errors, status=400)
            else:
                return response

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/inicio/')
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    messages.success(request,"Bienvenido al Sistema de Pagos de Agua")
                    return HttpResponseRedirect('/inicio/')
        form = LoginForm()
        ctx = {'form':form}
        return render(request,'login.html',ctx)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

@login_required(login_url='/login/')
def inicio_view(request):
    usuario = Usuario.objects.all()
    ctx = {'usuario': usuario}
    return render(request,'vista_principal.html', ctx)

################     USUARIO     #################

class ListadoUsuarios(ListView):
    model = Usuario
    template_name = 'usuario/listar_usuarios.html'
    queryset = Usuario.objects.order_by('idUsuario')
    context_object_name = 'usuarios'

def cedula_rep(nro, lista):
    #tesoreros = Tesorero.objects.all()
    numero_ced = nro
    rep = 0
    for l in lista:
        if l.cedula == numero_ced:
            rep = rep + 1
    # for t in tesoreros:
    #     if t.cedula == numero_ced:
    #         rep = rep + 1
    return rep

def user_rep(user, lista):
    user = user
    rep = 0
    for l in lista:
        if l.username == user:
            rep+= 1
    return rep 

def validarCedula(nro):
    l = len(nro)
    if l == 10 or l == 13: # verificar la longitud correcta
        cp = int(nro[0:2])
        if cp >= 1 and cp <= 22: # verificar codigo de provincia
            tercer_dig = int(nro[2])
            if tercer_dig >= 0 and tercer_dig < 6 : # numeros enter 0 y 6
                if l == 10:                   
                    return __validar_ced_ruc(nro,0)                       
                elif l == 13:
                    return __validar_ced_ruc(nro,0) and nro[10:13] != '000' # se verifica q los ultimos numeros no sean 000
            elif tercer_dig == 6:
                return __validar_ced_ruc(nro,1) # sociedades publicas
            elif tercer_dig == 9: # si es ruc
                return __validar_ced_ruc(nro,2) # sociedades privadas
            else:
                return 'Tercer digito invalido'
        else:
            return 'Codigo de provincia incorrecto'
    else:
        return 'Longitud incorrecta del numero ingresado'

def __validar_ced_ruc(nro,tipo):
    total = 0
    if tipo == 0: # cedula y r.u.c persona natural
        base = 10
        d_ver = int(nro[9])# digito verificador
        multip = (2, 1, 2, 1, 2, 1, 2, 1, 2)
    elif tipo == 1: # r.u.c. publicos
        return 'La cedula debe contener 10 digitos'
    elif tipo == 2: # r.u.c. juridicos y extranjeros sin cedula
        return 'La cedula debe contener 10 digitos'
    for i in range(0,len(multip)):
        p = int(nro[i]) * multip[i]
        if tipo == 0:
            total+=p if p < 10 else int(str(p)[0])+int(str(p)[1])
        else:
            total+=p
    mod = total % base
    val = base - mod if mod != 0 else 0
    return val == d_ver

def validarNumero(nro):
    l = len(nro)
    if l == 10:
        return True
    else:
        return False

@login_required
def registrarUsuario_view(request):
    usuarios = Usuario.objects.all()
    users = User.objects.all()
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        cedula = cedula_rep(request.POST.get("cedula",""), usuarios)
        usuario = user_rep(request.POST.get("username"), users)
        cedulaV = validarCedula(request.POST.get("cedula",""))
        celularV = validarNumero(request.POST.get("celular",""))
        if form.is_valid():
            if cedulaV == True:
                if celularV == True:
                    if cedula == 0:
                        if usuario == 0:    
                            user = form.save()
                            usuario = Usuario()
                            usuario.usuarioAgua = user
                            usuario.nombres = form.cleaned_data['nombres']
                            usuario.apellidos = form.cleaned_data['apellidos']
                            usuario.cedula = form.cleaned_data['cedula']
                            usuario.celular = form.cleaned_data['celular']
                            usuario.correo = form.cleaned_data['correo']
                            usuario.save()
                            messages.success(request, "Usuario Registrado con Éxito!")
                            return redirect(to='listar_usuario')
                        else:
                            return render(request,'usuario/registrar_usuario.html',{'error':'Usuario ya Existe','form':form})
                    else:
                        return render(request,'usuario/registrar_usuario.html',{'error':'Cedula ya Existe','form':form})
                else:
                        return render(request,'usuario/registrar_usuario.html',{'error':'Celular debe tener 10 dígitos','form':form})
            else:
                return render(request, 'usuario/registrar_usuario.html',{'error':'Cedula Inválida','form':form})
        else:
            return render(request,'usuario/registrar_usuario.html',{'form':form})
    else:
        return render(request,'usuario/registrar_usuario.html')

@login_required
def actualizarUsuario_view(request, idUsuario):
    usuario = Usuario.objects.get(idUsuario=idUsuario)
    usuarios = Usuario.objects.all()
    if request.method == "POST":
        form = UsuarioForms(request.POST, instance=usuario) 
        if form.is_valid():
            form.save()
            messages.success(request,"Usuario modificado con Éxito!")
            return redirect(to='listar_usuario')
        else:
            form = UsuarioForms(instance=usuario)
    else:
        form = UsuarioForms(instance=usuario)
        return render(request, 'usuario/modificar_usuario.html',{"u":usuario,'form':form})

################     TESOREROS         ###############

class ListadoTesoreros(ListView):
    model = Tesorero
    template_name = 'tesorero/listar_tesoreros.html'
    queryset = Tesorero.objects.order_by('idTesorero')
    context_object_name = 'tesoreros'

@login_required
def crearTesorero_view(request):
    tesoreros = Tesorero.objects.all()
    if request.method == 'POST':
        form = TesoreroForm(request.POST)
        cedula = cedula_rep(request.POST.get("cedula",""), tesoreros)
        cedulaV = validarCedula(request.POST.get("cedula",""))
        celularV = validarNumero(request.POST.get("celular",""))
        if form.is_valid():
            if cedulaV == True:
                if celularV == True:
                    if cedula == 0:
                        tesorero = Tesorero()
                        tesorero.nombres = form.cleaned_data['nombres']
                        tesorero.apellidos = form.cleaned_data['apellidos']
                        tesorero.cedula = form.cleaned_data['cedula']
                        tesorero.celular = form.cleaned_data['celular']
                        tesorero.correo = form.cleaned_data['correo']
                        tesorero.save()
                        messages.success(request, "Tesorero Registrado con Éxito!")
                        return redirect(to='listarTesoreros')
                    else:
                        return render(request,"tesorero/nuevo_tesorero.html", {'error':'Tesorero ya Existe!','form':form})
                else:
                    return render(request, "tesorero/nuevo_tesorero.html",{'error':'Celular debe tener 10 dígitos','form':form})
            else:
                return render(request, "tesorero/nuevo_tesorero.html", {'error':'Cedula Inválida','form':form})
        else:
            return render(request, "tesorero/nuevo_tesorero.html",{'form':form})
    else:
        return render(request,'tesorero/nuevo_tesorero.html')

@login_required
def actualizarTesorero_view(request,id):
    t = Tesorero.objects.get(idTesorero=id)
    tesoreros = Tesorero.objects.all()
    if request.method == 'POST':
        form = TesoreroForm(request.POST, instance=t)
        cedula = request.POST.get("cedula","")
        lonCelular = request.POST.get("celular","")
        if len(lonCelular) == 10:
            if form.is_valid():
                form.save()
                messages.success(request, "Tesorero Actualizado con Éxito!")
                return redirect(to='listarTesoreros')
            else:
                form = TesoreroForm(instance=t)
        else:
            return render(request, "tesorero/modificar_tesorero.html",{'error':'Celular debe tener 10 dígitos','form':form})
    else:
        form = TesoreroForm(instance=t)
        return render(request, 'tesorero/modificar_tesorero.html',{'t':t,'form':form})

################     PAGOS DE AGUA     ###############       

class ListadoPagos(ListView):
    model = Pago
    template_name = 'pagos/listar_pagos.html'
    queryset = Pago.objects.order_by('-mesDesde')
    context_object_name = 'pagos'

@login_required
def crearPago_view(request):
    usuarios = Usuario.objects.all()
    tesoreros = Tesorero.objects.all()
    if request.method == "POST":
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pago registrado con Éxito!")
            return redirect("listarPagos")
        else:
            return render(request, 'pagos/nuevo_pago.html', {"form": form, "usuarios": usuarios, "tesoreros": tesoreros})

    return render(request, 'pagos/nuevo_pago.html', {"usuarios": usuarios, "tesoreros": tesoreros})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')
    return None

class ReciboPdf(View):
    def get(self, request, pk, *args, **kwargs):
        pago = Pago.objects.filter(idPago=pk)
        context = {'pago':pago}
        pdf = render_to_pdf('pagos/recibo-agua.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

#################       SERVICIOS DE AGUA        ################

class ListadoServicios(ListView):
    model = ServicioAgua
    template_name = 'servicios/listar_servicios.html'
    query_set = ServicioAgua.objects.all()
    context_object_name = 'servicios'

@login_required
def nuevoServicioAgua_view(request):
    usuarios = Usuario.objects.all()
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Servicio de Agua Registrado con Éxito!")
            return redirect(to='vista_listarServicios')
        else:
            return render(request, "servicios/nuevo_servicioAgua.html",{'usuarios':usuarios,'form':form})
    else:
        return render(request,'servicios/nuevo_servicioAgua.html',{'usuarios':usuarios})

@login_required
def SuspenderServicio(request, id):
    servicio = ServicioAgua.objects.get(idServicioAgua=id)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            historial = HistorialServicio()
            servicio.costoActivacion = form.cleaned_data['costoActivacion']
            servicio.motivoSuspension = form.cleaned_data['motivoSuspension']
            servicio.estado = False
            historial.usuario = servicio.usuario
            historial.costoActivacion = servicio.costoActivacion
            historial.motivoSuspension = servicio.motivoSuspension
            historial.save()
            servicio.save()
            messages.success(request, "Servicio Suspendido con Éxito!")
            return redirect(to='vista_listarServicios')
        else:
            form = ServicioForm(instance=servicio)
            return render(request, 'servicios/suspender_servicio.html',{'form':form})
    else:
        form = ServicioForm(instance=servicio)
        return render(request, 'servicios/suspender_servicio.html',{'servicio':servicio,'form':form})

class ActivarServicio(MixinFormInvalid, DeleteView):
    model = ServicioAgua
    template_name = 'servicios/activar_servicio.html'
    def post(self, request, pk, *args, **kwargs):
        object = ServicioAgua.objects.get(idServicioAgua=pk)
        object.costoActivacion = 0
        object.motivoSuspension = "Ningún motivo"
        object.estado = True
        object.save()
        messages.success(request, "Servicio Activado con Éxito!")
        return HttpResponseRedirect('/listarServicios/')
    
    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

###############     HISTORIAL          ##############   

class Historial(ListView):
    model = HistorialServicio
    template_name = 'servicios/historial.html'
    query_set = HistorialServicio.objects.all()
    context_object_name = 'serviciosHistorial'

###############    CONSULTAR INFORMACION PAGOS DE AGUA     ################

class ConsultaPagos(ListView):
    def get(self, request, pk, *args, **kwargs):
        pagos = Pago.objects.filter(usuario=pk)
        context = {'pagos':pagos}
        return render(request, 'consultas/consultar_inf.html',context)
