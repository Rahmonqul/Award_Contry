# Generated by Django 5.1.4 on 2024-12-22 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_aboutcountryaward_text_ar_aboutcountryaward_text_cv_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text',
            new_name='text',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_ar',
            new_name='text_ar',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_cv',
            new_name='text_cv',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_de',
            new_name='text_de',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_en',
            new_name='text_en',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_es',
            new_name='text_es',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_fr',
            new_name='text_fr',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_kk',
            new_name='text_kk',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_uz',
            new_name='text_uz',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_uz_latn',
            new_name='text_uz_latn',
        ),
        migrations.RenameField(
            model_name='aboutcountryaward',
            old_name='Text_zh',
            new_name='text_zh',
        ),
    ]
