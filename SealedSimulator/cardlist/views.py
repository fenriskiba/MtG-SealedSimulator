from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from cardlist.models import Card, Set

def pack_select(request):
    card_list = Card.objects.order_by('card_name')
    template = loader.get_template('cardlist/index.html')
    context = RequestContext(request, {
        'card_list': card_list,
    })
    return HttpResponse(template.render(context))

def open_packs(request):
    return HttpResponse("This page will contain the cards from your open packs")

def print_selected_cards(request):
    return HttpResponse("This page will contain selected cards in an easy print format")
    
def import_set(request, set_name):
    return HttpResponse("Importing Set: %s." % set_name)
