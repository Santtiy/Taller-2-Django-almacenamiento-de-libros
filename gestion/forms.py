from datetime import date

from django import forms

from .models import Autor, Libro


class AutorForm(forms.ModelForm):
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Fecha de nacimiento",
    )

    class Meta:
        model = Autor
        fields = ["nombre", "correo", "nacionalidad", "fecha_nacimiento", "biografia"]
        labels = {
            "nombre": "Nombre completo",
            "correo": "Correo electronico",
            "nacionalidad": "Nacionalidad",
            "biografia": "Biografia",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"placeholder": "Ej. Gabriel Garcia Marquez"}),
            "correo": forms.EmailInput(attrs={"placeholder": "autor@correo.com"}),
            "nacionalidad": forms.TextInput(attrs={"placeholder": "Ej. Colombiana"}),
            "biografia": forms.Textarea(attrs={"rows": 4, "placeholder": "Informacion breve del autor"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                css_class = "form-control"
                if isinstance(field.widget, forms.Select):
                    css_class = "form-select"
                field.widget.attrs["class"] = css_class
            field.widget.attrs.setdefault("autocomplete", "off")
            if field_name == "biografia":
                field.required = False

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data["fecha_nacimiento"]
        if fecha_nacimiento > date.today():
            raise forms.ValidationError("La fecha de nacimiento no puede estar en el futuro.")
        return fecha_nacimiento


class LibroForm(forms.ModelForm):
    fecha_publicacion = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Fecha de publicacion",
    )

    class Meta:
        model = Libro
        fields = ["titulo", "autor", "genero", "fecha_publicacion", "isbn"]
        labels = {
            "titulo": "Titulo",
            "autor": "Autor",
            "genero": "Genero",
            "isbn": "ISBN",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ej. Cien anos de soledad"}),
            "genero": forms.TextInput(attrs={"placeholder": "Ej. Realismo magico"}),
            "isbn": forms.TextInput(attrs={"placeholder": "Ej. 9780307474728"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["autor"].queryset = Autor.objects.order_by("nombre")
        for field in self.fields.values():
            css_class = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
            field.widget.attrs["class"] = css_class
            field.widget.attrs.setdefault("autocomplete", "off")

    def clean_fecha_publicacion(self):
        fecha_publicacion = self.cleaned_data["fecha_publicacion"]
        if fecha_publicacion > date.today():
            raise forms.ValidationError("La fecha de publicacion no puede estar en el futuro.")
        return fecha_publicacion

    def clean_isbn(self):
        isbn = self.cleaned_data["isbn"].replace("-", "").replace(" ", "")
        if len(isbn) not in (10, 13) or not isbn.isdigit():
            raise forms.ValidationError("El ISBN debe tener 10 o 13 digitos numericos.")
        return isbn
