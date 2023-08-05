from django.forms import ModelForm
from .models import QuoteDetails
from django.utils.translation import gettext_lazy as _

class QuoteForm(ModelForm):
    class Meta:
        model = QuoteDetails
        fields = '__all__'
        labels = {
            'name': _('Customer Name'),
            'whatsapp': _('Customer WhatsApp No.'),
            'location': _('Customer Location'),
            'email': _('Customer Email ID'),
            'capacity': _('Capacity (in kW)'),
            'panel': _('Solar Panel Make Selection'),
            'inverter': _('Inverter Make Selection'),
            'price': _('Price (in INR)'),
        }