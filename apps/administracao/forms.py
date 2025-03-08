
from django import forms
from .models import Pessoa, Imobiliaria, Condominio, Imovel, Contrato

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = '__all__'

class ImobiliariaForm(forms.ModelForm):
    class Meta:
        model = Imobiliaria
        fields = '__all__'

class CondominioForm(forms.ModelForm):
    class Meta:
        model = Condominio
        fields = '__all__'

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        fields = '__all__'



PERIOD_CHOICES = (
    (6, "6 meses"),
    (12, "12 meses"),
    (24, "24 meses"),
)

class ContratoAluguelForm(forms.ModelForm):
    periodo_contrato = forms.ChoiceField(choices=PERIOD_CHOICES, label="Período de locação (meses)")

    class Meta:
        model = Contrato
        fields = [
            'imovel', 'inquilino', 'proprietario', 'imobiliaria', 'valor_aluguel',
            'data_inicio', 'observacoes', 'periodo_contrato', 'data_assinatura_contrato',
            'taxa_juros', 'taxa_multa', 'garantia', 'parcelamento_garantia',
            'modo_pagamento', 'dia_pagamento', 'taxa_adm', 'valor_caucao'
        ]

