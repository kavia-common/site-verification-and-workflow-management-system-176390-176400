from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Site, WorkflowStep

User = get_user_model()


class Command(BaseCommand):
    help = "Seed demo users, sites, and workflow steps."

    def handle(self, *args, **options):
        # Create demo users
        admin, _ = User.objects.get_or_create(username="admin", defaults={"is_staff": True, "is_superuser": True})
        if not admin.password:
            admin.set_password("admin123")
            admin.is_staff = True
            admin.is_superuser = True
            admin.save()

        user, _ = User.objects.get_or_create(username="demo", defaults={"email": "demo@example.com"})
        if not user.password:
            user.set_password("demo123")
            user.save()

        # Create sites
        site1, _ = Site.objects.get_or_create(name="Alpha Site", owner=admin, defaults={"address": "123 Alpha St"})
        site2, _ = Site.objects.get_or_create(name="Beta Site", owner=user, defaults={"address": "456 Beta Ave"})

        # Create workflow steps
        for site in (site1, site2):
            WorkflowStep.objects.get_or_create(site=site, name="Initial Review", defaults={"description": "Review submission"})
            WorkflowStep.objects.get_or_create(site=site, name="Field Inspection", defaults={"description": "Inspect onsite"})
            WorkflowStep.objects.get_or_create(site=site, name="Final Approval", defaults={"description": "Approve or reject"})

        self.stdout.write(self.style.SUCCESS("Demo data seeded. Users: admin/admin123, demo/demo123"))
