from flask import redirect, request, jsonify, session
from app.gmail_oauth import flow
from app.services.gmail_services import fetch_emails_service



def gmail_login_controller():
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )
    
    session["state"] = state
    print("login controller")

    return redirect(auth_url)


def gmail_callback_controller():
    
    if session.get("state") != request.args.get("state"):
        return jsonify({"error": "Invalid OAuth state"}), 400
    
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials

    emails = fetch_emails_service(credentials)
    print("callback controller")

    return jsonify({
        "message": "Emails fetched successfully",
        "emails": emails
    })
