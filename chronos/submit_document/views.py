from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):

	if request.method == 'GET':
		template = loader.get_template('submit_document/index.html')
		return HttpResponse(template.render(request))
	if request.method == 'POST':
		template = loader.get_template('submit_document/index.html')
		text = request.POST['text']
		return HttpResponse(template.render(request, {'text':text}))
