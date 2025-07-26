import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appvalidador.settings")
django.setup()

from django.contrib.auth.models import Group, User

# Grupos a serem criados
grupos = ['eureka', 'seeduc']

for nome in grupos:
    grupo, criado = Group.objects.get_or_create(name=nome)
    if criado:
        print(f'Grupo criado: {nome}')
    else:
        print(f'Grupo já existia: {nome}')

# Lista de usuários a criar
usuarios = [
    {'username': 'validador_eureka', 'senha': 'senha123', 'grupo': 'eureka'},
    {'username': 'validador_seeduc', 'senha': 'senha123', 'grupo': 'seeduc'},
]

for u in usuarios:
    if not User.objects.filter(username=u['username']).exists():
        user = User.objects.create_user(username=u['username'], password=u['senha'])
        grupo = Group.objects.get(name=u['grupo'])
        user.groups.add(grupo)
        print(f"Usuário '{u['username']}' criado e adicionado ao grupo '{u['grupo']}'")
    else:
        print(f"Usuário '{u['username']}' já existe")

