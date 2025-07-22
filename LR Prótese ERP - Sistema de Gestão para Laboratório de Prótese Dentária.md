# LR Prótese ERP - Sistema de Gestão para Laboratório de Prótese Dentária

## Visão Geral

O LR Prótese ERP é um sistema completo de gestão desenvolvido especificamente para laboratórios de prótese dentária. O sistema oferece controle integrado de todas as operações do laboratório, desde o cadastro de clientes até a entrega final dos trabalhos protéticos.

## Funcionalidades Principais

### 📊 Dashboard
- Visão geral das operações do laboratório
- Indicadores de performance em tempo real
- Alertas e notificações importantes
- Gráficos de faturamento e produtividade

### 👥 Gestão de Clientes
- Cadastro completo de dentistas e clínicas
- Histórico de relacionamento
- Controle de preferências e observações
- Segmentação por tipo de cliente

### 🦷 Gestão de Pacientes
- Cadastro detalhado de pacientes
- Histórico odontológico
- Vinculação com dentistas responsáveis
- Controle de tratamentos em andamento

### 📋 Ordens de Serviço
- Criação e acompanhamento de OS
- Controle de prazos e prioridades
- Especificações técnicas detalhadas
- Anexos e documentos relacionados

### ⚙️ Controle de Produção
- Fluxo de trabalho por etapas
- Kanban de produção
- Controle de qualidade
- Rastreabilidade completa

### 📦 Gestão de Estoque
- Controle de materiais e insumos
- Alertas de estoque mínimo
- Movimentações de entrada e saída
- Relatórios de consumo

### 💰 Módulo Financeiro
- Contas a receber e a pagar
- Fluxo de caixa
- Relatórios de faturamento
- Controle de inadimplência

### 📅 Agenda
- Calendário de eventos
- Agendamento de entregas e coletas
- Lembretes automáticos
- Integração com ordens de serviço

## Tecnologias Utilizadas

### Backend
- **Python 3.11** - Linguagem de programação
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados (desenvolvimento)
- **Flask-CORS** - Suporte a CORS

### Frontend
- **React 19** - Biblioteca JavaScript
- **Vite** - Build tool e dev server
- **React Router** - Roteamento
- **Tailwind CSS** - Framework CSS
- **Shadcn/UI** - Componentes de interface
- **Lucide React** - Ícones

## Estrutura do Projeto

```
lr-protese-erp/
├── backend/                 # Aplicação Flask
│   ├── src/
│   │   ├── models/         # Modelos de dados
│   │   ├── routes/         # Rotas da API
│   │   ├── database.py     # Configuração do banco
│   │   └── main.py         # Aplicação principal
│   ├── venv/               # Ambiente virtual Python
│   └── requirements.txt    # Dependências Python
├── frontend/               # Aplicação React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── pages/          # Páginas da aplicação
│   │   └── App.jsx         # Componente principal
│   ├── package.json        # Dependências Node.js
│   └── vite.config.js      # Configuração do Vite
└── README.md              # Este arquivo
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- pnpm (gerenciador de pacotes)

### Backend (Flask)

1. Navegue para o diretório do backend:
```bash
cd backend
```

2. Ative o ambiente virtual:
```bash
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python src/main.py
```

O backend estará disponível em `http://localhost:5001`

### Frontend (React)

1. Navegue para o diretório do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
pnpm install
```

3. Execute a aplicação:
```bash
pnpm run dev --host
```

O frontend estará disponível em `http://localhost:5173`

## Uso do Sistema

### Login
- **Usuário:** admin
- **Senha:** admin123

### Navegação
O sistema possui um menu lateral com acesso a todos os módulos:
- Dashboard (página inicial)
- Clientes
- Pacientes  
- Ordens de Serviço
- Produção
- Estoque
- Financeiro
- Agenda

## API Endpoints

### Dashboard
- `GET /api/dashboard/resumo` - Resumo geral do sistema

### Clientes
- `GET /api/clientes` - Listar clientes
- `POST /api/clientes` - Criar cliente
- `PUT /api/clientes/{id}` - Atualizar cliente
- `DELETE /api/clientes/{id}` - Excluir cliente

### Usuários
- `POST /api/users/login` - Autenticação
- `GET /api/users/profile` - Perfil do usuário

## Banco de Dados

O sistema utiliza SQLite para desenvolvimento, com as seguintes tabelas principais:

- **users** - Usuários do sistema
- **clientes** - Dentistas e clínicas
- **pacientes** - Pacientes dos dentistas
- **ordens_servico** - Ordens de serviço
- **etapas_producao** - Etapas de produção
- **materiais** - Materiais e insumos
- **movimentacoes_estoque** - Movimentações de estoque
- **contas_receber** - Contas a receber
- **contas_pagar** - Contas a pagar
- **eventos_agenda** - Eventos da agenda
- **anexos_os** - Anexos das ordens de serviço

## Desenvolvimento

### Adicionando Novos Módulos

1. **Backend:**
   - Criar modelo em `backend/src/models/`
   - Criar rotas em `backend/src/routes/`
   - Registrar blueprint em `main.py`

2. **Frontend:**
   - Criar página em `frontend/src/pages/`
   - Adicionar rota em `App.jsx`
   - Atualizar menu em `Layout.jsx`

### Padrões de Código

- **Backend:** Seguir padrões PEP 8 para Python
- **Frontend:** Usar ESLint e Prettier para formatação
- **Commits:** Usar conventional commits

## Segurança

- Autenticação baseada em sessão
- Validação de dados no backend
- Sanitização de inputs
- CORS configurado adequadamente

## Performance

- Paginação em listagens
- Lazy loading de componentes
- Otimização de queries SQL
- Cache de dados estáticos

## Suporte e Manutenção

Para suporte técnico ou dúvidas sobre o sistema:
- Documentação técnica disponível no código
- Logs detalhados para debugging
- Estrutura modular para facilitar manutenção

## Licença

Este projeto foi desenvolvido especificamente para o LR Prótese Dental.

## Versão

**v1.0.0** - Versão inicial com funcionalidades básicas implementadas.

