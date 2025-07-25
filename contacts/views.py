from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST

from contacts.forms import ContactForm
from .models import Contact

@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {
        'contacts': contacts,
        'form': ContactForm()
    }
    return render(request, 'contacts.html', context)

@login_required
def search_contacts(request):
    query = request.GET.get('search', '')
    import time
    time.sleep(2)
    # filtering by name or email
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    )
    return render(request, 'partials/contact-list.html', {'contacts': contacts })

@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form = ContactForm(request.POST, request.FILES, initial={'user': request.user})
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save() 

        context = {'contact': contact}
        response = render(request, 'partials/contact-row.html', context)  
        response['HX-Trigger'] = 'contact-created'
        return response
    else: 
        response = render(request, 'partials/add-contact-modal.html', {'form': form})  
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        return response

@login_required
@require_POST 
def delete_contact(request, pk):
    if request.POST.get("_method") != "DELETE":
        return HttpResponseNotAllowed(['DELETE'])

    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.delete()

    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'contact-deleted'
    return response    