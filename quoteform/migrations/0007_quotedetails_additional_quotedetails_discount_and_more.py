# Generated by Django 4.2.3 on 2023-08-08 08:35

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quoteform', '0006_quotedetails_treesystem_alter_quotedetails_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotedetails',
            name='additional',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='quotedetails',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='quotedetails',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='quotedetails',
            name='panel',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Rayzon', 'Rayzon'), ('Adani', 'Adani'), ('Goldi', 'Goldi'), ('Waree', 'Waree'), ('Pahal', 'Pahal')], max_length=100),
        ),
    ]
