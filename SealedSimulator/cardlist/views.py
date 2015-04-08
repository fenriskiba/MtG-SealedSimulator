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

#Utility Functions
    
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

