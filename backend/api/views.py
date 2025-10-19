from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Site, Verification, WorkflowStep, AuditLog
from .serializers import SiteSerializer, VerificationSerializer, WorkflowStepSerializer
from .permissions import IsStaffOrReadOnly


@api_view(['GET'])
def health(request):
    """Simple health endpoint."""
    return Response({"message": "Server is up!"})


def write_audit_log(user, action: str, instance, metadata: dict | None = None):
    """Helper to write an audit log entry."""
    try:
        AuditLog.objects.create(
            user=user if user.is_authenticated else None,
            action=action,
            model_name=instance.__class__.__name__,
            object_id=str(instance.pk),
            metadata=metadata or {},
        )
    except Exception:
        # Avoid failing main flow due to audit logging errors
        pass


# PUBLIC_INTERFACE
class SiteViewSet(viewsets.ModelViewSet):
    """CRUD for Site with custom verification and step listing."""
    queryset = Site.objects.all().order_by('-created_at')
    serializer_class = SiteSerializer
    permission_classes = [IsAuthenticated & IsStaffOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        write_audit_log(self.request.user, 'create', instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        write_audit_log(self.request.user, 'update', instance)

    @action(detail=True, methods=['post'], url_path='verify')
    def verify(self, request, pk=None):
        """Create a Verification with mock pass/fail and update Site status."""
        site = self.get_object()
        # Mock logic: alternate pass/fail based on current time seconds
        result = 'pass' if timezone.now().second % 2 == 0 else 'fail'
        notes = request.data.get('notes', '')
        verification = Verification.objects.create(
            site=site,
            verified_by=request.user if request.user.is_authenticated else None,
            result=result,
            notes=notes,
        )

        # Update site status
        site.status = 'verified' if result == 'pass' else 'failed'
        site.save(update_fields=['status', 'updated_at'])

        write_audit_log(request.user, 'custom', verification, metadata={'action': 'verify'})
        serializer = VerificationSerializer(verification)
        return Response({'verification': serializer.data, 'site_status': site.status}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='workflow-steps')
    def workflow_steps(self, request, pk=None):
        """List workflow steps for a site."""
        site = self.get_object()
        steps = site.workflow_steps.all().order_by('created_at')
        data = WorkflowStepSerializer(steps, many=True).data
        return Response(data)


# PUBLIC_INTERFACE
class VerificationViewSet(viewsets.ModelViewSet):
    """CRUD for Verification. Creation sets verified_by."""
    queryset = Verification.objects.all().order_by('-created_at')
    serializer_class = VerificationSerializer
    permission_classes = [IsAuthenticated & IsStaffOrReadOnly]

    def perform_create(self, serializer):
        instance = serializer.save(verified_by=self.request.user)
        write_audit_log(self.request.user, 'create', instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        write_audit_log(self.request.user, 'update', instance)


# PUBLIC_INTERFACE
class WorkflowStepViewSet(viewsets.ModelViewSet):
    """CRUD for WorkflowStep with custom completion action."""
    queryset = WorkflowStep.objects.all().order_by('created_at')
    serializer_class = WorkflowStepSerializer
    permission_classes = [IsAuthenticated & IsStaffOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        site_id = self.request.query_params.get('site')
        if site_id:
            qs = qs.filter(site_id=site_id)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        write_audit_log(self.request.user, 'create', instance)

    def perform_update(self, serializer):
        instance = serializer.save()
        write_audit_log(self.request.user, 'update', instance)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete(self, request, pk=None):
        """Mark a workflow step as completed and set completed_at."""
        step = self.get_object()
        step.mark_completed()
        write_audit_log(request.user, 'custom', step, metadata={'action': 'complete'})
        return Response(WorkflowStepSerializer(step).data)
