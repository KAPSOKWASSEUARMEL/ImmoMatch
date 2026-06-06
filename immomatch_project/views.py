from django.shortcuts import render, get_object_or_404
from .models import House

def house_list(request):
    houses = House.objects.filter(is_available=True).order_by('-created_at')
    context = {'houses': houses}
    return render(request, 'listings/house_list.html', context)

def house_detail(request, pk):
    house = get_object_or_404(House, pk=pk, is_available=True)
    context = {'house': house}
    return render(request, 'listings/house_detail.html', context)
