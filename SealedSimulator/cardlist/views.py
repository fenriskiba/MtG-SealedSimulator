from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from cardlist.models import Card, Set
import urllib2
import json
import time

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
    template = loader.get_template('cardlist/importset.html')
    set_data = getJsonData(set_name)
    context = RequestContext(request, {
        'set_data': set_data,
        'set_release': time.strptime(set_data['releaseDate'], '%Y-%m-%d')
    })
    return HttpResponse(template.render(context))

#Utility Function 
def getJsonData(set_name):
  json_string = urllib2.urlopen('http://mtgjson.com/json/' + set_name + '.json').read()
  data = json.loads(json_string)
  return data
