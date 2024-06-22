import resend
from secrets_parser import parse

resend.api_key = parse("variables.txt")["resend_key"]


def mail(to, subject, content):
    params = {
        "from": "Exun Clan <exun@exun.co>",
        "to": [to],
        "subject": subject,
        "html": content,
        "reply_to": "exun@dpsrkp.net",
    }
    resend.Emails.send(params)
