# Generated by Django 4.2.6 on 2024-02-21 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_tag_project_vote_ratio_project_vote_total_review_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='source_link',
        ),
    ]
