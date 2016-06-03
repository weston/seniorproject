from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import socket
from django.template import Context, Template

#Coinbase API
from coinbase.wallet.client import Client

#emails
import smtplib

RECV_HOST = "localhost"
RECV_PORT = 8050
SEND_HOST = "localhost"
SEND_PORT = 7140
SECONDARY_SEND_PORT = 7141
USERNAME    = 'chronobytesnoreply@gmail.com'
PASSWORD = 'seniorproject2016'

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
		SANDBOX_URL = 'https://api.sandbox.coinbase.com'
		client = Client(
    		"doxGjrubKnNJ4Y3p",
    		"Bmw4zqIHt3ntIFbRncDHhznfXWGHm24m",
    		base_api_uri=SANDBOX_URL
    	)
		account = client.get_accounts()[0]


		primary_account = client.get_primary_account()
		addr = account.create_address()
		newAddr = addr.address
		template = loader.get_template('submit_document/index.html')

		# Now we get the addr from the coinbase template
		# newAddr = ''
		# try:
		# 	newAddr = getNewWalletAddr()
		# except Exception as e:
		# 	newAddr ="Address not found. Is Bolt running?"

		ctx = {}	
		ctx['addr'] = newAddr
		context = Context(ctx)
		ctx["control"] = "GET"
		return HttpResponse(template.render(context))
	
	if request.method == 'POST':
		#We need use webhooks to check if the coinbase api wallet thingy does shit.

		template = loader.get_template('submit_document/index.html')
		to_email = request.POST['email']
		blockhash = sendHashToServer(request.POST['text'])
		ctx = {}
		ctx['blockhash'] = blockhash
		ctx['control'] = "POST"


		message_body = 'Your document was placed in the document with the hash: ' + blockhash + '\n\n'
		message_body+= 'You can see your block at this link: https://www.blocktrail.com/tBTC/tx/' + blockhash + '\n\n'

		##Verify that this email is okay
		##Then uncomment this
		to_email = 'chronobytesnoreply@gmail.com'
		##
		##

		fromaddr = 'chronobytesnoreply@gmail.com'
		toaddrs  = to_email
		msg = "\r\n".join([
			"From: chronobytesnoreply@gmail.com",
			"To: chronobytesnoreply@gmail.com",
			"Subject: Your Chronobyt.es Document Status",
			"",
			message_body
		])
		username = USERNAME
		password = PASSWORD
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login(username,password)
		server.sendmail(fromaddr, toaddrs, msg)
		server.quit()


		return HttpResponse(template.render(Context(ctx)))















