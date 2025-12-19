import imaplib
import email
import re
import time
import os

def check_verification_code(email_user, email_pass, imap_url='imap.gmail.com'):
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_url)
        mail.login(email_user, email_pass)
        mail.select('inbox')

        # Search for emails from GitHub
        status, response = mail.search(None, '(FROM "noreply@github.com")')
        
        if status != 'OK':
            print("No messages found!")
            return None

        # Get the list of email IDs
        mail_ids = response[0].split()
        if not mail_ids:
            print("No emails from GitHub found.")
            return None

        # Get the latest email ID
        latest_email_id = mail_ids[-1]

        # Fetch the email content
        status, response = mail.fetch(latest_email_id, '(RFC822)')
        
        for response_part in response:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                body = ""
                
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                else:
                    body = msg.get_payload(decode=True).decode()

                # Search for a 6-digit code or specific GitHub verification pattern
                code_match = re.search(r'\b\d{6}\b', body)
                if code_match:
                    return code_match.group(0)

        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # These would ideally be environment variables
    # USER: Replace with your actual credentials or set env vars
    EMAIL_USER = os.getenv('VERIFY_EMAIL_USER', 'rc.regiscarvalho@gmail.com')
    EMAIL_PASS = os.getenv('VERIFY_EMAIL_PASS', '') # User needs to provide this or an App Password

    if not EMAIL_PASS:
        print("Please set VERIFY_EMAIL_PASS environment variable (App Password for Gmail).")
    else:
        print(f"Checking for verification code for {EMAIL_USER}...")
        code = check_verification_code(EMAIL_USER, EMAIL_PASS)
        if code:
            print(f"FOUND CODE: {code}")
        else:
            print("No code found in the latest email.")
