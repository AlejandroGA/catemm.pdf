from fileinput import filename
from itertools import chain
import os
import urllib2
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from .forms import PrimerRegistroFORM,SegundoRegistroForm, OrderForm
from django.http import HttpResponse
from .models import PrimerRegistro, SegundoRegistro, Productos, ProductOrder, Order
from users.models import User
from io import BytesIO
from reportlab.platypus import  Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
import json
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Image
from datetime import datetime


# Create your views here.
def generar_pdf(request, cliente_id=None):
    im = Image('media/ifes/logo_opt.jpg', width=2*inch, height=2*inch)
    im.hAlign = 'CENTER'
    cliente = get_object_or_404(Order, id=cliente_id)
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "Orden_de_compra.pdf"
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=30,
                            leftMargin=60,
                            topMargin=30,
                            bottonMargin=10,
                            )
    doc.pagesize = landscape(A4)
    order = []

    styles = getSampleStyleSheet()
    header = Paragraph("Orden de compra", styles['Heading1'])
    fetch = [(f.order_date) for f in Order.objects.all() ]
    fecha = Paragraph("Fecha:", styles['Heading2'])
    order.append(im)
    order.append(header)
    order.append(fecha)

    headings = ('Orden de compra', 'Fecha', 'Monto total', 'Usuario', 'Operador','Producto','precio unitario','cantidad','total')
    allorder = [(p.orden_de_compra, p.order_date, p.total_amount, p.user, p.operador, a.product, a.product.price, a.quantity, (a.product.price*a.quantity)) for p in Order.objects.filter(user = cliente_id) for a in ProductOrder.objects.filter(order__user= cliente_id)]

    t = Table([headings] + allorder + fetch)
    t.setStyle(TableStyle(
        [
            ('GRID', (0,0), (10, -1), 1, colors.green),
            ('LINEBELOW', (0,0), (-1,0), 2, colors.greenyellow),
            ('BACKGROUND', (0,0), (-1,0), colors.green)
        ]
    ))

    order.append(t)
    doc.build(order)
    response.write(buff.getvalue())
    buff.close()
    return response





def index(request):
    return render(request, 'index.html',)

def nota_remision(request):
    return render(request, 'nota-remision.html')

def clientes(request):
    usuario = request.user
    cliente = PrimerRegistro.objects.filter(operador__username__contains = usuario)

    tarjeta = SegundoRegistro.objects.filter(operador__username__contains= usuario)
    ordenes = Order.objects.filter(operador__username__contains= usuario)
    return render(request, 'clientes.html', {
        'cliente': cliente,
        'tarjeta': tarjeta,
        'ordenes': ordenes,
    })


def desempeno(request):
    usuario = request.user
    mi_info = User.objects.get(username = usuario)
    total_clientes = PrimerRegistro.objects.filter(operador__username__contains= usuario).count()
    return render(request, 'desempeno.html', {'mi_info':mi_info,'total_clientes':total_clientes})



def primerRegistro(request):
    usuario = request.user
    if request.method == 'POST':
        form = PrimerRegistroFORM(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.operador = usuario
            post.save()
            return redirect('agregar_clientes')
    else:
        form = PrimerRegistroFORM()
    mis_clientes = PrimerRegistro.objects.filter(operador__username__contains=usuario)
    return render(request,'index.html',{'form':form, 'mis_clientes':mis_clientes} )

def PrimerRegistroEdit(request, pk, template_name='editar/primer_registro.html'):
    clientes = get_object_or_404(PrimerRegistro, pk=pk)
    form  = PrimerRegistroFORM(request.POST or None,  instance=clientes)
    if form.is_valid():
        form.save()
        return redirect('agregar_clientes')
    return render(request, template_name, {'form':form})
def PrimerRegistroDelete(request, pk, template_name='delete/confirmacion.html'):
    clientes = get_object_or_404(PrimerRegistro, pk=pk)
    if request.method=='POST':
        clientes.delete()
        return redirect('agregar_clientes')
    return render(request, template_name, {'object':clientes})

def segundoRegistro(request):
    usuario = request.user
    if request.method == 'POST':
        form = SegundoRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            posta = form.save(commit=False)
            posta.operador = usuario
            posta.save()
            return redirect('segundo_registro')
    else:
        form = SegundoRegistroForm()
    mis_clientes = SegundoRegistro.objects.filter(operador__username__contains=usuario)
    return render(request, 'segundo-registro.html', {'form':form, 'mis_clientes':mis_clientes})

def SegundoRegistroEdit(request, pk, template_name='editar/segundo_registro.html'):
     clientes = get_object_or_404(SegundoRegistro, pk=pk)
     form  = SegundoRegistroForm(request.POST or None,  instance=clientes)
     if form.is_valid():
         form.save()
         return redirect('segundo_registro')
     return render(request, template_name, {'form':form})


def SegundoRegistroDelete(request, pk, template_name='delete/confirmacion2.html'):
     clientes = get_object_or_404(SegundoRegistro, pk=pk)
     if request.method=='POST':
         clientes.delete()
         return redirect('segundo_registro')
     return render(request, template_name, {'object':clientes})



def orden_compra1(request, cliente_id=None):
    #data = serializers.serialize("json", Productos.objects.all(), fields=('pk', 'name', 'price'))
    cliente =get_object_or_404(PrimerRegistro, id=cliente_id)
    productos = Productos.objects.all()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            user = cliente
            order_content = json.loads(request.POST['cartJSONdata'])
            order = form.save(commit=False)
            order.user = user
            order.operador = request.user
            order.total_amount = 0
            order.save()   #We have to save the order before calculate ammount
            order.total_amount = saveOrderProducts(order_content, order)
            order.save()
            books = ProductOrder.objects.filter(order=order)
            products = list(chain( books,))
            return redirect('/')
            #return render(request, 'success.html', locals())
    else:
        form = OrderForm()
    #lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
    #serializado = json.dumps(lista)
    return render(request, 'odc/odc1.html', { 'productos':productos,
                                        'cliente':cliente,
                                        'form': form,
                                        #'data':data,
                                       #'lista':serializado,
                                       } )
def orden_compra2(request, cliente_id=None):
    #data = serializers.serialize("json", Productos.objects.all(), fields=('pk', 'name', 'price'))
    cliente =get_object_or_404(PrimerRegistro, id=cliente_id)
    productos = Productos.objects.all()
    #lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
    #serializado = json.dumps(lista)
    return render(request,'odc/odc2.html', { 'productos':productos,
                                        'cliente':cliente,
                                        #'data':data,
                                       #'lista':serializado,
                                       } )

def orden_compra3(request, cliente_id=None):
    #data = serializers.serialize("json", Productos.objects.all(), fields=('pk', 'name', 'price'))
    cliente =get_object_or_404(PrimerRegistro, id=cliente_id)
    productos = Productos.objects.all()
    #lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
    #serializado = json.dumps(lista)
    return render(request,'odc/odc3.html', { 'productos':productos,
                                        'cliente':cliente,
                                        #'data':data,
                                       #'lista':serializado,
                                       } )

def saveOrderProducts(order_content, order):
    amount = 0
    prod_error = False
    for product in order_content:
        product_uid = product['id']
        quantity = product['quantity']
        p_price = product['price']
        amount += float(p_price) * float(quantity)
        product_obj = Productos.objects.get(pk=product_uid)
        product_obj.save()
        prod_order = order.productorder_set.create(product=product_obj, quantity=quantity)

        if not prod_error:
            prod_order.save()
    return amount







