


from django.urls import path
from . import views

urlpatterns = [
    path("" , views.inicio , name = "home"),
    path("ver_cursos" , views.ver_cursos , name= "cursos"),
    #path("alta_curso/<nombre>" , views.alta_curso),
    path("alumnos" , views.alumnos , name = "alumnos"),
    path("alta_curso" , views.curso_formulario),
    path("baja_curso" , views.baja_formulario),
    path('buscar_curso', views.buscar_curso, name='buscar_curso'),
    path("buscar" , views.buscar),
    path("profesores" , views.profesores , name = "profesores"),
    path("registrar" , views.registrar, name = "registrar"),
    path("ingresar" , views.ver_alumnos, name = "ingresar"),
    path("elimina_curso/<int:id>", views.elimina_curso, name ="elimina_curso"),
    path("editar_curso/ <int:id>", views.editar, name = "editar_curso"),
    ]