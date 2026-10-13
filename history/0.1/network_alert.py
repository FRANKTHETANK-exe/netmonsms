import smtplib
from email.mime.text import MIMEText

def send_sms_via_email(phone_number, message, carrier_gateway):
	sender = 'REPLACE_WITH_SMTP_SENDER'
	password = 'REPLACE_WITH_SMTP_APP_PASSWORD'
	
	sms_gateway = f"{phone_number}@{carrier_gateway}"
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(sender, password)
	
	msg = MIMEText(message)
	server.sendmail(sender, sms_gateway, msg.as_string())
	server.quit()
	
send_sms_via_email('REPLACE_WITH_PHONE_NUMBER',"New device connected","tmomail.net")
