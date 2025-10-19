from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Site, Verification, WorkflowStep, AuditLog

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


# PUBLIC_INTERFACE
class SiteSerializer(serializers.ModelSerializer):
    """Serializer for Site model."""
    owner = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Site
        fields = ["id", "name", "address", "owner", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["owner"] = request.user
        return super().create(validated_data)


# PUBLIC_INTERFACE
class VerificationSerializer(serializers.ModelSerializer):
    """Serializer for Verification model."""
    verified_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Verification
        fields = ["id", "site", "verified_by", "result", "notes", "created_at", "updated_at"]
        read_only_fields = ["verified_by"]

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            validated_data["verified_by"] = request.user
        return super().create(validated_data)


# PUBLIC_INTERFACE
class WorkflowStepSerializer(serializers.ModelSerializer):
    """Serializer for WorkflowStep model."""
    assigned_to = UserSimpleSerializer(read_only=True)

    class Meta:
        model = WorkflowStep
        fields = [
            "id",
            "site",
            "name",
            "description",
            "status",
            "assigned_to",
            "completed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["assigned_to", "completed_at"]


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ["id", "user", "action", "model_name", "object_id", "metadata", "created_at", "updated_at"]
        read_only_fields = ["user"]
