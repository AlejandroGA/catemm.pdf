# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse


# Create your models here


class PrimerRegistro(models.Model):
    nombre = models.CharField(max_length=55)
    apellidos = models.CharField(max_length=80)
    direccion = models.TextField('dirección', )
    nsn = models.CharField(max_length=15)
    telefono = models.SmallIntegerField('teléfono', )
    empresa = models.CharField(max_length=254)
    registro_patronal = models.CharField(max_length=15)
    comision = models.DecimalField('comisión', max_digits=7, decimal_places=2)
    ife = models.FileField(upload_to='media/ifes')

    email = models.EmailField()
    numero_de_cuenta = models.CharField('número de cuenta', max_length=16)
    banco = models.CharField(max_length=15)
    operador = models.ForeignKey('users.User', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Primer Registro'

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('editar_primer_registro', kwargs={'pk': self.pk})


class SegundoRegistro(models.Model):
    cliente = models.ForeignKey(PrimerRegistro)
    fecha = models.DateField(auto_now_add=True)
    caratula = models.CharField('carátula', max_length=50)
    tarjeta_de_mejoravit = models.FileField(upload_to='media/targeta_infonavit')
    numero_tarjeta = models.SmallIntegerField('número de tarjeta')
    tarjeta_entregada = models.BooleanField()
    tarjeta_activa = models.BooleanField()
    tarjeta_con_fondos = models.BooleanField()
    credito = models.DecimalField('crédito', max_digits=7, decimal_places=2, blank=True, null=True)
    operador = models.ForeignKey('users.User', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Segundo Registro'

    def __str__(self):
        return self.cliente.nombre

    def get_absolute_url(self):
        return reverse('editar_segundo_registro', kwargs={'pk': self.pk})


# en teoria este es el segundo
class TercerRegistro(models.Model):
    cliente = models.ForeignKey(PrimerRegistro)
    compra = models.TextField()
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    efectivo = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)
    numero_credito = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = 'Tercer Registro'

    def __str__(self):
        return self.cliente


class Productos(models.Model):
    name = models.CharField(max_length=100)
    price = models.SmallIntegerField()

    class Meta:
        verbose_name = "Productos"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name

ODC_CHOICES = (
    ('1', 'Orden de Compra 1'),
    ('2', 'Orden de Compra 2'),
    ('3', 'Orden de Compra 3'),
)


class Order(models.Model):
    orden_de_compra = models.CharField(max_length=1,choices=ODC_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='date')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(PrimerRegistro)
    operador = models.ForeignKey('users.User')

    # Total amount should change every time we save
    # because orders can be modified via admin site


    def __str__(self):
        return 'Orden No. %i' % self.id

class ProductOrder(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Productos)
    quantity = models.IntegerField()
