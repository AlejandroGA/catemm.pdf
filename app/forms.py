# -*- encoding: utf-8 -*-
from .models import PrimerRegistro, SegundoRegistro, Order
from django import forms
from django.forms import ModelForm

class PrimerRegistroFORM(ModelForm):
    class Meta:
        model = PrimerRegistro
        fields = ('nombre', 'apellidos', 'direccion', 'nsn','telefono','empresa','registro_patronal','comision','ife','email','numero_de_cuenta','banco')
        #exclude = ['operador_que_lo_registro',]
        widgets={
            'nombre': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm  col-md-2'}),
            'apellidos': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm  col-md-2'}),
            'direccion': forms.Textarea(attrs={'rows':3,'cols':3,'type':'text','required':'true','class':'form-control form-control-sm'}),
            'nsn': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm','min':'8', 'max':"10"}),
            'telefono': forms.TextInput(attrs={'type':'number','required':'true','class':'form-control form-control-sm','placeholder':'Lada - digitos', 'max':"9999000000"}),
            'empresa': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm','placeholder':'Nombre de la empresa'}),
            'registro_patronal': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm','placeholder':'Número de registro patronal'}),
            'comision': forms.TextInput(attrs={'type':'number','required':'true','class':'form-control form-control-sm','placeholder':'Ejemplo: 15000.00','max':"50000"}),
            'ife': forms.ClearableFileInput(attrs={'type':'file','class':' form-control-sm'}),
            'email': forms.EmailInput(attrs={'type':'email','required':'true','class':'form-control form-control-sm','placeholder':'ejemplo@hotmail.com'}),
            'numero_de_cuenta': forms.TextInput(attrs={'type':'number','required':'true','class':'form-control form-control-sm','placeholder':'ejemplo: 4465-5487-5986-3215', 'max':"9999999999999999"}),
            'banco': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm'}),

        }

class SegundoRegistroForm(ModelForm):
    class Meta:
        model = SegundoRegistro
        fields = ('cliente', 'caratula', 'tarjeta_de_mejoravit', 'numero_tarjeta', 'tarjeta_entregada', 'tarjeta_activa', 'tarjeta_con_fondos', 'credito')
        widgets={
            'cliente': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm col-sm-4'}),
             'caratula': forms.TextInput(attrs={'type':'text','required':'true','class':'form-control form-control-sm  col-sm-4'}),
             'tarjeta_de_mejoravit': forms.ClearableFileInput(attrs={'type':'file','required':'true','class':'form-control form-control-sm  col-sm-4'}),
             'numero_tarjeta': forms.TextInput(attrs={'type':'select','required':'true','class':'form-control form-control-sm  col-md-2','placeholder':'ejemplo: 4488-9988-5533-1122', 'max':"9999999999999999"}),
             'tarjeta_entregada': forms.CheckboxInput(attrs={'class':'form-control form-control-sm  col-md-2'}),
             'tarjeta_activa': forms.CheckboxInput(attrs={'class':'form-control form-control-sm  col-md-2'}),
             'tarjeta_con_fondos': forms.CheckboxInput(attrs={'class':'form-control form-control-sm  col-md-2 '}),
             'credito': forms.TextInput(attrs={'type':'number','required':'true','class':'form-control form-control-sm  col-md-2','max':"9999999999",'placeholder':'Debe contener puntos decimales: 1500.00'}),
         }



class OrderForm(ModelForm):
    class Meta:
        model = Order
        exclude = ('user', 'id', 'total_amount')
        fields = ('orden_de_compra',)
