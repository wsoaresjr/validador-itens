from django.db import models
from django.contrib.auth.models import User, Group  # <--- este aqui corrige o erro

class Item(models.Model):
    titulo = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdfs/')
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Itens'

class Validacao(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[
            ('validado', '✅ Validado'),
            ('nao_validado', '❌ Reprovado')
        ]
    )
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.item.titulo} - {self.status}'

    class Meta:
        verbose_name = 'Validação'
        verbose_name_plural = 'Validações'
