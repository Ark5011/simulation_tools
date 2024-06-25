from django.shortcuts import render
from django.views import View
from .forms import TgForm

# Create your views here.
class Index(View):
    def get(self, request):
        form = TgForm()
        return render(request, 'calculator/index.html', {'form': form})

    def post(self, request):
        pass