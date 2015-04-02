from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from cardlist.models import Card, Set
from datetime import datetime
from time import mktime
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
    addSetToDatabase(set_data)
    context = RequestContext(request, {
        'set_data': set_data,
    })
    return HttpResponse(template.render(context))

#Utility Function 
def getJsonData(set_name):
  json_string = urllib2.urlopen('http://mtgjson.com/json/' + set_name + '.json').read()
  data = json.loads(json_string)
  return data
  
def addSetToDatabase(set_data):
    newSet = Set()
    newSet.set_name = set_data['name']
    newSet.set_abbrev = set_data['code']
    newSet.release_date = datetime.fromtimestamp(mktime(time.strptime(set_data['releaseDate'], '%Y-%m-%d')))
    newSet.save()
    
    #Eliminate all duplicate DB Rows
    for row in Set.objects.all():
        if Set.objects.filter(set_name=row.set_name).count() > 1:
            row.delete()
    
    addCardsToDatabase(set_data)
    return

def addCardsToDatabase(set_data):
    for card in set_data['cards']:
        newCard = Card()
        newCard.card_name = card['name']
        newCard.rarity = card['rarity']
        newCard.image_url = "http://api.mtgdb.info/content/card_images/" + str(card['multiverseid']) + ".jpeg" 
        newCard.set_abbrev = set_data['code']
        newCard.save()
        
    #Eliminate all duplicate DB Rows
    for row in Card.objects.all():
        if Card.objects.filter(image_url=row.image_url).count() > 1:
            row.delete()
        
    return
