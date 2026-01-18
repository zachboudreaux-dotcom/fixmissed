import os
import base64
import urllib.parse
import urllib.request
from urllib.parse import parse_qs

def basic_auth_header(account_sid, auth_token):
    creds = f"{account_sid}:{auth_token}".encode("utf-8")
    b64 = base64.b64encode(creds).decode("utf-8")
    return f"Basic {b64}"

def twilio_post(url, auth_header, data):
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("Authorization", auth_header)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode("utf-8", errors="replace")

def lambda_handler(event, context):
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8", errors="replace")

    params = parse_qs(body)

    # For <Dial action=...>, Twilio sends DialCallStatus
    dial_status = ((params.get("DialCallStatus") or [""])[0] or "").strip().lower()

    caller = ((params.get("From") or [""])[0] or "").strip()
    print("DIAL STATUS:", dial_status, "CALLER:", caller)
    print("RAW PARAMS:", {k: v[0] for k, v in params.items() if v})

    # Only text back if call was NOT answered
    # Typical DialCallStatus values: completed, no-answer, busy, failed
    if dial_status not in ["no-answer", "busy", "failed"]:
        return {"statusCode": 200, "body": f"Ignored dial status: {dial_status}"}

    account_sid = os.environ["TWILIO_ACCOUNT_SID"]
    auth_token  = os.environ["TWILIO_AUTH_TOKEN"]
    from_twilio = os.environ["TWILIO_FROM_NUMBER"]
    message     = os.environ.get(
        "AUTOREPLY_MESSAGE",
        "Sorry we missed your call — text us here and we’ll get back to you ASAP."
    )

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    auth = basic_auth_header(account_sid, auth_token)

    result = twilio_post(url, auth, {
        "From": from_twilio,
        "To": caller,
        "Body": message
    })

    print("SMS RESULT:", result)
    return {"statusCode": 200, "body": "Auto-reply SMS sent"}
