# Validador de Itens \U0001F4DD\U0001F50D

Sistema web desenvolvido em Django para gestão e validação de itens educacionais (questões) por diferentes grupos de usuários. Permite upload de arquivos em lote, registro de validações e geração de relatórios.

## ✨ Funcionalidades Principais

* \U0001F464 Autenticação de usuários com diferentes perfis (administrador, validador)
* \U0001F4C2 Upload em lote de arquivos PDF
* \U0001F4DD Interface de validação (aprovado / reprovado) com comentários
* \U0001F4C8 Relatórios por grupo e por usuário
* \U0001F4C4 Exportação de relatórios em PDF

## ⚖️ Tecnologias Utilizadas

* \U0001F40D Python 3.11
* \U0001F4DA Django 5.2
* \U0001F4BE SQLite (padrão) ou PostgreSQL (recomendado para produção)
* \U0001F4C3 Bootstrap 5.3 (interface)

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

\U0001F4BB Desenvolvido por [Exploratória Digital](https://exploratoriadigital.com.br) ✨
