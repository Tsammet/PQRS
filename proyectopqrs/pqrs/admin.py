from django.contrib import admin
from .models import piano
# Register your models here.

class pianoAdmin(admin.ModelAdmin):
    readonly_fields=("created", 'updated')

admin.site.register(piano, pianoAdmin)


