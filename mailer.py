import resend

resend.api_key="re_QpBXG2Qe_Pu5foXSoNZHRM8wRPNpyAWFN"

def mail(to, subject, content):
    params = {
        "from": "Exun Clan <exun@exun.co>",
        "to": [to],
        "subject": subject,
        "html": content,
        "reply_to":"exun@dpsrkp.net"
    }
    resend.Emails.send(params)