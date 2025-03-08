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
            inq = Pessoa.objects.create(
                nome=f"Inquilino {i}",
                data_nascimento=date(1990, random.randint(1, 12), random.randint(1, 28)),
                cpf="{:011d}".format(random.randint(0, 99999999999)),
                rg=str(random.randint(1000000, 9999999)),
                estado_civil="Solteiro",
                nacionalidade="Brasileiro",
                endereco=f"Rua Inquilino {i}, 100",
                tipo="inquilino"
            )
            inquilinos.append(inq)
        self.stdout.write("5 inquilinos criados.")

        # Criando 5 proprietários
        proprietarios = []
        for i in range(1, 6):
            prop = Pessoa.objects.create(
                nome=f"Proprietario {i}",
                data_nascimento=date(1970, random.randint(1, 12), random.randint(1, 28)),
                cpf="{:011d}".format(random.randint(0, 99999999999)),
                rg=str(random.randint(1000000, 9999999)),
                estado_civil="Casado",
                nacionalidade="Brasileiro",
                endereco=f"Avenida Proprietario {i}, 200",
                tipo="proprietario"
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
                proprietario=proprietarios[i - 1]
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

        # Atribuir para cada imobiliária um condomínio.
        # Neste exemplo, associamos:
        # - Imobiliaria 1 com Condominio 1
        # - Imobiliaria 2 com Condominio 2
        imobiliaria_condominio_map = {}
        if imobiliarias and len(condominios) >= 2:
            imobiliaria_condominio_map[imobiliarias[0]] = condominios[0]
            imobiliaria_condominio_map[imobiliarias[1]] = condominios[1]

        # Criando 20 imóveis e vinculando a uma imobiliária e ao condomínio associado a ela
        imoveis = []
        tipos_imovel = ['residencial', 'comercial']
        for i in range(1, 21):
            # Gera a referência básica
            ref = f"IMV{i:03d}"
            # Se já existe um imóvel com essa referência, gera uma nova referência com sufixo aleatório
            while Imovel.objects.filter(referencia=ref).exists():
                ref = f"IMV{i:03d}-{random.randint(100,999)}"
            imovel = Imovel.objects.create(
                referencia=ref,
                endereco=f"Rua Imovel {i}, {random.randint(1,300)}",
                valor_aluguel=round(random.uniform(1000.00, 5000.00), 2),
                valor_venda=round(random.uniform(200000.00, 500000.00), 2),
                tipo=random.choice(tipos_imovel),
                status="disponivel",
                observacoes=f"Imóvel {i} gerado automaticamente."
            )
            # Escolhe aleatoriamente uma imobiliária dentre as 2 criadas
            imobiliaria = random.choice(imobiliarias)
            imobiliaria.imoveis.add(imovel)
            # Vincula o imóvel ao condomínio associado à imobiliária escolhida
            condominio = imobiliaria_condominio_map.get(imobiliaria)
            if condominio:
                condominio.imoveis.add(imovel)
            imoveis.append(imovel)
        self.stdout.write("20 imóveis criados e vinculados a imobiliárias e condomínios.")
        self.stdout.write(self.style.SUCCESS("Seed executado com sucesso!"))
