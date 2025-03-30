from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Pessoa, Imobiliaria, Condominio, Imovel, Contrato, Pagamento
from .forms import PessoaForm, ImobiliariaForm, CondominioForm, ImovelForm, ContratoAluguelForm, LoginForm, PagamentoForm
from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta
from datetime import date
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib import messages
import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from decimal import Decimal


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
        # Limita o campo inquilino a pessoas do tipo "inquilino" com status 'disponivel'
        form.fields['inquilino'].queryset = Pessoa.objects.filter(tipo='inquilino', status='disponivel')
        # Desabilita os campos que serão preenchidos automaticamente
        form.fields['imovel'].disabled = True
        form.fields['proprietario'].disabled = True
        form.fields['imobiliaria'].disabled = True

        # Ajusta o tamanho dos inputs de taxas para inputs menores
        for field_name in ['taxa_juros', 'taxa_multa', 'taxa_adm']:
            if field_name in form.fields:
                form.fields[field_name].widget.attrs.update({'class': 'form-control form-control-sm'})
        return form

    def get_initial(self):
        initial = super().get_initial()

        # Preenche valores padrão para o formulário
        initial['data_assinatura_contrato'] = date.today()
        initial['data_inicio'] = date.today()
        initial['taxa_juros'] = 2
        initial['taxa_multa'] = 10
        initial['taxa_adm'] = 10
        initial['data_pagamento_caucao'] = date.today()
        initial['data_primeiro_pagamento'] = date.today()

        # Se o imóvel for passado por GET
        imovel_pk = self.request.GET.get('imovel')
        if imovel_pk:
            try:
                imovel = Imovel.objects.get(pk=imovel_pk)
                self.imovel_instance = imovel
                initial['imovel'] = imovel.pk
                initial['valor_aluguel'] = imovel.valor_aluguel
                initial['valor_caucao'] = imovel.valor_aluguel
                if imovel.imobiliaria:
                    initial['imobiliaria'] = imovel.imobiliaria.pk
                if imovel.proprietario:
                    initial['proprietario'] = imovel.proprietario.pk
            except Imovel.DoesNotExist:
                self.imovel_instance = None
        else:
            self.imovel_instance = None

        # Se o inquilino for passado por GET
        inquilino_pk = self.request.GET.get('inquilino')
        if inquilino_pk:
            try:
                inquilino = Pessoa.objects.get(pk=inquilino_pk, tipo='inquilino')
                initial['inquilino'] = inquilino.pk
            except Pessoa.DoesNotExist:
                pass

        # Cálculo automático do valor do primeiro pagamento
        if 'valor_aluguel' in initial and 'data_inicio' in initial:
            aluguel = initial['valor_aluguel']
            inicio = initial['data_inicio']
            dias_restantes = 30 - inicio.day
            if dias_restantes < 0:
                dias_restantes = 0
            initial['valor_primeiro_pagamento'] = (aluguel / 30) * dias_restantes

        return initial


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imovel_instance'] = self.imovel_instance
        return context

    def form_valid(self, form):
        # Obtém o período de contrato (em meses); se não for informado, assume 6 meses
        periodo_value = form.cleaned_data.get('periodo_contrato')
        try:
            periodo = int(periodo_value)
        except (TypeError, ValueError):
            periodo = 6

        contrato = form.save(commit=False)
        # Define o imóvel a partir da instância obtida via GET
        contrato.imovel = self.imovel_instance
        # Preenche os campos imobiliaria e proprietario a partir do imóvel
        if self.imovel_instance:
            if self.imovel_instance.imobiliaria:
                contrato.imobiliaria = self.imovel_instance.imobiliaria
            if self.imovel_instance.proprietario:
                contrato.proprietario = self.imovel_instance.proprietario

        # Calcula a data final com base na data de início e no período escolhido
        contrato.data_fim = contrato.data_inicio + relativedelta(months=periodo)
        contrato.periodo_contrato = periodo
        contrato.periodo_renovacao = periodo

        # Define o tipo e o status do contrato, e a data de assinatura como a data atual
        contrato.tipo = 'aluguel'
        contrato.status = 'ativo'
        contrato.data_assinatura_contrato = date.today()

        # Define valores padrão para as taxas, se não informadas
        if not contrato.taxa_juros:
            contrato.taxa_juros = 2
        if not contrato.taxa_multa:
            contrato.taxa_multa = 10
        if not contrato.taxa_adm:
            contrato.taxa_adm = 10

        # Define a caução como o mesmo valor do aluguel
        contrato.valor_caucao = contrato.valor_aluguel
        # Define a data de pagamento da caução como hoje
        contrato.data_pagamento_caucao = date.today()

        # Calcula o valor do primeiro pagamento automaticamente, se não for informado,
        # utilizando a fórmula: (valor_aluguel / 30) * (30 - dia de data_inicio)
        if not contrato.data_primeiro_pagamento:
            contrato.data_primeiro_pagamento = date.today()
        if not contrato.valor_primeiro_pagamento:
            dias_restantes = 30 - contrato.data_inicio.day
            if dias_restantes < 0:
                dias_restantes = 0
            contrato.valor_primeiro_pagamento = (contrato.valor_aluguel / 30) * dias_restantes

        contrato.save()

        # Atualiza o status do imóvel para "alugado"
        if self.imovel_instance:
            self.imovel_instance.status = 'alugado'
            self.imovel_instance.save()

        # Atualiza o status do inquilino para "indisponivel" e vincula o contrato à pessoa
        inquilino = contrato.inquilino
        inquilino.status = 'indisponivel'
        inquilino.contrato = contrato
        inquilino.save()

        # Gerar pendências de pagamento:
        # PARCELA 1: Já foi definida com data_primeiro_pagamento e valor_primeiro_pagamento,
        # e o status será "pago" se estes forem informados, ou "pendente" se não.
        if contrato.data_primeiro_pagamento and contrato.valor_primeiro_pagamento:
            first_due = contrato.data_primeiro_pagamento
            first_value = contrato.valor_primeiro_pagamento
            first_status = 'pago'
        else:
            first_due = contrato.data_inicio + timedelta(days=10)
            first_value = contrato.valor_aluguel
            first_status = 'pendente'

        Pagamento.objects.create(
            contrato=contrato,
            inquilino=contrato.inquilino,
            parcela=1,
            vencimento=first_due,
            valor=first_value,
            status=first_status
        )

        # PARCELAS 2 até N:
        # Se o campo dia_pagamento estiver preenchido, usamos-o; caso contrário, usamos o dia de data_inicio.
        from datetime import timedelta  # caso ainda não tenha sido importado
        if contrato.dia_pagamento:
            due_day = int(contrato.dia_pagamento)
            try:
                second_due = contrato.data_inicio.replace(day=due_day) + relativedelta(months=1)
            except ValueError:
                second_due = (contrato.data_inicio.replace(day=1) + relativedelta(months=2)) - timedelta(days=1)
        else:
            second_due = first_due + relativedelta(months=1)

        for i in range(2, contrato.periodo_contrato + 1):
            vencimento = second_due + relativedelta(months=i-2)
            Pagamento.objects.create(
                contrato=contrato,
                inquilino=contrato.inquilino,
                parcela=i,
                vencimento=vencimento,
                valor=contrato.valor_aluguel,
                status='pendente'
            )

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


class PagamentoListView(ListView):
    model = Pagamento
    template_name = "financeiro/pagamento_list.html"
    context_object_name = "pagamentos"

    def get_queryset(self):
        return Pagamento.objects.order_by('status', 'vencimento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hoje'] = date.today()
        context['pagamentos_pendentes'] = self.get_queryset().filter(status='pendente')
        context['pagamentos_pagos'] = self.get_queryset().filter(status='pago')
        return context

class PagamentoUpdateView(UpdateView):
    model = Pagamento
    fields = ['contrato','inquilino','parcela','vencimento', 'valor', 'status']
    template_name = "financeiro/pagamento_form.html"
    
    def get_success_url(self):
        return reverse_lazy('pagamento_list')

class PagamentoDeleteView(DeleteView):
    model = Pagamento
    template_name = "financeiro/pagamento_confirm_delete.html"
    
    def get_success_url(self):
        return reverse_lazy('pagamento_list')



class PagamentoCreateView(CreateView):
    model = Pagamento
    form_class = PagamentoForm
    template_name = "financeiro/pagamento_form.html"

    def get_initial(self):
        initial = super().get_initial()
        inquilino_pk = self.request.GET.get('inquilino')
        if inquilino_pk:
            try:
                inquilino = Pessoa.objects.get(pk=inquilino_pk, tipo='inquilino')
                initial['inquilino'] = inquilino.pk
                # Seleciona automaticamente o primeiro contrato vinculado ao inquilino, ordenado por ID
                contrato = inquilino.contratos_inquilino.order_by('id').first()
                if contrato:
                    initial['contrato'] = contrato.pk
            except Pessoa.DoesNotExist:
                pass
        return initial


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Se o inquilino for informado, desabilita o campo contrato para que ele seja selecionado automaticamente
        if self.request.GET.get('inquilino'):
            form.fields['contrato'].disabled = True
        return form

    def form_valid(self, form):
        pagamento = form.save(commit=False)
        pagamento.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('pagamento_list')



def calcular_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)

    data_pagamento_str = request.GET.get('data_pagamento')
    if data_pagamento_str:
        data_pagamento = date.fromisoformat(data_pagamento_str)
    else:
        data_pagamento = date.today()

    hoje = date.today()

    # Usa a data efetiva para o pagamento
    if pagamento.vencimento <= hoje:
        data_pagamento = hoje
    else:
        data_pagamento = pagamento.vencimento

    dias_atraso = (data_pagamento - pagamento.vencimento).days

    # Ajuste: inclui o dia do vencimento como primeiro dia em atraso
    if dias_atraso > 0:
        dias_atraso += 1

    juros = multa = Decimal('0.00')

    if dias_atraso > 0:
        multa = pagamento.valor * (pagamento.contrato.taxa_multa / 100)
        valor_base_para_juros = pagamento.valor + multa
        juros = (valor_base_para_juros * (pagamento.contrato.taxa_juros / 100) / 30) * dias_atraso

    total_pago = pagamento.valor + multa + juros

    return JsonResponse({
        'data_pagamento': data_pagamento.isoformat(),
        'dias_atraso': dias_atraso,
        'juros': round(juros, 2),
        'multa': round(multa, 2),
        'total_pago': round(total_pago, 2)
    })




def pagar_parcela(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    
    # Recebendo a data informada no corpo da requisição
    data_pagamento_str = json.loads(request.body).get('data_pagamento')
    if data_pagamento_str:
        data_pagamento = date.fromisoformat(data_pagamento_str)
    else:
        data_pagamento = date.today()

    dias_atraso = (data_pagamento - pagamento.vencimento).days
    if dias_atraso > 0:
        dias_atraso += 1
        multa = pagamento.valor * (pagamento.contrato.taxa_multa / 100)
        valor_base_para_juros = pagamento.valor + multa
        juros = (valor_base_para_juros * (pagamento.contrato.taxa_juros / 100) / 30) * dias_atraso
    else:
        juros = Decimal('0.00')
        multa = Decimal('0.00')

    pagamento.juros = juros
    pagamento.multa = multa
    pagamento.total_pago = pagamento.valor + juros + multa
    pagamento.data_pagamento = data_pagamento
    pagamento.status = 'pago'
    pagamento.save()

    return JsonResponse({'status': 'success', 'total_pago': str(pagamento.total_pago)})
