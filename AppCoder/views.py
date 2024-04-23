from django.shortcuts import render, redirect
from AppCoder.models import Curso, Avatar
from AppCoder.forms import Alumnos_formulario, AvatarForm
from AppCoder.models import Alumnos
from django.http import HttpResponse
from django.template import loader
from AppCoder.forms import Curso_formulario
from AppCoder.forms import Curso_formulario , UserEditForm
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.

def inicio(request):
    return render(request , "padre.html")


def alta_curso(request, nombre):
    curso =  Curso(nombre = nombre , camada = 123456)
    curso.save()

    texto = f"Se guardo en la BD el curso {curso.nombre} {curso.camada}"

    return HttpResponse(texto)

@login_required
def ver_cursos(request):
    cursos = Curso.objects.all()
    dicc = {"cursos" : cursos }
    plantilla = loader.get_template("cursos.html")
    documento = plantilla.render(dicc)
    return HttpResponse(documento) 

def ver_alumnos(request):
    alumnos_registrados = Alumnos.objects.all()
    dicc = {"Alumnos registrados" : alumnos_registrados }
    plantilla = loader.get_template("ingresar.html")
    documento = plantilla.render(dicc)
    return HttpResponse(documento) 



def alumnos(request):
    return render(request , "alumnos.html" )

def profesores(request):
    return render(request , "profesores.html" )

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



def buscar(request):
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        cursos = Curso.objects.filter(nombre__icontains= nombre)
        return render(request, "resultado_busqueda.html", {"cursos" : cursos})

    else:
        return HttpResponse ("Ingrese el nombre del curso")
    

def buscar_curso(request):

    return render(request, "buscar_curso.html")





def registrar(request):
    alumno_nuevo = Alumnos_formulario(request.POST or None)
    if request.method == "POST":
        if alumno_nuevo.is_valid():
            
            nombre = alumno_nuevo.cleaned_data['nombre']
            email = alumno_nuevo.cleaned_data['email']
            alumno = Alumnos(nombre=nombre, email=email)
            alumno.save()
            return render(request, "registrar.html", {'mensaje': 'Alumno registrado exitosamente.'})
    
    return render(request, "registrar.html")

def elimina_curso(request, id):
    
    curso = Curso.objects.get(id=id)
    curso.delete()
    curso= Curso.objects.all()
   

    return render(request, "cursos.html", {"cursos" : curso})

def editar(request , id):
    curso = Curso.objects.get(id=id)
    if request.method == "POST":
        mi_formulario = Curso_formulario( request.POST )
        if mi_formulario.is_valid():
            datos = mi_formulario.cleaned_data
            curso.nombre = datos["nombre"]
            curso.camada = datos["camada"]
            curso.save()
            curso = Curso.objects.all()
            return render(request , "cursos.html" , {"cursos":curso})

        
    else:
        mi_formulario = Curso_formulario(initial={"nombre":curso.nombre , "camada":curso.camada})
    
    return render( request , "editar_curso.html" , {"mi_formulario": mi_formulario , "curso":curso})



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


from django.shortcuts import redirect

def login_request(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            usuario = form.cleaned_data.get("username")
            contra = form.cleaned_data.get("password")

            user = authenticate(username=usuario , password=contra)

            if user is not None:
                login(request , user )
                avatares = Avatar.objects.filter(user=request.user.id)
                return render( request , "inicio.html" , {"url":avatares[0].imagen.url})
            else:
                return HttpResponse(f"Usuario no encontrado")
        else:
            return HttpResponse(f"FORM INCORRECTO {form}")


    form = AuthenticationForm()
    return render( request , "login.html" , {"form":form})



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

        if mi_formulario.is_valid():
            informacion = mi_formulario.cleaned_data
            usuario.email = informacion["email"]
            password = informacion["password1"]
            usuario.set_password(password)
            usuario.save()
            return render(request , "inicio.html")
    else:
        miFormulario = UserEditForm(initial={"email":usuario.email})
    
    return render( request , "editar_perfil.html", {"miFormulario":miFormulario, "usuario":usuario})

def actualizar_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user.avatar)
        if form.is_valid():
            avatar = form.save(commit=False)
            avatar.user = request.user
            avatar.save()
            return redirect('inicio')  # Corregido el nombre de la página de inicio
    else:
        form = AvatarForm(instance=request.user.avatar)  # Cargar avatar existente si hay uno

    return render(request, 'upload_avatar.html', {'form': form})