from django.contrib import admin
from .models import Records

admin.site.register(Records)

# @admin.register
# class RecordsAdmin(admin.ModelAdmin):
#     ...