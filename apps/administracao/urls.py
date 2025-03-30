from django.urls import path
from .views import (
    PessoaListView, PessoaDetailView, PessoaCreateView, PessoaUpdateView, PessoaDeleteView,
    ImobiliariaListView, ImobiliariaDetailView, ImobiliariaCreateView, ImobiliariaUpdateView, ImobiliariaDeleteView,
    CondominioListView, CondominioDetailView, CondominioCreateView, CondominioUpdateView, CondominioDeleteView, PagamentoCreateView,
    ImovelListView, ImovelDetailView, ImovelCreateView, ImovelUpdateView, ImovelDeleteView, PagamentoListView, PagamentoUpdateView,PagamentoDeleteView,
    ContratoListView, ContratoDetailView, ContratoUpdateView, ContratoDeleteView, index, AlugarImovelView, ContratoAluguelDetailView, UserLoginView, calcular_pagamento, pagar_parcela
)
from .views import logout_view


urlpatterns = [
    path('', index, name='index'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    # URLs para Pessoa
    path('pessoas/', PessoaListView.as_view(), name='pessoa_list'),
    path('pessoas/novo/', PessoaCreateView.as_view(), name='pessoa_create'),
    path('pessoas/<int:pk>/', PessoaDetailView.as_view(), name='pessoa_detail'),
    path('pessoas/<int:pk>/editar/', PessoaUpdateView.as_view(), name='pessoa_update'),
    path('pessoas/<int:pk>/excluir/', PessoaDeleteView.as_view(), name='pessoa_delete'),

    # URLs para Imobiliaria
    path('imobiliarias/', ImobiliariaListView.as_view(), name='imobiliaria_list'),
    path('imobiliarias/novo/', ImobiliariaCreateView.as_view(), name='imobiliaria_create'),
    path('imobiliarias/<int:pk>/', ImobiliariaDetailView.as_view(), name='imobiliaria_detail'),
    path('imobiliarias/<int:pk>/editar/', ImobiliariaUpdateView.as_view(), name='imobiliaria_update'),
    path('imobiliarias/<int:pk>/excluir/', ImobiliariaDeleteView.as_view(), name='imobiliaria_delete'),

    # URLs para Condominio
    path('condominios/', CondominioListView.as_view(), name='condominio_list'),
    path('condominios/novo/', CondominioCreateView.as_view(), name='condominio_create'),
    path('condominios/<int:pk>/', CondominioDetailView.as_view(), name='condominio_detail'),
    path('condominios/<int:pk>/editar/', CondominioUpdateView.as_view(), name='condominio_update'),
    path('condominios/<int:pk>/excluir/', CondominioDeleteView.as_view(), name='condominio_delete'),

    # URLs para Imovel
    path('imoveis/', ImovelListView.as_view(), name='imovel_list'),
    path('imoveis/novo/', ImovelCreateView.as_view(), name='imovel_create'),
    path('imoveis/<int:pk>/', ImovelDetailView.as_view(), name='imovel_detail'),
    path('imoveis/<int:pk>/editar/', ImovelUpdateView.as_view(), name='imovel_update'),
    path('imoveis/<int:pk>/excluir/', ImovelDeleteView.as_view(), name='imovel_delete'),

    # URLs para Contrato
    path('contratos/', ContratoListView.as_view(), name='contrato_list'),
    path('contratos/<int:pk>/', ContratoDetailView.as_view(), name='contrato_detail'),
    path('contratos/<int:pk>/editar/', ContratoUpdateView.as_view(), name='contrato_update'),
    path('contratos/<int:pk>/excluir/', ContratoDeleteView.as_view(), name='contrato_delete'),

    path('contratos/alugar/', AlugarImovelView.as_view(), name='contrato_alugar'),
    path('contratos/visualizar/<int:pk>/', ContratoAluguelDetailView.as_view(), name='contrato_visualizar'),

    path('pagamentos/', PagamentoListView.as_view(), name='pagamento_list'),
    path('pagamentos/create/', PagamentoCreateView.as_view(), name='pagamento_create'),

    path('pagamentos/<int:pk>/edit/', PagamentoUpdateView.as_view(), name='pagamento_update'),
    path('pagamentos/<int:pk>/delete/', PagamentoDeleteView.as_view(), name='pagamento_delete'),
    path('pagamento/calcular/<int:pk>/', calcular_pagamento, name='calcular_pagamento'),
    path('pagamento/pagar/<int:pk>/', pagar_parcela, name='pagar_parcela'),

]
