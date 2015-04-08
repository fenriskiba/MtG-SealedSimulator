from django.contrib import admin
from django.conf.urls import patterns
from django.template import RequestContext, loader
from datetime import datetime
from time import mktime
from django.http import HttpResponse
from cardlist.models import Card, Set
import json
import urllib2
import time

class CardAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Card Info', {'fields': ['card_name', 'rarity', 'image_url']}),
        (None, {'fields': ['set_abbrev']}),
    ]
    list_display = ('card_name', 'set_abbrev')
    list_filter = ['set_abbrev']
    search_fields = ['card_name']
    
class SetAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Set Info', {'fields': ['set_name', 'set_abbrev', 'release_date']}),
    ]
    list_display = ('set_abbrev', 'set_name', 'release_date')
    list_filter = ['release_date']
    search_fields = ['set_abbrev', 'set_name']
    
def import_set(request, set_name):
    template = loader.get_template('cardlist/importset.html')
    set_data = getJsonData(set_name)
    addSetToDatabase(set_data)
    context = RequestContext(request, {
        'set_data': set_data,
    })
    return HttpResponse(template.render(context))

def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            (r'^importset/(?P<set_name>\w+)/$', admin.site.admin_view(import_set))
        )
        return my_urls + urls
    return get_urls

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

admin.site.register(Card, CardAdmin)
admin.site.register(Set, SetAdmin)
admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls
