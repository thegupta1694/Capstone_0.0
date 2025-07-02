from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('team', 'professor', 'status', 'submitted_at', 'responded_at')
    list_filter = ('status', 'submitted_at', 'professor__user__department')
    search_fields = ('team__name', 'professor__user__first_name', 'professor__user__last_name')
    readonly_fields = ('submitted_at', 'responded_at')
    
    fieldsets = (
        ('Application Info', {
            'fields': ('team', 'professor', 'status')
        }),
        ('Messages', {
            'fields': ('message', 'professor_response')
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'responded_at')
        }),
    ) 