# Generated by Django 3.1 on 2020-10-14 09:58

from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations, models

import saleor.core.utils.json_serializer


def update_groups_with_manage_pages_with_new_permission(apps, schema_editor):
    # force post signal as permissions are created in post migrate signals
    # related Django issue https://code.djangoproject.com/ticket/23422
    emit_post_migrate_signal(2, False, "default")

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    manage_page_types_and_attributes_perm = Permission.objects.filter(
        codename="manage_page_types_and_attributes", content_type__app_label="page",
    ).first()

    groups = Group.objects.filter(
        permissions__content_type__app_label="page",
        permissions__codename="manage_pages",
    )
    for group in groups:
        group.permissions.add(manage_page_types_and_attributes_perm)


class Migration(migrations.Migration):

    dependencies = [
        ("page", "0013_update_publication_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="PageType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "private_metadata",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                        null=True,
                    ),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        encoder=saleor.core.utils.json_serializer.CustomJsonEncoder,
                        null=True,
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                (
                    "slug",
                    models.SlugField(allow_unicode=True, max_length=255, unique=True),
                ),
            ],
            options={
                "ordering": ("slug",),
                "permissions": (
                    (
                        "manage_page_types_and_attributes",
                        "Manage page types and attributes.",
                    ),
                ),
            },
        ),
        migrations.RunPython(
            update_groups_with_manage_pages_with_new_permission,
            migrations.RunPython.noop,
        ),
    ]