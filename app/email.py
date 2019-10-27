import base64, os
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document
# Settings
# Fill in these constants
#
# Obtain an OAuth access token from https://developers.docusign.com/oauth-token-generator
access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IjY4MTg1ZmYxLTRlNTEtNGNlOS1hZjFjLTY4OTgxMjIwMzMxNyJ9.eyJUb2tlblR5cGUiOjUsIklzc3VlSW5zdGFudCI6MTU3MjE0OTQ5NSwiZXhwIjoxNTcyMTc4Mjk1LCJVc2VySWQiOiJjYTAxNThiYy05MzExLTRmZjYtOWVlNC1hZjA4NzkyNzI4NjgiLCJzaXRlaWQiOjEsInNjcCI6WyJzaWduYXR1cmUiLCJjbGljay5tYW5hZ2UiLCJvcmdhbml6YXRpb25fcmVhZCIsImdyb3VwX3JlYWQiLCJwZXJtaXNzaW9uX3JlYWQiLCJ1c2VyX3JlYWQiLCJ1c2VyX3dyaXRlIiwiYWNjb3VudF9yZWFkIiwiZG9tYWluX3JlYWQiLCJpZGVudGl0eV9wcm92aWRlcl9yZWFkIiwiZHRyLnJvb21zLnJlYWQiLCJkdHIucm9vbXMud3JpdGUiLCJkdHIuZG9jdW1lbnRzLnJlYWQiLCJkdHIuZG9jdW1lbnRzLndyaXRlIiwiZHRyLnByb2ZpbGUucmVhZCIsImR0ci5wcm9maWxlLndyaXRlIiwiZHRyLmNvbXBhbnkucmVhZCIsImR0ci5jb21wYW55LndyaXRlIl0sImF1ZCI6ImYwZjI3ZjBlLTg1N2QtNGE3MS1hNGRhLTMyY2VjYWUzYTk3OCIsImlzcyI6Imh0dHBzOi8vYWNjb3VudC1kLmRvY3VzaWduLmNvbS8iLCJzdWIiOiJjYTAxNThiYy05MzExLTRmZjYtOWVlNC1hZjA4NzkyNzI4NjgiLCJhdXRoX3RpbWUiOjE1NzIxNDkyMTMsInB3aWQiOiI3OTFkZTA2MS02OTRmLTQxNGItOGQyZS1jYzAwZGYxZDIyOTgifQ.ipU-B6nUHRJTD2JXAKDQ5QmDPs7qw0oXORaz46hnXFoep1u2mKAoRfv1zadz1FbjWw3_ki__M8RJNlb0O2zGLonQvVkPDS7DOB56VHYQXUtUaJWUhW_sZpWNaO318I0PrG3Ql1GQ-OgPoj5Y01cjAGcNIMzWOE0jXEye120PIiQH3X0yp5icTghgHpVtdZ2akX02lyStuzlaqxRLmvoXV4cTemcd9gYyCx1cFK9DDA4PXS2N9QkN_JuEpV7YyD3tRvrZxxQtlGDYnRJhZrdLExrtlRcsT0oi1Lc2V5apt26mzgIkoAEYQlV-9Q3QcnGjkmFJ9VsWouG6RjVw7AfplQ"
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

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
          <meta charset="UTF-8">
        </head>
        <iframe source="https://example.com">
        <body style="font-family:sans-serif;margin-left:2em;">
        <h1 style="font-family: "Trebuchet MS", Helvetica, sans-serif;
            color: darkblue;margin-bottom: 0;">Summary of Contract</h1>
        <h4>Ordered by {signer_name}</h4>
        <p style="margin-top:0em; margin-bottom:0em;">Email: {signer_email}</p>
        {listOfSentences}
        <!-- Note the anchor tag for the signature field is in white. -->
        <h3 style="margin-top:3em;">Agreed: <span style="color:white;">**signature_1**/</span></h3>
        </body>
    </html>
  """


def send_document_for_signing(summary):

    """

    Sends the document <file_name> to be signed by <signer_name> via <signer_email>

    """



    # Create the component objects for the envelope definition...
    # with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
    # content_bytes = file.read()
    # base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    base64_file_content = base64.b64encode(bytes(create_document(summary), "utf-8")).decode("ascii")
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

send_document_for_signing()
