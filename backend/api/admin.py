from django.contrib import admin
from .models import Site, Verification, WorkflowStep, AuditLog

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "status", "created_at")
    list_filter = ("status", "owner")
    search_fields = ("name", "address")

@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ("id", "site", "verified_by", "result", "created_at")
    list_filter = ("result",)

@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ("id", "site", "name", "status", "assigned_to", "completed_at")
    list_filter = ("status",)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "model_name", "object_id", "user", "created_at")
    list_filter = ("action", "model_name")
