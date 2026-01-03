from django.contrib import admin
from .models import Project, Round, ProcessStep, Node, NodeLink


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'user', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('project', 'round_number', 'created_at')
    list_filter = ('round_number', 'created_at')
    search_fields = ('project__title',)


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('project', 'round', 'step_type', 'created_at')
    list_filter = ('step_type', 'created_at')
    search_fields = ('content',)


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'is_global', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'context')
    
    def is_global(self, obj):
        return obj.project is None
    is_global.boolean = True
    is_global.short_description = 'グローバルノード'


@admin.register(NodeLink)
class NodeLinkAdmin(admin.ModelAdmin):
    list_display = ('from_node', 'to_node', 'weight', 'created_at')
    list_filter = ('created_at',)

