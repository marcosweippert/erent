import random
from django.core.management.base import BaseCommand
from apps.administracao.models import Pessoa, Imobiliaria, Condominio, Imovel
from datetime import date

class Command(BaseCommand):
    help = "Popula o banco de dados com dados iniciais (seeds) aleatórios, sem apagar os dados existentes."

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando o seeding dos dados...")

        # Criando 5 inquilinos
        inquilinos = []
        for i in range(1, 6):
            cpf_value = "{:011d}".format(random.randint(0, 99999999999))
            inq = Pessoa.objects.create(
                nome=f"Inquilino {i}",
                data_nascimento=date(1990, random.randint(1, 12), random.randint(1, 28)),
                cpf=cpf_value,
                rg=str(random.randint(1000000, 9999999)),
                estado_civil="Solteiro",
                nacionalidade="Brasileiro",
                endereco=f"Rua Inquilino {i}, 100",
                tipo="inquilino",         # Ajustado para corresponder ao valor da opção
                chave_pix=cpf_value,      # Chave PIX igual ao CPF
                status="disponivel"       # Status fixo como disponivel
            )
            inquilinos.append(inq)
        self.stdout.write("5 inquilinos criados.")

        # Criando 5 proprietários
        proprietarios = []
        for i in range(1, 6):
            cpf_value = "{:011d}".format(random.randint(0, 99999999999))
            prop = Pessoa.objects.create(
                nome=f"Proprietario {i}",
                data_nascimento=date(1970, random.randint(1, 12), random.randint(1, 28)),
                cpf=cpf_value,
                rg=str(random.randint(1000000, 9999999)),
                estado_civil="Casado",
                nacionalidade="Brasileiro",
                endereco=f"Avenida Proprietario {i}, 200",
                tipo="proprietario",      # Ajustado para corresponder ao valor da opção
                chave_pix=cpf_value,      # Chave PIX igual ao CPF
                status="disponivel"       # Status fixo como disponivel
            )
            proprietarios.append(prop)
        self.stdout.write("5 proprietários criados.")


        # Criando 2 imobiliárias e vinculando a proprietários
        imobiliarias = []
        for i in range(1, 3):
            imobiliaria = Imobiliaria.objects.create(
                nome=f"Imobiliaria {i}",
                cnpj=str(random.randint(10**13, 10**14 - 1)),  # 14 dígitos
                endereco=f"Av. Imobiliaria {i}, 1000",
            )
            imobiliarias.append(imobiliaria)
        self.stdout.write("2 imobiliárias criadas.")

        # Criando 3 condomínios
        condominios = []
        for i in range(1, 4):
            condominio = Condominio.objects.create(
                nome=f"Condominio {i}",
                cnpj=str(random.randint(10**13, 10**14 - 1)),
                endereco=f"Rua Condominio {i}, 500"
            )
            condominios.append(condominio)
        self.stdout.write("3 condomínios criados.")

        # Mapeamento: associa cada imobiliária a um condomínio (se disponível)
        imobiliaria_condominio_map = {}
        if imobiliarias and len(condominios) >= 2:
            imobiliaria_condominio_map[imobiliarias[0]] = condominios[0]
            imobiliaria_condominio_map[imobiliarias[1]] = condominios[1]

        # Criando 20 imóveis e vinculando-os diretamente à imobiliária, ao condomínio e ao proprietário
        imoveis = []
        # Lista de tipos: Kitnet, Casa e Barracao, conforme alterações
        tipos_imovel = ['Kitnet', 'Casa', 'Barracao']
        for i in range(1, 11):
            ref = f"IMV{i:03d}"
            # Garante referência única
            while Imovel.objects.filter(referencia=ref).exists():
                ref = f"IMV{i:03d}-{random.randint(100,999)}"
            # Seleciona aleatoriamente uma imobiliária dentre as criadas
            imobiliaria = random.choice(imobiliarias)
            # Recupera o condomínio associado à imobiliária, se existir
            condominio = imobiliaria_condominio_map.get(imobiliaria)
            # Seleciona aleatoriamente um tipo de imóvel
            tipo = random.choice(tipos_imovel)
            # Define a categoria: se o tipo for Barracao, a categoria será Comercial; caso contrário, Residencial
            categoria = "Comercial" if tipo == "Barracao" else "Residencial"
            # Consulta no banco de dados as pessoas com tipo "proprietario" e seleciona uma aleatoriamente
            proprietario = random.choice(list(Pessoa.objects.filter(tipo__iexact="proprietario")))
            imovel = Imovel.objects.create(
                referencia=ref,
                endereco=f"Rua Imovel {i}, {random.randint(1,300)}",
                valor_aluguel=round(random.uniform(1000.00, 5000.00), 2),
                valor_venda=round(random.uniform(200000.00, 500000.00), 2),
                tipo=tipo,
                categoria=categoria,
                status="disponivel",
                observacoes=f"Imóvel {i} gerado automaticamente.",
                imobiliaria=imobiliaria,
                condominio=condominio,
                proprietario=proprietario
            )
            imoveis.append(imovel)
        self.stdout.write("20 imóveis criados e vinculados a imobiliárias, condomínios e proprietários através dos campos em Imovel.")
        self.stdout.write(self.style.SUCCESS("Seed executado com sucesso!"))

