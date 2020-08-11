from django.contrib import admin
from cycle_mails.models import Reunion, Recipient, Content, Crontab
from django import forms
from django.utils.translation import gettext as _
from django.contrib.admin.widgets import FilteredSelectMultiple


class RecipientForm(forms.ModelForm):
    recipient = forms.ModelMultipleChoiceField(
        queryset=Recipient.objects.all(),
        widget=FilteredSelectMultiple(_("Emails"), is_stacked=False)
    )

    class Meta:
        model = Reunion
        fields = ('name', 'emails')

class ContentInline(admin.StackedInline):
    model = Content
    max_num = 1

class CrontabInline(admin.TabularInline):
    model = Crontab

# Define the admin class
class ReunionAdmin(admin.ModelAdmin):
    # form = RecipientForm
    fields = ('name', 'emails')
    filter_horizontal = ('emails',) 
    inlines = [
        ContentInline,
        CrontabInline,
    ]

# Register your models here.
admin.site.register(Reunion, ReunionAdmin)
admin.site.register(Recipient)
