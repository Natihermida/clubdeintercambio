from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    if(request.session.get("usuario_id")):
        libros=Libro.objects.all()
        return render(request, "index.html")
        #redirijo a la pagina de login
        return redirect('usuarios:login')