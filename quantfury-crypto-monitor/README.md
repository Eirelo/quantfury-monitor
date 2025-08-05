# 🚀 Surveillance Crypto Quantfury 24/7

## 📊 Description
Système de surveillance automatique des 35 cryptomonnaies Quantfury qui fonctionne 24/7 dans le cloud via GitHub Actions et envoie des alertes instantanées sur Telegram.

## ✅ Fonctionnalités
- 🔄 **Surveillance automatique** toutes les 15 minutes
- 📱 **Notifications Telegram** instantanées  
- ☁️ **Fonctionne dans le cloud** (indépendant de votre ordinateur)
- 💰 **100% gratuit** (GitHub Actions + Telegram)
- 🎯 **35 cryptomonnaies** Quantfury surveillées

## 🚨 Types d'Alertes
- 🚀 **PUMP 1H** - Hausses rapides (5-12% selon crypto)
- 💥 **DUMP 1H** - Baisses rapides (5-12% selon crypto)
- 📈 **PUMP 24H** - Tendances haussières (10-20%)
- 📉 **DUMP 24H** - Tendances baissières (10-20%)
- 🔥 **PROCHE ATH** - Nouveaux sommets historiques

## 📋 Cryptomonnaies Surveillées
Bitcoin (BTC), Ethereum (ETH), Solana (SOL), Cardano (ADA), Polkadot (DOT), Chainlink (LINK), Avalanche (AVAX), Cosmos (ATOM), Uniswap (UNI), Litecoin (LTC), Bitcoin Cash (BCH), Ethereum Classic (ETC), Filecoin (FIL), Dogecoin (DOGE), XRP, Tezos (XTZ), Aave (AAVE), Dash (DASH), EOS, Fantom (FTM), Injective (INJ), IOTA, Decentraland (MANA), Polygon (POL), NEAR Protocol (NEAR), Neo (NEO), Optimism (OP), THORChain (RUNE), The Sandbox (SAND), Synthetix (SNX), Stacks (STX), Toncoin (TON), Theta Network (THETA), Aptos (APT), Arbitrum (ARB)

## ⚙️ Configuration

### 1. Créer un Bot Telegram
1. Ouvrir Telegram et chercher `@BotFather`
2. Envoyer `/newbot` et suivre les instructions
3. Copier le **token** du bot

### 2. Obtenir votre Chat ID
1. Envoyer un message à votre bot
2. Aller sur `https://api.telegram.org/bot<TOKEN>/getUpdates`
3. Copier votre **chat_id**

### 3. Configurer GitHub Secrets
1. Aller dans **Settings** > **Secrets and variables** > **Actions**
2. Ajouter ces secrets :
   - `TELEGRAM_BOT_TOKEN` : Token de votre bot
   - `TELEGRAM_CHAT_ID` : Votre chat ID

## 🚀 Démarrage
1. **Fork** ce repository
2. **Configurer** les secrets Telegram
3. **Activer** GitHub Actions dans votre fork
4. **Attendre** - La surveillance démarre automatiquement !

## 📱 Exemple de Notification
```
🚨 ALERTES CRYPTO QUANTFURY 🚨

🔴 Bitcoin (BTC)
💰 Prix: $67,234.5678
📊 1h: +6.2% | 24h: +12.4%
⚠️ 🚀 PUMP 1H: +6.2%
⚠️ 📈 PUMP 24H: +12.4%
🕐 14:30:15

📱 Surveillance automatique Quantfury 24/7
```

## 🔧 Personnalisation
Modifiez `crypto_monitor_github_actions.py` pour :
- Ajuster les seuils d'alerte
- Modifier la fréquence (dans `.github/workflows/crypto_monitor.yml`)
- Ajouter d'autres cryptomonnaies

## 💰 Coût
**0€** - Utilise les quotas gratuits de :
- GitHub Actions (2000 minutes/mois)
- CoinGecko API (gratuite)
- Telegram Bot (gratuit)

## 🛠️ Support
- GitHub Actions s'exécute automatiquement
- Logs disponibles dans l'onglet **Actions**
- Notifications Telegram instantanées

