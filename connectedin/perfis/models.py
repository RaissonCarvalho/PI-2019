from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=20, null= False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('Perfil')
    photo = models.ImageField(upload_to='profile_photo', blank=True, default='default_photo.png')

    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE, null=True)

    @property
    def email(self):
        return self.usuario.email


    def __str__(self):
        return self.nome


    def convidar(self, perfil_convidado):
        convite = Convite(solicitante=self, convidado=perfil_convidado)
        convite.save()


    def desfazer_amizade(self, perfil):
        self.contatos.remove(perfil)
        perfil.contatos.remove(self)


    def ja_eh_contato(self, perfil):
        return self.contatos.filter(id=perfil.id).exists()


    def tem_convite(self, perfil):
        return (Convite.objects.filter(solicitante=self, convidado=perfil).exists() or Convite.objects.filter(solicitante=perfil, convidado=self).exists())



    def foi_convidado(self, perfil):
        if Convite.objects.filter(solicitante=self, convidado=perfil).exists() or Convite.objects.filter(solicitante=perfil, convidado=self).exists():
            if Convite.objects.get(solicitante=perfil, convidado=self):
                return True
            else:
                return False
        else:
            return False



class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil,
                                    on_delete=models.CASCADE,
                                    related_name='convites_feitos' )
    convidado = models.ForeignKey(Perfil,
                                  on_delete= models.CASCADE,
                                  related_name='convites_recebidos')


    def aceitar(self):
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()


    def recusar(self):
        self.delete()
