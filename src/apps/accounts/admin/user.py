from django.contrib import admin
from src.apps.accounts.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
