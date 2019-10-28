import base64, os
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document
# Settings
# Fill in these constants
#
# Obtain an OAuth access token from https://developers.docusign.com/oauth-token-generator
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjY4MTg1ZmYxLTRlNTEtNGNlOS1hZjFjLTY4OTgxMjIwMzMxNyJ9.eyJUb2tlblR5cGUiOjUsIklzc3VlSW5zdGFudCI6MTU3MjE4NTcyMiwiZXhwIjoxNTcyMjE0NTIyLCJVc2VySWQiOiJjYTAxNThiYy05MzExLTRmZjYtOWVlNC1hZjA4NzkyNzI4NjgiLCJzaXRlaWQiOjEsInNjcCI6WyJzaWduYXR1cmUiLCJjbGljay5tYW5hZ2UiLCJvcmdhbml6YXRpb25fcmVhZCIsImdyb3VwX3JlYWQiLCJwZXJtaXNzaW9uX3JlYWQiLCJ1c2VyX3JlYWQiLCJ1c2VyX3dyaXRlIiwiYWNjb3VudF9yZWFkIiwiZG9tYWluX3JlYWQiLCJpZGVudGl0eV9wcm92aWRlcl9yZWFkIiwiZHRyLnJvb21zLnJlYWQiLCJkdHIucm9vbXMud3JpdGUiLCJkdHIuZG9jdW1lbnRzLnJlYWQiLCJkdHIuZG9jdW1lbnRzLndyaXRlIiwiZHRyLnByb2ZpbGUucmVhZCIsImR0ci5wcm9maWxlLndyaXRlIiwiZHRyLmNvbXBhbnkucmVhZCIsImR0ci5jb21wYW55LndyaXRlIl0sImF1ZCI6ImYwZjI3ZjBlLTg1N2QtNGE3MS1hNGRhLTMyY2VjYWUzYTk3OCIsImlzcyI6Imh0dHBzOi8vYWNjb3VudC1kLmRvY3VzaWduLmNvbS8iLCJzdWIiOiJjYTAxNThiYy05MzExLTRmZjYtOWVlNC1hZjA4NzkyNzI4NjgiLCJhbXIiOlsiaW50ZXJhY3RpdmUiXSwiYXV0aF90aW1lIjoxNTcyMTg1NzE5LCJwd2lkIjoiNzkxZGUwNjEtNjk0Zi00MTRiLThkMmUtY2MwMGRmMWQyMjk4In0.ClG0CPwfLWpoOSRj6vZeGx98G0HZCJ4oVk4gLGGX_F22fCCIDkJl2KM45pXbOpHUBdXBLyNA2CBQcPPkegLpQtveVPvzDhN6BwDuArVPN0deO3XR_zYw_co65gbfK6RtcVdrCcbw66izDBEC3Xla6c-SVVk72H_McbRB8UHM5wcoqaDbitYCw6ZqtLrsuWUZbmqdup-Yt-8bAd_Jfgo9Twc2bYDT1h-_YRGX-sT1UQ7VhIBE_L07kyL-Vc28leFnIll-CkSRpAE-xGdJU9J81Q91SgY_Mb5UnyVSyOHY0lbCPalUU96maQj_vkwf40P8V08OQFo51_TkQ6nhLqeaJQ"
# Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the
# upper right corner of the screen by your picture or the default picture. 
account_id = "6c3750d9-1488-4228-b14a-d642da87e222"
# Recipient Information:
signer_name = "Vineeth Voruganti"
signer_email = "vineeth.voruganti@gmail.com"
# The document you wish to send. Path is relative to the root directory of this repo.

file_name_path = 'tesla.pdf';

base_path = 'https://demo.docusign.net/restapi'

# Constants
APP_PATH = os.path.dirname(os.path.abspath(__file__))


def create_document(summary):
	""" Creates document 1 -- an html document"""
	listOfSentences = "<ol>"
	for i in range(len(summary)):
		listOfSentences += "<li>{}</li>".format(summary[i])
	listOfSentences += "</ol>"

	returnVal = """
	<!DOCTYPE html>
	<html>
		<head>
		  <meta charset="UTF-8">
		</head>
		<iframe source="https://example.com">
		<body style="font-family:sans-serif;margin-left:2em;">
		<h1 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
			color: darkblue;margin-bottom: 0;">Summary of Contract</h1>
		<h4>Ordered by {}</h4>
		<p style="margin-top:0em; margin-bottom:0em;">Email: {}</p>
		{}
		<!-- Note the anchor tag for the signature field is in white. -->
		<h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
		</body>
	</html>
	""".format(signer_name, signer_email, listOfSentences)
	print returnVal
	return returnVal


def send_document_for_signing(summary):

	"""

	Sends the document <file_name> to be signed by <signer_name> via <signer_email>

	"""



	# Create the component objects for the envelope definition...
	# with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
	# content_bytes = file.read()
	# base64_file_content = base64.b64encode(content_bytes).decode('ascii')

	base64_file_content = base64.b64encode(bytes(create_document(summary)).encode("utf-8")).decode("ascii")
	document = Document( # create the DocuSign document object 
		document_base64 = base64_file_content, 
		name = 'Example document', # can be different from actual file name
		file_extension = 'html', # many different document types are accepted
		document_id = 1 # a label used to reference the doc

	)




	# Create the signer recipient model 

	signer = Signer( # The signer

		email = signer_email, name = signer_name, recipient_id = "1", routing_order = "1")



	# Create a sign_here tab (field on the document)

	sign_here = SignHere(
		anchor_string = "**signature_1**", anchor_units = "pixels",
		anchor_y_offset = "10", anchor_x_offset = "20")

	# sign_here = SignHere( # DocuSign SignHere field/tab

	#     d = '1', page_number = '1', recipient_id = '1', tab_label = 'SignHereTab',

	#     x_position = '195', y_position = '147')



	# Add the tabs model (including the sign_here tab) to the signer

	signer.tabs = Tabs(sign_here_tabs = [sign_here]) # The Tabs object wants arrays of the different field/tab types




	# Next, create the top level envelope definition and populate it.

	envelope_definition = EnvelopeDefinition(

		email_subject = "Please sign this document sent from the Python SDK",

		documents = [document], # The order in the docs array determines the order in the envelope

		recipients = Recipients(signers = [signer]), # The Recipients object wants arrays for each recipient type

		status = "sent" # requests that the envelope be created and sent.

	)
	# Ready to go: send the envelope request

	api_client = ApiClient()

	api_client.host = base_path

	api_client.set_default_header("Authorization", "Bearer " + access_token)



	envelope_api = EnvelopesApi(api_client)

	results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)

	return results
