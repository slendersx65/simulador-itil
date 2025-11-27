from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, MiniCurso, Evaluacion, PlantillaCorreo, PreguntaImagen


@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name', 'edad', 'sexo', 'is_admin', 'rol')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name', 'edad', 'sexo', 'is_admin', 'rol')}),
    )


@admin.register(PlantillaCorreo)
class PlantillaCorreoAdmin(admin.ModelAdmin):
    list_display = ('id', 'es_phishing')
    list_filter = ('es_phishing',)


@admin.register(PreguntaImagen)
class PreguntaImagenAdmin(admin.ModelAdmin):
    list_display = ('id', 'es_phishing')
    list_filter = ('es_phishing',)
    search_fields = ('consejo',)


admin.site.register(MiniCurso)
admin.site.register(Evaluacion)
