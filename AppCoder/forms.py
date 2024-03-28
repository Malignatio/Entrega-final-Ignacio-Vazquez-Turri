
from django import forms


class Curso_formulario(forms.Form):

    nombre = forms.CharField(max_length=30)
    camada = forms.IntegerField()


class Alumnos_formulario(forms.Form):
    nombre = forms.CharField(max_length=40)
    email = forms.EmailField(max_length=40)

class Profesores_formulario(forms.Form):

    nombre = forms.CharField(max_length=40)
    cursos_dicta = forms.CharField(max_length=40)