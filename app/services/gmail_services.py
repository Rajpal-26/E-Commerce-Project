import base64
import os
from googleapiclient.discovery import build

from app.models.email import Email
from app.models.email_attachments import Email_Attachment
from app import db


# Folder to store attachments
ATTACHMENT_FOLDER = "email_attachments_files"

# Create folder if not exists
os.makedirs(ATTACHMENT_FOLDER, exist_ok=True)


ALLOWED_SENDERS = [
    "unknownid101090@gmail.com"
]


def fetch_emails_service(credentials):

    service = build("gmail", "v1", credentials=credentials)

    results = service.users().messages().list(
        userId="me",
        maxResults=20
    ).execute()

    messages = results.get("messages", [])

    stored_emails = []

    for message in messages:

        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        payload = msg.get("payload", {})
        headers = payload.get("headers", [])

        sender = next(
            (h["value"] for h in headers if h["name"] == "From"),
            None
        )

        subject = next(
            (h["value"] for h in headers if h["name"] == "Subject"),
            None
        )

        body = ""

        # Skip if sender missing
        if sender is None:
            continue

        sender_email = sender.split("<")[-1].replace(">", "")

        # Allow only specific senders
        if sender_email not in ALLOWED_SENDERS:
            continue

        # Prevent duplicate emails
        existing_email = Email.query.filter_by(gmail_id=msg["id"]).first()
        if existing_email:
            continue

        # Recursive function to extract body and find all attachments
        attachments_list = []
        
        def traverse_payload(part):
            nonlocal body
            
            # Recursively search sub-parts
            if "parts" in part:
                for subpart in part["parts"]:
                    traverse_payload(subpart)
            
            # Extract data
            filename = part.get("filename")
            part_body = part.get("body", {})
            data = part_body.get("data")
            attachment_id = part_body.get("attachmentId")

            # Extract Body: prefer text/plain
            if part.get("mimeType") == "text/plain" and data and not filename:
                if not body:  # Only capture first text body found
                    try:
                        body = base64.urlsafe_b64decode(data).decode("utf-8")
                    except Exception:
                        pass
            
            # Extract Attachments
            if filename and attachment_id:
                attachments_list.append({
                    "filename": filename,
                    "attachmentId": attachment_id
                })

        # Start traversal
        traverse_payload(payload)
        
        # Fallback for simple emails (no parts)
        if not body and payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
             try:
                 body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
             except Exception:
                 pass

        email = Email(
            gmail_id=msg["id"],
            sender=sender_email,
            subject=subject,
            body=body
        )

        db.session.add(email)
        db.session.flush()

        # Handle attachments
        for att in attachments_list:
            filename = att["filename"]
            attachment_id = att["attachmentId"]
            
            # sanitize filename
            filename = filename.replace(" ", "_")

            try:
                attachment = service.users().messages().attachments().get(
                    userId="me",
                    messageId=msg["id"],
                    id=attachment_id
                ).execute()

                file_data = base64.urlsafe_b64decode(attachment["data"])

                filepath = os.path.join(
                    ATTACHMENT_FOLDER,
                    filename
                )

                with open(filepath, "wb") as f:
                    f.write(file_data)

                attachment_record = Email_Attachment(
                    email_id=email.id,
                    filename=filename,
                    filepath=filepath
                )

                db.session.add(attachment_record)
            except Exception as e:
                print(f"Error saving attachment {filename}: {e}")

        stored_emails.append({
            "sender": sender_email,
            "subject": subject
        })

    db.session.commit()

    return stored_emails