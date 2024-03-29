# Generated by Django 4.1.3 on 2023-03-24 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("team", "0004_alter_team_plan"),
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="active_team_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="userprofiles",
                to="team.team",
            ),
        ),
    ]
