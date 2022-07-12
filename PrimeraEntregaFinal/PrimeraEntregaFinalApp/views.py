from concurrent.futures import ProcessPoolExecutor
from xml.sax.handler import property_declaration_handler
from django.db.models import Q
from django.shortcuts import redirect, render
from django.http import HttpResponse
from PrimeraEntregaFinalApp.models import *
from django.template import Template, Context
from .forms import *
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
def foro(request):
   foro = Foro.objects.all() 
   print(foro)
   return render(request, "PrimeraEntregaFinalApp/foro.html", {"foro":foro})

def inicio(request):
    inicio = Inicio.objects.all()
    print(inicio)
#VER
    if request.user.is_authenticated:
        try:
            avatar = Avatar.objects.get(usuario=request.user)
            url = avatar.imagen.url
        except:
            url = "/media/avatar/generica.jpg"
    return render(request, "PrimeraEntregaFinalApp/index.html", {"inicio": inicio}) 

def base(request):
    return render(request, "PrimeraEntregaFinalApp/base.html", {})

def login_request(request):
    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
                return redirect("login")
        else:
            return redirect("login")
    
    form = AuthenticationForm()

    return render(request,"PrimeraEntregaFinalApp/login.html",{"form":form})

def register_request(request):

    if request.method == "POST":
        
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') # es la primer contraseña, no la confirmacion

            form.save() # registramos el usuario
            # iniciamos la sesion
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
                return redirect("login")

        return render(request,"PrimeraEntregaFinalApp/register.html",{"form":form})

    # form = UserCreationForm()
    form = UserRegisterForm()

    return render(request,"PrimeraEntregaFinalApp/register.html",{"form":form})

def logout_request(request):
    logout(request)
    return redirect("inicio")

@login_required
def agregar_avatar(request):
    
    if request.method == "POST":
            
        form = AvatarForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(username=request.user.username) # usuario con el que estamos loggueados
            avatar = Avatar(usuario=user, imagen=form.cleaned_data["imagen"])
            avatar.save()

            # avatar = Avatar()
            # avatar.usuario = request.user
            # avatar.imagen = form.cleaned_data["imagen"]
            # avatar.save()

            return redirect("inicio")
    else:
        form = AvatarForm()
    return render(request,"PrimeraEntregaFinalApp/agregar_avatar.html",{"form":form})

@login_required
def editar_perfil(request):

    user = request.user # usuario con el que estamos loggueados

    if request.method == "POST":
        
        form = UserEditForm(request.POST) # cargamos datos llenados

        if form.is_valid():

            info = form.cleaned_data
            user.email = info["email"]
            user.first_name = info["first_name"]
            user.last_name = info["last_name"]
            user.avatar = info["avatar"]
            # user.password = info["password1"]

            user.save()

            return redirect("inicio")

    else:
        form = UserEditForm(initial={"email":user.email, "first_name":user.first_name, "last_name":user.last_name})

    return render(request,"PrimeraEntregaFinalApp/editar_perfil.html",{"form":form})



@login_required
def socios(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            socios = Socio.objects.filter( Q(apellido__icontains=search) | Q(deportes__icontains=search) ).values()
            return render(request, "PrimeraEntregaFinalApp/socios.html",{"socios":socios, "search":True, "busqueda":search})
        
    socios = Socio.objects.all()
    print(socios)
    return render(request, "PrimeraEntregaFinalApp/socios.html", {"socios": socios})

@staff_member_required
def crear_socio(request):
    if request.method == "POST":
        formulario = NuevoSocio(request.POST)
        print(formulario)

        if formulario.is_valid:
            info = formulario.cleaned_data
            socios = Socio(nombre=info["nombre"],apellido=info["apellido"],deportes=info["deportes"],edad=info["edad"],email=info["email"])
            socios.save()
            return redirect("socios")

    else:
        formulario = NuevoSocio()
        return render(request,"PrimeraEntregaFinalApp/socio_form.html",{"form":formulario})

@staff_member_required
def eliminar_socio(request, socio_id):
    socio = Socio.objects.get(id=socio_id)
    socio.delete()
    return redirect("socios")

@staff_member_required
def editar_socio(request, socio_id):
    socio = Socio.objects.get(id=socio_id)

    if request.method == "POST":

        formulario = NuevoSocio(request.POST)

        if formulario.is_valid():
            
            info_socio = formulario.cleaned_data
            
            socio.nombre = info_socio["nombre"]
            socio.apellido = info_socio["apellido"]
            socio.edad = info_socio["edad"]
            socio.deportes = info_socio["deportes"]
            socio.email = info_socio["email"]
            socio.save()

            return redirect("socios")

    formulario = NuevoSocio(initial={"nombre":socio.nombre, "apellido":socio.apellido, "edad": socio.edad, "deportes": socio.deportes, "email": socio.email})
    return render(request,"PrimeraEntregaFinalApp/socio_form.html",{"form":formulario})


@staff_member_required
def eliminar_profesor(request, profesor_id):
    profesor = Profesor.objects.get(id=profesor_id)
    profesor.delete()
    return redirect("profesores")

@staff_member_required
def editar_profesor(request, profesor_id):
    profesor = Profesor.objects.get(id=profesor_id)

    if request.method == "POST":

        formulario = NuevoProfesor(request.POST)

        if formulario.is_valid():
            
            info_profe = formulario.cleaned_data
            
            profesor.nombre = info_profe["nombre"]
            profesor.apellido = info_profe["apellido"]
            profesor.deporte = info_profe["deporte"]
            profesor.email = info_profe["email"]
            profesor.save()

            return redirect("profesores")

    formulario = NuevoProfesor(initial={"nombre":profesor.nombre, "apellido":profesor.apellido, "deporte": profesor.deporte, "email": profesor.email})
    return render(request,"PrimeraEntregaFinalApp/profesor_form.html",{"form":formulario})

@login_required
def profesores(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            profesores = Profesor.objects.filter( Q(apellido__icontains=search) | Q(deporte__icontains=search) ).values()
            return render(request, "PrimeraEntregaFinalApp/profesores.html",{"profesores":profesores, "search":True, "busqueda":search})
        
    profesores = Profesor.objects.all()
    print(profesores)
    return render(request,"PrimeraEntregaFinalApp/profesores.html" , {"profesores": profesores})

@staff_member_required
def crear_profesor(request):
    if request.method == "POST":
        formulario = NuevoProfesor(request.POST)
        print(formulario)

        if formulario.is_valid:
            info = formulario.cleaned_data
            profesor = Profesor(nombre=info["nombre"],apellido=info["apellido"],deporte=info["deporte"],email=info["email"])
            profesor.save()
            return redirect("profesores")

    else:
        formulario = NuevoProfesor()
        return render(request,"PrimeraEntregaFinalApp/profesor_form.html",{"form":formulario})



def deportes(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            deportes = Deporte.objects.filter( Q(profesor__icontains=search) | Q(deporte__icontains=search) ).values()
            return render(request, "PrimeraEntregaFinalApp/deportes.html",{"deportes":deportes, "search":True, "busqueda":search})
        
    deportes = Deporte.objects.all()
    print(deportes)
    return render(request, "PrimeraEntregaFinalApp/deportes.html", {"deportes": deportes})

@staff_member_required
def crear_deporte(request):
    if request.method == "POST":
        formulario = NuevoDeporte(request.POST)
        print(formulario)

        if formulario.is_valid:
            info = formulario.cleaned_data
            deporte = Deporte(deporte=info["deporte"],profesor=info["profesor"],horario=info["horario"])
            deporte.save()
            return redirect("deportes")

    else:
        formulario = NuevoDeporte()
        return render(request,"PrimeraEntregaFinalApp/deporte_form.html",{"form":formulario})

@staff_member_required
def eliminar_deporte(request, deporte_id):
    deporte = Deporte.objects.get(id=deporte_id)
    deporte.delete()
    return redirect("deportes")

@staff_member_required
def editar_deporte(request, deporte_id):
    deporte = Deporte.objects.get(id=deporte_id)

    if request.method == "POST":

        formulario = NuevoDeporte(request.POST)

        if formulario.is_valid():
            
            info_deporte = formulario.cleaned_data
            
            deporte.deporte = info_deporte["deporte"]
            deporte.profesor = info_deporte["profesor"]
            deporte.horario = info_deporte["horario"]
            deporte.save()

            return redirect("deportes")

    formulario = NuevoDeporte(initial={"deporte":deporte.deporte, "profesor":deporte.profesor, "horario": deporte.horario})
    return render(request,"PrimeraEntregaFinalApp/deporte_form.html",{"form":formulario})


@login_required
def administracion(request):
    if request.method == "POST":
        search = request.POST["search"]
        if search != "":
            administracion = Administrador.objects.filter( Q(puesto__icontains=search) | Q(apellido__icontains=search) ).values()
            return render(request, "PrimeraEntregaFinalApp/administracion.html",{"administracion":administracion, "search":True, "busqueda":search})
    administracion = Administrador.objects.all()
    print(administracion)
    return render(request, "PrimeraEntregaFinalApp/administracion.html", {"administracion": administracion})   

@staff_member_required
def crear_administrador(request):
    if request.method == "POST":
        formulario = NuevoAdministrador(request.POST)
        print(formulario)

        if formulario.is_valid:
            info = formulario.cleaned_data
            administracion = Administrador(puesto=info["puesto"],nombre=info["nombre"],apellido=info["apellido"],email=info["email"])
            administracion.save()
            return redirect("administracion")

    else:
        formulario = NuevoAdministrador()
        return render(request,"PrimeraEntregaFinalApp/admin_form.html",{"form":formulario})

@staff_member_required
def eliminar_administrador(request, administrador_id):
    administrador = Administrador.objects.get(id=administrador_id)
    administrador.delete()
    return redirect("administracion")

@staff_member_required
def editar_administrador(request, administrador_id):
    
    administracion = Administrador.objects.get(id=administrador_id)

    if request.method == "POST":

        formulario = NuevoAdministrador(request.POST)

        if formulario.is_valid():
            
            info_admin = formulario.cleaned_data
            
            administracion.puesto = info_admin["puesto"]
            administracion.nombre = info_admin["nombre"]
            administracion.apellido = info_admin["apellido"]
            administracion.email = info_admin["email"]
            administracion.save()

            return redirect("administracion")

    formulario = NuevoAdministrador(initial={"puesto":administracion.puesto, "nombre":administracion.nombre, "apellido": administracion.apellido, "email":administracion.email})
    return render(request,"PrimeraEntregaFinalApp/admin_form.html",{"form":formulario})


class SociosList(LoginRequiredMixin, ListView):
    model = Socio
    template_name = "PrimeraEntregaFinalApp/socios_list.html"

class SociosDetail(DetailView):
    model = Socio
    template_name = "PrimeraEntregaFinalApp/socios_detail.html"
    
class AdminDetail(DetailView):
    model = Administrador
    template_name = "PrimeraEntregaFinalApp/admin_detail.html"
    
class DeporteDetail(DetailView):
    model = Deporte
    template_name = "PrimeraEntregaFinalApp/deporte_detail.html"
    
class ProfesorDetail(DetailView):
    model = Profesor
    template_name = "PrimeraEntregaFinalApp/profe_detail.html"
    
class SociosCreate(CreateView):
    model = Socio
    success_url = "/PrimeraEntregaFinalApp/socios/list"
    fields = ["nombre", "apellido", "edad", "deportes", "email"]

class SociosUpdate(UpdateView):
    model = Socio
    success_url = "/PrimeraEntregaFinalApp/socios/list"
    fields = ["nombre", "apellido", "edad", "deportes", "email"]

class SociosDelete(DeleteView):
    model = Socio
    success_url = "/PrimeraEntregaFinalApp/socios/list"
