from django import forms

class VirtualMachineForm(forms.Form):
    name = forms.CharField(max_length=100)
    memory = forms.IntegerField()
    vcpu = forms.IntegerField()




from .models import VirtualMachine

class VirtualMachineForm(forms.ModelForm):
    class Meta:
        model = VirtualMachine
        fields = ['name', 'memory', 'vcpu']