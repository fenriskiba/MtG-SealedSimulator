from django.shortcuts import render
from django.http import HttpResponse

def pack_select(request):
    return HttpResponse("Hello World. Welcome to The MtG Sealed Simulator.")

def open_packs(request):
    return HttpResponse("This page will contain the cards from your open packs")

def print_selected_cards(request):
    return HttpResponse("This page will contain selected cards in an easy print format")
