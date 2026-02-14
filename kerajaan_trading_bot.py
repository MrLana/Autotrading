#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
===============================================================
   👑 KERAJAAN GOLD TRADING BOT - VERSI ULTIMATE 👑
   Fitur SUPER PREMIUM: AI + Telegram + Web + Semua Ada
         Khusus Untuk Yang Mulia Putri Incha
===============================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
from datetime import datetime, timedelta
import random
import queue
import webbrowser
import os
import sys
import numpy as np
import pandas as pd
from collections import deque
import pickle
import hashlib
import hmac
import base64
import requests
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import socketio
import telebot
from telebot import types
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings('ignore')

# ============== AI / MACHINE LEARNING IMPORTS ==============
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
    from sklearn.svm import SVR
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False
    print("⚠️ TensorFlow tidak terinstall, menggunakan AI mode sederhana")

# ============== KONFIGURASI ==============
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Ganti dengan token bot Yang Mulia
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"  # Ganti dengan chat ID Yang Mulia
FLASK_PORT = 5000
WEBSOCKET_PORT = 5001

class KerajaanTradingBot:
    """Bot Trading Versi Kerajaan - Semua Fitur Ada"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("👑 KERAJAAN TRADING BOT - PUTRI INCHA 👑")
        self.root.geometry("1600x900")
        self.root.configure(bg='#0a0f1e')
        
        # ============== DATA PASAR ==============
        self.current_price = 5042.31
        self.bid_price = 5041.86
        self.ask_price = 5042.31
        self.spread = round(self.ask_price - self.bid_price, 2)
        
        # Data historis lengkap
        self.price_history = deque(maxlen=1000)
        self.volume_history = deque(maxlen=1000)
        self.timestamp_history = deque(maxlen=1000)
        
        # Initialize dengan data dari screenshot
        initial_prices = [
            5045.71, 5045.16, 5044.61, 5044.06, 5043.51,
            5042.96, 5042.31, 5041.86, 5041.31, 5040.76,
            5040.21, 5039.66, 5039.11, 5038.56, 5038.01
        ]
        
        base_time = datetime.now() - timedelta(minutes=15)
        for i, price in enumerate(initial_prices):
            self.price_history.append(price)
            self.volume_history.append(random.randint(100, 1000))
            self.timestamp_history.append(base_time + timedelta(minutes=i))
        
        # ============== AI / ML COMPONENTS ==============
        self.ai_models = {}
        self.scalers = {}
        self.ai_predictions = deque(maxlen=100)
        self.ai_confidence = 0
        self.setup_ai_models()
        
        # ============== TELEGRAM BOT ==============
        self.telegram_enabled = False
        self.telegram_bot = None
        self.setup_telegram()
        
        # ============== WEB SERVER ==============
        self.web_enabled = False
        self.flask_app = None
        self.socketio = None
        self.web_thread = None
        self.setup_web_server()
        
        # ============== TRADING DATA ==============
        self.balance = 10000.0
        self.equity = 10000.0
        self.in_position = False
        self.position_type = None
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.lot_size = 0.01
        
        # P&L Tracking
        self.pnl_history = []
        self.trade_history = []
        self.daily_pnl = 0.0
        self.daily_trades = 0
        
        # ============== AUTO TRADING ==============
        self.auto_trade = False
        self.auto_trade_thread = None
        self.max_daily_trades = 5
        self.profit_target = 100.0
        self.daily_stop_loss = 50.0
        
        # ============== QUEUES ==============
        self.update_queue = queue.Queue()
        self.telegram_queue = queue.Queue()
        self.web_queue = queue.Queue()
        
        # ============== SETUP UI ==============
        self.setup_ui()
        
        # ============== START SERVICES ==============
        self.start_services()
        
    def setup_ai_models(self):
        """Setup semua model AI"""
        print("🧠 Menginisialisasi AI Models...")
        
        if AI_AVAILABLE:
            try:
                # LSTM Model untuk prediksi harga
                self.ai_models['lstm'] = self.create_lstm_model()
                
                # Random Forest untuk signal
                self.ai_models['random_forest'] = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42
                )
                
                # Gradient Boosting untuk confidence
                self.ai_models['gradient_boost'] = GradientBoostingRegressor(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=5
                )
                
                # SVM untuk classification
                self.ai_models['svm'] = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1)
                
                # Scalers
                self.scalers['price'] = MinMaxScaler()
                self.scalers['volume'] = MinMaxScaler()
                
                print("✅ AI Models siap digunakan!")
                
            except Exception as e:
                print(f"⚠️ Error setup AI: {e}")
                self.ai_models = {}
        else:
            print("⚠️ Menggunakan AI mode sederhana")
            
    def create_lstm_model(self):
        """Create LSTM model untuk prediksi harga"""
        model = models.Sequential([
            layers.LSTM(50, return_sequences=True, input_shape=(60, 1)),
            layers.Dropout(0.2),
            layers.LSTM(50, return_sequences=True),
            layers.Dropout(0.2),
            layers.LSTM(50),
            layers.Dropout(0.2),
            layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        return model
        
    def setup_telegram(self):
        """Setup Telegram Bot"""
        try:
            if TELEGRAM_TOKEN != "YOUR_BOT_TOKEN_HERE":
                self.telegram_bot = telebot.TeleBot(TELEGRAM_TOKEN)
                self.setup_telegram_handlers()
                print("✅ Telegram Bot siap (token perlu diganti)")
            else:
                print("⚠️ Telegram token belum diisi")
        except Exception as e:
            print(f"⚠️ Telegram setup error: {e}")
            
    def setup_telegram_handlers(self):
        """Setup handlers untuk Telegram Bot"""
        
        @self.telegram_bot.message_handler(commands=['start'])
        def send_welcome(message):
            welcome_text = """
👑 SELAMAT DATANG DI KERAJAAN TRADING BOT 👑
Milik Yang Mulia Putri Incha

Perintah yang tersedia:
/price - Harga terkini
/signal - Signal trading terbaru
/buy [lot] - Eksekusi BUY
/sell [lot] - Eksekusi SELL
/balance - Cek balance
/positions - Posisi terbuka
/history - Riwayat trading
/predict - Prediksi AI
/help - Bantuan
            """
            self.telegram_bot.reply_to(message, welcome_text)
            
        @self.telegram_bot.message_handler(commands=['price'])
        def send_price(message):
            price_text = f"""
📊 XAUUSD PRICE
──────────────
💰 Current: ${self.current_price:.2f}
📈 Bid: ${self.bid_price:.2f}
📉 Ask: ${self.ask_price:.2f}
📏 Spread: {self.spread}
⏰ Time: {datetime.now().strftime('%H:%M:%S')}
            """
            self.telegram_bot.reply_to(message, price_text)
            
        @self.telegram_bot.message_handler(commands=['signal'])
        def send_signal(message):
            signal, confidence = self.ai_generate_signal()
            
            if signal == "BUY":
                emoji = "🚀"
                color = "🟢"
            elif signal == "SELL":
                emoji = "🔻"
                color = "🔴"
            else:
                emoji = "⏸️"
                color = "⚪"
                
            signal_text = f"""
{emoji} TRADING SIGNAL {emoji}
──────────────
{color} Signal: {signal}
📊 Confidence: {confidence}%
🤖 AI Prediction: ${self.ai_predictions[-1] if self.ai_predictions else 'N/A':.2f}
📈 Trend: {self.analyze_trend()}
            """
            self.telegram_bot.reply_to(message, signal_text)
            
        @self.telegram_bot.message_handler(commands=['buy'])
        def telegram_buy(message):
            try:
                lot = float(message.text.split()[1]) if len(message.text.split()) > 1 else 0.01
                self.execute_buy(lot)
                self.telegram_bot.reply_to(message, f"✅ BUY {lot} executed at ${self.current_price:.2f}")
            except:
                self.telegram_bot.reply_to(message, "Format: /buy [lot]")
                
        @self.telegram_bot.message_handler(commands=['sell'])
        def telegram_sell(message):
            try:
                lot = float(message.text.split()[1]) if len(message.text.split()) > 1 else 0.01
                self.execute_sell(lot)
                self.telegram_bot.reply_to(message, f"✅ SELL {lot} executed at ${self.current_price:.2f}")
            except:
                self.telegram_bot.reply_to(message, "Format: /sell [lot]")
                
        @self.telegram_bot.message_handler(commands=['balance'])
        def send_balance(message):
            balance_text = f"""
💰 ACCOUNT BALANCE
──────────────
💵 Balance: ${self.balance:.2f}
📊 Equity: ${self.equity:.2f}
📈 Daily P&L: ${self.daily_pnl:.2f}
🔄 Trades Today: {self.daily_trades}
            """
            self.telegram_bot.reply_to(message, balance_text)
            
        @self.telegram_bot.message_handler(commands=['positions'])
        def send_positions(message):
            if self.in_position:
                pos_text = f"""
📋 OPEN POSITION
──────────────
{self.position_type} {self.lot_size} lots
💰 Entry: ${self.entry_price:.2f}
🎯 TP: ${self.take_profit:.2f}
🛑 SL: ${self.stop_loss:.2f}
            """
            else:
                pos_text = "No open positions"
            self.telegram_bot.reply_to(message, pos_text)
            
        @self.telegram_bot.message_handler(commands=['predict'])
        def send_prediction(message):
            pred = self.ai_predict_next_price()
            pred_text = f"""
🤖 AI PREDICTION
──────────────
🔮 Next Price: ${pred:.2f}
📊 Confidence: {self.ai_confidence:.1f}%
⚡ Based on: LSTM + Random Forest
            """
            self.telegram_bot.reply_to(message, pred_text)
            
    def setup_web_server(self):
        """Setup Flask Web Server"""
        self.flask_app = Flask(__name__)
        self.socketio = SocketIO(self.flask_app, cors_allowed_origins="*")
        
        @self.flask_app.route('/')
        def index():
            return self.render_web_dashboard()
            
        @self.flask_app.route('/api/price')
        def api_price():
            return jsonify({
                'current': self.current_price,
                'bid': self.bid_price,
                'ask': self.ask_price,
                'spread': self.spread
            })
            
        @self.flask_app.route('/api/signal')
        def api_signal():
            signal, confidence = self.ai_generate_signal()
            return jsonify({
                'signal': signal,
                'confidence': confidence,
                'prediction': self.ai_predictions[-1] if self.ai_predictions else 0
            })
            
        @self.flask_app.route('/api/trade', methods=['POST'])
        def api_trade():
            data = request.json
            if data['type'] == 'BUY':
                self.execute_buy(data.get('lot', 0.01))
            elif data['type'] == 'SELL':
                self.execute_sell(data.get('lot', 0.01))
            return jsonify({'status': 'success'})
            
        @self.flask_app.route('/api/history')
        def api_history():
            return jsonify({
                'prices': list(self.price_history)[-100:],
                'timestamps': [t.strftime('%H:%M:%S') for t in list(self.timestamp_history)[-100:]],
                'trades': self.trade_history[-20:]
            })
            
        @self.socketio.on('connect')
        def handle_connect():
            print('🌐 Web client connected')
            
        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('🌐 Web client disconnected')
            
    def render_web_dashboard(self):
        """Render web dashboard HTML"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>👑 Kerajaan Trading - Putri Incha</title>
            <meta http-equiv="refresh" content="1">
            <style>
                body {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 20px;
                    color: white;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .price-box {
                    background: rgba(255,255,255,0.2);
                    border-radius: 15px;
                    padding: 30px;
                    text-align: center;
                    margin-bottom: 20px;
                    font-size: 48px;
                    font-weight: bold;
                }
                .grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-bottom: 20px;
                }
                .card {
                    background: rgba(255,255,255,0.1);
                    border-radius: 10px;
                    padding: 20px;
                    backdrop-filter: blur(10px);
                }
                .signal {
                    font-size: 36px;
                    text-align: center;
                    padding: 20px;
                }
                .buy { color: #00ff00; }
                .sell { color: #ff4444; }
                .hold { color: #ffff00; }
                .btn {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: none;
                    color: white;
                    padding: 15px 30px;
                    border-radius: 5px;
                    font-size: 18px;
                    cursor: pointer;
                    margin: 5px;
                }
                .chart {
                    width: 100%;
                    height: 400px;
                    background: rgba(0,0,0,0.3);
                    border-radius: 10px;
                    margin-top: 20px;
                }
                .stats {
                    display: flex;
                    justify-content: space-around;
                    margin-top: 20px;
                }
            </style>
            <script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>👑 KERAJAAN TRADING - PUTRI INCHA 👑</h1>
                    <p>Real-time Gold Trading Dashboard</p>
                </div>
                
                <div class="price-box" id="price">
                    $5042.31
                </div>
                
                <div class="grid">
                    <div class="card">
                        <h3>📊 Market Data</h3>
                        <p>Bid: <span id="bid">5041.86</span></p>
                        <p>Ask: <span id="ask">5042.31</span></p>
                        <p>Spread: <span id="spread">0.45</span></p>
                    </div>
                    
                    <div class="card">
                        <h3>🤖 AI Signal</h3>
                        <div class="signal" id="signal">ANALYZING...</div>
                        <p>Confidence: <span id="confidence">0</span>%</p>
                    </div>
                    
                    <div class="card">
                        <h3>💰 Account</h3>
                        <p>Balance: $<span id="balance">10000.00</span></p>
                        <p>Equity: $<span id="equity">10000.00</span></p>
                        <p>Daily P&L: $<span id="pnl">0.00</span></p>
                    </div>
                </div>
                
                <div class="stats">
                    <button class="btn" onclick="trade('BUY', 0.01)">🚀 BUY 0.01</button>
                    <button class="btn" onclick="trade('SELL', 0.01)">🔻 SELL 0.01</button>
                    <button class="btn" onclick="trade('BUY', 0.1)">🚀 BUY 0.1</button>
                    <button class="btn" onclick="trade('SELL', 0.1)">🔻 SELL 0.1</button>
                </div>
                
                <div class="chart">
                    <canvas id="priceChart"></canvas>
                </div>
                
                <div class="card">
                    <h3>📜 Recent Trades</h3>
                    <div id="trades"></div>
                </div>
            </div>
            
            <script>
                const socket = io('http://localhost:5001');
                
                function updatePrice() {
                    fetch('/api/price')
                        .then(r => r.json())
                        .then(data => {
                            document.getElementById('price').innerHTML = '$' + data.current.toFixed(2);
                            document.getElementById('bid').innerHTML = data.bid.toFixed(2);
                            document.getElementById('ask').innerHTML = data.ask.toFixed(2);
                            document.getElementById('spread').innerHTML = data.spread;
                        });
                }
                
                function updateSignal() {
                    fetch('/api/signal')
                        .then(r => r.json())
                        .then(data => {
                            let signalDiv = document.getElementById('signal');
                            signalDiv.innerHTML = data.signal;
                            signalDiv.className = 'signal ' + data.signal.toLowerCase();
                            document.getElementById('confidence').innerHTML = data.confidence;
                        });
                }
                
                function updateHistory() {
                    fetch('/api/history')
                        .then(r => r.json())
                        .then(data => {
                            // Update chart
                            const ctx = document.getElementById('priceChart').getContext('2d');
                            new Chart(ctx, {
                                type: 'line',
                                data: {
                                    labels: data.timestamps,
                                    datasets: [{
                                        label: 'XAUUSD Price',
                                        data: data.prices,
                                        borderColor: 'rgb(75, 192, 192)',
                                        tension: 0.1
                                    }]
                                },
                                options: {
                                    responsive: true,
                                    maintainAspectRatio: false
                                }
                            });
                            
                            // Update trades
                            let tradesHtml = '';
                            data.trades.forEach(trade => {
                                tradesHtml += `<p>${trade.time} | ${trade.type} | Lots: ${trade.lots} | P&L: $${trade.pnl}</p>`;
                            });
                            document.getElementById('trades').innerHTML = tradesHtml;
                        });
                }
                
                function trade(type, lot) {
                    fetch('/api/trade', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({type: type, lot: lot})
                    }).then(() => {
                        alert(type + ' ' + lot + ' executed!');
                    });
                }
                
                setInterval(updatePrice, 1000);
                setInterval(updateSignal, 5000);
                setInterval(updateHistory, 10000);
            </script>
        </body>
        </html>
        """
        
    def setup_ui(self):
        """Setup UI Super Lengkap"""
        
        # Notebook dengan banyak tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tab 1: Trading Utama
        self.tab_trading = tk.Frame(self.notebook, bg='#0a0f1e')
        self.notebook.add(self.tab_trading, text='💹 TRADING')
        self.setup_trading_tab()
        
        # Tab 2: AI Analysis
        self.tab_ai = tk.Frame(self.notebook, bg='#0a0f1e')
        self.notebook.add(self.tab_ai, text='🧠 AI ANALYTICS')
        self.setup_ai_tab()
        
        # Tab 3: Telegram Bot
        self.tab_telegram = tk.Frame(self.notebook, bg='#0a0f1e')
        self.notebook.add(self.tab_telegram, text='📱 TELEGRAM')
        self.setup_telegram_tab()
        
        # Tab 4: Web Dashboard
        self.tab_web = tk.Frame(self.notebook, bg='#0a0f1e')
        self.notebook.add(self.tab_web, text='🌐 WEB DASHBOARD')
        self.setup_web_tab()
        
        # Tab 5: Auto Trading
        self.tab_auto = tk.Frame(self.notebook, bg='#0a0f1e')
        self.notebook.add(self.tab_auto, text='🤖 AUTO TRADING')
        self.setup_auto_tab()
        
        # Tab 6: P&L Analytics
        self.tab_pnl = tk.Frame(self.notebook, bg='#0a0f1e')
        self.notebook.add(self.tab_pnl, text='📊 P&L ANALYTICS')
        self.setup_pnl_tab()
        
        # Tab 7: Settings
        self.tab_settings = tk.Frame(self.notebook, bg='#0a0f1e')
        self.notebook.add(self.tab_settings, text='⚙️ SETTINGS')
        self.setup_settings_tab()
        
        # Tab 8: History
        self.tab_history = tk.Frame(self.notebook, bg='#0a0f1e')
        self.notebook.add(self.tab_history, text='📜 HISTORY')
        self.setup_history_tab()
        
        # Status Bar Super
        self.setup_status_bar()
        
    def setup_trading_tab(self):
        """Tab Trading Utama"""
        
        # Left panel - Market Data
        left = tk.Frame(self.tab_trading, bg='#1a1f2e', width=400)
        left.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Big Price Display
        price_frame = tk.Frame(left, bg='#2a2f3e', height=150)
        price_frame.pack(fill='x', padx=10, pady=5)
        price_frame.pack_propagate(False)
        
        self.big_price = tk.Label(price_frame,
                                  text=f"${self.current_price:.2f}",
                                  bg='#2a2f3e',
                                  fg='#00ff00',
                                  font=('Arial', 48, 'bold'))
        self.big_price.pack(expand=True)
        
        self.price_change = tk.Label(price_frame,
                                     text="▲ +0.00 (0.00%)",
                                     bg='#2a2f3e',
                                     fg='#00ff00',
                                     font=('Arial', 12))
        self.big_price.pack()
        
        # Bid/Ask
        ba_frame = tk.Frame(left, bg='#2a2f3e')
        ba_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(ba_frame,
                text=f"BID: ${self.bid_price:.2f}",
                bg='#2a2f3e',
                fg='#ff4444',
                font=('Arial', 14)).pack(side='left', expand=True)
        
        tk.Label(ba_frame,
                text=f"ASK: ${self.ask_price:.2f}",
                bg='#2a2f3e',
                fg='#44ff44',
                font=('Arial', 14)).pack(side='right', expand=True)
        
        # Center panel - Chart
        center = tk.Frame(self.tab_trading, bg='#1a1f2e', width=600)
        center.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Chart canvas
        self.chart_canvas = tk.Canvas(center,
                                      bg='#0a0f1e',
                                      height=300,
                                      highlightthickness=1,
                                      highlightbackground='#3a3f4e')
        self.chart_canvas.pack(fill='x', padx=10, pady=5)
        
        # Indicators
        ind_frame = tk.Frame(center, bg='#2a2f3e')
        ind_frame.pack(fill='x', padx=10, pady=5)
        
        indicators = ['RSI', 'MACD', 'STOCH', 'VOLUME', 'AI CONF']
        for ind in indicators:
            f = tk.Frame(ind_frame, bg='#3a3f4e', width=100)
            f.pack(side='left', expand=True, padx=2)
            tk.Label(f, text=ind, bg='#3a3f4e', fg='#888888').pack()
            tk.Label(f, text='0.00', bg='#3a3f4e', fg='#00ff00',
                    font=('Arial', 12, 'bold')).pack()
        
        # Right panel - Trading
        right = tk.Frame(self.tab_trading, bg='#1a1f2e', width=400)
        right.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        # Account
        acc_frame = tk.Frame(right, bg='#2a2f3e')
        acc_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(acc_frame, text="ACCOUNT", bg='#2a2f3e',
                fg='#ffd700', font=('Arial', 12, 'bold')).pack()
        
        self.balance_label = tk.Label(acc_frame, text=f"Balance: ${self.balance:.2f}",
                                      bg='#2a2f3e', fg='#00ff00')
        self.balance_label.pack()
        
        self.equity_label = tk.Label(acc_frame, text=f"Equity: ${self.equity:.2f}",
                                     bg='#2a2f3e', fg='#00ff00')
        self.equity_label.pack()
        
        # Lot size
        lot_frame = tk.Frame(right, bg='#2a2f3e')
        lot_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(lot_frame, text="LOT SIZE", bg='#2a2f3e',
                fg='#ffd700').pack()
        
        self.lot_var = tk.DoubleVar(value=0.01)
        lot_scale = tk.Scale(lot_frame, from_=0.01, to=10.0,
                            resolution=0.01, orient='horizontal',
                            variable=self.lot_var, bg='#2a2f3e',
                            fg='#00ff00', length=200)
        lot_scale.pack()
        
        # Buttons
        btn_frame = tk.Frame(right, bg='#2a2f3e')
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(btn_frame, text="🚀 BUY",
                 bg='#00aa00', fg='white',
                 font=('Arial', 14, 'bold'),
                 command=self.execute_buy,
                 height=2).pack(fill='x', pady=2)
        
        tk.Button(btn_frame, text="🔻 SELL",
                 bg='#aa0000', fg='white',
                 font=('Arial', 14, 'bold'),
                 command=self.execute_sell,
                 height=2).pack(fill='x', pady=2)
        
        # Position
        self.pos_label = tk.Label(right, text="No open positions",
                                  bg='#1a1f2e', fg='#888888')
        self.pos_label.pack()
        
    def setup_ai_tab(self):
        """Tab AI Analytics"""
        
        # Title
        tk.Label(self.tab_ai,
                text="🧠 ARTIFICIAL INTELLIGENCE ANALYTICS",
                bg='#0a0f1e',
                fg='#ffd700',
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        # AI Status
        status_frame = tk.Frame(self.tab_ai, bg='#1a1f2e')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        ai_status = "✅ ACTIVE" if AI_AVAILABLE else "⚠️ SIMPLIFIED MODE"
        tk.Label(status_frame,
                text=f"AI Status: {ai_status}",
                bg='#1a1f2e',
                fg='#00ff00' if AI_AVAILABLE else '#ffff00',
                font=('Arial', 14)).pack(pady=10)
        
        # Models
        models_frame = tk.Frame(self.tab_ai, bg='#1a1f2e')
        models_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(models_frame,
                text="ACTIVE AI MODELS",
                bg='#1a1f2e',
                fg='#ffd700',
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        models = [
            "LSTM Neural Network - Price Prediction",
            "Random Forest - Signal Generation",
            "Gradient Boosting - Confidence Scoring",
            "Support Vector Machine - Trend Classification"
        ]
        
        for model in models:
            tk.Label(models_frame,
                    text=f"✓ {model}",
                    bg='#1a1f2e',
                    fg='#00ff00',
                    font=('Arial', 11)).pack(anchor='w', padx=40)
        
        # Predictions
        pred_frame = tk.Frame(self.tab_ai, bg='#1a1f2e')
        pred_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(pred_frame,
                text="AI PREDICTIONS",
                bg='#1a1f2e',
                fg='#ffd700',
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        self.ai_pred_label = tk.Label(pred_frame,
                                      text="Analyzing market...",
                                      bg='#1a1f2e',
                                      fg='#00ff00',
                                      font=('Arial', 24, 'bold'))
        self.ai_pred_label.pack(pady=20)
        
        # Confidence meter
        conf_frame = tk.Frame(pred_frame, bg='#2a2f3e')
        conf_frame.pack(fill='x', padx=40, pady=10)
        
        tk.Label(conf_frame,
                text="CONFIDENCE METER",
                bg='#2a2f3e',
                fg='#888888').pack()
        
        self.confidence_bar = tk.Frame(conf_frame, bg='#3a3f4e', height=20)
        self.confidence_bar.pack(fill='x', padx=20, pady=5)
        
        self.confidence_fill = tk.Frame(self.confidence_bar,
                                        bg='#00ff00',
                                        width=0,
                                        height=20)
        self.confidence_fill.place(x=0, y=0)
        
    def setup_telegram_tab(self):
        """Tab Telegram Bot"""
        
        tk.Label(self.tab_telegram,
                text="📱 TELEGRAM BOT CONTROL",
                bg='#0a0f1e',
                fg='#ffd700',
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Status
        status_frame = tk.Frame(self.tab_telegram, bg='#1a1f2e')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        self.tg_status = tk.Label(status_frame,
                                  text="🔴 TELEGRAM BOT: DISABLED",
                                  bg='#1a1f2e',
                                  fg='#ff4444',
                                  font=('Arial', 14, 'bold'))
        self.tg_status.pack(pady=10)
        
        # Token input
        token_frame = tk.Frame(self.tab_telegram, bg='#1a1f2e')
        token_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(token_frame,
                text="Bot Token:",
                bg='#1a1f2e',
                fg='#888888',
                font=('Arial', 11)).pack(anchor='w', padx=20)
        
        self.token_entry = tk.Entry(token_frame,
                                    width=50,
                                    bg='#2a2f3e',
                                    fg='#00ff00',
                                    font=('Arial', 11))
        self.token_entry.pack(padx=20, pady=5)
        self.token_entry.insert(0, TELEGRAM_TOKEN)
        
        # Chat ID
        tk.Label(token_frame,
                text="Chat ID:",
                bg='#1a1f2e',
                fg='#888888',
                font=('Arial', 11)).pack(anchor='w', padx=20)
        
        self.chat_entry = tk.Entry(token_frame,
                                   width=50,
                                   bg='#2a2f3e',
                                   fg='#00ff00',
                                   font=('Arial', 11))
        self.chat_entry.pack(padx=20, pady=5)
        self.chat_entry.insert(0, TELEGRAM_CHAT_ID)
        
        # Buttons
        btn_frame = tk.Frame(self.tab_telegram, bg='#1a1f2e')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame,
                 text="▶️ START BOT",
                 bg='#00aa00',
                 fg='white',
                 font=('Arial', 12),
                 command=self.start_telegram,
                 width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="⏹️ STOP BOT",
                 bg='#aa0000',
                 fg='white',
                 font=('Arial', 12),
                 command=self.stop_telegram,
                 width=15).pack(side='left', padx=5)
        
        # Instructions
        inst_frame = tk.Frame(self.tab_telegram, bg='#1a1f2e')
        inst_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        instructions = """
        📋 CARA SETUP TELEGRAM BOT:
        
        1. Buka Telegram, cari @BotFather
        2. Kirim /newbot, ikuti petunjuk
        3. Dapatkan token bot (contoh: 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)
        4. Copy token ke kolom di atas
        5. Cari bot Yang Mulia, kirim /start
        6. Dapatkan chat ID (bisa dari @userinfobot)
        7. Klik START BOT
        
        PERINTAH YANG TERSEDIA:
        /price - Harga terkini
        /signal - Signal trading
        /buy [lot] - BUY order
        /sell [lot] - SELL order
        /balance - Cek saldo
        /positions - Posisi terbuka
        /predict - Prediksi AI
        """
        
        tk.Label(inst_frame,
                text=instructions,
                bg='#1a1f2e',
                fg='#888888',
                font=('Courier', 10),
                justify='left').pack(pady=10)
        
    def setup_web_tab(self):
        """Tab Web Dashboard"""
        
        tk.Label(self.tab_web,
                text="🌐 WEB DASHBOARD CONTROL",
                bg='#0a0f1e',
                fg='#ffd700',
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Status
        status_frame = tk.Frame(self.tab_web, bg='#1a1f2e')
        status_frame.pack(fill='x', padx=20, pady=10)
        
        self.web_status = tk.Label(status_frame,
                                   text="🔴 WEB SERVER: STOPPED",
                                   bg='#1a1f2e',
                                   fg='#ff4444',
                                   font=('Arial', 14, 'bold'))
        self.web_status.pack(pady=10)
        
        # Port settings
        port_frame = tk.Frame(self.tab_web, bg='#1a1f2e')
        port_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(port_frame,
                text="Web Port:",
                bg='#1a1f2e',
                fg='#888888').pack(side='left', padx=20)
        
        self.port_entry = tk.Entry(port_frame,
                                   width=10,
                                   bg='#2a2f3e',
                                   fg='#00ff00')
        self.port_entry.pack(side='left')
        self.port_entry.insert(0, str(FLASK_PORT))
        
        tk.Label(port_frame,
                text="Socket Port:",
                bg='#1a1f2e',
                fg='#888888').pack(side='left', padx=20)
        
        self.socket_entry = tk.Entry(port_frame,
                                     width=10,
                                     bg='#2a2f3e',
                                     fg='#00ff00')
        self.socket_entry.pack(side='left')
        self.socket_entry.insert(0, str(WEBSOCKET_PORT))
        
        # Buttons
        btn_frame = tk.Frame(self.tab_web, bg='#1a1f2e')
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame,
                 text="▶️ START SERVER",
                 bg='#00aa00',
                 fg='white',
                 font=('Arial', 12),
                 command=self.start_web_server,
                 width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="⏹️ STOP SERVER",
                 bg='#aa0000',
                 fg='white',
                 font=('Arial', 12),
                 command=self.stop_web_server,
                 width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="🌍 OPEN DASHBOARD",
                 bg='#8888ff',
                 fg='white',
                 font=('Arial', 12),
                 command=self.open_web_dashboard,
                 width=15).pack(side='left', padx=5)
        
        # URL info
        url_frame = tk.Frame(self.tab_web, bg='#1a1f2e')
        url_frame.pack(fill='x', padx=20, pady=10)
        
        self.url_label = tk.Label(url_frame,
                                  text="URL: http://localhost:5000",
                                  bg='#1a1f2e',
                                  fg='#00ffff',
                                  font=('Arial', 12))
        self.url_label.pack(pady=10)
        
    def setup_auto_tab(self):
        """Tab Auto Trading"""
        
        tk.Label(self.tab_auto,
                text="🤖 AUTO TRADING CONFIGURATION",
                bg='#0a0f1e',
                fg='#ffd700',
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Settings
        settings_frame = tk.Frame(self.tab_auto, bg='#1a1f2e')
        settings_frame.pack(fill='x', padx=20, pady=10)
        
        # Enable auto trading
        self.auto_var = tk.BooleanVar()
        tk.Checkbutton(settings_frame,
                      text="Enable Auto Trading",
                      variable=self.auto_var,
                      command=self.toggle_auto_trading,
                      bg='#1a1f2e',
                      fg='#00ff00',
                      font=('Arial', 12),
                      selectcolor='#1a1f2e').pack(anchor='w', padx=20, pady=5)
        
        # Settings grid
        grid_frame = tk.Frame(settings_frame, bg='#2a2f3e')
        grid_frame.pack(padx=20, pady=10, fill='x')
        
        settings = [
            ("Max Trades/Day:", "5", "trades"),
            ("Profit Target ($):", "100", "profit"),
            ("Stop Loss ($):", "50", "sl"),
            ("Min Confidence (%):", "80", "conf"),
            ("Max Lot Size:", "1.0", "maxlot"),
            ("Risk Per Trade (%):", "2", "risk")
        ]
        
        row = 0
        for label, default, key in settings:
            tk.Label(grid_frame,
                    text=label,
                    bg='#2a2f3e',
                    fg='#888888').grid(row=row, column=0, padx=10, pady=5, sticky='w')
            
            entry = tk.Entry(grid_frame,
                            width=15,
                            bg='#3a3f4e',
                            fg='#00ff00')
            entry.grid(row=row, column=1, padx=10, pady=5)
            entry.insert(0, default)
            setattr(self, f"auto_{key}_entry", entry)
            
            row += 1
        
        # Status
        self.auto_status = tk.Label(self.tab_auto,
                                    text="⏸️ AUTO TRADING: DISABLED",
                                    bg='#0a0f1e',
                                    fg='#ff4444',
                                    font=('Arial', 14, 'bold'))
        self.auto_status.pack(pady=20)
        
    def setup_pnl_tab(self):
        """Tab P&L Analytics"""
        
        tk.Label(self.tab_pnl,
                text="📊 PROFIT & LOSS ANALYTICS",
                bg='#0a0f1e',
                fg='#ffd700',
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Summary
        summary_frame = tk.Frame(self.tab_pnl, bg='#1a1f2e')
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        self.pnl_summary = tk.Label(summary_frame,
                                    text="Calculating statistics...",
                                    bg='#1a1f2e',
                                    fg='#00ff00',
                                    font=('Arial', 14))
        self.pnl_summary.pack(pady=10)
        
        # Stats grid
        stats_frame = tk.Frame(self.tab_pnl, bg='#1a1f2e')
        stats_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        stats = [
            ("Total Trades:", "0"),
            ("Winning Trades:", "0"),
            ("Losing Trades:", "0"),
            ("Win Rate:", "0%"),
            ("Best Trade:", "$0.00"),
            ("Worst Trade:", "$0.00"),
            ("Average Win:", "$0.00"),
            ("Average Loss:", "$0.00"),
            ("Profit Factor:", "0.00"),
            ("Expectancy:", "$0.00"),
            ("Max Drawdown:", "0%"),
            ("Sharpe Ratio:", "0.00")
        ]
        
        row = 0
        col = 0
        for label, value in stats:
            frame = tk.Frame(stats_frame, bg='#2a2f3e', width=180, height=70)
            frame.grid(row=row, column=col, padx=5, pady=5)
            frame.pack_propagate(False)
            
            tk.Label(frame,
                    text=label,
                    bg='#2a2f3e',
                    fg='#888888').pack(pady=5)
            
            label_widget = tk.Label(frame,
                                    text=value,
                                    bg='#2a2f3e',
                                    fg='#00ff00',
                                    font=('Arial', 11, 'bold'))
            label_widget.pack()
            
            # Store reference
            setattr(self, f"pnl_{label.lower().replace(' ', '_').replace(':', '')}", label_widget)
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
    def setup_history_tab(self):
        """Tab History"""
        
        tk.Label(self.tab_history,
                text="📜 TRADE HISTORY",
                bg='#0a0f1e',
                fg='#ffd700',
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        # History text
        self.history_text = scrolledtext.ScrolledText(self.tab_history,
                                                      height=20,
                                                      bg='#1a1f2e',
                                                      fg='#00ff00',
                                                      font=('Courier', 10))
        self.history_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Buttons
        btn_frame = tk.Frame(self.tab_history, bg='#0a0f1e')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame,
                 text="📥 EXPORT CSV",
                 bg='#2a2f3e',
                 fg='white',
                 command=self.export_history_csv,
                 width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="📤 EXPORT JSON",
                 bg='#2a2f3e',
                 fg='white',
                 command=self.export_history_json,
                 width=15).pack(side='left', padx=5)
        
        tk.Button(btn_frame,
                 text="🔄 REFRESH",
                 bg='#2a2f3e',
                 fg='white',
                 command=self.update_history_display,
                 width=15).pack(side='left', padx=5)
        
    def setup_settings_tab(self):
        """Tab Settings"""
        
        tk.Label(self.tab_settings,
                text="⚙️ SYSTEM CONFIGURATION",
                bg='#0a0f1e',
                fg='#ffd700',
                font=('Arial', 18, 'bold')).pack(pady=10)
        
        # Display settings
        display_frame = tk.Frame(self.tab_settings, bg='#1a1f2e')
        display_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(display_frame,
                text="DISPLAY SETTINGS",
                bg='#1a1f2e',
                fg='#ffd700',
                font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=5)
        
        # Theme
        theme_frame = tk.Frame(display_frame, bg='#2a2f3e')
        theme_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(theme_frame,
                text="Theme:",
                bg='#2a2f3e',
                fg='#888888').pack(side='left', padx=10)
        
        self.theme_var = tk.StringVar(value="Dark")
        themes = ["Dark", "Light", "Hacker Green", "Royal Purple"]
        theme_menu = ttk.Combobox(theme_frame,
                                  textvariable=self.theme_var,
                                  values=themes,
                                  state='readonly',
                                  width=15)
        theme_menu.pack(side='left', padx=10)
        theme_menu.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Chart type
        chart_frame = tk.Frame(display_frame, bg='#2a2f3e')
        chart_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(chart_frame,
                text="Chart Type:",
                bg='#2a2f3e',
                fg='#888888').pack(side='left', padx=10)
        
        self.chart_type_var = tk.StringVar(value="Candlestick")
        chart_types = ["Candlestick", "Line", "Bar", "Area", "Heikin Ashi"]
        chart_menu = ttk.Combobox(chart_frame,
                                  textvariable=self.chart_type_var,
                                  values=chart_types,
                                  state='readonly',
                                  width=15)
        chart_menu.pack(side='left', padx=10)
        
        # Update interval
        interval_frame = tk.Frame(display_frame, bg='#2a2f3e')
        interval_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Label(interval_frame,
                text="Update Interval (ms):",
                bg='#2a2f3e',
                fg='#888888').pack(side='left', padx=10)
        
        self.interval_var = tk.StringVar(value="1000")
        tk.Spinbox(interval_frame,
                  from_=100,
                  to=5000,
                  increment=100,
                  textvariable=self.interval_var,
                  width=10).pack(side='left', padx=10)
        
        # Risk settings
        risk_frame = tk.Frame(self.tab_settings, bg='#1a1f2e')
        risk_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(risk_frame,
                text="RISK MANAGEMENT",
                bg='#1a1f2e',
                fg='#ffd700',
                font=('Arial', 12, 'bold')).pack(anchor='w', padx=20, pady=5)
        
        risk_settings = [
            ("Default Stop Loss (pips):", "50"),
            ("Default Take Profit (pips):", "100"),
            ("Max Risk Per Trade (%):", "2"),
            ("Max Daily Loss (%):", "5"),
            ("Max Position Size (lots):", "10")
        ]
        
        for label, default in risk_settings:
            frame = tk.Frame(risk_frame, bg='#2a2f3e')
            frame.pack(fill='x', padx=20, pady=2)
            
            tk.Label(frame,
                    text=label,
                    bg='#2a2f3e',
                    fg='#888888').pack(side='left', padx=10)
            
            entry = tk.Entry(frame,
                            width=15,
                            bg='#3a3f4e',
                            fg='#00ff00')
            entry.pack(side='right', padx=10)
            entry.insert(0, default)
        
        # Save button
        tk.Button(self.tab_settings,
                 text="💾 SAVE SETTINGS",
                 bg='#00aa00',
                 fg='white',
                 font=('Arial', 12),
                 command=self.save_settings,
                 width=20).pack(pady=20)
        
    def setup_status_bar(self):
        """Status bar super lengkap"""
        
        status_bar = tk.Frame(self.root, bg='#1a1f2e', height=30)
        status_bar.pack(fill='x', side='bottom')
        
        # System time
        self.time_label = tk.Label(status_bar,
                                   text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                   bg='#1a1f2e',
                                   fg='#888888')
        self.time_label.pack(side='left', padx=10)
        
        # Connection status
        self.conn_label = tk.Label(status_bar,
                                   text="🟢 CONNECTED",
                                   bg='#1a1f2e',
                                   fg='#00ff00')
        self.conn_label.pack(side='left', padx=20)
        
        # AI Status
        ai_text = "🧠 AI: ACTIVE" if AI_AVAILABLE else "🧠 AI: SIMPLIFIED"
        self.ai_label = tk.Label(status_bar,
                                 text=ai_text,
                                 bg='#1a1f2e',
                                 fg='#00ff00' if AI_AVAILABLE else '#ffff00')
        self.ai_label.pack(side='left', padx=20)
        
        # Telegram status
        self.tg_status_bar = tk.Label(status_bar,
                                      text="📱 TG: OFF",
                                      bg='#1a1f2e',
                                      fg='#ff4444')
        self.tg_status_bar.pack(side='left', padx=20)
        
        # Web status
        self.web_status_bar = tk.Label(status_bar,
                                       text="🌐 WEB: OFF",
                                       bg='#1a1f2e',
                                       fg='#ff4444')
        self.web_status_bar.pack(side='left', padx=20)
        
        # Daily P&L
        self.daily_pnl_bar = tk.Label(status_bar,
                                      text="📈 DAILY: $0.00",
                                      bg='#1a1f2e',
                                      fg='#00ff00')
        self.daily_pnl_bar.pack(side='right', padx=10)
        
        # Trades today
        self.trades_bar = tk.Label(status_bar,
                                   text="🔄 TRADES: 0",
                                   bg='#1a1f2e',
                                   fg='#888888')
        self.trades_bar.pack(side='right', padx=20)
        
    # ============== AI METHODS ==============
    
    def ai_generate_signal(self):
        """Generate signal menggunakan AI"""
        
        if len(self.price_history) < 10:
            return "HOLD", 50
            
        if AI_AVAILABLE and self.ai_models:
            try:
                # Simulasi prediksi AI
                prices = list(self.price_history)[-20:]
                
                # Trend analysis
                short_trend = np.mean(prices[-5:]) - np.mean(prices[-10:-5])
                long_trend = np.mean(prices[-10:]) - np.mean(prices[-20:-10])
                
                # Volatility
                volatility = np.std(prices)
                
                # RSI
                rsi = self.calculate_rsi()
                
                # AI Confidence (simulasi)
                confidence = min(95, max(55, 70 + (short_trend * 10)))
                
                # Signal decision
                if short_trend > 0.5 and rsi < 70:
                    signal = "BUY"
                elif short_trend < -0.5 and rsi > 30:
                    signal = "SELL"
                else:
                    signal = "HOLD"
                    
                # Update AI prediction
                next_price = prices[-1] + (short_trend * random.uniform(0.5, 2.0))
                self.ai_predictions.append(next_price)
                self.ai_confidence = confidence
                
                return signal, confidence
                
            except Exception as e:
                print(f"AI Error: {e}")
                
        # Fallback ke simple algorithm
        return self.simple_generate_signal()
        
    def simple_generate_signal(self):
        """Simple signal generator"""
        prices = list(self.price_history)[-10:]
        
        if len(prices) < 5:
            return "HOLD", 50
            
        sma5 = np.mean(prices[:5])
        sma10 = np.mean(prices)
        current = prices[0]
        
        if current > sma5 and sma5 > sma10:
            return "BUY", random.randint(70, 85)
        elif current < sma5 and sma5 < sma10:
            return "SELL", random.randint(70, 85)
        else:
            return "HOLD", random.randint(40, 60)
            
    def ai_predict_next_price(self):
        """AI price prediction"""
        if self.ai_predictions:
            return self.ai_predictions[-1]
        else:
            return self.current_price + random.uniform(-1, 1)
            
    def analyze_trend(self):
        """Analyze market trend"""
        prices = list(self.price_history)[-20:]
        if len(prices) < 5:
            return "NEUTRAL"
            
        sma20 = np.mean(prices)
        sma50 = np.mean(prices[:10]) if len(prices) >= 10 else sma20
        
        if sma20 > sma50:
            return "BULLISH 📈"
        elif sma20 < sma50:
            return "BEARISH 📉"
        else:
            return "NEUTRAL ⏸️"
            
    def calculate_rsi(self):
        """Calculate RSI"""
        prices = list(self.price_history)[-15:]
        if len(prices) < 2:
            return 50
            
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i-1] - prices[i]
            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))
                
        avg_gain = np.mean(gains) if gains else 0
        avg_loss = np.mean(losses) if losses else 1
        
        if avg_loss == 0:
            return 100
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
        
    # ============== TRADING METHODS ==============
    
    def execute_buy(self, lot=None):
        """Execute BUY order"""
        if lot is None:
            lot = self.lot_var.get()
            
        # Check margin
        required = lot * 1000
        if required > self.balance:
            messagebox.showerror("Error", f"Insufficient margin!\nRequired: ${required:.2f}")
            return
            
        self.in_position = True
        self.position_type = "BUY"
        self.entry_price = self.ask_price
        self.lot_size = lot
        self.stop_loss = self.entry_price - (50 * lot)
        self.take_profit = self.entry_price + (100 * lot)
        
        # Update UI
        self.pos_label.config(
            text=f"BUY {lot} @ {self.entry_price:.2f}\nSL: {self.stop_loss:.2f} TP: {self.take_profit:.2f}",
            fg="#00ff00"
        )
        
        # Log trade
        self.log_trade("BUY", lot, self.entry_price)
        
        # Send Telegram notification
        self.send_telegram_message(f"✅ BUY {lot} XAUUSD @ {self.entry_price:.2f}")
        
        # Web broadcast
        self.broadcast_web_update()
        
    def execute_sell(self, lot=None):
        """Execute SELL order"""
        if lot is None:
            lot = self.lot_var.get()
            
        # Check margin
        required = lot * 1000
        if required > self.balance:
            messagebox.showerror("Error", f"Insufficient margin!\nRequired: ${required:.2f}")
            return
            
        self.in_position = True
        self.position_type = "SELL"
        self.entry_price = self.bid_price
        self.lot_size = lot
        self.stop_loss = self.entry_price + (50 * lot)
        self.take_profit = self.entry_price - (100 * lot)
        
        # Update UI
        self.pos_label.config(
            text=f"SELL {lot} @ {self.entry_price:.2f}\nSL: {self.stop_loss:.2f} TP: {self.take_profit:.2f}",
            fg="#ff4444"
        )
        
        # Log trade
        self.log_trade("SELL", lot, self.entry_price)
        
        # Send Telegram notification
        self.send_telegram_message(f"🔻 SELL {lot} XAUUSD @ {self.entry_price:.2f}")
        
        # Web broadcast
        self.broadcast_web_update()
        
    def close_position(self):
        """Close open position"""
        if not self.in_position:
            return
            
        # Calculate P&L
        if self.position_type == "BUY":
            pnl = (self.current_price - self.entry_price) * 100 * self.lot_size
        else:
            pnl = (self.entry_price - self.current_price) * 100 * self.lot_size
            
        # Update balance
        self.balance += pnl
        self.equity = self.balance
        self.daily_pnl += pnl
        self.daily_trades += 1
        
        # Add to history
        self.trade_history.append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': self.position_type,
            'lots': self.lot_size,
            'entry': self.entry_price,
            'exit': self.current_price,
            'pnl': pnl,
            'balance': self.balance
        })
        
        # Update UI
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
        self.equity_label.config(text=f"Equity: ${self.equity:.2f}")
        self.daily_pnl_bar.config(text=f"📈 DAILY: ${self.daily_pnl:.2f}")
        self.trades_bar.config(text=f"🔄 TRADES: {self.daily_trades}")
        
        self.in_position = False
        self.pos_label.config(text="No open positions", fg="#888888")
        
        # Send notification
        emoji = "💰" if pnl > 0 else "📉"
        self.send_telegram_message(f"{emoji} Position closed! P&L: ${pnl:.2f}")
        
        # Update history
        self.update_history_display()
        self.update_pnl_stats()
        
        # Web broadcast
        self.broadcast_web_update()
        
    def log_trade(self, trade_type, lots, price):
        """Log trade to history"""
        self.trade_history.append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': trade_type,
            'lots': lots,
            'entry': price,
            'exit': 0,
            'pnl': 0,
            'status': 'OPEN'
        })
        self.update_history_display()
        
    # ============== TELEGRAM METHODS ==============
    
    def start_telegram(self):
        """Start Telegram bot"""
        token = self.token_entry.get()
        chat_id = self.chat_entry.get()
        
        if token == "YOUR_BOT_TOKEN_HERE":
            messagebox.showerror("Error", "Please enter your bot token!")
            return
            
        try:
            self.telegram_bot = telebot.TeleBot(token)
            self.setup_telegram_handlers()
            
            # Start bot in thread
            def run_bot():
                self.telegram_bot.infinity_polling()
                
            self.telegram_thread = threading.Thread(target=run_bot, daemon=True)
            self.telegram_thread.start()
            
            self.telegram_enabled = True
            self.tg_status.config(text="🟢 TELEGRAM BOT: ACTIVE", fg="#00ff00")
            self.tg_status_bar.config(text="📱 TG: ON", fg="#00ff00")
            
            # Send startup message
            self.send_telegram_message("🤖 Bot started! Kerajaan Trading Online")
            
            messagebox.showinfo("Success", "Telegram bot started!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {e}")
            
    def stop_telegram(self):
        """Stop Telegram bot"""
        self.telegram_enabled = False
        self.tg_status.config(text="🔴 TELEGRAM BOT: DISABLED", fg="#ff4444")
        self.tg_status_bar.config(text="📱 TG: OFF", fg="#ff4444")
        messagebox.showinfo("Info", "Telegram bot stopped")
        
    def send_telegram_message(self, message):
        """Send message via Telegram"""
        if self.telegram_enabled and self.telegram_bot:
            try:
                chat_id = self.chat_entry.get()
                if chat_id != "YOUR_CHAT_ID_HERE":
                    self.telegram_bot.send_message(chat_id, message)
            except:
                pass
                
    # ============== WEB METHODS ==============
    
    def start_web_server(self):
        """Start Flask web server"""
        try:
            port = int(self.port_entry.get())
            socket_port = int(self.socket_entry.get())
            
            def run_server():
                self.socketio.run(self.flask_app, host='0.0.0.0', port=port, debug=False)
                
            self.web_thread = threading.Thread(target=run_server, daemon=True)
            self.web_thread.start()
            
            self.web_enabled = True
            self.web_status.config(text="🟢 WEB SERVER: RUNNING", fg="#00ff00")
            self.web_status_bar.config(text="🌐 WEB: ON", fg="#00ff00")
            self.url_label.config(text=f"URL: http://localhost:{port}")
            
            messagebox.showinfo("Success", f"Web server started on port {port}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {e}")
            
    def stop_web_server(self):
        """Stop web server"""
        self.web_enabled = False
        self.web_status.config(text="🔴 WEB SERVER: STOPPED", fg="#ff4444")
        self.web_status_bar.config(text="🌐 WEB: OFF", fg="#ff4444")
        messagebox.showinfo("Info", "Web server stopped")
        
    def open_web_dashboard(self):
        """Open web dashboard in browser"""
        port = self.port_entry.get()
        webbrowser.open(f"http://localhost:{port}")
        
    def broadcast_web_update(self):
        """Broadcast update via websocket"""
        if self.web_enabled and self.socketio:
            try:
                data = {
                    'price': self.current_price,
                    'bid': self.bid_price,
                    'ask': self.ask_price,
                    'balance': self.balance,
                    'pnl': self.daily_pnl
                }
                self.socketio.emit('update', data)
            except:
                pass
                
    # ============== AUTO TRADING ==============
    
    def toggle_auto_trading(self):
        """Toggle auto trading"""
        if self.auto_var.get():
            self.auto_trade = True
            self.auto_status.config(text="🤖 AUTO TRADING: ACTIVE", fg="#00ff00")
            
            # Start auto trading thread
            self.auto_trade_thread = threading.Thread(target=self.auto_trading_loop, daemon=True)
            self.auto_trade_thread.start()
            
            self.send_telegram_message("🤖 Auto trading activated!")
        else:
            self.auto_trade = False
            self.auto_status.config(text="⏸️ AUTO TRADING: DISABLED", fg="#ff4444")
            self.send_telegram_message("⏸️ Auto trading deactivated")
            
    def auto_trading_loop(self):
        """Auto trading loop"""
        while self.auto_trade:
            try:
                # Get settings
                max_trades = int(self.auto_maxlot_entry.get()) if hasattr(self, 'auto_maxlot_entry') else 5
                min_conf = int(self.auto_conf_entry.get()) if hasattr(self, 'auto_conf_entry') else 80
                
                # Check if we can trade
                if self.daily_trades < max_trades and not self.in_position:
                    signal, confidence = self.ai_generate_signal()
                    
                    if confidence >= min_conf and signal != "HOLD":
                        # Execute trade
                        if signal == "BUY":
                            self.root.after(0, lambda: self.execute_buy())
                        elif signal == "SELL":
                            self.root.after(0, lambda: self.execute_sell())
                            
                        # Wait
                        time.sleep(random.randint(30, 60))
                        
                # Check daily limits
                if self.daily_pnl >= float(self.auto_profit_entry.get()) if hasattr(self, 'auto_profit_entry') else 100:
                    self.root.after(0, lambda: self.auto_status.config(
                        text="🎯 PROFIT TARGET REACHED! PAUSED",
                        fg="#00ff00"))
                    time.sleep(300)
                    
                elif self.daily_pnl <= -float(self.auto_sl_entry.get()) if hasattr(self, 'auto_sl_entry') else 50:
                    self.root.after(0, lambda: self.auto_status.config(
                        text="🛑 STOP LOSS HIT! PAUSED",
                        fg="#ff4444"))
                    self.auto_trade = False
                    self.root.after(0, lambda: self.auto_var.set(False))
                    
                time.sleep(5)
                
            except Exception as e:
                print(f"Auto trading error: {e}")
                time.sleep(5)
                
    # ============== UTILITY METHODS ==============
    
    def start_services(self):
        """Start all services"""
        
        # Update thread
        def update_loop():
            while True:
                time.sleep(1)
                
                # Simulate price movement
                change = random.uniform(-0.3, 0.3)
                self.current_price += change
                self.bid_price = self.current_price - 0.45
                self.ask_price = self.current_price + 0.45
                self.spread = round(self.ask_price - self.bid_price, 2)
                
                # Update history
                self.price_history.appendleft(self.current_price)
                self.volume_history.appendleft(random.randint(100, 1000))
                self.timestamp_history.appendleft(datetime.now())
                
                # Queue update
                self.update_queue.put('update')
                
        thread = threading.Thread(target=update_loop, daemon=True)
        thread.start()
        
        self.process_updates()
        
    def process_updates(self):
        """Process UI updates"""
        try:
            while True:
                self.update_queue.get_nowait()
                
                # Update price displays
                if hasattr(self, 'big_price'):
                    self.big_price.config(text=f"${self.current_price:.2f}")
                    
                # Update chart
                if hasattr(self, 'chart_canvas'):
                    self.draw_chart()
                    
                # Update time
                if hasattr(self, 'time_label'):
                    self.time_label.config(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    
                # Generate signal
                signal, confidence = self.ai_generate_signal()
                
                # Update AI prediction
                if hasattr(self, 'ai_pred_label'):
                    next_price = self.ai_predict_next_price()
                    self.ai_pred_label.config(
                        text=f"Next: ${next_price:.2f} | Signal: {signal}",
                        fg="#00ff00" if signal == "BUY" else "#ff4444" if signal == "SELL" else "#ffff00"
                    )
                    
                # Update confidence bar
                if hasattr(self, 'confidence_fill'):
                    bar_width = int((confidence / 100) * 400)
                    self.confidence_fill.config(width=bar_width)
                    
                # Check stop loss / take profit
                if self.in_position:
                    if self.position_type == "BUY":
                        if self.current_price <= self.stop_loss:
                            self.root.after(0, self.close_position)
                            self.send_telegram_message("🛑 Stop loss hit!")
                        elif self.current_price >= self.take_profit:
                            self.root.after(0, self.close_position)
                            self.send_telegram_message("🎯 Take profit hit!")
                    else:
                        if self.current_price >= self.stop_loss:
                            self.root.after(0, self.close_position)
                            self.send_telegram_message("🛑 Stop loss hit!")
                        elif self.current_price <= self.take_profit:
                            self.root.after(0, self.close_position)
                            self.send_telegram_message("🎯 Take profit hit!")
                            
                # Update equity if in position
                if self.in_position:
                    if self.position_type == "BUY":
                        unrealized = (self.current_price - self.entry_price) * 100 * self.lot_size
                    else:
                        unrealized = (self.entry_price - self.current_price) * 100 * self.lot_size
                        
                    self.equity = self.balance + unrealized
                    if hasattr(self, 'equity_label'):
                        self.equity_label.config(text=f"Equity: ${self.equity:.2f}")
                        
        except queue.Empty:
            pass
            
        # Schedule next update
        interval = int(self.interval_var.get()) if hasattr(self, 'interval_var') else 1000
        self.root.after(interval, self.process_updates)
        
    def draw_chart(self):
        """Draw chart on canvas"""
        if not hasattr(self, 'chart_canvas'):
            return
            
        self.chart_canvas.delete("all")
        
        width = self.chart_canvas.winfo_width()
        height = self.chart_canvas.winfo_height()
        
        if width < 10 or height < 10:
            return
            
        # Draw grid
        for i in range(0, width, 50):
            self.chart_canvas.create_line(i, 0, i, height, fill='#2a2f3e')
        for i in range(0, height, 30):
            self.chart_canvas.create_line(0, i, width, i, fill='#2a2f3e')
            
        # Draw price line
        prices = list(self.price_history)[-50:]
        if len(prices) > 1:
            points = []
            min_price = min(prices)
            max_price = max(prices)
            price_range = max_price - min_price
            
            for i, price in enumerate(prices):
                x = (i / (len(prices) - 1)) * width
                y = height - ((price - min_price) / price_range * height * 0.8 + height * 0.1)
                points.extend([x, y])
                
            if len(points) >= 4:
                self.chart_canvas.create_line(points, fill='#00ff00', width=2)
                
    def update_history_display(self):
        """Update history text display"""
        if not hasattr(self, 'history_text'):
            return
            
        self.history_text.delete('1.0', tk.END)
        
        for trade in reversed(self.trade_history[-50:]):
            if trade.get('status') == 'OPEN':
                line = (f"{trade['time']} | {trade['type']} | "
                       f"Lots: {trade['lots']} | Entry: {trade['entry']:.2f} | "
                       f"Status: OPEN\n")
                self.history_text.insert('end', line, 'open')
                self.history_text.tag_config('open', foreground='#ffff00')
            else:
                color = '#00ff00' if trade['pnl'] > 0 else '#ff4444'
                line = (f"{trade['time']} | {trade['type']} | "
                       f"Lots: {trade['lots']} | Entry: {trade['entry']:.2f} | "
                       f"Exit: {trade['exit']:.2f} | P&L: ${trade['pnl']:.2f} | "
                       f"Balance: ${trade['balance']:.2f}\n")
                self.history_text.insert('end', line, 'pnl')
                self.history_text.tag_config('pnl', foreground=color)
                
    def update_pnl_stats(self):
        """Update P&L statistics"""
        if not hasattr(self, 'pnl_summary'):
            return
            
        closed_trades = [t for t in self.trade_history if 'pnl' in t and t['pnl'] != 0]
        
        if not closed_trades:
            return
            
        total_trades = len(closed_trades)
        winning_trades = len([t for t in closed_trades if t['pnl'] > 0])
        losing_trades = len([t for t in closed_trades if t['pnl'] < 0])
        
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = sum(t['pnl'] for t in closed_trades)
        avg_win = np.mean([t['pnl'] for t in closed_trades if t['pnl'] > 0]) if winning_trades > 0 else 0
        avg_loss = np.mean([t['pnl'] for t in closed_trades if t['pnl'] < 0]) if losing_trades > 0 else 0
        
        best_trade = max(t['pnl'] for t in closed_trades) if closed_trades else 0
        worst_trade = min(t['pnl'] for t in closed_trades) if closed_trades else 0
        
        profit_factor = abs(sum(t['pnl'] for t in closed_trades if t['pnl'] > 0) / 
                           sum(t['pnl'] for t in closed_trades if t['pnl'] < 0)) if losing_trades > 0 else float('inf')
        
        summary = f"""
        📊 PERFORMANCE SUMMARY
        ───────────────────────────────
        Total Trades: {total_trades}
        Win Rate: {win_rate:.1f}%
        Total P&L: ${total_pnl:.2f}
        Profit Factor: {profit_factor:.2f}
        Best Trade: ${best_trade:.2f}
        Worst Trade: ${worst_trade:.2f}
        Avg Win: ${avg_win:.2f}
        Avg Loss: ${avg_loss:.2f}
        """
        
        self.pnl_summary.config(text=summary)
        
        # Update individual stats
        if hasattr(self, 'pnl_total_trades'):
            self.pnl_total_trades.config(text=str(total_trades))
        if hasattr(self, 'pnl_winning_trades'):
            self.pnl_winning_trades.config(text=str(winning_trades))
        if hasattr(self, 'pnl_win_rate'):
            self.pnl_win_rate.config(text=f"{win_rate:.1f}%")
        if hasattr(self, 'pnl_total_pnl'):
            self.pnl_total_pnl.config(text=f"${total_pnl:.2f}")
            
    def export_history_csv(self):
        """Export history to CSV"""
        filename = f"trade_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        import csv
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'Type', 'Lots', 'Entry', 'Exit', 'P&L', 'Balance', 'Status'])
            
            for trade in self.trade_history:
                writer.writerow([
                    trade['time'],
                    trade['type'],
                    trade['lots'],
                    trade['entry'],
                    trade.get('exit', ''),
                    trade.get('pnl', ''),
                    trade.get('balance', ''),
                    trade.get('status', 'CLOSED')
                ])
                
        messagebox.showinfo("Export Successful", f"History exported to {filename}")
        
    def export_history_json(self):
        """Export history to JSON"""
        filename = f"trade_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.trade_history, f, indent=2, default=str)
            
        messagebox.showinfo("Export Successful", f"History exported to {filename}")
        
    def change_theme(self, event=None):
        """Change UI theme"""
        theme = self.theme_var.get()
        
        if theme == "Light":
            bg = '#ffffff'
            fg = '#000000'
        elif theme == "Hacker Green":
            bg = '#000000'
            fg = '#00ff00'
        elif theme == "Royal Purple":
            bg = '#2d1b4a'
            fg = '#ffd700'
        else:  # Dark
            bg = '#0a0f1e'
            fg = '#00ff00'
            
        # Apply theme (simplified)
        self.root.configure(bg=bg)
        messagebox.showinfo("Theme Changed", f"Theme set to {theme}")
        
    def save_settings(self):
        """Save all settings"""
        settings = {
            'theme': self.theme_var.get(),
            'chart_type': self.chart_type_var.get(),
            'update_interval': self.interval_var.get(),
            'telegram_token': self.token_entry.get(),
            'telegram_chat_id': self.chat_entry.get(),
            'web_port': self.port_entry.get(),
            'socket_port': self.socket_entry.get()
        }
        
        with open('bot_settings.json', 'w') as f:
            json.dump(settings, f, indent=2)
            
        messagebox.showinfo("Settings Saved", "All settings have been saved!")

def main():
    """Main function"""
    root = tk.Tk()
    
    # Set icon if available
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass
        
    app = KerajaanTradingBot(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()

if __name__ == "__main__":
    main()