from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import csv
from .models import Usuario, MiniCurso, Evaluacion, PreguntaImagen
from django import forms


# ------------------------------
# Validación de administrador
# ------------------------------
def is_admin(user):
    return user.is_staff or getattr(user, 'is_admin', False)


# ------------------------------
# Dashboard general
# ------------------------------
@login_required
def dashboard(request):
    return render(request, 'simulador/dashboard.html')


# ------------------------------
# LOGIN / LOGOUT
# ------------------------------
def login_admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.rol == 'admin':
            login(request, user)
            return redirect('simulador:dashboard_admin')
        else:
            messages.error(request, "Credenciales inválidas o no eres administrador.")

    return render(request, 'simulador/login_admin.html')


def login_alumno(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.rol == 'alumno':
            login(request, user)
            return redirect('simulador:dashboard_alumno')
        else:
            messages.error(request, "Credenciales inválidas o no eres alumno.")

    return render(request, 'simulador/login_alumno.html')


def logout_view(request):
    logout(request)
    return redirect('/')


# ------------------------------
# DASHBOARD ROLES
# ------------------------------
@login_required
def dashboard_admin(request):
    if request.user.rol != 'admin':
        return redirect('simulador:dashboard_alumno')

    return render(request, 'simulador/dashboard_admin.html')


@login_required
def dashboard_alumno(request):
    if request.user.rol != 'alumno':
        return redirect('simulador:dashboard_admin')

    return render(request, 'simulador/dashboard_alumno.html')


# ------------------------------
# REGISTRO DE ALUMNO
# ------------------------------
def registro_alumno(request):
    if request.method == 'POST':
        nombre = request.POST.get('full_name')
        edad = request.POST.get('edad')
        sexo = request.POST.get('sexo')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Usuario.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect('registro_alumno')

        Usuario.objects.create(
            full_name=nombre,
            edad=edad,
            sexo=sexo,
            username=username,
            password=make_password(password),
            rol='alumno'
        )

        messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return redirect('simulador:login_alumno')

    return render(request, 'simulador/registro_alumno.html')


# ------------------------------
# MINI CURSO
# ------------------------------
class MiniCursoForm(forms.ModelForm):
    class Meta:
        model = MiniCurso
        fields = ['titulo', 'descripcion', 'contenido_html']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'contenido_html': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }


@login_required
@user_passes_test(is_admin)
def editar_minicurso(request):
    minicurso = MiniCurso.objects.order_by('-fecha_creacion').first()

    if not minicurso:
        minicurso = MiniCurso.objects.create(
            titulo='', descripcion='', contenido_html=''
        )

    if request.method == 'POST':
        form = MiniCursoForm(request.POST, instance=minicurso)
        if form.is_valid():
            form.save()
            messages.success(request, "Mini curso actualizado correctamente.")
            return redirect('simulador:dashboard_admin')
    else:
        form = MiniCursoForm(instance=minicurso)

    return render(request, 'simulador/editar_minicurso.html', {'form': form})


@login_required
def ver_minicurso(request):
    minicurso = MiniCurso.objects.order_by('-fecha_creacion').first()
    return render(request, 'simulador/ver_minicurso.html', {'minicurso': minicurso})


# ------------------------------
# EVALUACIÓN POR IMÁGENES (NUEVO SISTEMA)
# ------------------------------
@login_required
def pregunta(request, numero):
    preguntas = list(PreguntaImagen.objects.all().order_by("id"))
    total = len(preguntas)

    if total == 0:
        messages.error(request, "No hay preguntas cargadas.")
        return redirect("simulador:dashboard_alumno")

    if numero > total:
        return redirect("simulador:finalizar_evaluacion")

    pregunta = preguntas[numero - 1]

    if request.method == "POST":
        resp = request.POST.get("respuesta")

        request.session.setdefault("respuestas", {})
        request.session["respuestas"][str(pregunta.id)] = resp
        request.session.modified = True

        return redirect(f"/evaluacion/{numero + 1}/")

    return render(request, "simulador/pregunta_imagen.html", {
        "pregunta": pregunta,
        "numero": numero,
        "total": total,
    })


@login_required
def finalizar_evaluacion(request):
    respuestas = request.session.get("respuestas", {})
    preguntas = PreguntaImagen.objects.all().order_by("id")

    aciertos = 0
    detalles = []

    for p in preguntas:
        correcta = "phishing" if p.es_phishing else "legitimo"
        respondio = respuestas.get(str(p.id))

        es_correcta = (correcta == respondio)
        if es_correcta:
            aciertos += 1

        detalles.append({
            "pregunta": p,
            "correcta": correcta,
            "respondio": respondio,
            "es_correcta": es_correcta,
            "consejo": p.consejo,
        })

    total = len(preguntas)
    porcentaje = round(aciertos / total * 100, 2)

    Evaluacion.objects.create(
        usuario=request.user,
        aciertos=aciertos,
        total=total,
        porcentaje=porcentaje
    )

    request.session.pop("respuestas", None)

    return render(request, "simulador/resultado_detallado.html", {
        "porcentaje": porcentaje,
        "aciertos": aciertos,
        "total": total,
        "detalles": detalles
    })


# ------------------------------
# EXPORTAR CSV
# ------------------------------
@user_passes_test(is_admin)
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=\"resultados_simulador.csv\"'
    writer = csv.writer(response)

    writer.writerow(['Nombre completo', 'Edad', 'Sexo', 'Aciertos', 'Total', 'Porcentaje', 'Fecha'])

    for e in Evaluacion.objects.select_related('usuario').all():
        writer.writerow([
            e.usuario.full_name,
            e.usuario.edad,
            e.usuario.sexo,
            e.aciertos,
            e.total,
            e.porcentaje,
            e.fecha.strftime("%Y-%m-%d %H:%M")
        ])

    return response

def debug_users(request):
    User = get_user_model()
    users = User.objects.all()
    data = "<h2>Usuarios en Railway</h2><br><br>"

    for u in users:
        data += f"""
        ID: {u.id} |
        username: {u.username} |
        email: {u.email} |
        rol: {u.rol} |
        superuser: {u.is_superuser} |
        staff: {u.is_staff} |
        full_name: {u.full_name}
        <br>
        """

    return HttpResponse(data)