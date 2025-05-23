from django.contrib import admin
from .models import Producto, Categoria, Calificacion, FranjaHoraria, Mesa, NotificacionUsuario, Reserva, Pedido, Notificacion


class MenuAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "precio")
    search_fields = ("nombre", "precio")
    list_filter = ("precio",)


admin.site.register(Categoria)
admin.site.register(Calificacion)
admin.site.register(FranjaHoraria)
admin.site.register(Mesa)
admin.site.register(Reserva)
admin.site.register(Pedido)
admin.site.register(Notificacion)
admin.site.register(NotificacionUsuario)
admin.site.register(Producto, MenuAdmin)
