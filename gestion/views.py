from django.shortcuts import get_object_or_404, redirect, render

from .forms import AutorForm, LibroForm
from .models import Autor, Libro


def inicio(request):
	return redirect('lista_autores')


def lista_autores(request):
	autores = Autor.objects.all()
	return render(request, 'gestion/lista_autores.html', {'autores': autores})


def crear_autor(request):
	form = AutorForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('lista_autores')
	return render(request, 'gestion/form_autor.html', {'form': form})


def editar_autor(request, pk):
	autor = get_object_or_404(Autor, pk=pk)
	form = AutorForm(request.POST or None, instance=autor)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('lista_autores')
	return render(request, 'gestion/form_autor.html', {'form': form, 'autor': autor})


def eliminar_autor(request, pk):
	autor = get_object_or_404(Autor, pk=pk)
	if request.method == 'POST':
		autor.delete()
		return redirect('lista_autores')
	return render(request, 'gestion/eliminar_autor.html', {'autor': autor})


def lista_libros(request):
	libros = Libro.objects.select_related('autor').all()
	return render(request, 'gestion/lista_libros.html', {'libros': libros})


def crear_libro(request):
	form = LibroForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('lista_libros')
	return render(request, 'gestion/form_libro.html', {'form': form})


def editar_libro(request, pk):
	libro = get_object_or_404(Libro, pk=pk)
	form = LibroForm(request.POST or None, instance=libro)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('lista_libros')
	return render(request, 'gestion/form_libro.html', {'form': form, 'libro': libro})


def eliminar_libro(request, pk):
	libro = get_object_or_404(Libro, pk=pk)
	if request.method == 'POST':
		libro.delete()
		return redirect('lista_libros')
	return render(request, 'gestion/eliminar_libro.html', {'libro': libro})
