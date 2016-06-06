import smtplib
import json
import socket
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string, get_template
from django.template import Context, Template
from django.http import HttpResponse

from models import User

from coinbase.wallet import client

USERNAME    = 'chronobytesnoreply@gmail.com'
PASSWORD = 'seniorproject2016'

MIN_PAYMENT = float(5 / 1000)

RECV_HOST = "localhost"
RECV_PORT = 8050
SEND_HOST = "localhost"
SEND_PORT = 7140
SECONDARY_SEND_PORT = 7141

def sendHashToServer(hash_dat):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((SEND_HOST,SEND_PORT))
	sock.sendall(hash_dat)
	sock.close()
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect((SEND_HOST,SECONDARY_SEND_PORT))
	txn_hash = sock.recv(1024)
	sock.close()
	return txn_hash

def sendEmailToUser(to_email, txn_hash):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Your chronobyt.es submission"
	msg['From'] = USERNAME
	msg['To'] = to_email

	ctx = {
		'EMAIL': to_email,
		'HASH': txn_hash
	}

	text_message = "Text version"
	html_message = render_to_string('email_body.html', ctx)

	msg.attach(MIMEText(text_message, 'plain'))
	msg.attach(MIMEText(html_message, 'html'))

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(USERNAME,PASSWORD)
	server.sendmail(USERNAME, to_email, msg.as_string())
	server.quit()
	print "Email sent"

@csrf_exempt
def coinbase_hook(request):
	# valid_callback = client.verify_callback(request.body, request.META['CB-SIGNATURE'])
	# if not valid_callback:
	# 	return HttpResponse()

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
	
	txn_hash = sendHashToServer(user.hash_value)
	
	user.txn_hash = txn_hash
	user.save()

	sendEmailToUser(user.email, txn_hash)

	return HttpResponse()
