
import imaplib
import ssl
import email
import webbrowser
import os

imap_server = 'imap.uns.ac.rs'
port = 993
user = input('User: ')
password = input('Pass: ')
context = ssl.create_default_context()

def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text)

with imaplib.IMAP4_SSL(imap_server, port, ssl_context=context) as server:
    server.login(user, password)

    server.select('INBOX', readonly=True)

    temp, msg = server.search(None, 'all')
    for num in msg[0].split():
        temp, msg = server.fetch(num, '(RFC822)')

        for response in msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])

                subject, encoding = email.header.decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)

                From, encoding = email.header.decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)

                print("Subject:", subject)
                print("From:", From)

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            print(body)
                        elif "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    content_type = msg.get_content_type()
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        print(body)

                if content_type == "text/html" and input("Do you want to view this message in your browser (Y/N)?: ") == "Y":
                    if not os.path.isdir("Web"):
                        os.mkdir("Web")
                    filename = str(len(os.listdir("Web"))) + "_index" + "(" + clean(subject) + ")" + ".html"
                    filepath = os.path.join("Web", filename)
                    open(filepath, "w").write(body)
                    webbrowser.open(filepath)
                print("="*100)