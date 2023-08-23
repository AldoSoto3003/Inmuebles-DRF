from django.contrib import admin
from inmuebleslist_app.models import Comentario, Edificacion, Empresa

admin.site.register(Edificacion)
admin.site.register(Empresa)
admin.site.register(Comentario)