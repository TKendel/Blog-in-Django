from django.core.exceptions import ValidationError

def validate_small_length(value):
	if len(value)>100:
		raise ValidationError("The name is too big")
	return value

def validate_description(value):
	if len(value)>255:
		raise ValidationError("The description is too big")
	return value

def validate_number(value):
	counter = 0
	for i in range(len(value)):
		if value[i] < "0" or value[i] > "9":
			counter += 1
	if counter > 0:
		raise ValidationError("Please enter a valid phone number")
	return value