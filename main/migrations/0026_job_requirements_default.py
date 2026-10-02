from django.db import migrations, models


def replace_null_requirements(apps, schema_editor):
    Job = apps.get_model('main', 'Job')
    Job.objects.filter(requirements__isnull=True).update(requirements='')


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_application_resume_template_and_accepted_status'),
    ]

    operations = [
        migrations.RunPython(replace_null_requirements, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='job',
            name='requirements',
            field=models.CharField(default='', max_length=500),
        ),
    ]
