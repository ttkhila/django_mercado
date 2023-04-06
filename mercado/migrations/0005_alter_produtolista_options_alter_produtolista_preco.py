# Generated by Django 4.1.3 on 2022-12-03 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercado', '0004_alter_produtolista_produto'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produtolista',
            options={'ordering': ('produto',)},
        ),
        migrations.AlterField(
            model_name='produtolista',
            name='preco',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, null=True),
        ),
    ]