from django.conf.urls import patterns, url
from cardlist import views

urlpatterns = patterns('',
    url(r'^$', views.pack_select, name='pack select'),
    url(r'^openpacks/$', views.open_packs, name='open packs'),
    url(r'^printcards/$', views.print_selected_cards, name='print cards'),
    url(r'^importset/(?P<set_name>\w+)/$', views.import_set, name='import set'),
)
