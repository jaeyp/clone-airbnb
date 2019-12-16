# Generated by Django 2.2.5 on 2019-12-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20191216_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('', 'Select language'), ('en', 'English'), ('ko', 'Korean')], default='en', max_length=2, null=True, verbose_name='language'),
        ),
    ]
