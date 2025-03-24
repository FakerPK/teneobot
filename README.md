#  Teneo Network Automated Farming Bot For 100% Uptime
### Automate your connection to the Teneo API with this script. Manage multiple accounts and ensure 24/7 uptime. Referral Code: f35PB
![AGPL License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)  
![Node.js](https://img.shields.io/badge/Node.js-16%2B-green)

## Features 🌟
* 🔄 Automatic proxy rotation
* 🔑 Multi-account support
* 🚦 Connection state management
* 🌈 Colorful console interface

----

## Requirements 📋
#### 🏗️ Infrastructure
- **VPS Server**: AWS/GCP/DigitalOcean ($2-5/month)
- **ISP Proxies**: **MUST** use residential proxies (SOCKS5 format)
  - Recommended: [proxies.fo ISP Plan](https://app.proxies.fo/ref/f1353b58-10c4-98a5-d94d-6164e2efcfaf)
  ![Proxy Setup](https://github.com/user-attachments/assets/c81fc995-11f9-4448-9355-0065d4286cf2)
  ![Proxy Plan](https://github.com/user-attachments/assets/bbd22e0a-22c7-42cf-8608-361d7310e0ae)

<summary><strong>💻 Development Environment</strong></summary>

**Choose your language:**

<details>
<summary>Node.js 18+</summary>
For Linux:
  
```bash
# Official PPA
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```
For Windows:

```bash
# Using winget
winget install OpenJS.NodeJS

# OR official installer
https://nodejs.org/en/download/
```
</details>
</details>
----

## 🔑 Account Setup
1. Go to the [Teneo Dashboard](https://dashboard.teneo.pro/dashboard), Use My Refferal code as it helps me out alot: *f35PB*
2. Log in with your credentials
3. Add your account details to the `account.json` file in the following format:
```bash
email,password
```
Example:
```bash
user1@example.com,password123
user2@example.com,password456
```

----
## Setup Guide 🛠️

### 1️⃣ Clone Repository
```bash
git clone https://github.com/FakerPK/teneobot.git
cd teneobot
```

### 2️⃣ Configuration Files

**account.json**
```bash
email1,password1
email2,password2
```

**proxy.txt** (100+ recommended)
```bash
http://username:pass@ip:port
socks://username:pass@ip:port
socks5://username:pass@ip:port
```

### 3️⃣ Proxy Setup
1. Buy [ISP proxies](https://app.proxies.fo/ref/f1353b58-10c4-98a5-d94d-6164e2efcfaf)
2. Generate SOCKS5 proxies
3. Add them to the proxy file

### 4️⃣ Run Bot

<details>
<summary><strong>Javascript Version Script</strong></summary>

```java
npm install
npm start
```
</details>

----
##  **💸Donations**
If you would like to support me or the development of this projects, you can make a donation using the following addresses:

  ### Crypto Wallet Addresses
  - **Solana**:
```javascript
9SqcZjiUAz9SYBBLwuA9uJG4UzwqC5HNWV2cvXPk3Kro
```
  - **EVM**: 
```javascript
0x2d550c8A47c60A43F8F4908C5d462184A40922Ef
```
  - **BTC**:
```json
bc1qhx7waktcttam9q9nt0ftdguguwg5lzq5hnasmm
```
  - **SUI**
```javascript
0x1f928f99c3c17813239363a1c7ee958529786947e837c544e3aa2b88216c1be8
```
 **TRON**
```json
TVY97kfPGVBvsyrxtTiHrjXigAakpv9azX
```
----
## Support 🆘  
Join my Discord or Telegram Group for Daily Scripts and Invite Codes and Contact `FakerPK` on:  
<p align="center">
  <a href="https://t.me/+rurxli5cagplMjM8"><img width="60px" alt="Telegram" src="https://img.icons8.com/fluency/96/0088CC/telegram-app.png"/></a>
  <a href="https://discord.gg/mjzgatMCk8"><img width="60px" alt="Discord" src="https://img.icons8.com/fluency/96/FFA500/discord-logo.png"/></a> &#8287;
  <a href="https://medium.com/@FakerPK"><img width="60px" src="https://img.icons8.com/ios-filled/96/F0F0EC/medium-monogram.png" alt="Medium"></a>&#8287;
</p>

----
> **Warning**  
> ⚠️ Using datacenter proxies will result in **ZERO** earnings! Only use ISP proxies.
