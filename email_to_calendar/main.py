import os
import ssl
import email
import imaplib
from dotenv import load_dotenv
from bs4 import BeautifulSoup
# from email.header import decode_header

load_dotenv()
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context = ssl.create_default_context()
context.set_ciphers('DEFAULT@SECLEVEL=1')
imap_server = os.getenv('SERVER', 'server')
username = os.getenv('EMAIL', 'email')
password = os.getenv('PASSWORD', 'password')
imap = imaplib.IMAP4_SSL(imap_server, ssl_context=context, port=993)

imap.login(username, password)

imap.select('INBOX')
status, response = imap.search(None, 'UNSEEN')
mail_ids = response[0].decode()
id_list = mail_ids.split()
for i in id_list:
    _, data = imap.fetch(str(i), '(RFC822)') 
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1].decode("utf-8"))
            email_subject = msg['subject']
            email_from = msg['from']
            if 'undangan' in email_subject.lower():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        content = part.get_payload()
                        soup = BeautifulSoup(content, 'html.parser')                       
                        print(soup.prettify())
    imap.store(i, '-FLAGS', '\\SEEN')
