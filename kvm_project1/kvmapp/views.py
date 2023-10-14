import libvirt
from django.shortcuts import render, get_object_or_404, redirect

from .forms import VirtualMachineForm
from .models import VirtualMachine


# Create your views here.



def home(request):
    return render(request, 'kvmapp/home.html')

def vm_list(request):
    conn = libvirt.open('qemu:///system')
    vm_list = []
    if conn is None:
        error_message = "Impossible de se connecter à l'hyperviseur KVM"
    else:
        for vm_id in conn.listDomainsID():
            vm = conn.lookupByID(vm_id)
            vm_info = {
                'id': vm_id,
                'name': vm.name(),
                'state': vm.state()[0],
                'memory': vm.info()[1],
                'vcpu': vm.info()[3],
            }
            vm_list.append(vm_info)
        conn.close()
        error_message = None
    context = {
        'vm_list': vm_list,
        'error_message': error_message
    }
    return render(request, 'kvmapp/vm_list.html', context)


def supprimer_vm(request, vm_id):
    # Récupérer l'objet VirtualMachine correspondant à l'ID fourni

    vm = VirtualMachine.objects.get(id=vm_id)

    if request.method == 'POST':
        # Vérifier si la machine virtuelle est active, si oui, l'arrêter d'abord
        if vm.state == 'running':
            vm.stop()

        # Supprimer la machine virtuelle
        vm.delete()

        return redirect('vm_list')  # Rediriger vers la liste des machines virtuelles après la suppression réussie

    context = {'vm': vm}
    return render(request, 'kvmapp/supprimer_vm.html', context)


def vm_detail(request, vm_id):
    vm = get_object_or_404(VirtualMachine, id=vm_id)
    context = {
        'vm': vm,
    }
    return render(request, 'kvmapp/vm_detail.html', context)

# def vm_start(request, vm_id):
#     vm = get_object_or_404(VirtualMachine, id=vm_id)
#     vm.start()
#     return redirect('vm_detail', vm_id=vm_id)
def vm_start(request, vm_id):
    vm = get_object_or_404(VirtualMachine, pk=vm_id)

    # Logic to start the virtual machine
    vm.start()  # Replace this with your own logic to start the virtual machine

    # Save the updated state of the virtual machine
    vm.state = 'running'
    vm.save()

    #return redirect('vm_detail', vm_id=vm_id)
    return render(request, 'vm_started.html', {'vm': vm})

# def vm_stop(request, vm_id):
#     # Récupère l'objet VirtualMachine correspondant à l'ID fourni
#     vm = get_object_or_404(VirtualMachine, id=vm_id)
#
#     # Arrête la machine virtuelle
#     vm.stop()
#
#     # Redirige l'utilisateur vers la page de détails de la machine virtuelle
#     return HttpResponseRedirect(reverse('vm_detail', args=(vm.id,)))

def vm_stop(request, vm_id):
    vm = get_object_or_404(VirtualMachine, id=vm_id)
    vm.stop()
    return redirect('vm_detail', vm_id=vm_id)








def vm_new(request):
    if request.method == 'POST':
        form = VirtualMachineForm(request.POST)
        if form.is_valid():
            vm = form.save(commit=False)
            # vm = VirtualMachine(name=form.cleaned_data['name'],
            #                     memory=form.cleaned_data['memory'],
            #                     vcpu=form.cleaned_data['vcpu'])
            vm.save()
            return redirect('vm_detail', vm_id=vm.id)
    else:
        form = VirtualMachineForm()
    context = {
        'form': form,
    }
    return render(request, 'kvmapp/vm_new.html', context)





def creer_vm(request):
    if request.method == 'POST':
        nom_vm = request.POST.get('nom_vm')
        memoire = request.POST.get('memoire')
        vcpu = 1
        os = request.POST.get('os')
        # Effectuer des validations sur les données entrées par l'utilisateur

        # Créer la nouvelle machine virtuelle

        conn = libvirt.open('qemu:///system')
        xml = '''<domain type='kvm'>
                    <name>{}</name>
                    <memory unit='KiB'>{}</memory>
                    <vcpu placement='static'>{}</vcpu>
                    <os>
                        <type arch='x86_64' machine='pc-i440fx-2.9'>hvm</type>
                        <boot dev='hd'/>
                    </os>
                </domain>'''.format(nom_vm, memoire, vcpu)
        dom = conn.createXML(xml, 0)
        conn.close()


        # Rediriger l'utilisateur vers la page de confirmation
        context = {
            'nom_vm': nom_vm,
            'memoire': memoire,
            'vcpu': vcpu,
            'os': os,
        }
        return render(request, 'kvmapp/confirmation.html', context=context)


    else:
        # Afficher la page de création de machine virtuelle
        return render(request, 'kvmapp/creer_vm.html')


def confirmation(request):
    return render(request, 'confirmation.html')