from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.db.models import Q
from cardlist.models import Card, Set
from datetime import datetime
from time import mktime
from random import randint
import urllib2
import json
import time
import random

def pack_select(request):
    pack1 = generatePack("KTK")
    pack2 = generatePack("KTK")
    pack3 = generatePack("KTK")
    pack4 = generatePack("FRF")
    pack5 = generatePack("FRF")
    pack6 = generatePack("FRF")
    template = loader.get_template('cardlist/index.html')
    context = RequestContext(request, {
        'pack1': pack1,
        'pack2': pack2,
        'pack3': pack3,
        'pack4': pack4,
        'pack5': pack5,
        'pack6': pack6,
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

#Utility Functions

def getJsonData(set_name):
  json_string = urllib2.urlopen('http://mtgjson.com/json/' + set_name + '.json').read()
  data = json.loads(json_string)
  return data
  
def addSetToDatabase(set_data):
    #Add new set
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
    #Add new cards
    for card in set_data['cards']:
        newCard = Card()
        newCard.card_name = card['name']
        newCard.rarity = card['rarity']
        newCard.image_url = "http://api.mtgdb.info/content/card_images/" + str(card['multiverseid']) + ".jpeg" 
        newCard.set_abbrev = set_data['code']
        newCard.save()
        
    #Eliminate all duplicate DB Rows and all Basic Lands
    for row in Card.objects.all():
        if Card.objects.filter(image_url=row.image_url).count() > 1:
            row.delete()
        elif row.card_name == "Plains":
            row.delete()
        elif row.card_name == "Island":
            row.delete()
        elif row.card_name == "Swamp":
            row.delete()
        elif row.card_name == "Mountain":
            row.delete()
        elif row.card_name == "Forest":
            row.delete()
    return
    
def generatePack(given_set_name):
    givenSet = Card.objects.filter(set_abbrev=given_set_name)
    mythics = givenSet.filter(rarity="Mythic Rare")
    rares = givenSet.filter(rarity="Rare")
    uncommons = givenSet.filter(rarity="Uncommon")
    commons = givenSet.filter(rarity="Common")
    pack = []
    
    isMythic = (randint(0, 5) == 0)
    
    #Generate Rare
    if(isMythic):
        pack.append(random.choice(mythics))
    else:
        pack.append(random.choice(rares))
    
    #Generate Uncommons
    for i in range(0,3):
        newCard = random.choice(uncommons)
        while newCard in pack:
            newCard = random.choice(uncommons)
        pack.append(newCard)
    
    #Generate Commons
    for i in range(0,10):
        newCard = random.choice(commons)
        while newCard in pack:
            newCard = random.choice(commons)
        pack.append(newCard)
    
    return pack

