# Generated by Django 5.1.7 on 2025-03-25 12:41

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.CharField(max_length=50, unique=True)),
                ('endereco', models.CharField(max_length=255)),
                ('valor_aluguel', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_venda', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tipo', models.CharField(choices=[('residencial', 'Residencial'), ('comercial', 'Comercial'), ('industrial', 'Industrial')], max_length=15)),
                ('status', models.CharField(choices=[('disponivel', 'Disponível'), ('alugado', 'Alugado'), ('venda', 'Venda')], max_length=15)),
                ('observacoes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('data_nascimento', models.DateField()),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('rg', models.CharField(max_length=20)),
                ('estado_civil', models.CharField(max_length=20)),
                ('nacionalidade', models.CharField(max_length=50)),
                ('endereco', models.CharField(max_length=255)),
                ('chave_pix', models.CharField(blank=True, max_length=255, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('inquilino', 'Inquilino'), ('proprietario', 'Proprietário'), ('imobiliario', 'Imobiliário')], max_length=15)),
                ('status', models.CharField(blank=True, choices=[('disponivel', 'Disponível'), ('indisponivel', 'Indisponível')], max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Imobiliaria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=14, unique=True)),
                ('endereco', models.CharField(max_length=255)),
                ('imoveis', models.ManyToManyField(blank=True, to='administracao.imovel')),
                ('proprietario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='administracao.pessoa')),
            ],
        ),
        migrations.CreateModel(
            name='Condominio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cnpj', models.CharField(blank=True, max_length=14, null=True)),
                ('endereco', models.CharField(max_length=255)),
                ('imoveis', models.ManyToManyField(blank=True, to='administracao.imovel')),
            ],
        ),
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('aluguel', 'Aluguel'), ('compra_venda', 'Compra e Venda')], max_length=20)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado')], max_length=20)),
                ('valor_aluguel', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('valor_venda', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('periodo_contrato', models.PositiveIntegerField(choices=[(6, '6 meses'), (12, '12 meses'), (24, '24 meses')])),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField(blank=True, null=True)),
                ('data_assinatura_contrato', models.DateField(blank=True, null=True)),
                ('taxa_juros', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('taxa_multa', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('taxa_adm', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('garantia', models.CharField(choices=[('caucao', 'Caução'), ('fiador', 'Fiador'), ('sem garantia', 'Sem garantia')], max_length=20)),
                ('valor_caucao', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('parcelamento_garantia', models.PositiveIntegerField(blank=True, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')], null=True)),
                ('modo_pagamento', models.CharField(blank=True, choices=[('pix', 'Pix'), ('boleto bancario', 'Boleto Bancário')], max_length=20, null=True)),
                ('dia_pagamento', models.CharField(blank=True, choices=[('5', '5'), ('10', '10'), ('15', '15'), ('20', '20')], max_length=20, null=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('imobiliaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contratos_imobiliaria', to='administracao.imobiliaria')),
                ('imovel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracao.imovel')),
                ('inquilino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contratos_inquilino', to='administracao.pessoa')),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contratos_proprietario', to='administracao.pessoa')),
            ],
            options={
                'verbose_name': 'Contrato',
                'verbose_name_plural': 'Contratos',
            },
        ),
        migrations.CreateModel(
            name='Renovacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo_renovacao', models.PositiveIntegerField(blank=True, choices=[(6, '6 meses'), (12, '12 meses'), (24, '24 meses')])),
                ('data_inicio_renovacao', models.DateField(blank=True, null=True)),
                ('data_fim_renovacao', models.DateField(blank=True, null=True)),
                ('valor_aluguel_reajustado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('data_assinatura_renovacao', models.DateField(blank=True, null=True)),
                ('indice_ipca', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('contrato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administracao.contrato')),
            ],
        ),
    ]
