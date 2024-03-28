from django.shortcuts import render
from AppCoder.models import Curso
from AppCoder.forms import Alumnos_formulario
from AppCoder.models import Alumnos
from django.http import HttpResponse
from django.template import loader
from AppCoder.forms import Curso_formulario

# Create your views here.

def inicio(request):
    return render(request , "padre.html")


def alta_curso(request, nombre):
    curso =  Curso(nombre = nombre , camada = 123456)
    curso.save()

    texto = f"Se guardo en la BD el curso {curso.nombre} {curso.camada}"

    return HttpResponse(texto)


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
