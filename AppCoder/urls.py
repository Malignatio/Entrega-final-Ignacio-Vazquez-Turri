


from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("" , views.inicio , name = "home"),
    path("ver_cursos" , views.ver_cursos , name= "cursos"),
    #path("alta_curso/<nombre>" , views.alta_curso),
    path("alumnos" , views.alumnos , name = "alumnos"),
    path("alta_curso" , views.curso_formulario),
    path("baja_curso" , views.baja_formulario),
    path('buscar_curso', views.buscar_curso, name='buscar_curso'),
    path('error_buscar_curso', views.error_buscar_curso, name='error_buscar_curso'),
    path("buscar" , views.buscar),
    path("profesores" , views.profesores , name = "profesores"),
    path("ingresar" , views.ver_alumnos, name = "ingresar"),
    path("elimina_curso/<int:id>", views.elimina_curso, name ="elimina_curso"),
    path("editar_curso/ <int:id>", views.editar, name = "editar_curso"),
    path("login", views.login_request, name = "Login"),
    path("error_login", views.error_login, name = "Error_Login"),
    path("inicio", views.login_inicio, name = "inicio"),
    path("subir_avatar", views.subir_avatar, name = "subir_avatar"),
    path("register", views.register, name= "Register"),
    path("logout" , LogoutView.as_view(template_name="logout.html") , name="Logout"),
    path("editarPerfil" , views.editarPerfil , name="EditarPerfil"),
   
    
    ]