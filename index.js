const fs = require('fs');
const path = require('path');
const axios = require('axios');
const WebSocket = require('ws');
const chalk = require('chalk');
const inquirer = require('inquirer');
const { SocksProxyAgent } = require('socks-proxy-agent');

class AccountManager {
    constructor() {
        this.accounts = [];
        this.proxies = [];
        this.useProxy = false;
        this.enableAutoRetry = false;
        this.connections = {};
        this.messages = [];
        this.userIds = [];
        this.browserIds = [];
        this.accessTokens = [];
    }

    printBanner() {
        console.clear();
        console.log(chalk.yellowBright(`
        ███████╗ █████╗ ██╗  ██╗███████╗██████╗  ██████╗ ██╗  ██╗ 
        ██╔════╝██╔══██╗██║ ██╔╝██╔════╝██╔══██╗ ██╔══██╗██║ ██╔╝ 
        █████╗  ███████║█████╔╝ █████╗  ██████╔╝ ██████╔╝█████╔╝  
        ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██╗ ██╔═══╝ ██╔═██╗  
        ██║     ██║  ██║██║  ██╗███████╗██║  ██║ ██║     ██║  ██╗     
        ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═╝     ╚═╝  ╚═╝     
        `));
        console.log(chalk.cyanBright('🚀 TENEO BOT | AUTOMATE AND DOMINATE '));
        console.log(chalk.red('═══════════════════════════════════════════════════'));
    }

    loadAccounts() {
        try {
            const data = fs.readFileSync(path.join(__dirname, 'account.txt'), 'utf8');
            this.accounts = data.split('\n')
                .filter(line => line.trim())
                .map(line => line.split(',').slice(0, 2));
        } catch (err) {
            console.error(chalk.red('❌ account.txt not found!'));
            process.exit(1);
        }
    }

    saveAccounts() {
        const content = this.accounts.map(([email, password]) => `${email},${password}`).join('\n');
        fs.writeFileSync(path.join(__dirname, 'account.txt'), content);
        console.log(chalk.green('✅ Accounts saved to account.txt'));
    }

    async addAccountsInteractively() {
        this.printBanner();
        console.log(chalk.yellowBright('Interactive Account Setup'));
        console.log(chalk.yellow('Enter account details below. Type "done" when finished.'));

        while (true) {
            const answers = await inquirer.prompt([
                {
                    type: 'input',
                    name: 'email',
                    message: chalk.green(`Enter email for account ${this.accounts.length + 1} (or 'done' to finish):`),
                },
            ]);

            if (answers.email.toLowerCase() === 'done') break;

            const passwordAnswer = await inquirer.prompt([
                {
                    type: 'password',
                    name: 'password',
                    message: chalk.green(`Enter password for account ${this.accounts.length + 1}:`),
                },
            ]);

            this.accounts.push([answers.email, passwordAnswer.password]);
            console.log(chalk.green(`✅ Account ${this.accounts.length} added: ${answers.email}`));
        }

        this.saveAccounts();
    }

    loadProxies() {
        try {
            const data = fs.readFileSync(path.join(__dirname, 'proxy.txt'), 'utf8');
            this.proxies = data.split('\n')
                .filter(line => line.trim())
                .map(proxy => this.normalizeProxy(proxy));
        } catch (err) {
            console.error(chalk.red('❌ proxy.txt not found!'));
            process.exit(1);
        }
    }

    normalizeProxy(proxy) {
        if (!proxy.startsWith('http://') && !proxy.startsWith('https://') && !proxy.startsWith('socks')) {
            return `http://${proxy}`;
        }
        return proxy;
    }

    async getUserId(index) {
        const [email, password] = this.accounts[index];
        const url = 'https://auth.teneo.pro/api/login';
        const headers = {
            'x-api-key': 'OwAG3kib1ivOJG4Y0OCZ8lJETa6ypvsDtGmdhcjB',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        };

        let proxy = this.useProxy ? this.proxies[index % this.proxies.length] : null;

        try {
            const response = await axios.post(url, { email, password }, {
                headers,
                proxy: this.parseProxy(proxy),
                timeout: 30000,
            });

            if (response.status === 200) {
                const { user, access_token } = response.data;
                this.userIds[index] = user.id;
                this.accessTokens[index] = access_token;
                this.browserIds[index] = `browser-${index}-${Math.floor(Math.random() * 9000 + 1000)}`;
                this.messages[index] = 'Connected successfully';
                console.log(chalk.green(`✅ Account ${index + 1} authenticated`));
                await this.connectWebSocket(index);
            } else {
                throw new Error(`Authentication failed: ${response.statusText}`);
            }
        } catch (error) {
            this.messages[index] = `Error: ${error.message}`;
            console.error(chalk.red(`❌ Account ${index + 1} failed: ${error.message}`));
            if (this.enableAutoRetry) {
                console.warn(chalk.yellow(`⚠️ Retrying account ${index + 1} in 3 minutes...`));
                await new Promise(resolve => setTimeout(resolve, 180000));
                await this.getUserId(index);
            }
        }
    }

    parseProxy(proxy) {
        if (!proxy) return null;
        const parsed = new URL(proxy);
        return {
            protocol: parsed.protocol.replace(':', ''),
            host: parsed.hostname,
            port: parseInt(parsed.port, 10),
        };
    }

    async connectWebSocket(index) {
        const wsUrl = `wss://secure.ws.teneo.pro/websocket?accessToken=${this.accessTokens[index]}`;
        const proxy = this.useProxy ? this.proxies[index % this.proxies.length] : null;

        try {
            const agent = proxy && proxy.startsWith('socks') ? new SocksProxyAgent(proxy) : undefined;
            const ws = new WebSocket(wsUrl, { agent });

            ws.on('open', () => {
                console.log(chalk.green(`✅ WebSocket connected for account ${index + 1}`));
                this.connections[index] = ws;
                setInterval(() => this.sendPing(index), 60000);
            });

            ws.on('message', (data) => {
                const message = JSON.parse(data);
                if (message.pointsTotal) {
                    console.log(chalk.blue(`📊 Points updated for account ${index + 1}`));
                }
            });

            ws.on('close', () => {
                console.warn(chalk.yellow(`⚠️ WebSocket closed for account ${index + 1}, reconnecting...`));
                setTimeout(() => this.connectWebSocket(index), 5000);
            });

            ws.on('error', (err) => {
                console.error(chalk.red(`❌ WebSocket error: ${err.message}`));
                setTimeout(() => this.connectWebSocket(index), 5000);
            });
        } catch (error) {
            console.error(chalk.red(`❌ WebSocket connection failed: ${error.message}`));
            setTimeout(() => this.connectWebSocket(index), 5000);
        }
    }

    sendPing(index) {
        if (this.connections[index]) {
            this.connections[index].send(JSON.stringify({ type: 'PING' }));
            console.log(chalk.green(`🏓 Ping sent for account ${index + 1}`));
        }
    }

    async run() {
        this.printBanner();
        this.loadAccounts();
        this.loadProxies();

        const menu = [
            { name: 'Add Accounts Interactively', value: 'add_accounts' },
            { name: 'Use Proxies', value: 'use_proxies' },
            { name: 'Enable Auto-Retry', value: 'enable_retry' },
            { name: 'Start Automation', value: 'start' },
            { name: 'Exit', value: 'exit' },
        ];

        while (true) {
            const { choice } = await inquirer.prompt([
                {
                    type: 'list',
                    name: 'choice',
                    message: 'Choose an option:',
                    choices: menu,
                },
            ]);

            if (choice === 'add_accounts') {
                await this.addAccountsInteractively();
            } else if (choice === 'use_proxies') {
                this.useProxy = true;
                console.log(chalk.green('✅ Proxies enabled.'));
            } else if (choice === 'enable_retry') {
                this.enableAutoRetry = true;
                console.log(chalk.green('✅ Auto-retry enabled.'));
            } else if (choice === 'start') {
                break;
            } else if (choice === 'exit') {
                console.warn(chalk.yellow('🛑 Exiting...'));
                process.exit(0);
            }
        }

        if (this.useProxy && this.proxies.length < this.accounts.length) {
            console.error(chalk.red('❌ Not enough proxies!'));
            process.exit(1);
        }

        // Initialize account data structures
        for (let i = 0; i < this.accounts.length; i++) {
            this.messages[i] = '';
            this.userIds[i] = '';
            this.browserIds[i] = '';
            this.accessTokens[i] = '';
        }

        // Start authentication for all accounts
        await Promise.all(this.accounts.map((_, index) => this.getUserId(index)));

        console.log(chalk.green('✅ All accounts authenticated. Running automation...'));
    }
}

(async () => {
    const manager = new AccountManager();
    try {
        await manager.run();
    } catch (error) {
        console.error(chalk.red(`❌ Fatal error: ${error.message}`));
    }
})();
