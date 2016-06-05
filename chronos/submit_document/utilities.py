import smtplib
import json
import socket
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string, get_template
from django.template import Context, Template
from django.http import HttpResponse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

def sendEmailToUser(to_email, txn_hash):
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Link"
	msg['From'] = USERNAME
	msg['To'] = to_email
	# ctx = {
	# 	'HASH_PLACEHOLDER': txn_hash,
	# 	'EMAIL_PLACEHOLDER': to_email
	# }

	#html_message = get_template('static/email_body.html').render(Context(ctx))
	text_message = "Text version"
	html_message = render_to_string('email_body.html', {})
	html_message = html_message.replace("HASH_PLACEHOLDER",txn_hash)
	html_message = html_message.replace("EMAIL_PLACEHOLDER",to_email)

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
