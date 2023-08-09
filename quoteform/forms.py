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
            'email': _('(Optional) Customer Email ID'),
            'treesystem': _('Solar Tree System'),
            'capacity': _('Capacity (in kW)'),
            'panel': _('Solar Panel Make Selection'),
            'inverter': _('Inverter Make Selection'),
            'price': _('Price (in INR)'),
            'discount': _('Discount % (in numbers, leave blank if none)'),
            'additional': _('Additional Charges (in numbers, leave blank if none)'),
        }