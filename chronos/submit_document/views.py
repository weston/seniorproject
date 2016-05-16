from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import socket
from django.template import Context, Template
HOST = "localhost"
PORT = 8050
 
def getNewWalletAddr():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	data = sock.recv(1024)
	sock.close(); 
	return data 

# Create your views here.
@csrf_exempt
def index(request):

	if request.method == 'GET':
		template = loader.get_template('submit_document/index.html')
		newAddr = getNewWalletAddr()
		ctx = {}	
		ctx['recvAddr'] = newAddr
		context = Context(ctx)
		return HttpResponse(template.render(context))
	if request.method == 'POST':
		template = loader.get_template('submit_document/index.html')
		text = request.POST['text']
		return HttpResponse(template.render(request, {'text':text}))
