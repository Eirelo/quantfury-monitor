#!/usr/bin/env python3
"""
SURVEILLANCE CRYPTO QUANTFURY 24/7 - GITHUB ACTIONS + TELEGRAM
Solution cloud gratuite qui fonctionne indépendamment de votre ordinateur
Notifications instantanées sur Telegram
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class QuantfuryCryptoMonitorCloud:
    """Surveillance crypto cloud avec notifications Telegram"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        
        # Configuration Telegram (variables d'environnement)
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        # Liste des 35 cryptomonnaies Quantfury
        self.quantfury_cryptos = {
            "bitcoin": {"symbol": "BTC", "name": "Bitcoin", "priority": 1},
            "ethereum": {"symbol": "ETH", "name": "Ethereum", "priority": 1},
            "solana": {"symbol": "SOL", "name": "Solana", "priority": 1},
            "cardano": {"symbol": "ADA", "name": "Cardano", "priority": 2},
            "polkadot": {"symbol": "DOT", "name": "Polkadot", "priority": 2},
            "chainlink": {"symbol": "LINK", "name": "Chainlink", "priority": 2},
            "avalanche-2": {"symbol": "AVAX", "name": "Avalanche", "priority": 2},
            "cosmos": {"symbol": "ATOM", "name": "Cosmos", "priority": 2},
            "uniswap": {"symbol": "UNI", "name": "Uniswap", "priority": 2},
            "litecoin": {"symbol": "LTC", "name": "Litecoin", "priority": 2},
            "bitcoin-cash": {"symbol": "BCH", "name": "Bitcoin Cash", "priority": 2},
            "ethereum-classic": {"symbol": "ETC", "name": "Ethereum Classic", "priority": 3},
            "filecoin": {"symbol": "FIL", "name": "Filecoin", "priority": 3},
            "dogecoin": {"symbol": "DOGE", "name": "Dogecoin", "priority": 3},
            "ripple": {"symbol": "XRP", "name": "XRP", "priority": 2},
            "tezos": {"symbol": "XTZ", "name": "Tezos", "priority": 3},
            "aave": {"symbol": "AAVE", "name": "Aave", "priority": 2},
            "dash": {"symbol": "DASH", "name": "Dash", "priority": 3},
            "eos": {"symbol": "EOS", "name": "EOS", "priority": 3},
            "fantom": {"symbol": "FTM", "name": "Fantom", "priority": 3},
            "injective-protocol": {"symbol": "INJ", "name": "Injective", "priority": 3},
            "iota": {"symbol": "IOTA", "name": "IOTA", "priority": 3},
            "decentraland": {"symbol": "MANA", "name": "Decentraland", "priority": 3},
            "matic-network": {"symbol": "POL", "name": "Polygon", "priority": 2},
            "near": {"symbol": "NEAR", "name": "NEAR Protocol", "priority": 3},
            "neo": {"symbol": "NEO", "name": "Neo", "priority": 3},
            "optimism": {"symbol": "OP", "name": "Optimism", "priority": 3},
            "thorchain": {"symbol": "RUNE", "name": "THORChain", "priority": 3},
            "the-sandbox": {"symbol": "SAND", "name": "The Sandbox", "priority": 3},
            "havven": {"symbol": "SNX", "name": "Synthetix", "priority": 3},
            "blockstack": {"symbol": "STX", "name": "Stacks", "priority": 3},
            "the-open-network": {"symbol": "TON", "name": "Toncoin", "priority": 3},
            "theta-token": {"symbol": "THETA", "name": "Theta Network", "priority": 3},
            "aptos": {"symbol": "APT", "name": "Aptos", "priority": 3},
            "arbitrum": {"symbol": "ARB", "name": "Arbitrum", "priority": 3}
        }
        
        # Seuils d'alerte par priorité
        self.alert_thresholds = {
            1: {"pump_1h": 5, "dump_1h": -5, "pump_24h": 10, "dump_24h": -10},
            2: {"pump_1h": 8, "dump_1h": -8, "pump_24h": 15, "dump_24h": -15},
            3: {"pump_1h": 12, "dump_1h": -12, "pump_24h": 20, "dump_24h": -20}
        }
    
    def get_crypto_data(self) -> Optional[List[Dict]]:
        """Récupère les données crypto de CoinGecko"""
        try:
            coin_ids = ",".join(self.quantfury_cryptos.keys())
            
            url = f"{self.base_url}/coins/markets"
            params = {
                "vs_currency": "usd",
                "ids": coin_ids,
                "order": "market_cap_desc",
                "per_page": len(self.quantfury_cryptos),
                "page": 1,
                "sparkline": False,
                "price_change_percentage": "1h,24h,7d"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Erreur récupération données: {e}")
            return None
    
    def analyze_crypto_data(self, data: List[Dict]) -> List[Dict]:
        """Analyse les données et détecte les alertes"""
        alerts = []
        
        for crypto in data:
            coin_id = crypto["id"]
            if coin_id not in self.quantfury_cryptos:
                continue
                
            coin_info = self.quantfury_cryptos[coin_id]
            priority = coin_info["priority"]
            thresholds = self.alert_thresholds[priority]
            
            name = coin_info["name"]
            symbol = coin_info["symbol"]
            current_price = crypto["current_price"]
            change_1h = crypto.get("price_change_percentage_1h", 0) or 0
            change_24h = crypto.get("price_change_percentage_24h", 0) or 0
            change_7d = crypto.get("price_change_percentage_7d_in_currency", 0) or 0
            
            # Détection des alertes
            alert_types = []
            
            # Alertes 1h
            if change_1h >= thresholds["pump_1h"]:
                alert_types.append(f"🚀 PUMP 1H: +{change_1h:.1f}%")
            elif change_1h <= thresholds["dump_1h"]:
                alert_types.append(f"💥 DUMP 1H: {change_1h:.1f}%")
            
            # Alertes 24h
            if change_24h >= thresholds["pump_24h"]:
                alert_types.append(f"📈 PUMP 24H: +{change_24h:.1f}%")
            elif change_24h <= thresholds["dump_24h"]:
                alert_types.append(f"📉 DUMP 24H: {change_24h:.1f}%")
            
            # Alerte ATH
            ath = crypto.get("ath", 0)
            if ath and current_price >= ath * 0.995:
                alert_types.append("🔥 PROCHE ATH!")
            
            if alert_types:
                alert = {
                    "name": name,
                    "symbol": symbol,
                    "price": current_price,
                    "change_1h": change_1h,
                    "change_24h": change_24h,
                    "change_7d": change_7d,
                    "priority": priority,
                    "alerts": alert_types,
                    "timestamp": datetime.now().isoformat()
                }
                alerts.append(alert)
        
        return alerts
    
    def send_telegram_message(self, message: str) -> bool:
        """Envoie un message via Telegram Bot"""
        if not self.telegram_bot_token or not self.telegram_chat_id:
            print("Configuration Telegram manquante")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            data = {
                "chat_id": self.telegram_chat_id,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()
            
            print("Message Telegram envoyé avec succès")
            return True
            
        except Exception as e:
            print(f"Erreur envoi Telegram: {e}")
            return False
    
    def format_alert_message(self, alerts: List[Dict]) -> str:
        """Formate les alertes pour Telegram"""
        if not alerts:
            return None
        
        # Trier par priorité
        alerts.sort(key=lambda x: x["priority"])
        
        message = "🚨 <b>ALERTES CRYPTO QUANTFURY</b> 🚨\n\n"
        
        for alert in alerts:
            priority_emoji = "🔴" if alert["priority"] == 1 else "🟡" if alert["priority"] == 2 else "🟢"
            
            message += f"{priority_emoji} <b>{alert['name']} ({alert['symbol']})</b>\n"
            message += f"💰 Prix: ${alert['price']:,.4f}\n"
            message += f"📊 1h: {alert['change_1h']:+.1f}% | 24h: {alert['change_24h']:+.1f}%\n"
            
            for alert_type in alert["alerts"]:
                message += f"⚠️ {alert_type}\n"
            
            message += f"🕐 {datetime.fromisoformat(alert['timestamp']).strftime('%H:%M:%S')}\n\n"
        
        message += f"📱 Surveillance automatique Quantfury 24/7"
        
        return message
    
    def run_monitoring_cycle(self):
        """Exécute un cycle de surveillance"""
        print(f"🔄 Début surveillance Quantfury - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Récupération des données
        data = self.get_crypto_data()
        if not data:
            print("❌ Impossible de récupérer les données")
            return
        
        print(f"✅ Données récupérées pour {len(data)} cryptomonnaies")
        
        # Analyse et détection d'alertes
        alerts = self.analyze_crypto_data(data)
        
        if alerts:
            print(f"🚨 {len(alerts)} alerte(s) détectée(s)")
            
            # Formatage et envoi du message
            message = self.format_alert_message(alerts)
            if message:
                success = self.send_telegram_message(message)
                if success:
                    print("📱 Alertes envoyées sur Telegram")
                else:
                    print("❌ Échec envoi Telegram")
            
            # Affichage console pour debug
            for alert in alerts:
                print(f"🔔 {alert['name']}: {', '.join(alert['alerts'])}")
        else:
            print("✅ Aucune alerte détectée - Marché stable")
        
        print("✅ Cycle de surveillance terminé")

def main():
    """Point d'entrée principal"""
    print("🚀 SURVEILLANCE CRYPTO QUANTFURY CLOUD 24/7")
    print("=" * 60)
    print("📊 35 cryptomonnaies Quantfury surveillées")
    print("📱 Notifications Telegram instantanées")
    print("☁️ Fonctionne indépendamment de votre ordinateur")
    print("=" * 60)
    
    monitor = QuantfuryCryptoMonitorCloud()
    monitor.run_monitoring_cycle()

if __name__ == "__main__":
    main()

