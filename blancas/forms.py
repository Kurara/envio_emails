from django import forms
from blancas import models
import logging

logger = logging.getLogger(__name__)


class SearchForm(forms.Form):
    province = forms.ModelChoiceField(
        queryset=models.Province.objects.all().order_by('name'),
        label="Provincia",
        widget = forms.Select(
            choices=models.Province.objects.all().values_list('id', 'name'),
            attrs={}
        ),
        to_field_name='name'
        
    )
    city = forms.CharField(label="Localidad")
    letter_start = forms.CharField(label="Letras iniciales")
    letter_end = forms.CharField(label="Letras finales", required=False)

    def get_names(self):
        print("searching names...")
        start = self.cleaned_data.get('letter_start').upper()
        end = self.cleaned_data.get('letter_end')

        items = models.Surname.objects.filter(surname__gte=start)
        if end:
            items = items.filter(surname__lte=end.upper())
        else:
            next_letter = chr(ord(start[0]) + 1)
            items = items.filter(surname__lt=next_letter)

        logger.info("found {} surnames".format(items.count()))
        return items

