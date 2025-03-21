from django.shortcuts import render,get_object_or_404, redirect
from libros.models import Libro
from prestamos.models import Prestamo
from django.contrib.auth.decorators import login_required


def index(request):
    if not request.session.get('usuario_id'):
        return redirect('usuarios:login')

    usuario_id = request.session.get('usuario_id')

    # 1️⃣ Obtener libros que NO son del usuario actual (para solicitar)
   
    libros_disponibles = Libro.objects.exclude(usuario_id=request.session.get('usuario_id')).exclude(libro_id__in=Prestamo.objects.filter(estado_id=3).values('libro_id'))           
   
    

    return render(request, "prestamos/index.html", {
        'libros_disponibles': libros_disponibles,
        
    })

def solicitar(request, libro_id):
    libro = Libro.objects.get(libro_id=libro_id)
    #no solicitar libro ya solicitado
    if(Prestamo.objects.filter(libro_id=libro_id,estado_id=1)):
        return redirect('prestamos:index')
    prestamo = Prestamo(libro=libro, usuario_id=request.session.get('usuario_id'), estado_id=1)
    prestamo.save()
    return redirect('prestamos:index')  # Redirige a la lista de libros, por ejemplo.   

def aceptar(request, prestamos_id):
    prestamo = Prestamo.objects.get(prestamos_id=prestamos_id)
    prestamo.estado_id = 3
    prestamo.save()
    return redirect('prestamos:index')  # Redirige a la lista de libros, por ejemplo.

def cancelar(request, prestamos_id):
    prestamo = Prestamo.objects.get(prestamos_id=prestamos_id)
    prestamo.estado_id = 2
    prestamo.save()
    return redirect('prestamos:index')  # Redirige a la lista de libros, por ejemplo.