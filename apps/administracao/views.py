from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pessoa, Imobiliaria, Condominio, Imovel, Contrato
from .forms import PessoaForm, ImobiliariaForm, CondominioForm, ImovelForm, ContratoAluguelForm, LoginForm
from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta
from datetime import date
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages



def index(request):

    imoveis = Imovel.objects.filter(status='disponivel')
    return render(request, 'index.html', {'imoveis': imoveis})




class UserLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu do sistema.")
    return redirect('login')


class PessoaListView(ListView):
    model = Pessoa
    template_name = "pessoa/pessoa_list.html"

class PessoaDetailView(DetailView):
    model = Pessoa
    template_name = "pessoa/pessoa_detail.html" 

class PessoaCreateView(CreateView):
    model = Pessoa
    form_class = PessoaForm
    template_name = "pessoa/pessoa_form.html" 
    success_url = reverse_lazy('pessoa_list')

class PessoaUpdateView(UpdateView):
    model = Pessoa
    form_class = PessoaForm
    template_name = "pessoa/pessoa_form.html"
    success_url = reverse_lazy('pessoa_list')

class PessoaDeleteView(DeleteView):
    model = Pessoa
    template_name = "pessoa/pessoa_confirm_delete.html"
    success_url = reverse_lazy('pessoa_list')




class ImobiliariaListView(ListView):
    model = Imobiliaria
    template_name = "imobiliaria/imobiliaria_list.html"

class ImobiliariaDetailView(DetailView):
    model = Imobiliaria
    template_name = "imobiliaria/imobiliaria_detail.html"

class ImobiliariaCreateView(CreateView):
    model = Imobiliaria
    form_class = ImobiliariaForm
    template_name = "imobiliaria/imobiliaria_form.html"
    success_url = reverse_lazy('imobiliaria_list')

class ImobiliariaUpdateView(UpdateView):
    model = Imobiliaria
    form_class = ImobiliariaForm
    template_name = "imobiliaria/imobiliaria_form.html"
    success_url = reverse_lazy('imobiliaria_list')

class ImobiliariaDeleteView(DeleteView):
    model = Imobiliaria
    template_name = "imobiliaria/imobiliaria_confirm_delete.html"
    success_url = reverse_lazy('imobiliaria_list')




class CondominioListView(ListView):
    model = Condominio
    template_name = "condominio/condominio_list.html"

class CondominioDetailView(DetailView):
    model = Condominio
    template_name = "condominio/condominio_detail.html"

class CondominioCreateView(CreateView):
    model = Condominio
    form_class = CondominioForm
    template_name = "condominio/condominio_form.html"
    success_url = reverse_lazy('condominio_list')

class CondominioUpdateView(UpdateView):
    model = Condominio
    form_class = CondominioForm
    template_name = "condominio/condominio_form.html"
    success_url = reverse_lazy('condominio_list')

class CondominioDeleteView(DeleteView):
    model = Condominio
    template_name = "condominio/condominio_confirm_delete.html"
    success_url = reverse_lazy('condominio_list')




class ImovelListView(ListView):
    model = Imovel
    template_name = "imovel/imovel_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disponiveis'] = Imovel.objects.filter(status='disponivel')
        context['alugados'] = Imovel.objects.filter(status='alugado')
        return context


class ImovelDetailView(DetailView):
    model = Imovel
    template_name = "imovel/imovel_detail.html"

class ImovelCreateView(CreateView):
    model = Imovel
    form_class = ImovelForm
    template_name = "imovel/imovel_form.html"
    success_url = reverse_lazy('imovel_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Filtra para exibir apenas pessoas do tipo 'proprietario'
        form.fields['proprietario'].queryset = Pessoa.objects.filter(tipo='proprietario')
        return form
    
class ImovelUpdateView(UpdateView):
    model = Imovel
    form_class = ImovelForm
    template_name = "imovel/imovel_form.html"
    success_url = reverse_lazy('imovel_list')

class ImovelDeleteView(DeleteView):
    model = Imovel
    template_name = "imovel/imovel_confirm_delete.html"
    success_url = reverse_lazy('imovel_list')




class ContratoListView(ListView):
    model = Contrato
    template_name = "contrato/contrato_list.html"

class ContratoDetailView(DetailView):
    model = Contrato
    template_name = "contrato/contrato_aluguel_detail.html"

class ContratoUpdateView(UpdateView):
    model = Contrato
    form_class = ContratoAluguelForm
    template_name = "contrato/contrato_aluguel_form.html"
    success_url = reverse_lazy('contrato_list')

class ContratoDeleteView(DeleteView):
    model = Contrato
    template_name = "contrato/contrato_confirm_delete.html"
    success_url = reverse_lazy('contrato_list')



class AlugarImovelView(CreateView):
    model = Contrato
    form_class = ContratoAluguelForm
    template_name = "contrato/contrato_aluguel_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['inquilino'].queryset = Pessoa.objects.filter(tipo='inquilino', status='disponivel')
        form.fields['imovel'].disabled = True
        form.fields['proprietario'].disabled = True
        form.fields['imobiliaria'].disabled = True
        return form

    def get_initial(self):
        initial = super().get_initial()
        imovel_pk = self.request.GET.get('imovel')
        if imovel_pk:
            try:
                imovel = Imovel.objects.get(pk=imovel_pk)
                # Armazena o imóvel para exibição no template
                self.imovel_instance = imovel
                initial['imovel'] = imovel.pk
                initial['valor_aluguel'] = imovel.valor_aluguel
                # Preenche os campos imobiliaria e proprietario diretamente a partir do imóvel
                if imovel.imobiliaria:
                    initial['imobiliaria'] = imovel.imobiliaria.pk
                if imovel.proprietario:
                    initial['proprietario'] = imovel.proprietario.pk
            except Imovel.DoesNotExist:
                self.imovel_instance = None
        else:
            self.imovel_instance = None

        # Se houver o parâmetro inquilino na URL, preenche-o
        inquilino_pk = self.request.GET.get('inquilino')
        if inquilino_pk:
            try:
                inquilino = Pessoa.objects.get(pk=inquilino_pk, tipo='inquilino')
                initial['inquilino'] = inquilino.pk
            except Pessoa.DoesNotExist:
                pass

        # Define a data de assinatura como a data atual
        initial['data_assinatura_contrato'] = date.today()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imovel_instance'] = self.imovel_instance
        return context

    def form_valid(self, form):
        # Obtém o período selecionado (em meses); se não for informado, assume 6 meses
        periodo_value = form.cleaned_data.get('periodo_contrato')
        try:
            periodo = int(periodo_value)
        except (TypeError, ValueError):
            periodo = 6

        contrato = form.save(commit=False)
        # Define o imóvel a partir da instância obtida via GET
        contrato.imovel = self.imovel_instance
        # Preenche os campos imobiliaria e proprietario diretamente do imóvel
        if self.imovel_instance:
            if self.imovel_instance.imobiliaria:
                contrato.imobiliaria = self.imovel_instance.imobiliaria
            if self.imovel_instance.proprietario:
                contrato.proprietario = self.imovel_instance.proprietario

        # Calcula a data final com base na data de início e no período escolhido
        contrato.data_fim = contrato.data_inicio + relativedelta(months=periodo)
        contrato.periodo_contrato = periodo
        contrato.periodo_renovacao = periodo
        
        # Define o tipo e o status do contrato
        contrato.tipo = 'aluguel'
        contrato.status = 'ativo'
        contrato.data_assinatura_contrato = date.today()
        contrato.save()

        # Atualiza o status do imóvel para "alugado"
        if self.imovel_instance:
            self.imovel_instance.status = 'alugado'
            self.imovel_instance.save()

        # Atualiza o status do inquilino para "indisponivel"
        inquilino = contrato.inquilino
        inquilino.status = 'indisponivel'
        inquilino.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('contrato_list')









class ContratoAluguelDetailView(DetailView):
    model = Contrato
    template_name = "contrato/contrato_aluguel_pdf.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contrato = self.object

        # Dados do Imóvel
        context['referencia'] = contrato.imovel.referencia
        context['endereco_imovel'] = contrato.imovel.endereco

        # Dados do Locador (Proprietário)
        context['locador'] = contrato.proprietario.nome
        context['estado_civil_locador'] = contrato.proprietario.estado_civil
        context['cpf_locador'] = contrato.proprietario.cpf
        context['rg_locador'] = contrato.proprietario.rg
        context['cidade_locador'] = contrato.proprietario.endereco
        context['chave_pix'] = contrato.proprietario.chave_pix


        # Dados do Locatário (Inquilino)
        context['nome_completo'] = contrato.inquilino.nome
        context['estado_civil'] = contrato.inquilino.estado_civil
        context['cpf_cnpj'] = contrato.inquilino.cpf
        context['rg_expedidor'] = contrato.inquilino.rg
        context['endereco_atual'] = contrato.inquilino.endereco

        # Dados do Contrato
        context['prazo_locacao'] = contrato.periodo_contrato
        context['data_inicio'] = contrato.data_inicio
        context['data_final'] = contrato.data_fim
        context['data_assinatura_contrato'] = contrato.data_assinatura_contrato
        context['dia_pagamento'] = contrato.dia_pagamento

        # Valores e encargos
        context['valor_aluguel'] = contrato.valor_aluguel
        context['taxa_juros'] = contrato.taxa_juros
        context['taxa_multa'] = contrato.taxa_multa
        context['taxa_adm'] = contrato.taxa_adm
        context['dia_pagamento'] = contrato.dia_pagamento


        # Garantia
        context['garantia'] = contrato.garantia
        context['parcelamento_garantia'] = contrato.parcelamento_garantia
        context['valor_caucao'] = contrato.valor_caucao
        # Modo de pagamento
        context['modo_pagamento'] = contrato.modo_pagamento

        # Observações
        context['observacoes'] = contrato.observacoes

        # Campos adicionais (você pode ajustá-los se houver valores específicos)
        context['data_pagamento'] = ""
        context['forma_pagamento'] = ""
        context['caucao'] = ""
        return context

