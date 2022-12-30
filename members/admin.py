from django.contrib import admin
from .models import Member
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class MemberAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_display_links = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('date_joined', 'last_login')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Member, MemberAdmin)
