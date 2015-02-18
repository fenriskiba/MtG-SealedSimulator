from django.contrib import admin
from cardlist.models import Card, Set

class CardAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Card Info', {'fields': ['card_name', 'image_url']}),
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

admin.site.register(Card, CardAdmin)
admin.site.register(Set, SetAdmin)
