# Guia de Instalação - LR Prótese ERP

## Instalação em Ambiente de Produção

### 1. Preparação do Servidor

#### Requisitos do Sistema
- Ubuntu 20.04+ ou CentOS 8+
- Python 3.11+
- Node.js 20+
- Nginx (recomendado)
- SSL Certificate (recomendado)

#### Instalação das Dependências

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip nodejs npm nginx

# Instalar pnpm
npm install -g pnpm

# Instalar PM2 para gerenciamento de processos
npm install -g pm2
```

### 2. Configuração do Backend

#### Clonagem e Configuração
```bash
# Clonar o projeto
git clone <repository-url> /var/www/lr-protese-erp
cd /var/www/lr-protese-erp

# Configurar backend
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Configuração do Banco de Dados
```bash
# Para produção, recomenda-se PostgreSQL
sudo apt install postgresql postgresql-contrib

# Criar banco de dados
sudo -u postgres createdb lr_protese_erp
sudo -u postgres createuser lr_protese_user

# Configurar senha (substitua 'senha_segura')
sudo -u postgres psql -c "ALTER USER lr_protese_user PASSWORD 'senha_segura';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE lr_protese_erp TO lr_protese_user;"
```

#### Variáveis de Ambiente
```bash
# Criar arquivo .env no diretório backend
cat > backend/.env << EOF
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_muito_segura_aqui
DATABASE_URL=postgresql://lr_protese_user:senha_segura@localhost/lr_protese_erp
CORS_ORIGINS=https://seudominio.com
EOF
```

#### Configuração do PM2
```bash
# Criar arquivo ecosystem.config.js
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'lr-protese-backend',
    script: 'backend/venv/bin/python',
    args: 'backend/src/main.py',
    cwd: '/var/www/lr-protese-erp',
    env: {
      FLASK_ENV: 'production',
      PORT: 5001
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
}
EOF
```

### 3. Configuração do Frontend

#### Build de Produção
```bash
cd frontend

# Instalar dependências
pnpm install

# Configurar variáveis de ambiente
cat > .env.production << EOF
VITE_API_URL=https://seudominio.com/api
EOF

# Build de produção
pnpm run build
```

### 4. Configuração do Nginx

```bash
# Criar configuração do site
sudo cat > /etc/nginx/sites-available/lr-protese-erp << EOF
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name seudominio.com www.seudominio.com;

    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # Frontend (React)
    location / {
        root /var/www/lr-protese-erp/frontend/dist;
        try_files \$uri \$uri/ /index.html;
        
        # Cache estático
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Logs
    access_log /var/log/nginx/lr-protese-erp.access.log;
    error_log /var/log/nginx/lr-protese-erp.error.log;
}
EOF

# Ativar site
sudo ln -s /etc/nginx/sites-available/lr-protese-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Inicialização dos Serviços

```bash
# Iniciar backend com PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Verificar status
pm2 status
```

### 6. Configuração de Backup

#### Script de Backup do Banco
```bash
cat > /usr/local/bin/backup-lr-protese.sh << EOF
#!/bin/bash
BACKUP_DIR="/var/backups/lr-protese-erp"
DATE=\$(date +%Y%m%d_%H%M%S)

mkdir -p \$BACKUP_DIR

# Backup do banco de dados
pg_dump -h localhost -U lr_protese_user lr_protese_erp > \$BACKUP_DIR/db_backup_\$DATE.sql

# Backup dos arquivos
tar -czf \$BACKUP_DIR/files_backup_\$DATE.tar.gz /var/www/lr-protese-erp

# Manter apenas os últimos 7 backups
find \$BACKUP_DIR -name "*.sql" -mtime +7 -delete
find \$BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/backup-lr-protese.sh

# Agendar backup diário
echo "0 2 * * * /usr/local/bin/backup-lr-protese.sh" | sudo crontab -
```

### 7. Monitoramento

#### Logs
```bash
# Logs do backend
pm2 logs lr-protese-backend

# Logs do Nginx
sudo tail -f /var/log/nginx/lr-protese-erp.access.log
sudo tail -f /var/log/nginx/lr-protese-erp.error.log
```

#### Monitoramento de Recursos
```bash
# Instalar htop para monitoramento
sudo apt install htop

# Verificar uso de recursos
htop
pm2 monit
```

## Instalação em Ambiente de Desenvolvimento

### 1. Configuração Rápida

```bash
# Clonar repositório
git clone <repository-url>
cd lr-protese-erp

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
python src/main.py

# Frontend (em outro terminal)
cd frontend
pnpm install
pnpm run dev --host
```

### 2. Configuração com Docker (Opcional)

```dockerfile
# Dockerfile.backend
FROM python:3.11-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
EXPOSE 5001

CMD ["python", "src/main.py"]
```

```dockerfile
# Dockerfile.frontend
FROM node:20-alpine

WORKDIR /app
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install

COPY frontend/ .
RUN pnpm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 80
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5001:5001"
    environment:
      - FLASK_ENV=development
    volumes:
      - ./backend:/app

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

## Solução de Problemas

### Problemas Comuns

1. **Erro de CORS**
   - Verificar configuração de CORS no backend
   - Confirmar URLs permitidas

2. **Banco de dados não conecta**
   - Verificar credenciais
   - Confirmar se o serviço PostgreSQL está rodando

3. **Frontend não carrega**
   - Verificar se o build foi executado
   - Confirmar configuração do Nginx

4. **API não responde**
   - Verificar se o backend está rodando
   - Conferir logs do PM2

### Comandos Úteis

```bash
# Reiniciar serviços
pm2 restart lr-protese-backend
sudo systemctl restart nginx

# Verificar logs
pm2 logs
sudo journalctl -u nginx

# Verificar portas
sudo netstat -tlnp | grep :5001
sudo netstat -tlnp | grep :80
```

## Atualizações

### Processo de Atualização

1. **Backup completo**
2. **Parar serviços**
3. **Atualizar código**
4. **Instalar dependências**
5. **Executar migrações**
6. **Rebuild frontend**
7. **Reiniciar serviços**
8. **Verificar funcionamento**

```bash
# Script de atualização
#!/bin/bash
cd /var/www/lr-protese-erp

# Backup
/usr/local/bin/backup-lr-protese.sh

# Parar serviços
pm2 stop lr-protese-backend

# Atualizar código
git pull origin main

# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
pnpm install
pnpm run build

# Reiniciar
pm2 start lr-protese-backend
sudo systemctl reload nginx
```

## Segurança

### Recomendações de Segurança

1. **Firewall**
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

2. **SSL/TLS**
   - Usar certificados válidos
   - Configurar HSTS
   - Desabilitar protocolos inseguros

3. **Banco de Dados**
   - Senhas fortes
   - Conexões criptografadas
   - Backups regulares

4. **Sistema**
   - Atualizações regulares
   - Monitoramento de logs
   - Acesso restrito

## Suporte

Para suporte técnico:
- Verificar logs primeiro
- Documentar o problema
- Incluir informações do ambiente
- Contatar equipe de desenvolvimento

