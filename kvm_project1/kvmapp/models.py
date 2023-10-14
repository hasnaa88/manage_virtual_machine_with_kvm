from django.db import models

from django.urls import reverse


def get_absolute_url():
    return reverse('vm_list')


class VirtualMachine(models.Model):
    # Champ 'state' pour représenter l'état de la machine virtuelle, avec une valeur par défaut de 0
    state = models.IntegerField(default=0)

    # Définition du gestionnaire d'objets par défaut 'objects'
    objects = models.Manager()

    name = models.CharField(max_length=200)
    # ip_address = models.CharField(max_length=200,default='0.0.0.0')
    # port = models.IntegerField()
    state = models.IntegerField(default=0)
    is_running = models.BooleanField(default=False)
    memory = models.IntegerField()
    vcpu = models.IntegerField()

    def __str__(self):
        return self.name

    def start(self):
        # Code pour démarrer la machine virtuelle ici
        self.is_running = True
        self.save()

    def stop(self):
        # Code pour arrêter la machine virtuelle ici
        self.is_running = False
        self.save()
