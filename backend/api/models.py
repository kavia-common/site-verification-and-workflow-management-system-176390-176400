from django.conf import settings
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """Abstract base model to track creation and updates."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Site(TimestampedModel):
    """Represents a site to be verified and processed through a workflow."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
        ('in_progress', 'In Progress'),
    ]

    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, default='')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sites'
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='pending')

    def __str__(self) -> str:
        return f"{self.name} ({self.status})"


class Verification(TimestampedModel):
    """A verification record for a given site."""
    RESULT_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail'),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='verifications')
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verifications_performed'
    )
    result = models.CharField(max_length=8, choices=RESULT_CHOICES)
    notes = models.TextField(blank=True, default='')

    def __str__(self) -> str:
        return f"Verification({self.site_id}): {self.result}"


class WorkflowStep(TimestampedModel):
    """Represents a step in the workflow for a site."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('blocked', 'Blocked'),
    ]

    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='workflow_steps')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_steps'
    )
    completed_at = models.DateTimeField(null=True, blank=True)

    def mark_completed(self):
        self.status = 'completed'
        if not self.completed_at:
            self.completed_at = timezone.now()
        self.save(update_fields=['status', 'completed_at', 'updated_at'])

    def __str__(self) -> str:
        return f"{self.name} - {self.status}"


class AuditLog(TimestampedModel):
    """Audit trail for create/update actions with JSON metadata."""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('custom', 'Custom'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=32, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=128)
    object_id = models.CharField(max_length=64)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"{self.action} on {self.model_name}({self.object_id})"
