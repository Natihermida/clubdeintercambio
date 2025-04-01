from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Libro
from .forms import LibroForm
from prestamos.models import Prestamo, Estado
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def index(request):
    if(request.session.get('usuario_id')): 
        libros = Libro.objects.filter(usuario_id=request.session.get('usuario_id'))
        return render(request, 'index.html', {'libros': libros}) 
    else:
        #redirijo a la pagina de login
        return redirect('usuarios:login')
    
def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)  
        if user is not None:
            login(request, user)
            return redirect("libros:index")  
        else:
            return render(request, "usuarios/login.html", {"error": "Credenciales incorrectas"})
    
    return render(request, "usuarios/login.html")    

def alta_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.usuario_id = request.session.get('usuario_id')
            form.save()
            return redirect('libros:index')  # Redirige a la lista de libros, por ejemplo.
    else:
        form = LibroForm()
    return render(request, 'alta_libro.html', {'form': form})

def borrar(request, libro_id):
    
        libro = Libro.objects.get(libro_id=libro_id)
        libro.delete()
        return redirect('libros:index')
    
def ver(request, libro_id):
    libro = Libro.objects.get(libro_id=libro_id)
    prestamos= libro.prestamos.all()
    print(prestamos)
    return render(request, 'ver.html', {'libro': libro, 'prestamos': prestamos})

def editar(request,libro_id):
    libro = Libro.objects.get(libro_id=libro_id)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            return redirect('libros:index')  # Redirige a la lista de libros, por ejemplo.
    else:
        form = LibroForm(instance=libro)
        return render(request, 'alta_libro.html', {'form': form})