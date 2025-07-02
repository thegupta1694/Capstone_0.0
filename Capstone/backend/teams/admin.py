from django.contrib import admin
from .models import Team, TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader', 'member_count', 'is_full', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'leader__username', 'leader__first_name', 'leader__last_name')
    readonly_fields = ('member_count', 'is_full')
    
    fieldsets = (
        ('Team Info', {
            'fields': ('name', 'leader')
        }),
        ('Status', {
            'fields': ('member_count', 'is_full')
        }),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'status', 'invited_at', 'responded_at')
    list_filter = ('status', 'invited_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'team__name')
    readonly_fields = ('invited_at',) 