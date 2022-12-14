# Generated by Django 4.1.3 on 2022-11-28 21:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mercado', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ListaCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('data_fechamento', models.DateTimeField()),
                ('finalizada', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('img', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Mercado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('img', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mercado.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Unidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('sigla', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProdutoLista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('indicado', models.BooleanField(default=False)),
                ('data_lancamento', models.DateTimeField(auto_now=True)),
                ('lista_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mercado.listacompra')),
                ('marca', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mercado.marca')),
                ('mercado', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='mercado.mercado')),
                ('produto', models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='mercado.produto')),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='unidade',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mercado.unidade'),
        ),
    ]
