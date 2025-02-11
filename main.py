# Copyright (C) 2025 FakerPK
# Licensed under the AGPL-3.0: https://www.gnu.org/licenses/agpl-3.0.html
# This software is provided "as-is" without any warranties.

import os
import sys
import json
import asyncio
import aiohttp
import requests
from colorama import Fore, Style, init
from datetime import datetime, timedelta
import random
import readline
import keyboard
from urllib.parse import urlparse
from requests.exceptions import ProxyError, ConnectionError

init(autoreset=True)

class AccountManager:
    def __init__(self):
        self.accounts = []
        self.proxies = []
        self.use_proxy = False
        self.enable_auto_retry = False
        self.current_account_index = 0
        self.connections = {}
        self.potential_points = []
        self.countdowns = []
        self.points_totals = []
        self.points_today = []
        self.last_updated = []
        self.messages = []
        self.user_ids = []
        self.browser_ids = []
        self.access_tokens = []

    def load_accounts(self):
        try:
            with open('account.txt', 'r') as f:
                self.accounts = [line.strip().split(',')[:2] for line in f if line.strip()]
        except FileNotFoundError:
            self.print_error("account.txt not found!")
            sys.exit(1)

    def save_accounts(self):
        """Save accounts to account.txt."""
        with open('account.txt', 'w') as f:
            for email, password in self.accounts:
                f.write(f"{email},{password}\n")
        self.print_success("Accounts saved to account.txt")

    def add_accounts_interactively(self):
        """Add accounts interactively via user input."""
        self.print_banner()
        print(f"{Fore.CYAN + Style.BRIGHT}Interactive Account Setup{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Enter account details below. Type 'done' when finished.{Style.RESET_ALL}")

        while True:
            email = input(f"{Fore.GREEN}Enter email for account {len(self.accounts) + 1} (or 'done' to finish): {Style.RESET_ALL}")
            if email.lower() == 'done':
                break
            password = input(f"{Fore.GREEN}Enter password for account {len(self.accounts) + 1}: {Style.RESET_ALL}")
            self.accounts.append((email, password))
            self.print_success(f"Account {len(self.accounts)} added: {email}")

        self.save_accounts()

    def load_proxies(self):
        try:
            with open('proxy.txt', 'r') as f:
                self.proxies = [self.normalize_proxy(line.strip()) for line in f if line.strip()]
        except FileNotFoundError:
            self.print_error("proxy.txt not found!")
            sys.exit(1)

    def save_proxies(self):
        """Save proxies to proxy.txt."""
        with open('proxy.txt', 'w') as f:
            for proxy in self.proxies:
                f.write(f"{proxy}\n")
        self.print_success("Proxies saved to proxy.txt")

    def normalize_proxy(self, proxy):
        if not proxy.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
            return f'http://{proxy}'
        return proxy

    def validate_proxy(self, proxy):
        """Validate if a proxy is functional."""
        test_url = "http://httpbin.org/ip"
        try:
            response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                return True
        except (ProxyError, ConnectionError, Exception):
            pass
        return False

    def remove_bad_proxies(self):
        """Remove non-functional proxies from the proxy list and save the updated list."""
        self.print_banner()
        print(f"{Fore.YELLOW}Checking and removing bad proxies...{Style.RESET_ALL}")
        original_count = len(self.proxies)
        self.proxies = [proxy for proxy in self.proxies if self.validate_proxy(proxy)]
        removed_count = original_count - len(self.proxies)
        if removed_count > 0:
            self.print_warning(f"Removed {removed_count} bad proxies.")
        else:
            self.print_success("All proxies are functional.")
        self.save_proxies()

    def print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        banner = f"""{Fore.YELLOW + Style.BRIGHT}
        ███████╗ █████╗ ██╗  ██╗███████╗██████╗  ██████╗ ██╗  ██╗ 
        ██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗ ██╔══██╗██║ ██╔╝ 
        █████╗  ███████║█████╔╝ █████╗  ██████╔╝ ██████╔╝█████╔╝  
        ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗ ██╔═══╝ ██╔═██╗  
        ██║     ██║  ██║██║  ██╗███████╗██║  ██║ ██║     ██║  ██╗     
        ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═╝     ╚═╝  ╚═╝     
        {Style.RESET_ALL}
        {Fore.LIGHTBLUE_EX + Style.BRIGHT}🚀 TENEO BOT | AUTOMATE AND DOMINATE {Style.RESET_ALL}
        """
        print(banner)
        print(f"{Fore.RED}═══════════════════════════════════════════════════════════════════════════{Style.RESET_ALL}")

    def print_error(self, message):
        print(f"{Fore.RED}❌ {Style.BRIGHT}{message}{Style.RESET_ALL}")

    def print_success(self, message):
        print(f"{Fore.GREEN}✅ {Style.BRIGHT}{message}{Style.RESET_ALL}")

    def print_warning(self, message):
        print(f"{Fore.YELLOW}⚠️ {Style.BRIGHT}{message}{Style.RESET_ALL}")

    def display_menu(self):
        self.print_banner()
        print(f"{Fore.CYAN + Style.BRIGHT}Choose an option:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1]{Style.RESET_ALL} Add Accounts Interactively")
        print(f"{Fore.GREEN}[2]{Style.RESET_ALL} Use Proxies")
        print(f"{Fore.GREEN}[3]{Style.RESET_ALL} Enable Auto-Retry")
        print(f"{Fore.GREEN}[4]{Style.RESET_ALL} Remove Bad Proxies")
        print(f"{Fore.GREEN}[5]{Style.RESET_ALL} Start Automation")
        print(f"{Fore.RED}[6]{Style.RESET_ALL} Exit")

    async def get_user_id(self, index):
        email, password = self.accounts[index]
        url = "https://auth.teneo.pro/api/login"
        headers = {
            'x-api-key': 'OwAG3kib1ivOJG4Y0OCZ8lJETa6ypvsDtGmdhcjB',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }

        while True:
            try:
                proxy = self.proxies[index % len(self.proxies)] if self.use_proxy else None
                proxy_dict = {
                    'http': proxy,
                    'https': proxy
                } if proxy else None

                if proxy and not self.validate_proxy(proxy):
                    self.print_warning(f"Proxy {proxy} is invalid. Removing from list.")
                    self.proxies.remove(proxy)
                    continue

                response = requests.post(url, json={
                    'email': email,
                    'password': password
                }, headers=headers, proxies=proxy_dict, timeout=30)

                if response.status_code == 200:
                    data = response.json()
                    self.user_ids[index] = data['user']['id']
                    self.access_tokens[index] = data['access_token']
                    self.browser_ids[index] = f"browser-{index}-{random.randint(1000,9999)}"
                    self.messages[index] = "Connected successfully"
                    self.print_success(f"Account {index+1} authenticated")
                    await self.connect_websocket(index)
                    break
                else:
                    self.print_warning(f"Failed to authenticate account {index+1}: {response.text}")
                    raise Exception("Authentication failed")

            except Exception as e:
                self.messages[index] = f"Error: {str(e)}"
                self.print_error(f"Account {index+1} failed: {str(e)}")
                if self.enable_auto_retry:
                    self.print_warning(f"Retrying account {index+1} in 3 minutes...")
                    await asyncio.sleep(180)
                else:
                    break

    async def connect_websocket(self, index):
        ws_url = f"wss://secure.ws.teneo.pro/websocket?accessToken={self.access_tokens[index]}"
        proxy = self.proxies[index % len(self.proxies)] if self.use_proxy else None

        try:
            connector = None
            if proxy:
                if proxy.startswith("socks"):
                    from aiohttp_socks import ProxyConnector
                    connector = ProxyConnector.from_url(proxy)
                else:
                    connector = aiohttp.TCPConnector()

            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.ws_connect(ws_url) as ws:
                    self.connections[index] = ws
                    self.last_updated[index] = datetime.now()
                    await self.start_pinging(index)
                    await self.handle_messages(index, ws)

        except Exception as e:
            self.print_error(f"WebSocket error: {str(e)}")
            await asyncio.sleep(5)
            await self.connect_websocket(index)

    async def handle_messages(self, index, ws):
        async for message in ws:
            data = json.loads(message.data)
            if 'pointsTotal' in data:
                self.points_totals[index] = data['pointsTotal']
                self.points_today[index] = data['pointsToday']
                self.last_updated[index] = datetime.now()
                self.update_display()

    async def start_pinging(self, index):
        while True:
            if index in self.connections:
                await self.connections[index].send_json({'type': 'PING'})
                self.print_success(f"Ping sent for account {index+1}")
            await asyncio.sleep(60)

    def update_display(self):
        self.print_banner()
        for i, account in enumerate(self.accounts):
            status_color = Fore.GREEN if self.messages[i] == "Connected successfully" else Fore.RED
            print(f"{status_color}Account {i+1}: {account[0]} - {self.messages[i]}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}Press A/D to switch accounts | C to exit{Style.RESET_ALL}")

    async def run(self):
        self.load_accounts()
        self.load_proxies()

        while True:
            self.display_menu()
            choice = input(f"{Fore.CYAN}Enter your choice: {Style.RESET_ALL}")

            if choice == '1':
                self.add_accounts_interactively()
            elif choice == '2':
                self.use_proxy = True
                self.print_success("Proxies enabled.")
            elif choice == '3':
                self.enable_auto_retry = True
                self.print_success("Auto-retry enabled.")
            elif choice == '4':
                self.remove_bad_proxies()
            elif choice == '5':
                break
            elif choice == '6':
                self.print_warning("Exiting...")
                sys.exit(0)
            else:
                self.print_error("Invalid choice. Please try again.")

        if self.use_proxy and len(self.proxies) < len(self.accounts):
            self.print_error("Not enough proxies!")
            sys.exit(1)

        for _ in range(len(self.accounts)):
            self.potential_points.append(0)
            self.countdowns.append("Calculating...")
            self.points_totals.append(0)
            self.points_today.append(0)
            self.last_updated.append(None)
            self.messages.append("")
            self.user_ids.append("")
            self.browser_ids.append("")
            self.access_tokens.append("")

        tasks = [self.get_user_id(i) for i in range(len(self.accounts))]
        await asyncio.gather(*tasks)

        keyboard.add_hotkey('a', lambda: self.switch_account(-1))
        keyboard.add_hotkey('d', lambda: self.switch_account(1))
        keyboard.add_hotkey('c', lambda: sys.exit(0))

        while True:
            await asyncio.sleep(1)

    def switch_account(self, direction):
        self.current_account_index = (self.current_account_index + direction) % len(self.accounts)
        self.update_display()

if __name__ == "__main__":
    manager = AccountManager()
    try:
        asyncio.run(manager.run())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}🛑 Shutting down...{Style.RESET_ALL}")
        sys.exit(0)
