# Generated by Django 4.2.7 on 2024-02-09 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import plane.db.models.user
import uuid


def migrate_user_extra_profile(apps, schema_editor):
    Profile = apps.get_model("db", "Profile")
    User = apps.get_model("db", "User")

    Profile.objects.bulk_create(
        [
            Profile(
                user_id=user.get("id"),
                theme=user.get("theme"),
                is_tour_completed=user.get("is_tour_completed"),
                use_case=user.get("use_case"),
                is_onboarded=user.get("is_onboarded"),
                last_workspace_id=user.get("last_workspace_id"),
                billing_address_country=user.get("billing_address_country"),
                billing_address=user.get("billing_address"),
                has_billing_address=user.get("has_billing_address"),
            )
            for user in User.objects.values(
                "id",
                "theme",
                "is_tour_completed",
                "onboarding_step",
                "use_case",
                "role",
                "is_onboarded",
                "last_workspace_id",
                "billing_address_country",
                "billing_address",
                "has_billing_address",
            )
        ],
        batch_size=1000,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("db", "0058_alter_moduleissue_issue_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created At"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("expires", models.DateTimeField()),
                ("token", models.TextField(unique=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Session",
                "verbose_name_plural": "Sessions",
                "db_table": "sessions",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created At"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("theme", models.JSONField(default=dict)),
                ("is_tour_completed", models.BooleanField(default=False)),
                (
                    "onboarding_step",
                    models.JSONField(
                        default=plane.db.models.user.get_default_onboarding
                    ),
                ),
                ("use_case", models.TextField(blank=True, null=True)),
                (
                    "role",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                ("is_onboarded", models.BooleanField(default=False)),
                ("last_workspace_id", models.UUIDField(null=True)),
                (
                    "billing_address_country",
                    models.CharField(default="INDIA", max_length=255),
                ),
                ("billing_address", models.JSONField(null=True)),
                ("has_billing_address", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Profile",
                "verbose_name_plural": "Profiles",
                "db_table": "profiles",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Created At"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Last Modified At"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        db_index=True,
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("provider_account_id", models.CharField(max_length=255)),
                (
                    "provider",
                    models.CharField(
                        choices=[("google", "Google"), ("github", "Github")]
                    ),
                ),
                ("access_token", models.TextField()),
                ("access_token_expired_at", models.DateTimeField(null=True)),
                ("refresh_token", models.TextField(blank=True, null=True)),
                ("refresh_token_expired_at", models.DateTimeField(null=True)),
                (
                    "last_connected_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("metadata", models.JSONField(default=dict)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Account",
                "verbose_name_plural": "Accounts",
                "db_table": "accounts",
                "ordering": ("-created_at",),
                "unique_together": {("provider", "provider_account_id")},
            },
        ),
        migrations.RunPython(migrate_user_extra_profile),
        migrations.RemoveField(
            model_name="user",
            name="billing_address",
        ),
        migrations.RemoveField(
            model_name="user",
            name="billing_address_country",
        ),
        migrations.RemoveField(
            model_name="user",
            name="has_billing_address",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_onboarded",
        ),
        migrations.RemoveField(
            model_name="user",
            name="is_tour_completed",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_workspace_id",
        ),
        migrations.RemoveField(
            model_name="user",
            name="my_issues_prop",
        ),
        migrations.RemoveField(
            model_name="user",
            name="onboarding_step",
        ),
        migrations.RemoveField(
            model_name="user",
            name="role",
        ),
        migrations.RemoveField(
            model_name="user",
            name="theme",
        ),
        migrations.RemoveField(
            model_name="user",
            name="use_case",
        ),
    ]
