# -*- coding: utf-8 -*-
from django.db import models
from  app.models import SegundoRegistro

# Create your models here.
class ComisionEmpleados(models.Model):
    cliente = models.ForeignKey(SegundoRegistro)
    monto = models.DecimalField(max_digits=7, decimal_places=2)
    liquidado = models.BooleanField()
    operador = models.ForeignKey('users.User', default=1)
    class Meta:
        verbose_name_plural = "Comisión Empleados"