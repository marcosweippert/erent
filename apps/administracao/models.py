from django.db import models

class Pessoa(models.Model):
    TIPOS = (
        ('inquilino', 'Inquilino'),
        ('proprietario', 'Proprietário'),
        ('imobiliario', 'Imobiliário'),
    )
    STATUS_INQUILINO = (
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
    )
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=20)
    estado_civil = models.CharField(max_length=20)
    nacionalidade = models.CharField(max_length=50)
    endereco = models.CharField(max_length=255)
    chave_pix = models.CharField(max_length=255, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=15, choices=TIPOS)
    status = models.CharField(max_length=15, choices=STATUS_INQUILINO, blank=True, null=True)

    def __str__(self):
        return self.nome

class Imobiliaria(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=255)
    proprietario = models.ForeignKey(Pessoa, on_delete=models.SET_NULL, null=True, blank=True)
    imoveis = models.ManyToManyField('Imovel', blank=True)

    def __str__(self):
        return self.nome

class Condominio(models.Model):
    nome = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=14, null=True, blank=True)
    endereco = models.CharField(max_length=255)
    imoveis = models.ManyToManyField('Imovel', blank=True)

    def __str__(self):
        return self.nome

class Imovel(models.Model):
    TIPOS_IMOVEL = (
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
        ('industrial', 'Industrial'),
    )

    STATUS_IMOVEL = (
        ('disponivel', 'Disponível'),
        ('alugado', 'Alugado'),
        ('venda', 'Venda'),
    )

    referencia = models.CharField(max_length=50, unique=True)
    endereco = models.CharField(max_length=255)
    valor_aluguel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=TIPOS_IMOVEL)
    status = models.CharField(max_length=15, choices=STATUS_IMOVEL)
    observacoes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f'{self.referencia} - {self.endereco}'

class Contrato(models.Model):
    STATUS_CONTRATO = (
        ('ativo', 'Ativo'),
        ('finalizado', 'Finalizado'),
        ('cancelado', 'Cancelado'),
    )

    TIPO_CONTRATO = (
        ('aluguel', 'Aluguel'),
        ('compra_venda', 'Compra e Venda'),
    )
    GARANTIA_CONTRATO = (
        ('caucao', 'Caução'),
        ('fiador', 'Fiador'),
        ('sem garantia', 'Sem garantia'),
    )

    TIPO_PAGAMENTO = (
        ('pix', 'Pix'),
        ('boleto bancario', 'Boleto Bancário'),
    )
    DIA_PAGAMENTO = (
        ('5', '5'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
    )

    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    inquilino = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='contratos_inquilino')
    proprietario = models.ForeignKey(Pessoa, on_delete=models.CASCADE, related_name='contratos_proprietario')
    imobiliaria = models.ForeignKey(Imobiliaria, on_delete=models.CASCADE, related_name='contratos_imobiliaria')
    tipo = models.CharField(max_length=20, choices=TIPO_CONTRATO)
    status = models.CharField(max_length=20, choices=STATUS_CONTRATO)
    valor_aluguel = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    periodo_contrato = models.PositiveIntegerField(choices=[(6, '6 meses'), (12, '12 meses'), (24, '24 meses')])
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    data_assinatura_contrato = models.DateField(null=True, blank=True)
    taxa_juros = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    taxa_multa = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    taxa_adm = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    garantia = models.CharField(max_length=20, choices=GARANTIA_CONTRATO)
    valor_caucao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    parcelamento_garantia = models.PositiveIntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6')], blank=True, null=True)
    modo_pagamento = models.CharField(max_length=20, choices=TIPO_PAGAMENTO, blank=True, null=True)
    dia_pagamento = models.CharField(max_length=20, choices=DIA_PAGAMENTO, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Contrato {self.id} - {self.imovel.referencia}'

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

class Renovacao(models.Model):
    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    periodo_renovacao = models.PositiveIntegerField(choices=[(6, '6 meses'), (12, '12 meses'), (24, '24 meses')], blank=True)
    data_inicio_renovacao = models.DateField(null=True, blank=True)
    data_fim_renovacao = models.DateField(null=True, blank=True)
    valor_aluguel_reajustado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_assinatura_renovacao = models.DateField(null=True, blank=True)
    indice_ipca = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'renovacao {self.id} - {self.contrato.id}'