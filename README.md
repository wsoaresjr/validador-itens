# Validador de Itens

Sistema web desenvolvido em Django para gestão e validação de itens educacionais (questões) por diferentes grupos de usuários. Permite upload de arquivos em lote, registro de validações e geração de relatórios.

## ✨ Funcionalidades Principais

* Autenticação de usuários com diferentes perfis (administrador, validador)
* Upload em lote de arquivos PDF
* Interface de validação (aprovado / reprovado) com comentários
* Relatórios por grupo e por usuário
* Exportação de relatórios em PDF

## ⚖️ Tecnologias Utilizadas

* Python 3.11
* Django 5.2
* SQLite (padrão) ou PostgreSQL (recomendado para produção)
* Bootstrap 5.3 (interface)

## ✍️ Instalação Local

```bash
# Clone o repositório
$ git clone https://github.com/seu-usuario/validador-itens.git
$ cd validador-itens

# Crie e ative o ambiente virtual
$ python -m venv venv
$ source venv/bin/activate  # Linux/macOS
$ .\venv\Scripts\activate  # Windows

# Instale as dependências
(venv) $ pip install -r requirements.txt

# Aplique as migrações e inicie o servidor local
(venv) $ python manage.py migrate
(venv) $ python manage.py runserver
```

## ✉️ Credenciais de Teste (opcional)

Crie superusuário com:

```bash
(venv) $ python manage.py createsuperuser
```

## 🔧 Estrutura do Projeto

```
validador-itens/
├── core/               # App principal com views, templates, urls
├── static/             # Arquivos estáticos (CSS, JS, imagens)
├── templates/          # Templates HTML
├── media/              # Pasta para arquivos enviados (PDFs)
├── appvalidador/       # Configuração geral do Django
├── manage.py
└── requirements.txt
```

## 📚 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para detalhes.

---

