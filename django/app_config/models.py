from django.db import models

class BaseModel(models.Model):
    ativo = models.BooleanField("Ativo",default=True)
    data_criacao = models.DateField('Data de criação', auto_now_add=True)
    data_modificacao = models.DateField("Data de modificação", auto_now=True)

    class Meta:
        abstract=True
