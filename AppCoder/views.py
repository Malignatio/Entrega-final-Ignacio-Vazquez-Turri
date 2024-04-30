from django.shortcuts import render, redirect
from AppCoder.models import Curso, Avatar
from AppCoder.forms import AvatarForm
from AppCoder.models import Alumnos, Profesores
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from AppCoder.forms import Curso_formulario
from AppCoder.forms import Curso_formulario , UserEditForm
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def inicio(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    url_avatar = avatares[0].imagen.url if avatares.exists() else None
    return render(request, "padre.html", {"url_avatar": url_avatar})


@login_required
def ver_cursos(request):
    cursos = Curso.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    url_avatar = avatares[0].imagen.url if avatares.exists() else None
    dicc = {"cursos" : cursos }
    plantilla = loader.get_template("cursos.html")
    documento = plantilla.render(dicc)
    return render(request , "cursos.html", {"cursos": cursos,"url_avatar":url_avatar if avatares.exists () else None})



def alumnos(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    url_avatar = avatares[0].imagen.url if avatares.exists() else None
    
    return render(request , "alumnos.html", {"alumnos": alumnos, "url_avatar":url_avatar if avatares.exists () else None})


def profesores (request):
    profesores= Profesores.objects.all()
    avatares = Avatar.objects.filter(user=request.user.id)
    url_avatar = avatares[0].imagen.url if avatares.exists() else None

    return render(request , "profesores.html", {"profesores": profesores, "url_avatar":url_avatar if avatares.exists () else None})

def curso_formulario(request):

    if request.method == "POST":

        mi_formulario = Curso_formulario( request.POST )

        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso = Curso( nombre=datos["nombre"] , camada=datos["camada"])
            curso.save()
            return render(request , "formulario.html")


    return render(request , "formulario.html")


def baja_formulario(request):
    return render(request , "baja_formulario.html" )

def error_login(request):
    return render(request , "Error_Login.html" )

def error_buscar_curso(request):
    return render(request , "error_buscar_curso.html" )




def buscar(request):
    if "nombre" in request.GET:
        nombre = request.GET["nombre"]
        cursos = Curso.objects.filter(nombre__icontains=nombre)
        if cursos.exists():
            return render(request, "resultado_busqueda.html", {"cursos": cursos})
        else:
            return render(request, "error_buscarcurso.html")
    else:
        return render(request, "error_buscarcurso.html")
    

def buscar_curso(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    url_avatar = avatares[0].imagen.url if avatares.exists() else None
    return render(request, "buscar_curso.html",{"cursos": buscar_curso,"url_avatar":url_avatar if avatares.exists () else None})



def elimina_curso(request, id):
    avatares = Avatar.objects.filter(user=request.user.id)
    url_avatar = avatares[0].imagen.url if avatares.exists() else None    
    curso = Curso.objects.get(id=id)
    curso.delete()
    curso= Curso.objects.all()
   

    return render(request, "cursos.html", {"cursos" : curso,"url_avatar":url_avatar if avatares.exists () else None})

def editar(request , id):
    avatares = Avatar.objects.filter(user=request.user.id)
    url_avatar = avatares[0].imagen.url if avatares.exists() else None    
    curso = Curso.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Curso_formulario( request.POST )
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso.nombre = datos["nombre"]
            curso.camada = datos["camada"]
            curso.save()
            curso = Curso.objects.all()
            return render(request , "cursos.html" , {"cursos":curso, "url_avatar":url_avatar if avatares.exists () else None})

        
    else:
        mi_formulario = Curso_formulario(initial={"nombre":curso.nombre , "camada":curso.camada , "url_avatar":url_avatar if avatares.exists () else None})
    
    return render( request , "editar_curso.html" , {"mi_formulario": mi_formulario , "curso":curso, "url_avatar":url_avatar if avatares.exists () else None})



def ver_alumnos(request):
    
    alumno = None
    if 'nombre' in request.GET:
        nombre = request.GET['nombre']
        try:
            alumno = Alumnos.objects.get(nombre=nombre)
        except Alumnos.DoesNotExist:   
            f"El alumno no fue encontrado"
            pass  

    return render(request, 'ingresar.html', {'alumno': alumno})



def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            user = authenticate(username=usuario , password=contra)

            if user is not None:
                login(request , user)
                avatares = Avatar.objects.filter(user=request.user.id)
                url_avatar = avatares[0].imagen.url if avatares.exists() else None

                if avatares.exists():  
                    url_avatar = avatares[0].imagen.url if avatares.exists() else None
                    return render(request, "inicio.html", {"url_avatar":url_avatar if avatares.exists () else None})
                else:
                    return render(request, "inicio.html")
            else:
                return render(request, "error_login.html") 
        else:
            return render(request, "error_login.html") 

    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def login_inicio(request):
    if request.method == "GET":
        
        if request.user.is_authenticated:
            avatares = Avatar.objects.filter(user=request.user.id)
            url_avatar = avatares[0].imagen.url if avatares.exists() else None
            if avatares.exists():
                return render(request, "inicio.html", {"url_avatar":url_avatar if avatares.exists () else None})
            else:
               
                return render(request, "inicio.html")
        else:
            
            return render(request, "login.html", {"form": AuthenticationForm()})


def register(request):
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
           
        return render(request, "inicio.html")
    else:
        form = UserCreationForm()
    return render(request , "registro.html" , {"form":form})

def editarPerfil(request):
    usuario = request.user

    if request.method =="POST":
        mi_formulario = UserEditForm(request.POST)
        avatares = Avatar.objects.filter(user=request.user.id)
        url_avatar = avatares[0].imagen.url if avatares.exists() else None

        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            usuario.email = informacion["email"]
            password = informacion["password1"]
            usuario.set_password(password)
            usuario.save()
            return render(request, "inicio.html", {"url_avatar":url_avatar if avatares.exists () else None})
    else:
        miFormulario = UserEditForm(initial={"email":usuario.email} )
    
    return render( request , "editar_perfil.html", {"miFormulario":miFormulario, "usuario":usuario})



def subir_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            Avatar.objects.filter(user=request.user).delete()
            avatar = form.save(commit=False)
            avatar.user = request.user
            avatar.save()
            return redirect('inicio')
    else:
        avatar_instance = Avatar.objects.filter(user=request.user).first()
        form = AvatarForm(instance=avatar_instance)
    
    if avatar_instance:
        url_avatar = avatar_instance.imagen.url
    else:
        url_avatar = None
    
    return render(request, 'subir_avatar.html', {'form': form, 'url_avatar': url_avatar})
