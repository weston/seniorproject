from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import socket
from django.template import Context, Template
RECV_HOST = "localhost"
RECV_PORT = 8050
SEND_HOST = "localhost"
SEND_PORT = 7140

def getNewWalletAddr():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((RECV_HOST, RECV_PORT))
	data = sock.recv(1024)
	sock.close(); 
	return data 

def sendHashToServer(hash):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
	sock.connect((SEND_HOST,SEND_PORT))
	sock.sendall(hash)
	sock.close()

# Create your views here.
@csrf_exempt
def index(request):

	if request.method == 'GET':
		template = loader.get_template('submit_document/index.html')
		newAddr = getNewWalletAddr()
		ctx = {}	
		ctx['msg'] = "Please send bitcoin to this address: " + newAddr
		context = Context(ctx)
		return HttpResponse(template.render(context))
	if request.method == 'POST':
		template = loader.get_template('submit_document/index.html')
		sendHashToServer(request.POST['text'])
		ctx = {}
		ctx['msg'] = "Thank you for submitting your hash. "
		ctx['msg'] += "You will soon be able to see your document on the block chain."
		return HttpResponse(template.render(Context(ctx)))
