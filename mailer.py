from secrets_parser import parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, ssl

password=parse("variables.txt")["password"]

def mail(to, subject, content):
    message=MIMEMultipart("alternative")
    message["Subject"]=subject
    message["From"]="Exun Clan <exun@dpsrkp.net>"
    message["to"]=to
    
    text = content
    message.attach(MIMEText(text, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("exun@dpsrkp.net", password)
        server.sendmail(
            "exun@dpsrkp.net", to, message.as_string()
    )