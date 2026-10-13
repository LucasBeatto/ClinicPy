# ClinicPy

ClinicPy é um sistema de gerenciamento médico desenvolvido em Python com foco em aprendizado prático de desenvolvimento backend, banco de dados relacional, orientação a objetos, APIs REST e arquitetura de software.

O projeto foi criado com o objetivo de simular uma aplicação real de comunicação e gerenciamento entre médicos e pacientes, permitindo evoluir gradualmente de um sistema conectado ao banco de dados para uma API completa utilizando FastAPI.

## Objetivo do projeto

O ClinicPy permitirá que médicos e pacientes utilizem o mesmo sistema com funcionalidades diferentes de acordo com o perfil do usuário.

### Paciente

O paciente poderá:

- Criar uma conta
- Fazer login
- Atualizar seus dados pessoais
- Pesquisar médicos
- Visualizar informações dos médicos
- Solicitar consultas
- Acompanhar o status das consultas
- Visualizar consultas futuras
- Visualizar histórico de consultas
- Cancelar consultas
- Receber documentos médicos
- Baixar receitas
- Baixar atestados
- Baixar pedidos de exames
- Futuramente conversar com médicos através de chat

### Médico

O médico poderá:

- Criar uma conta
- Fazer login
- Atualizar dados profissionais
- Informar CRM e UF
- Cadastrar suas especialidades
- Configurar dias e horários de atendimento
- Visualizar solicitações de consultas
- Aceitar ou recusar consultas
- Visualizar consultas confirmadas
- Consultar seus pacientes
- Enviar documentos
- Enviar receitas
- Enviar atestados
- Enviar pedidos de exames
- Finalizar consultas
- Futuramente conversar com pacientes através de chat

## Regras de negócio

1. Um paciente não pode possuir duas contas com o mesmo CPF.
2. Um médico não pode possuir duas contas com o mesmo CRM e UF.
3. Um horário não pode ser ocupado por duas consultas ativas do mesmo médico.
4. O paciente solicita a consulta.
5. O médico pode aceitar ou recusar uma solicitação.
6. Apenas consultas confirmadas podem passar para o status `em_andamento`.
7. Apenas consultas em andamento podem ser finalizadas.
8. Um paciente só pode acessar documentos relacionados às próprias consultas.
9. Um médico só pode enviar documentos para pacientes vinculados a uma consulta.
10. O chat só poderá existir quando houver vínculo entre médico e paciente.
11. O médico poderá definir seus dias e horários de atendimento.
12. Um paciente só poderá solicitar consultas dentro da disponibilidade do médico.
13. A disponibilidade deverá ser verificada novamente no momento da confirmação do agendamento.

## Banco de dados

O banco de dados utilizado atualmente é MySQL.

### Tabelas

- `usuario`
- `paciente`
- `medico`
- `especialidade`
- `medico_especialidade`
- `disponibilidade`
- `consulta`
- `documento`

A tabela de mensagens será implementada futuramente.

## Relacionamentos

### Usuário e Paciente

Relação:

`1:1`

Um usuário do tipo paciente possui apenas um perfil de paciente.

### Usuário e Médico

Relação:

`1:1`

Um usuário do tipo médico possui apenas um perfil médico.

### Médico e Especialidade

Relação:

`N:N`

Um médico pode possuir várias especialidades e uma especialidade pode possuir vários médicos.

A relação é realizada através da tabela:

`medico_especialidade`

### Médico e Disponibilidade

Relação:

`1:N`

Um médico pode possuir vários períodos de disponibilidade.

### Paciente e Consulta

Relação:

`1:N`

Um paciente pode possuir várias consultas.

### Médico e Consulta

Relação:

`1:N`

Um médico pode possuir várias consultas.

### Consulta e Documento

Relação:

`1:N`

Uma consulta pode possuir vários documentos.

## Status das consultas

Atualmente uma consulta pode possuir os seguintes status:

- `pendente`
- `confirmada`
- `recusada`
- `cancelada`
- `em_andamento`
- `finalizada`

Toda nova solicitação começa automaticamente como:

`pendente`

## Disponibilidade médica

Cada médico poderá configurar seus períodos de atendimento.

Exemplo:

```text
Segunda-feira
08:00 às 12:00

Segunda-feira
14:00 às 18:00

Quarta-feira
08:00 às 12:00
```

A duração padrão das consultas também será definida pelo médico.

Os dias da semana são representados internamente de forma numérica:

```text
1 = Segunda-feira
2 = Terça-feira
3 = Quarta-feira
4 = Quinta-feira
5 = Sexta-feira
6 = Sábado
7 = Domingo
```

## Segurança

As senhas dos usuários não serão armazenadas diretamente no banco de dados.

O sistema utilizará hash seguro para armazenar senhas.

Está prevista a utilização de:

- Argon2
- autenticação por token
- JWT
- controle de permissões entre pacientes e médicos

Dados sensíveis de configuração são armazenados através de variáveis de ambiente no arquivo `.env`.

O arquivo `.env` não é versionado no Git.

## Tecnologias

Atualmente o projeto utiliza:

- Python
- MySQL
- SQLAlchemy
- PyMySQL
- python-dotenv
- Git
- GitHub

Também já estão instalados e serão utilizados durante a evolução do projeto:

- FastAPI
- Alembic
- Uvicorn
- Pydantic

## Estrutura atual

```text
ClinicPy/
│
├── app/
│   │
│   ├── database/
│   │   ├── base.py
│   │   └── connection.py
│   │
│   └── models/
│       ├── associations.py
│       ├── usuario.py
│       ├── paciente.py
│       ├── medico.py
│       ├── especialidade.py
│       └── disponibilidade.py
│
├── .env
├── .gitignore
├── README.md
│
├── test_connection.py
├── test_session.py
├── test_usuario.py
├── test_paciente.py
├── test_medico.py
└── test_disponibilidade.py
```

O arquivo `.env` é ignorado pelo Git e não deve ser publicado.

## ORM

O projeto utiliza SQLAlchemy para fazer o mapeamento objeto-relacional entre as tabelas MySQL e as classes Python.

Atualmente já estão mapeadas as seguintes entidades:

- Usuario
- Paciente
- Medico
- Especialidade
- Disponibilidade

Os seguintes relacionamentos ORM já estão funcionando:

```text
Usuario 1:1 Paciente

Usuario 1:1 Medico

Medico N:N Especialidade

Medico 1:N Disponibilidade
```

## Conexão com o banco

A aplicação já possui conexão funcional entre:

```text
Python
↓
SQLAlchemy
↓
PyMySQL
↓
MySQL
↓
ClinicPy
```

As configurações do banco são carregadas através do arquivo `.env`.

Exemplo de estrutura:

```env
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
DB_NAME=clinicpy
```

Nunca devem ser adicionadas credenciais reais ao repositório.

## Funcionalidades já concluídas

- Modelagem inicial do banco de dados
- Criação das tabelas
- Chaves primárias
- Chaves estrangeiras
- Restrições de unicidade
- Relacionamentos `1:1`
- Relacionamentos `1:N`
- Relacionamento `N:N`
- Validações com `CHECK`
- Conexão Python com MySQL
- Configuração do SQLAlchemy
- Configuração de sessões
- Criação da Base ORM
- Model Usuario
- Model Paciente
- Model Medico
- Model Especialidade
- Model Disponibilidade
- Testes de consulta ao banco utilizando ORM

## Próximas etapas

As próximas etapas previstas são:

- Criar o model `Consulta`
- Criar o model `Documento`
- Finalizar todos os relacionamentos ORM
- Implementar cadastro de usuários através do Python
- Implementar hash de senhas
- Implementar regras de negócio
- Criar schemas com Pydantic
- Criar API REST com FastAPI
- Implementar autenticação
- Implementar JWT
- Criar endpoints para pacientes
- Criar endpoints para médicos
- Criar endpoints para consultas
- Criar endpoints para disponibilidade
- Criar upload de documentos
- Implementar migrations com Alembic
- Criar testes automatizados
- Criar documentação da API
- Adicionar Docker
- Fazer deploy da aplicação
- Desenvolver interface web
- Implementar chat médico-paciente

## Planejamento de arquitetura

A arquitetura final prevista será aproximadamente:

```text
Frontend
   ↓
FastAPI
   ↓
Routes
   ↓
Services
   ↓
Repositories
   ↓
SQLAlchemy ORM
   ↓
MySQL
```

Também serão adicionadas camadas específicas para:

- autenticação
- segurança
- validação
- upload de documentos
- configuração
- testes

## Status

Projeto em desenvolvimento.

O ClinicPy está sendo desenvolvido como projeto de estudo e portfólio, com foco em aplicar conhecimentos de Python, orientação a objetos, SQL, MySQL, APIs REST, autenticação, Git, arquitetura backend e desenvolvimento de aplicações reais.