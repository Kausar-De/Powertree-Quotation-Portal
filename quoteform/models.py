from django.db import models
from multiselectfield import MultiSelectField
from django.utils import timezone

# Create your models here.

class QuoteDetails(models.Model):
    TREESYSTEMS = (
        ('Solar Rooftop System', 'Solar Rooftop System'),
        ('Solar Gazebo System', 'Solar Gazebo System'),
        ('Solar Hybrid System', 'Solar Hybrid System'),
    )

    MODULES = (
        ('Mono Bifacial - 330/335/340W', 'Mono Bifacial - 330/335/340W'),
        ('Mono Perc - 535/540/545W', 'Mono Perc - 535/540/545W'),
        ('Poly Crystalline - 535/540/545W', 'Poly Crystalline - 535/540/545W'),
    )
    
    PANELS = (
        ('Rayzon', 'Rayzon'),
        ('Adani', 'Adani'),
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
    location = models.CharField(max_length = 100, null = True)
    email = models.CharField(max_length = 100, null = True, blank = True)
    treesystem = models.TextField(max_length = 50, choices = TREESYSTEMS, default = 'Choose Tree System...')
    capacity = models.FloatField(null = True)
    module = models.TextField(max_length = 50, choices = MODULES, default = 'Choose Module...')
    panel = MultiSelectField(choices = PANELS, max_choices = 4, max_length = 100)
    inverter = MultiSelectField(choices = INVERTERS, max_choices = 7, max_length = 100)
    price = models.FloatField(null = True)
    discount = models.IntegerField(default = 0, null = True, blank = True)
    additional = models.FloatField(default = 0, null = True, blank = True)
    revision = models.FloatField(null = True)
    created_date = models.DateTimeField(default = timezone.now, null = True)
    revision_date = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.name