from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone

# Create your models here.

class QuoteDetails(models.Model):
    MODULES = (
        ('Mono - 540W', 'Mono - 540W'),
        ('Mono - 545W', 'Mono - 545W'),
        ('Poly - 330W', 'Poly - 330W'),
        ('Poly - 335W', 'Poly - 335W'),
    )
    
    PANELS = (
        ('Rayzon', 'Rayzon'),
        ('Goldi', 'Goldi'),
        ('Waree', 'Waree'),
        ('Pahal', 'Pahal'),
    )

    INVERTERS = (
        ('KSolare', 'KSolare'),
        ('Solaryaan', 'Solaryaan'),
        ('Solis', 'Solis'),
        ('Polycab', 'Polycab'),
        ('Sofar', 'Sofar'),
        ('Sungrow', 'Sungrow'),
        ('GrowWATT', 'GrowWATT'),
    )

    name = models.CharField(max_length = 500, null = True)
    whatsapp = models.CharField(max_length = 15, null = True)
    capacity = models.IntegerField(null = True)
    module = models.TextField(max_length = 20, choices = MODULES, default = 'Choose Module...')
    panel = MultiSelectField(choices = PANELS, max_choices = 4, max_length = 100)
    inverter = MultiSelectField(choices = INVERTERS, max_choices = 7, max_length = 100)
    price = models.FloatField(null = True)
    revision = models.FloatField(null = True)
    created_date = models.DateTimeField(default = timezone.now, null = True)
    revision_date = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.name