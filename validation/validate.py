from fastapi import HTTPException
import re
import random
import string

def return_data(data: str, ip: str,timestamp:int,otp:int,exp_time:int) -> dict:
	
	userData = {
		"fname": "",
		"lname": "",
		"email": "",
		"ph_number": "",
		"username": "",
		"password": "",
		"old_password":None,
		"ip": {
      		"ip_signup":{
            	"timestamp": timestamp,
            	"ip":ip
             },
			"ip_login": {
				"timestamp": [],
				"ip":[]
       		},
   			"ip_update": {
				"timestamp":[],
				"ip":[]
			}
   		},
		"is_verified" : "false",
		"otp_verification":{
			"otp": otp,
			"expiration_time" : exp_time
		}

	}

	userData["fname"] = (data.first_name).lower()
	userData["lname"] = (data.last_name).lower()
	userData["email"] = data.email
	userData["ph_number"] = data.phone_number.split()
	userData["username"] = data.username
	userData["password"] = data.password

	return userData


def validate_data(data):
	missing = []

	if not data.first_name:
		missing.append("first_name")
	if not data.last_name:
		missing.append("last_name")
	if not data.email:
		missing.append("email")
	if not data.phone_number:
		missing.append("phone_number")

	# Phone Number Analysis
	phone_number = data.phone_number.split()
	if len(phone_number[1]) != 10:
		missing.append("invalid phone number")
	if len(phone_number[0]) > 3:
		missing.append("invalid country code")

	if any(char.isalpha() for char in data.phone_number):
		missing.append(
			"invalid phone number : phone number does not any contain alphabet")

	# Password Analysis
	if len(data.password) < 8:
		missing.append("password too short")
	if not is_valid_email(data.email):
		missing.append("invalid email")

	# User Name Analysis
	if any(char for char in data.username if (char in '[@_!#$%^&*()<>?/\|}{~:]')):
		missing.append("invalid username")

	#  Name Analysis
	if any((char.isdigit() or not char.isalpha()) for char in data.first_name):
		missing.append(
			"invalid firstname : firstname does not any contain numeric data or special character")

	if any((char.isdigit() or not char.isalpha()) for char in data.last_name):
		missing.append(
			"invalid lastname : lastname does not any contain numeric data or special character")

	# O/P Error
	if missing:
		detail = f"Required fields are missing or blank or error: {', '.join(missing)}"
		raise HTTPException(status_code=422, detail=detail)

	# Your processing logic here
	return {"message": "User created successfully"}


def is_valid_email(email):
	pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
	if re.match(pattern, email):
		return True
	else:
		return False


