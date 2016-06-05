import smtplib
import json
import socket
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from models import User

USERNAME    = 'chronobytesnoreply@gmail.com'
PASSWORD = 'seniorproject2016'

MIN_PAYMENT = float(5 / 1000)


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

def sendEmailToUser(to_email, blockhash):
	message_body = 'Your document was placed in the document with the hash: ' + blockhash + '\n\n'
	message_body+= 'You can see your block at this link: https://www.blocktrail.com/tBTC/tx/' + blockhash + '\n\n'
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

@csrf_exempt
def coinbase_hook(request):
	payment_data = json.loads(request.body)
	btc_address = payment_data['data']['address']
	payment_amount = float(payment_data['additional_data']['amount']['amount'])

	user = User.objects.get(btc_address=btc_address)

	if not user:
		return HttpResponse()

	if payment_amount < MIN_PAYMENT:
		return HttpResponse()

	user.payment_received = True
	user.save()
	
	sendHashToServer(user.hash_value)

	return HttpResponse()
