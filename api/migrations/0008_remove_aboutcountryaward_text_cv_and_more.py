# Generated by Django 5.1.4 on 2024-12-22 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_text_aboutcountryaward_text_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutcountryaward',
            name='text_cv',
        ),
        migrations.RemoveField(
            model_name='aboutcountryaward',
            name='text_en',
        ),
        migrations.RemoveField(
            model_name='aboutcountryaward',
            name='text_zh',
        ),
        migrations.RemoveField(
            model_name='award',
            name='description_cv',
        ),
        migrations.RemoveField(
            model_name='award',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='award',
            name='description_zh',
        ),
        migrations.RemoveField(
            model_name='award',
            name='name_cv',
        ),
        migrations.RemoveField(
            model_name='award',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='award',
            name='name_zh',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='name_cv',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='decision',
            name='name_zh',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='biography_cv',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='biography_en',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='biography_zh',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='full_name_cv',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='full_name_en',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='full_name_zh',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='position_cv',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='position_en',
        ),
        migrations.RemoveField(
            model_name='partner',
            name='position_zh',
        ),
        migrations.RemoveField(
            model_name='sociallink',
            name='name_cv',
        ),
        migrations.RemoveField(
            model_name='sociallink',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='sociallink',
            name='name_zh',
        ),
    ]