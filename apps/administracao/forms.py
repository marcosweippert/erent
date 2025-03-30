
from django import forms
from .models import Pessoa, Imobiliaria, Condominio, Imovel, Contrato, Pagamento

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



from django import forms
from .models import Contrato

PERIOD_CHOICES = (
    (6, "6 meses"),
    (12, "12 meses"),
    (24, "24 meses"),
)

class ContratoAluguelForm(forms.ModelForm):
    periodo_contrato = forms.ChoiceField(
        choices=PERIOD_CHOICES,
        label="Período de locação (meses)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Contrato
        fields = [
            'imovel', 'inquilino', 'proprietario', 'imobiliaria', 'valor_aluguel',
            'data_inicio', 'observacoes', 'periodo_contrato', 'data_assinatura_contrato',
            'taxa_juros', 'taxa_multa', 'garantia', 'parcelamento_garantia',
            'modo_pagamento', 'dia_pagamento', 'taxa_adm', 'valor_caucao',
            'data_pagamento_caucao', 'data_primeiro_pagamento', 'valor_primeiro_pagamento'
        ]
        widgets = {
            'imovel': forms.HiddenInput(),
            'inquilino': forms.Select(attrs={'class': 'form-control'}),
            'proprietario': forms.Select(attrs={'class': 'form-control'}),
            'imobiliaria': forms.Select(attrs={'class': 'form-control'}),
            'valor_aluguel': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_valor_aluguel'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'id_data_inicio'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_assinatura_contrato': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'taxa_juros': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'taxa_multa': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'garantia': forms.Select(attrs={'class': 'form-control'}),
            'parcelamento_garantia': forms.Select(attrs={'class': 'form-control'}),
            'modo_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'dia_pagamento': forms.Select(attrs={'class': 'form-control'}),
            'taxa_adm': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': '0.01'}),
            'valor_caucao': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_pagamento_caucao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_primeiro_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_primeiro_pagamento': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_valor_primeiro_pagamento'}),
        }



from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))




class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['inquilino', 'contrato', 'parcela', 'vencimento', 'valor', 'status']
        widgets = {
            'inquilino': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'contrato': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'parcela': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'vencimento': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
            'status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }
