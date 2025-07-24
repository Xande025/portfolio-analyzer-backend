# 🚀 Guia de Instalação - Analisador de Portfólio

Este guia fornece instruções detalhadas para instalar e configurar o Analisador de Portfólio em diferentes ambientes.

## 📋 Requisitos do Sistema

### Mínimos
- **Sistema Operacional**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.11 ou superior
- **Node.js**: 18.0 ou superior
- **RAM**: 4GB mínimo, 8GB recomendado
- **Espaço em Disco**: 2GB livres
- **Conexão**: Internet para dados financeiros

### Recomendados
- **Python**: 3.11.x (versão mais recente)
- **Node.js**: 20.x LTS
- **RAM**: 16GB para melhor performance
- **SSD**: Para melhor velocidade de I/O

## 🛠️ Instalação Rápida

### Opção 1: Script Automático (Linux/macOS)
```bash
curl -fsSL https://raw.githubusercontent.com/seu-repo/install.sh | bash
```

### Opção 2: Instalação Manual
Siga as instruções detalhadas abaixo para sua plataforma.

## 🐧 Linux (Ubuntu/Debian)

### 1. Atualizar Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Python 3.11
```bash
# Ubuntu 22.04+
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Ubuntu 20.04 (adicionar PPA)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

### 3. Instalar Node.js
```bash
# Usando NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verificar instalação
node --version
npm --version
```

### 4. Instalar Git
```bash
sudo apt install git -y
```

### 5. Clonar e Configurar Projeto
```bash
# Clonar repositório
git clone https://github.com/seu-usuario/portfolio-analyzer.git
cd portfolio-analyzer

# Configurar backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configurar frontend
cd ../portfolio-frontend
npm install
npm run build

# Copiar build para Flask
cp -r dist/* ../portfolio-analyzer/src/static/
```

### 6. Executar Aplicação
```bash
cd ../portfolio-analyzer
source venv/bin/activate
python src/main.py
```

## 🍎 macOS

### 1. Instalar Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Instalar Python 3.11
```bash
brew install python@3.11
```

### 3. Instalar Node.js
```bash
brew install node@20
```

### 4. Instalar Git
```bash
brew install git
```

### 5. Configurar Projeto
```bash
# Clonar repositório
git clone https://github.com/seu-usuario/portfolio-analyzer.git
cd portfolio-analyzer

# Configurar backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Configurar frontend
cd ../portfolio-frontend
npm install
npm run build

# Copiar build para Flask
cp -r dist/* ../portfolio-analyzer/src/static/
```

### 6. Executar Aplicação
```bash
cd ../portfolio-analyzer
source venv/bin/activate
python src/main.py
```

## 🪟 Windows

### 1. Instalar Python 3.11
1. Baixe Python 3.11 do [site oficial](https://www.python.org/downloads/)
2. Execute o instalador
3. ✅ Marque "Add Python to PATH"
4. ✅ Marque "Install for all users"
5. Clique em "Install Now"

### 2. Instalar Node.js
1. Baixe Node.js 20 LTS do [site oficial](https://nodejs.org/)
2. Execute o instalador
3. Siga as instruções padrão

### 3. Instalar Git
1. Baixe Git do [site oficial](https://git-scm.com/download/win)
2. Execute o instalador
3. Use configurações padrão

### 4. Configurar Projeto
```cmd
# Abrir PowerShell como Administrador

# Clonar repositório
git clone https://github.com/seu-usuario/portfolio-analyzer.git
cd portfolio-analyzer

# Configurar backend
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Configurar frontend
cd ..\portfolio-frontend
npm install
npm run build

# Copiar build para Flask
xcopy /E /I dist\* ..\portfolio-analyzer\src\static\
```

### 5. Executar Aplicação
```cmd
cd ..\portfolio-analyzer
venv\Scripts\activate
python src\main.py
```

## 🐳 Docker

### Dockerfile
```dockerfile
# Multi-stage build
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend
COPY portfolio-frontend/package*.json ./
RUN npm ci --only=production

COPY portfolio-frontend/ ./
RUN npm run build

FROM python:3.11-slim AS backend

WORKDIR /app
COPY portfolio-analyzer/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY portfolio-analyzer/ ./
COPY --from=frontend-build /app/frontend/dist/ ./src/static/

EXPOSE 5000
CMD ["python", "src/main.py"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  portfolio-analyzer:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### Executar com Docker
```bash
# Build e executar
docker-compose up --build

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

## ☁️ Deploy em Nuvem

### Heroku
```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Criar app
heroku create seu-portfolio-analyzer

# Configurar buildpacks
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python

# Deploy
git push heroku main

# Abrir app
heroku open
```

### Vercel (Frontend apenas)
```bash
# Instalar Vercel CLI
npm i -g vercel

# Deploy frontend
cd portfolio-frontend
vercel --prod
```

### AWS EC2
```bash
# Conectar à instância
ssh -i sua-chave.pem ubuntu@seu-ip

# Instalar dependências
sudo apt update
sudo apt install python3.11 python3.11-venv nodejs npm nginx -y

# Configurar aplicação
git clone https://github.com/seu-usuario/portfolio-analyzer.git
cd portfolio-analyzer

# Seguir passos de instalação Linux
# Configurar Nginx como proxy reverso
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
Crie arquivo `.env` na raiz do projeto:
```bash
# Desenvolvimento
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=dev-secret-key-change-in-production

# Produção
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secret-key-here

# APIs (opcional)
ALPHA_VANTAGE_API_KEY=your-api-key
FINNHUB_API_KEY=your-api-key

# Database (opcional)
DATABASE_URL=postgresql://user:pass@localhost/portfolio_db

# Cache (opcional)
REDIS_URL=redis://localhost:6379/0
```

### Configuração de Banco de Dados
```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///portfolio.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
```

### Nginx (Produção)
```nginx
# /etc/nginx/sites-available/portfolio-analyzer
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/portfolio-analyzer/src/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Systemd Service (Linux)
```ini
# /etc/systemd/system/portfolio-analyzer.service
[Unit]
Description=Portfolio Analyzer
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/portfolio-analyzer
Environment=PATH=/home/ubuntu/portfolio-analyzer/venv/bin
ExecStart=/home/ubuntu/portfolio-analyzer/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar e iniciar serviço
sudo systemctl enable portfolio-analyzer
sudo systemctl start portfolio-analyzer
sudo systemctl status portfolio-analyzer
```

## 🔍 Verificação da Instalação

### Testes Básicos
```bash
# Testar backend
curl http://localhost:5000/api/search?query=AAPL

# Testar frontend
curl http://localhost:5000/

# Verificar logs
tail -f flask.log
```

### Testes de Funcionalidade
1. Abra http://localhost:5000
2. Busque por "AAPL"
3. Adicione ao portfólio
4. Visualize métricas no dashboard
5. Teste otimização
6. Configure um alerta

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"
```bash
# Linux/macOS
which python3.11
export PATH="/usr/bin/python3.11:$PATH"

# Windows
where python
# Adicionar Python ao PATH nas variáveis de ambiente
```

### Erro: "Node não encontrado"
```bash
# Verificar instalação
node --version
npm --version

# Reinstalar se necessário
# Linux: sudo apt install nodejs npm
# macOS: brew install node
# Windows: Baixar do site oficial
```

### Erro: "Módulo não encontrado"
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "Porta em uso"
```bash
# Encontrar processo usando porta 5000
lsof -i :5000  # Linux/macOS
netstat -ano | findstr :5000  # Windows

# Matar processo
kill -9 PID  # Linux/macOS
taskkill /PID PID /F  # Windows
```

### Erro: "Dados financeiros não carregam"
1. Verificar conexão com internet
2. Testar APIs manualmente:
   ```bash
   curl "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
   ```
3. Verificar firewall/proxy
4. Tentar símbolos diferentes

## 📞 Suporte

### Documentação
- [Guia do Usuário](USER_GUIDE.md)
- [Documentação da API](API_DOCS.md)
- [Guia de Desenvolvimento](DEVELOPMENT.md)

### Comunidade
- **GitHub Issues**: Para bugs e features
- **Discussions**: Para dúvidas gerais
- **Email**: suporte@analisador-portfolio.com

### Logs Úteis
```bash
# Backend logs
tail -f flask.log

# Sistema logs (Linux)
journalctl -u portfolio-analyzer -f

# Nginx logs (se usando)
tail -f /var/log/nginx/error.log
```

---

**Instalação concluída! 🎉 Acesse http://localhost:5000 para começar a usar.**

