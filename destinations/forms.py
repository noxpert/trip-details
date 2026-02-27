from django import forms

from .models import Trip


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'name': 'Trip Name',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # After validation, add is-invalid to any field that has errors.
        if self.is_bound:
            for field_name, field in self.fields.items():
                if self.errors.get(field_name):
                    existing = field.widget.attrs.get('class', '')
                    field.widget.attrs['class'] = f'{existing} is-invalid'.strip()


