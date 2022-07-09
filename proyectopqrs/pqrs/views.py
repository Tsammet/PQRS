from django.conf import settings
from django.shortcuts import redirect, render
from .models import piano, pqrs, usuario, agendar_cita
from datetime import datetime, timezone
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.


def creacion_pqrs(request):


    if request.method == "POST":
        rq_tipo_solicitud = request.POST['tipo_solicitud']
        rq_cedula= request.POST['cedula']
        rq_asunto = request.POST['asunto']
        rq_comentario = request.POST['comentario']
        rq_fecha_solicitud = datetime.now()


        try:
            registrado  = usuario.objects.get(cc = rq_cedula)

            registra_pqrs = pqrs(
            tipo_solicitud = rq_tipo_solicitud,
            usuario = registrado,
            asunto = rq_asunto,
            comentario = rq_comentario,
            fecha_solicitud = rq_fecha_solicitud
            )

            registra_pqrs.save()
            
            
            email = registrado.correo
            nombres = registrado.nombres
            apellidos = registrado.apellidos
            fecha = registra_pqrs.fecha_solicitud
            asunto = registra_pqrs.asunto
            id = registra_pqrs.id
            

            template = get_template('pqrs/envio_email_crea_pqrs.html')

            # se renderiza el template y se envian los parametros

            content = template.render({'email':email, 'nombre':nombres, 'apellido':apellidos, 'fecha':fecha, 'asunto':asunto, 'id':id})

            msg = EmailMultiAlternatives(
                'Empresa: STEINWAY & SONS',
                'estimado',
                
                settings.EMAIL_HOST_USER,
                [email]
            )

            msg.attach_alternative(content, 'text/html')
            msg.send()

            # return redirect('pqrs')

        
        except:
            return render(request, 'pqrs/creacion_pqrs.html', {"error": "Usuario no registrado"})

       



    return render(request, 'pqrs/creacion_pqrs.html')




def registro_cliente(request):
    if request.method == "POST":
        rq_nombres = request.POST['nombres']
        rq_apellidos = request.POST['apellidos']
        rq_cedula = request.POST['cedula']
        rq_correo = request.POST['correo']
        rq_tipo_cliente = request.POST['tipo_cliente']

        registrado = usuario.objects.filter(cc__exact=rq_cedula).count()

        if registrado > 0:
            return render(request, 'pqrs/registro_cliente.html', {"error": "Usted ya se encuentra registrado."})

        else:
            registro = usuario(
                nombres = rq_nombres,
                apellidos = rq_apellidos,
                cc = rq_cedula,
                correo = rq_correo,
                tipo_cliente = rq_tipo_cliente
            )

            registro.save()


    return render(request, 'pqrs/registro_cliente.html')



def crm(request):

    tabla_crm = pqrs.objects.all().order_by('-id')


    paginator = Paginator(tabla_crm, 3)
    page =  request.GET.get('page')
    tabla_crm = paginator.get_page(page)


    # todas_pqrs = pqrs.objects.all()
    # asunto_abierto = pqrs.objects.filter(estado_pqrs = "ABIERTO")
    # pregunta = pqrs.objects.filter(tipo_solicitud = "P")
    # queja = pqrs.objects.filter(tipo_solicitud = "Q")
    # reclamo = pqrs.objects.filter(tipo_solicitud = "R")
    # solicitud = pqrs.objects.filter(tipo_solicitud = "S")


    if request.method == "POST":
        if request.POST['submit'] == "todas":
            tabla_crm = pqrs.objects.all()

        if request.POST['submit'] == "abiertas":
            tabla_crm = pqrs.objects.filter(estado_pqrs = "ABIERTO")

        if request.POST['submit'] == "P":
            tabla_crm = pqrs.objects.filter(tipo_solicitud = "P")

        if request.POST['submit'] == "Q":
            tabla_crm = pqrs.objects.filter(tipo_solicitud = "Q")

        if request.POST['submit'] == "R":
            tabla_crm = pqrs.objects.filter(tipo_solicitud = "R")

        if request.POST['submit'] == "S":
            tabla_crm = pqrs.objects.filter(tipo_solicitud = "S")

    return render(request, 'pqrs/CRM.html', {'tabla_crm': tabla_crm})



def fcrm_id(request, id):


    crm = pqrs.objects.get(id = id)

    editando = False

    if request.method == 'POST':

        if request.POST['submit'] == 'editar':

            editando = True

    if request.method == "POST":
        if request.POST['submit']== 'guardar':
            rq_tratamiento = request.POST['tratamiento']
            
            crm.tratamiento = rq_tratamiento
            crm.save()
            

        
    if request.method == 'POST':
        if request.POST['submit'] == 'eliminar':

            crm.delete()
            return redirect('crm')

    if request. method == "POST":
        if request.POST['submit'] == "atender":

            crm.estado_pqrs = "PROGRESO"
            crm.save()

    if request. method == "POST":
        if request.POST['submit'] == "devolver":

            crm.estado_pqrs = "ABIERTO"
            crm.save()
        
    if request. method == "POST":
        if request.POST['submit'] == "cerrar":

            crm.estado_pqrs = "CERRADO"
            crm.save()

    if request. method == "POST":
        if request.POST['submit'] == "reabrir":

            crm.estado_pqrs = "PROGRESO"
            crm.save()

    if request. method == "POST":
        if request.POST['submit'] == "notificar":
            
            email = crm.usuario.correo
            nombres = crm.usuario.nombres
            tratamiento = crm.tratamiento
            apellidos = crm.usuario.apellidos

            template = get_template('pqrs/envio_email_cerrado.html')

            # se renderiza el template y se envian los parametros

            content = template.render({'email':email, 'nombre':nombres, 'tratamiento':tratamiento, 'apellido': apellidos})

            msg = EmailMultiAlternatives(
                'Empresa: STEINWAY & SONS',
                'estimado',
                
                settings.EMAIL_HOST_USER,
                [email]
            )

            msg.attach_alternative(content, 'text/html')
            msg.send()

    
    return render(request, 'pqrs/crm_id.html', {'crm':crm, "editando":editando})

def cliente(request):

    users = usuario.objects.all().order_by('-id')


    paginator = Paginator(users, 3)
    page =  request.GET.get('page')
    users = paginator.get_page(page)

    if request.method == "POST":
        busqueda = request.POST["buscar"]

   
        if busqueda:
            users = usuario.objects.filter(
                Q(nombres__icontains = busqueda) |
                Q(apellidos__icontains = busqueda) |
                Q(tipo_cliente__icontains = busqueda)

            ).distinct()

    return render(request, 'pqrs/cliente.html', {"usuarios":users})

def cliente_pqr(request, id):

    user = usuario.objects.get(id = id)

    # CONSULTA SQL

    # query = "SELECT id FROM pqrs_pqrs"
    # usario_html = usuario.objects.raw(query)

    usuario_html=usuario.objects.filter(id = id)

    pqr = pqrs.objects.filter(usuario__id = id)


    return render(request, 'pqrs/cliente_pqrs.html', {'usuario':user, 'pqr':pqr, 'usser':usuario_html})


def historia(request):
    return render(request, 'pqrs/historia.html')

def nuevo_piano(request):
    if request.method == "POST":
        rq_referencia_piano = request.POST['referencia_piano']
        rq_precio= request.POST['precio']
        rq_contenido = request.POST['contenido']
        rq_imagen = request.FILES['imagen']
        
        reg_piano = piano(
            referencia_piano = rq_referencia_piano,
            precio = rq_precio,
            contenido = rq_contenido,
            image= rq_imagen
        )

        reg_piano.save()

    return render(request, 'pqrs/nuevo_piano.html')


def agendar(request):

    if request.method == "POST":
        rq_cedula = request.POST['cedula']
        rq_asunto_cita = request.POST['asunto_cita']
        rq_fecha_inicio = request.POST['fecha_inicio']
        rq_fecha_salida = request.POST['fecha_salida']
      
    
        registrado  = usuario.objects.get(cc = rq_cedula)

        cita = agendar_cita(
                usuario = registrado,
                asunto_cita  = rq_asunto_cita,
                fecha_inicio = rq_fecha_inicio,
                fecha_salida = rq_fecha_salida
            )

        citas_anteriores = agendar_cita.objects.all()
        cita_valida = True
        cita.fecha_inicio = datetime.strptime(cita.fecha_inicio, '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
        cita.fecha_salida = datetime.strptime(cita.fecha_salida, '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)



        for cita_anterior in citas_anteriores:

            if cita.fecha_inicio >=  cita_anterior.fecha_inicio and cita.fecha_inicio <= cita_anterior.fecha_salida:
                    cita_valida = False

            elif cita.fecha_salida >= cita_anterior.fecha_inicio and cita.fecha_salida <= cita_anterior.fecha_salida:
                    cita_valida = False


        if cita_valida == True:
                cita.save()
                return render(request, 'pqrs/calendar.html', {'valida': 'Su cita ha sido creada con exito'})  
            
        elif cita_valida == False:
                return render(request, 'pqrs/calendar.html', {'error': 'Ya hay una cita reservada a esa hora, intente reservarla en otro horario'})


        email = registrado.correo
        nombres = registrado.nombres
        apellidos = registrado.apellidos
        fecha_inicio = rq_fecha_inicio
        fecha_salida = rq_fecha_salida
        

        template = get_template('pqrs/creacioncita.html')

        content = template.render({'email':email, 'nombre':nombres, 'apellido':apellidos, 'fecha_inicio': fecha_inicio, 'fecha_salida': fecha_salida})

        msg = EmailMultiAlternatives(
                'Empresa: STEINWAY & SONS',
                'estimado',
                
                settings.EMAIL_HOST_USER,
                [email]
            )

        msg.attach_alternative(content, 'text/html')
        msg.send()


    
        return render(request, 'pqrs/calendar.html', {"error": "Debe estar registrado para crear una cita"})
            

    return render(request,'pqrs/calendar.html')

