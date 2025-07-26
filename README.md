# Validador de Itens

🧪 Aplicação web simplificada para validação de itens educacionais por diferentes grupos, com controle de acesso, upload de arquivos em lote e relatórios por grupo e usuário.

## 🛠️ Tecnologias Utilizadas

* 🐍 Python 3.11
* 🌐 Django 5
* 🐘 PostgreSQL
* 🐳 Docker e Docker Compose
* 🚦 Nginx
* 🔐 Certbot + Let's Encrypt
* 🖥️ Portainer (para gerenciamento de containers)

## ✨ Funcionalidades

* 🔐 Autenticação de usuários por grupo
* 📤 Upload de arquivos PDF com identificação de itens
* 📝 Registro de validações (por grupo e por usuário)
* 📊 Geração de relatórios:
  * 🧑‍🤝‍🧑 Validações por Grupo
  * 👤 Validações por Usuário
  * 🧾 Relatório em PDF
* ⚙️ Painel administrativo Django (/admin)

## 🚀 Instalação com Docker

### 1. Clone o repositório

```bash
git clone git@github.com:usuario/validador-itens.git
cd validador-itens
```

### 2. Crie o arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com as variáveis:

```ini
DB_NAME=validador
DB_USER=usuario
DB_PASSWORD=senha
```

### 3. Suba os containers

```bash
docker compose up --build -d
```

### 4. Migrações e superusuário

```bash
docker compose exec web bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 5. Gere os arquivos estáticos

```bash
python manage.py collectstatic --noinput
exit
```

### 6. Gere o certificado SSL (Let's Encrypt)

```bash
docker compose stop nginx
mkdir -p certbot/www

docker compose run --rm certbot
```

### 7. Suba novamente o Nginx com HTTPS

```bash
docker compose up -d
```

🌐 Acesse via HTTPS: [https://validacaoitens.com](https://validacaoitens.com)



## ✅ Boas práticas

* 📄 O arquivo `nginx/default.conf` está em `.gitignore` e não é versionado.
* 🛡️ Evite expor credenciais. Mantenha as variáveis de ambiente fora do Git.
* 📊 Utilize o Portainer para monitorar containers.

## 📄 Licença

Este projeto está sob a licença MIT.
