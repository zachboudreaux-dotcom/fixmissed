import os
import base64
from urllib.parse import parse_qs

def lambda_handler(event, context):
    # Decode body (Twilio sends form-encoded; API Gateway may base64 it)
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8", errors="replace")

    params = parse_qs(body)
    caller = ((params.get("From") or [""])[0] or "").strip()

    owner = os.environ.get("OWNER_NUMBER", "").strip()

    # If owner isn't set, fall back to a friendly message
    if not owner:
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="alice">
    Thanks for calling. We are not available right now. Please text us and we will get back to you as soon as possible.
  </Say>
</Response>"""
        return {"statusCode": 200, "headers": {"Content-Type": "text/xml"}, "body": twiml}

    # This makes it "ring" the OWNER_NUMBER.
    # action=... is where Twilio will POST the dial result (answered/no-answer/busy/failed)
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial timeout="20" action="/twilio/status" method="POST">
    <Number>{owner}</Number>
  </Dial>
</Response>"""

    return {"statusCode": 200, "headers": {"Content-Type": "text/xml"}, "body": twiml}
