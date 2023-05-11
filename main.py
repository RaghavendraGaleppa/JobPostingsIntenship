import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



def send_email_with_file(sender, recipient, subject, file_path, smtp, attachment_path):
    # Read the message from the file
    with open(file_path, 'r') as f:
        message_text = f.read()

    # Create the message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    body = message_text
    message.attach(MIMEText(body, 'plain'))
    
    filename = os.path.basename(attachment_path)
    with open(attachment_path, 'rb') as f:
	    attachment = MIMEApplication(f.read(), _subtype='pdf')
	    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(attachment)

    # Send the message
    smtp.sendmail(sender, recipient, message.as_string())


def setup_smtp_server(username, password):
	smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	smtp_server.ehlo()
	smtp_server.login(username, password)
	return smtp_server


# Inquiry about Internship Opportunities at [Company Name]

def check_if_word_is_email(word:str):
	"""
		Given a word, check if it is a valid email or not.
	:param word: str
	:return: True if word is a valid email else False
	"""
	if re.match(r"[^@]+@[^@]+\.[^@]+", word):
		return True
	return False


def clean_email(email_string: str):
	"""
	If there are any special characters at the end of the word for example join18f@gsa.gov.,
	then remove the special characters.
	:param email_string: str
	:return: cleaned_email_string: str
	"""
	# Remove the special characters from the end of the email
	if email_string[-1] in ['.', ',']:
		email_string = email_string[:-1]
	email_string = email_string.strip()
	return email_string


def get_email_info(file_path):
	"""
		Given the file_path, read the last few lines and check 
		if there is any email given in the last few lines.
	:param file_path: 
	:return: email: str, if email is found in the last few lines else None
	"""
	email = None
	with open(file_path, 'r') as f:
		lines = f.readlines()
		for line in lines[-10:]:
			# Split the line into words
			words = line.split()
			for word in words:
				if check_if_word_is_email(word):
					email = word
					break
			if email:
				break
	return email


if __name__ == '__main__':
	# file_path = 'company-profiles/exmaple.md'
	# email = get_email_info(file_path)
	# email = clean_email(email)
	# if email:
	# 	print(f"Email found: {email}")
	# else:
	# 	print("No email found in the file.")
	smtp_obj = setup_smtp_server('Raghavendrar403@gmail.com', 
	                             'dcabkmchqkbtecjq')
	send_email_with_file(
		'Raghavendrar403@gmail.com', 
		'Raghavendrar404@gmail.com',
		"Nothing",
		"company-profiles/exmaple.md",
		smtp_obj
	)
