from django import forms
from .models import UserRoles, Languages

class UserRolesForm(forms.ModelForm):
    class Meta:
        model = UserRoles
        fields =  ['Name', 'Description', 'CreatedBy','CreatedDate','UpdatedBy','UpdatedDate','IsActive']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name:
                if field_name != 'IsActive':
                    field.widget.attrs.update({
                        'class': 'form-control text-white bg-dark',
                    })

            if field_name in ['CreatedBy', 'CreatedDate', 'UpdatedBy', 'UpdatedDate']:
                field.widget.attrs.update({
                    'disabled': True,
                    'class': 'form-control text-white bg-secondary',
                })


class LanguagesForm(forms.ModelForm):
    class Meta:
        model = Languages
        fields =  ['Name', 'CreatedBy','CreatedDate','UpdatedBy','UpdatedDate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name:
                if field_name != 'IsActive':
                    field.widget.attrs.update({
                        'class': 'form-control text-white bg-dark',
                    })

            if field_name in ['CreatedBy', 'CreatedDate', 'UpdatedBy', 'UpdatedDate']:
                field.widget.attrs.update({
                    'disabled': True,
                    'class': 'form-control text-white bg-secondary',
                })
