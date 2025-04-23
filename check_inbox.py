import imaplib
import email
from email.header import decode_header
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER
from send_email import send_email
from groq_bot import get_groq_reply
from conversation_db import get_conversation, update_conversation

def clean_header(text):
    return text.replace('\r', '').replace('\n', '').strip()

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset() or "utf-8"
                return part.get_payload(decode=True).decode(charset, errors="ignore")
    return msg.get_payload(decode=True).decode(errors="ignore")

def check_and_respond():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    mail.select("inbox")

    _, messages = mail.search(None, '(UNSEEN)')
    for num in messages[0].split():
        _, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        sender = email.utils.parseaddr(msg["From"])[1]
        subject = decode_header(msg["Subject"])[0][0]
        subject = subject.decode() if isinstance(subject, bytes) else subject
        subject = clean_header(subject)
        body = get_body(msg)

        print(f"\n📥 New message from {sender}")
        print(f"📌 Subject: {subject}")
        print(f"✉️ Body: {body[:100]}...")

        # 🧠 Get prior conversation
        messages = get_conversation(sender)
        if not messages:
            messages.append({"role": "system", "content": "You are a helpful assistant for Prismatic Technologies."})
        messages.append({"role": "user", "content": body})

        reply = get_groq_reply(messages)
        messages.append({"role": "assistant", "content": reply})

        update_conversation(sender, messages)
        send_email(sender, f"Re: {subject}", reply)

    mail.logout()
