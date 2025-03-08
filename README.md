Projeto Erent
Projeto Erent é uma aplicação web desenvolvida com Django para a administração de imóveis. O sistema permite o cadastro e gerenciamento de pessoas (inquilinos, proprietários e imobiliários), imobiliárias, condomínios, imóveis e contratos de locação/compra e venda.

Funcionalidades
Cadastro e Gerenciamento de Registros:

Pessoas: Cadastro de inquilinos, proprietários e imobiliários.
Imobiliárias: Gestão de imobiliárias, associadas a um proprietário e aos imóveis.
Condomínios: Cadastro de condomínios e vinculação de imóveis.
Imóveis: Registro de imóveis com informações como referência, endereço, valores de aluguel e venda, tipo e status.
Contratos: Criação de contratos de locação e compra/venda, com cálculo automático de datas, garantia, modo e dia de pagamento.
Geração de Contratos:

Cálculo da data final do contrato com base em períodos pré-definidos (6, 12 ou 24 meses).
Impressão e visualização de contratos com layout responsivo e adequado para impressão em papel A4.
Interface Responsiva:

Layouts desenvolvidos com Bootstrap 4.5 para uma boa experiência em dispositivos móveis e desktops.
Seed de Dados:

Comando de seed para popular o banco de dados com dados iniciais, facilitando testes e desenvolvimento.
Tecnologias Utilizadas
Linguagem: Python 3.x
Framework: Django 5.x
Banco de Dados: PostgreSQL (pode ser configurado conforme sua necessidade)
Front-end: HTML, CSS, Bootstrap 4.5
Estrutura do Projeto
apps/administracao/
Contém os modelos (models), visualizações (views), formulários (forms), templates e comandos de seed para gerenciamento dos dados do sistema.

templates/
Arquivos HTML que compõem a interface do usuário. O arquivo base.html define o layout principal e é estendido pelos demais templates.

manage.py
Arquivo de gerenciamento do Django.

Instalação e Configuração
Clone o repositório:

bash
Copiar
git clone https://github.com/marcosweippert/erent.git
Crie e ative um ambiente virtual:

bash
Copiar
cd projeto_erent
python -m venv venv
# No Linux/macOS:
source venv/bin/activate
# No Windows:
venv\Scripts\activate
Instale as dependências:

bash
Copiar
pip install -r requirements.txt
Configure o banco de dados:
Atualize as configurações de banco de dados em settings.py conforme sua instalação do PostgreSQL ou outro banco de dados.

Execute as migrações:

bash
Copiar
python manage.py migrate
Popule o banco de dados (opcional):

bash
Copiar
python manage.py seed
Execute o servidor de desenvolvimento:

bash
Copiar
python manage.py runserver
Uso
Acesse a página inicial em http://127.0.0.1:8000/.
Utilize a barra de navegação para acessar as seções:
Pessoas
Imobiliárias
Condomínios
Imóveis
Contratos
Cada seção permite a criação, edição, visualização e exclusão dos registros.

Contribuição
Contribuições são muito bem-vindas! Para contribuir:

Faça um fork do repositório.
Crie uma branch para sua feature: git checkout -b minha-feature.
Faça suas alterações e commit: git commit -am "Adiciona nova feature".
Envie a branch para o seu fork: git push origin minha-feature.
Abra um Pull Request.
Licença
Este projeto está licenciado sob a Licença MIT.

Contato
Caso tenha dúvidas ou sugestões, entre em contato pelo e-mail marcos.weippert@gmail.com
