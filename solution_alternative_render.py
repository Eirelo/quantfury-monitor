#!/usr/bin/env python3
"""
SURVEILLANCE CRYPTO QUANTFURY 24/7 - RENDER.COM + DISCORD
Solution alternative avec hébergement Render et notifications Discord
"""

import requests
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
from flask import Flask, jsonify

app = Flask(__name__)

class QuantfuryCryptoMonitorRender:
    """Surveillance crypto sur Render.com avec Discord"""
    
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        
        # Configuration Discord Webhook
        self.discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
        
        # Même liste de cryptos que la version GitHub Actions
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
        
        # Seuils d'alerte
        self.alert_thresholds = {
            1: {"pump_1h": 5, "dump_1h": -5, "pump_24h": 10, "dump_24h": -10},
            2: {"pump_1h": 8, "dump_1h": -8, "pump_24h": 15, "dump_24h": -15},
            3: {"pump_1h": 12, "dump_1h": -12, "pump_24h": 20, "dump_24h": -20}
        }
        
        self.last_check = None
        self.alert_count = 0
    
    def get_crypto_data(self) -> Optional[List[Dict]]:
        """Récupère les données crypto"""
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
        """Analyse et détecte les alertes"""
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
            
            alert_types = []
            
            # Détection alertes
            if change_1h >= thresholds["pump_1h"]:
                alert_types.append(f"🚀 PUMP 1H: +{change_1h:.1f}%")
            elif change_1h <= thresholds["dump_1h"]:
                alert_types.append(f"💥 DUMP 1H: {change_1h:.1f}%")
            
            if change_24h >= thresholds["pump_24h"]:
                alert_types.append(f"📈 PUMP 24H: +{change_24h:.1f}%")
            elif change_24h <= thresholds["dump_24h"]:
                alert_types.append(f"📉 DUMP 24H: {change_24h:.1f}%")
            
            # ATH
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
                    "priority": priority,
                    "alerts": alert_types,
                    "timestamp": datetime.now().isoformat()
                }
                alerts.append(alert)
        
        return alerts
    
    def send_discord_message(self, alerts: List[Dict]) -> bool:
        """Envoie les alertes sur Discord"""
        if not self.discord_webhook_url or not alerts:
            return False
        
        try:
            # Créer embed Discord
            embeds = []
            
            for alert in alerts[:5]:  # Limite à 5 alertes par message
                color = 0xFF0000 if alert["priority"] == 1 else 0xFFFF00 if alert["priority"] == 2 else 0x00FF00
                
                embed = {
                    "title": f"{alert['name']} ({alert['symbol']})",
                    "color": color,
                    "fields": [
                        {"name": "💰 Prix", "value": f"${alert['price']:,.4f}", "inline": True},
                        {"name": "📊 1h", "value": f"{alert['change_1h']:+.1f}%", "inline": True},
                        {"name": "📊 24h", "value": f"{alert['change_24h']:+.1f}%", "inline": True},
                        {"name": "🚨 Alertes", "value": "\n".join(alert["alerts"]), "inline": False}
                    ],
                    "timestamp": alert["timestamp"],
                    "footer": {"text": "Surveillance Quantfury 24/7"}
                }
                embeds.append(embed)
            
            payload = {
                "content": "🚨 **ALERTES CRYPTO QUANTFURY** 🚨",
                "embeds": embeds
            }
            
            response = requests.post(self.discord_webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            
            print("Message Discord envoyé avec succès")
            return True
            
        except Exception as e:
            print(f"Erreur envoi Discord: {e}")
            return False
    
    def run_monitoring_cycle(self):
        """Exécute un cycle de surveillance"""
        print(f"🔄 Surveillance Quantfury - {datetime.now().strftime('%H:%M:%S')}")
        
        # Récupération données
        data = self.get_crypto_data()
        if not data:
            return {"status": "error", "message": "Impossible de récupérer les données"}
        
        # Analyse
        alerts = self.analyze_crypto_data(data)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "cryptos_checked": len(data),
            "alerts_found": len(alerts),
            "status": "success"
        }
        
        if alerts:
            print(f"🚨 {len(alerts)} alerte(s) détectée(s)")
            success = self.send_discord_message(alerts)
            result["discord_sent"] = success
            self.alert_count += len(alerts)
        else:
            print("✅ Aucune alerte - Marché stable")
        
        self.last_check = datetime.now().isoformat()
        return result

# Instance globale du monitor
monitor = QuantfuryCryptoMonitorRender()

@app.route('/')
def home():
    """Page d'accueil avec statut"""
    return jsonify({
        "service": "Surveillance Crypto Quantfury 24/7",
        "status": "active",
        "cryptos_monitored": len(monitor.quantfury_cryptos),
        "last_check": monitor.last_check,
        "total_alerts": monitor.alert_count,
        "discord_configured": bool(monitor.discord_webhook_url)
    })

@app.route('/check')
def manual_check():
    """Vérification manuelle"""
    result = monitor.run_monitoring_cycle()
    return jsonify(result)

@app.route('/health')
def health():
    """Health check pour Render"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

def background_monitoring():
    """Surveillance en arrière-plan"""
    while True:
        try:
            monitor.run_monitoring_cycle()
            time.sleep(900)  # 15 minutes
        except Exception as e:
            print(f"Erreur surveillance: {e}")
            time.sleep(300)  # 5 minutes en cas d'erreur

if __name__ == '__main__':
    import threading
    
    # Démarrer la surveillance en arrière-plan
    monitor_thread = threading.Thread(target=background_monitoring, daemon=True)
    monitor_thread.start()
    
    # Démarrer le serveur Flask
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

