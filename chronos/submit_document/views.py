from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import socket
from django.template import Context, Template
RECV_HOST = "localhost"
RECV_PORT = 8050
SEND_HOST = "localhost"
SEND_PORT = 7140
SECONDARY_SEND_PORT = 7141

def getNewWalletAddr():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((RECV_HOST, RECV_PORT))
	data = sock.recv(1024)
	sock.close(); 
	return data 

def sendHashToServer(hash_dat):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((SEND_HOST,SEND_PORT))
	sock.sendall(hash_dat)
	sock.close()
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((SEND_HOST,SECONDARY_SEND_PORT))
	blockHash = sock.recv(1024)
	sock.close()
	return blockHash



# Create your views here.
@csrf_exempt
def index(request):
	if request.method == 'GET':
		template = loader.get_template('submit_document/index.html')
		newAddr = ''
		try:
			newAddr = getNewWalletAddr()
		except Exception as e:
			newAddr ="Address not found. Is Bolt running?"
		ctx = {}	
		ctx['addr'] = newAddr
		context = Context(ctx)
		ctx["control"] = "GET"
		return HttpResponse(template.render(context))
	
	if request.method == 'POST':
		template = loader.get_template('submit_document/index.html')
		print request.POST['text']
		blockhash = sendHashToServer(request.POST['text'])
		ctx = {}
		ctx['blockhash'] = blockhash
		ctx['control'] = "POST"
		return HttpResponse(template.render(Context(ctx)))
