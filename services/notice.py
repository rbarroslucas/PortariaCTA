import base64
import os.path
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config.dependencies import get_admin

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    creds = None
    if os.path.exists('services/token.json'):
        creds = Credentials.from_authorized_user_file('services/token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/services/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('/services/token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    message = EmailMessage()
    message.set_content(message_text)
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {
        'raw': encoded_message
    }

def send_message(service, user_id, message):
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message Id: {sent_message['id']}")
        return sent_message
    except Exception as error:
        print(f"An error occurred: {error}")
        return None


class MailNotice():
    def __init__(self):
        self.service = gmail_authenticate()

    def update_admins(self, session):
        mails_dict = get_admin(session)
        self.adminsMail = []
        for key in mails_dict:
            admin = mails_dict[key]
            self.adminsMail.append(admin['email'])

    def data_to_message(self, data, type):
        if type == "uber":
            message = "Liberação de Uber"
        elif type == "delivery":
            message = "Liberação de Comida"
        else:
            message = "Foda-se"

        return message

    def send_notices(self, data, type):
        message_text = self.data_to_message(data, type)
        for admin_mail in self.adminsMail:
            message = create_message("portariadcta@gmail.com", admin_mail, "Nova Liberação", message_text)
            send_message(self.service, "me", message)

