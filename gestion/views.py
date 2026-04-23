from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AutorForm, LibroForm
from .models import Autor, Libro


def inicio(request):
	return redirect('lista_autores')


def lista_autores(request):
	autores = Autor.objects.order_by('nombre')
	return render(request, 'gestion/lista_autores.html', {'autores': autores})


def crear_autor(request):
	form = AutorForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		autor = form.save()
		messages.success(request, f'Autor "{autor.nombre}" creado correctamente.')
		return redirect('lista_autores')
	return render(request, 'gestion/autor_form.html', {'form': form})


def editar_autor(request, pk):
	autor = get_object_or_404(Autor, pk=pk)
	form = AutorForm(request.POST or None, instance=autor)
	if request.method == 'POST' and form.is_valid():
		autor = form.save()
		messages.success(request, f'Autor "{autor.nombre}" actualizado correctamente.')
		return redirect('lista_autores')
	return render(request, 'gestion/autor_form.html', {'form': form, 'autor': autor})


def eliminar_autor(request, pk):
	autor = get_object_or_404(Autor, pk=pk)
	if request.method == 'POST':
		nombre_autor = autor.nombre
		autor.delete()
		messages.success(request, f'Autor "{nombre_autor}" eliminado correctamente.')
		return redirect('lista_autores')
	return render(request, 'gestion/autor_confirm_delete.html', {'autor': autor})


def lista_libros(request):
	libros = Libro.objects.select_related('autor').order_by('titulo')
	return render(request, 'gestion/lista_libros.html', {'libros': libros})


def crear_libro(request):
	form = LibroForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		libro = form.save()
		messages.success(request, f'Libro "{libro.titulo}" creado correctamente.')
		return redirect('lista_libros')
	return render(request, 'gestion/libro_form.html', {'form': form})


def editar_libro(request, pk):
	libro = get_object_or_404(Libro, pk=pk)
	form = LibroForm(request.POST or None, instance=libro)
	if request.method == 'POST' and form.is_valid():
		libro = form.save()
		messages.success(request, f'Libro "{libro.titulo}" actualizado correctamente.')
		return redirect('lista_libros')
	return render(request, 'gestion/libro_form.html', {'form': form, 'libro': libro})


def eliminar_libro(request, pk):
	libro = get_object_or_404(Libro, pk=pk)
	if request.method == 'POST':
		titulo_libro = libro.titulo
		libro.delete()
		messages.success(request, f'Libro "{titulo_libro}" eliminado correctamente.')
		return redirect('lista_libros')
	return render(request, 'gestion/libro_confirm_delete.html', {'libro': libro})
