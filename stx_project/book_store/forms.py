from datetime import date, datetime
from django import forms
from django.forms import widgets
from .models import Book


class DateSelectorWidget(widgets.MultiWidget):
    def __init__(self, attrs=None):
        days = [(d, d) for d in range(1, 32)]
        months = [(m, m) for m in range(1, 13)]
        years = [(year, year)
                 for year in range(datetime.now().year + 1, 1000, -1)]
        _widgets = (
            widgets.Select(attrs=attrs, choices=years),
            widgets.Select(attrs=attrs, choices=months),
            widgets.Select(attrs=attrs, choices=days),
        )
        super(DateSelectorWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.year, value.month, value.day]
        return [None, None, None]

    def format_output(self, rendered_widgets):
        return ''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        datelist = [
            widget.value_from_datadict(data, files, name + '_%s' % i)
            for i, widget in enumerate(self.widgets)]
        D = date(
            year=int(datelist[0]),
            month=int(datelist[1]),
            day=int(datelist[2]),
        )
        return D


class BookCreateForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = [
            'created_date',
            'publish_date_type',
            'author'
        ]

        fields = [
            'title',
            'publish_date',
            'page_count',
            'thumbnail_url',
            'language',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text'
            }),
            'publish_date': DateSelectorWidget(attrs={
                'name': 'publish_dateee'
            }),
            'page_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'type': 'number'
            }),
            'language': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'en',
                'max_length': 2
            }),
            'thumbnail_url': forms.URLInput(attrs={
                'class': 'form-control',
                'type': 'url',
                'placeholder': 'https://example.com',
                'max_length': 255,
                'required': False
            }),
        }
