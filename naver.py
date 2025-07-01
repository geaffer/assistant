from imapclient import IMAPClient
import pyzmail
from datetime import datetime, timedelta

def fetch_recent_emails(email, app_password):
    HOST = 'imap.naver.com'
    MAILBOX = 'INBOX'
    search_date = (datetime.now() - timedelta(days=1)).strftime('%d-%b-%Y')
    email_list = []

    with IMAPClient(HOST) as client:
        client.login(email, app_password)
        client.select_folder(MAILBOX)
        messages = client.search(['SINCE', search_date])

        for uid in messages:
            raw_message = client.fetch([uid], ['BODY[]'])[uid][b'BODY[]']
            message = pyzmail.PyzMessage.factory(raw_message)

            subject = message.get_subject() or ''
            from_ = message.get_addresses('from')[0][1] or ''
            body = ''
            if message.text_part:
                body = message.text_part.get_payload().decode(message.text_part.charset, errors='ignore')
            elif message.html_part:
                body = message.html_part.get_payload().decode(message.html_part.charset, errors='ignore')

            if '[광고]' in subject:
                continue  # 광고는 제외

            is_priority = any(keyword in (subject + body + from_).lower() for keyword in ['투라', 'tura'])

            email_list.append({
                'subject': subject.strip(),
                'from': from_,
                'body': body.strip(),
                'priority': is_priority
            })

    email_list.sort(key=lambda x: x['priority'], reverse=True)
    return email_list
