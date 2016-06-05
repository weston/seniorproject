import smtplib

USERNAME    = 'chronobytesnoreply@gmail.com'
PASSWORD = 'seniorproject2016'

def sendEmailToUser(to_email, blockhash):
	message_body = 'Your document was placed in the document with the hash: ' + blockhash + '\n\n'
	message_body+= 'You can see your block at this link: https://www.blocktrail.com/tBTC/tx/' + blockhash + '\n\n'

	to_email = 'chronobytesnoreply@gmail.com'

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