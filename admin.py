from django.contrib import admin

# Register your models here.
from models import Table

class TableAdmin(admin.ModelAdmin):
	pass


admin.site.register(Table, TableAdmin)