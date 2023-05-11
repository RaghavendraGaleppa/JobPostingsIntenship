import json
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
import re





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


def send_email_with_file(sender, company_profile_path: str, attachment_path, smtp):
	email = get_email_info(company_profile_path)
	if email is None:
		print(f"Skipping for {company_profile_path} as no email found.")
		return False
	
	email = clean_email(email)
	
	recipient = email
	
	message_text = ""
	with open("email_application.txt", 'r') as f:
		message_text = f.read()
		
	company_name = os.path.basename(company_profile_path).split('.')[0]
	my_name = "Raghavendra"
	subject = f"Inquiry about Internship Opportunities at {company_name}"
	# Company name will be of the format company-name, Make it Company Name
	company_name = company_name.replace('-', ' ').title()
	message_text = message_text.format(name=my_name, company_name=company_name)
	
		
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
	return email


def setup_smtp_server(username, password):
	smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	smtp_server.ehlo()
	smtp_server.login(username, password)
	return smtp_server

def get_all_files(path):
	# Get the absolute path to all files in the directory
	files = [os.path.join(path, file) for file in os.listdir(path)]
	return files


def send_mails_to_files(path_to_company_profiles):
	
	all_company_profiles = get_all_files(path_to_company_profiles)
	log_data = {}
	# Check if a file called log_data.json exists if yes then load the data from it
	if os.path.exists('log_data.json'):
		with open('log_data.json', 'r') as f:
			log_data = json.load(f)
	
	smtp_obj = setup_smtp_server('Raghavendrar403@gmail.com',
	                             'dcabkmchqkbtecjq')
	
	dict_countries = read_company_profiles_list()
	for company_profile in all_company_profiles:
		# Check if the company_profile is already processed or not
		# Get the name of the file
		company_name = os.path.basename(company_profile).split('.')[0]
		if company_name in log_data:
			print(f"Skipping {company_profile} as already processed.")
			continue
			
		if dict_countries.get(company_name) != "USA":
			print(f"Skipping {company_profile} as not from USA.")
			continue
	
		res = send_email_with_file(
			'Raghavendrar403@gmail.com',
			company_profile,
			"Resume.pdf",
			smtp_obj
		)
		if res is True:
			print(f"Email sent to {company_name}, at {res}")
			log_data[company_name] = res
		else:
			print(f"Email not sent to {company_name}")
		# Save the log_data
		with open('log_data.json', 'w') as f:
			json.dump(log_data, f)
	# Close the smtp server
	smtp_obj.close()
	

def read_company_profiles_list():
	text = ""
	with open('company-profiles.md', 'r') as f:
		text = f.read()
		
	# Split by lines
	lines = text.split('\n')
	dict_for_countries = {}
	for line in lines:
		try:
			# use regular expressions to extract the information
			name = re.search(r"\[(.*?)\]", line).group(1)
			website = re.search(r"\((.*?)\)", line).group(1)
			region = line.split("|")[-1].strip()
			
			website = website.split('/')[-1].split('.')[0]
			dict_for_countries[website] = region
		except:
			continue
		
	return dict_for_countries


if __name__ == '__main__':
	# read_company_profiles_list()
	send_mails_to_files("company-profiles")