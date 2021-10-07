
import smtplib, ssl

smtp_server = 'smtp.uns.ac.rs'
port = 587
email = input('Email: ')
password = input('Pass: ')
context = ssl.create_default_context()

with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context=context)
    server.login(email, password)
    print('It worked!')