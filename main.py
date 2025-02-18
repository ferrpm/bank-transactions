import imaplib
import email

EMAIL_USER = "xxx@gmail.com"
EMAIL_PASS = "password"
IMAP_SERVER = "imap.gmail.com"


mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_USER, EMAIL_PASS)
mail.select("inbox")

result, data = mail.search(None, 'FROM "notificacion@notificacionesbaccr.com"')

for num in data[0].split():
    result, msg_data = mail.fetch(num, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)
    print(msg)
    email_body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                email_body = part.get_payload(decode=True).decode()
    else:
        email_body = msg.get_payload(decode=True).decode()
    print(email_body)

mail.logout()
