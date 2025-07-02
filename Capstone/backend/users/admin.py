from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProfessorProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'is_active')
    list_filter = ('role', 'department', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'department')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'department')}),
    )


@admin.register(ProfessorProfile)
class ProfessorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'research_domains', 'total_slots', 'filled_slots', 'available_slots')
    list_filter = ('total_slots',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'research_domains')
    readonly_fields = ('available_slots',)
    
    fieldsets = (
        ('Professor Info', {
            'fields': ('user', 'bio')
        }),
        ('Research & Slots', {
            'fields': ('research_domains', 'total_slots', 'filled_slots', 'available_slots')
        }),
    ) 