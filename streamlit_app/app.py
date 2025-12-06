import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
import sys
import requests
from dotenv import load_dotenv
from supabase import create_client
import plotly.express as px
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json
import tensorflow as tf
from PIL import Image


# Set page configuration
st.set_page_config(
    page_title="AgriTech",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🏆 ELITE ENTERPRISE DESIGN - World-Class AgriTech Intelligence Platform
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* ============================================
       💎 REFINED LUXURY COLOR SYSTEM
       Elite enterprise AgriTech palette
    ============================================ */
    :root {
        /* Deep Charcoal Foundation */
        --bg-primary: #0B0F12;
        --bg-secondary: #0F1419;
        --bg-tertiary: #141B22;
        --bg-card: #12171C;
        --bg-elevated: #16\1C23;
        --bg-overlay: #1A2129;
        
        /* Refined Emerald Intelligence */
        --emerald-primary: #10B981;
        --emerald-light: #34D399;
        --emerald-glow: rgba(16, 185, 129, 0.25);
        --teal-accent: #14B8A6;
        --cyan-subtle: #06B6D4;
        
        /* Precision Neutrals */
        --border-subtle: rgba(255, 255, 255, 0.06);
        --border-medium: rgba(255, 255, 255, 0.10);
        --border-strong: rgba(255, 255, 255, 0.15);
        
        /* Typography Hierarchy */
        --text-primary: #F9FAFB;
        --text-secondary: #D1D5DB;
        --text-tertiary: #9CA3AF;
        --text-muted: #6B7280;
        --text-disabled: #4B5563;
        
        /* Intelligent Accents */
        --accent-success: #10B981;
        --accent-warning: #F59E0B;
        --accent-error: #EF4444;
        --accent-info: #3B82F6;
        
        /* Elevation System */
        --elevation-1: 0 1px 3px rgba(0, 0, 0, 0.3), 0 1px 2px rgba(0, 0, 0, 0.2);
        --elevation-2: 0 4px 12px rgba(0, 0, 0, 0.4), 0 2px 4px rgba(0, 0, 0, 0.3);
        --elevation-3: 0 8px 24px rgba(0, 0, 0, 0.5), 0 4px 8px rgba(0, 0, 0, 0.4);
        --elevation-4: 0 16px 48px rgba(0, 0, 0, 0.6), 0 8px 16px rgba(0, 0, 0, 0.5);
        
        /* Glow Effects */
        --glow-emerald: 0 0 24px rgba(16, 185, 129, 0.2);
        --glow-subtle: 0 0 32px rgba(16, 185, 129, 0.1);
        --glow-strong: 0 0 48px rgba(16, 185, 129, 0.3);
    }
    
    /* ============================================
       🎯 ELITE FOUNDATION & RESETS
    ============================================ */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        font-feature-settings: 'cv11', 'ss01', 'ss02';
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Luxury Background with Vignette */
    .main {
        background: 
            radial-gradient(circle at 50% 0%, rgba(16, 185, 129, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 100% 100%, rgba(6, 182, 212, 0.02) 0%, transparent 50%),
            linear-gradient(180deg, #0B0F12 0%, #0F1419 50%, #0B0F12 100%);
        background-attachment: fixed;
        position: relative;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 50% 50%, transparent 0%, rgba(0, 0, 0, 0.3) 100%);
        pointer-events: none;
        z-index: 1;
    }
    
    .block-container {
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
        max-width: 1360px !important;
        position: relative;
        z-index: 2;
    }
    
    /* ============================================
       👑 ELITE HERO HEADER
       Floating luxury intelligence banner
    ============================================ */
    .premium-hero {
        position: relative;
        background: 
            linear-gradient(135deg, 
                rgba(16, 185, 129, 0.12) 0%,
                rgba(20, 184, 166, 0.08) 50%,
                rgba(6, 182, 212, 0.05) 100%),
            linear-gradient(180deg, 
                var(--bg-elevated) 0%,
                var(--bg-card) 100%);
        padding: 4rem 3.5rem;
        border-radius: 20px;
        margin-bottom: 3.5rem;
        overflow: hidden;
        box-shadow: 
            var(--elevation-4),
            var(--glow-subtle),
            0 0 0 1px var(--border-subtle) inset;
        border: 1px solid var(--border-medium);
        backdrop-filter: blur(24px);
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .premium-hero:hover {
        transform: translateY(-2px);
    }
    
    .premium-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(0, 255, 136, 0.15) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 20s ease-in-out infinite;
    }
    
    .premium-hero::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -10%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.1) 0%, transparent 70%);
        border-radius: 50%;
        animation: float 15s ease-in-out infinite reverse;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        33% { transform: translate(30px, -30px) rotate(120deg); }
        66% { transform: translate(-20px, 20px) rotate(240deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 10;
    }
    
    .hero-logo {
        font-size: 4rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 20px rgba(0, 255, 136, 0.5));
        animation: pulse-glow 3s ease-in-out infinite;
    }
    
    @keyframes pulse-glow {
        0%, 100% { filter: drop-shadow(0 4px 20px rgba(0, 255, 136, 0.5)); }
        50% { filter: drop-shadow(0 4px 40px rgba(0, 255, 136, 0.8)); }
    }
    
    .hero-title {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
        font-size: 3.75rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.03em;
        text-shadow: 0 2px 40px rgba(0, 0, 0, 0.5);
        line-height: 1.05;
        background: linear-gradient(135deg, #ffffff 0%, #d1fae5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.125rem;
        color: var(--text-secondary);
        margin: 1.25rem 0 0 0;
        font-weight: 500;
        letter-spacing: 0.005em;
        line-height: 1.6;
    }
    
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.65rem 1.5rem;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid var(--border-medium);
        border-radius: 100px;
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--emerald-light);
        margin-top: 2rem;
        backdrop-filter: blur(12px);
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.3),
            0 0 0 1px rgba(16, 185, 129, 0.1) inset;
        transition: all 0.3s ease;
    }
    
    .hero-badge:hover {
        background: rgba(16, 185, 129, 0.12);
        border-color: var(--emerald-primary);
        box-shadow: 
            0 6px 24px rgba(16, 185, 129, 0.2),
            0 0 0 1px rgba(16, 185, 129, 0.2) inset;
    }
    
    /* ============================================
       💎 UNIFIED GLASS CARDS - Elite Components
    ============================================ */
    .glass-card {
        background: 
            linear-gradient(135deg, 
                rgba(255, 255, 255, 0.03) 0%,
                rgba(255, 255, 255, 0.01) 100%),
            var(--bg-card);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border: 1px solid var(--border-subtle);
        border-radius: 18px;
        padding: 2.25rem;
        margin-bottom: 2rem;
        box-shadow: var(--elevation-2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%,
            rgba(16, 185, 129, 0.3) 50%,
            transparent 100%);
        opacity: 0.6;
    }
    
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-medium);
        box-shadow: 
            var(--elevation-3),
            var(--glow-subtle);
    }
    
    .glass-card-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--glass-border);
    }
    
    .glass-card-icon {
        font-size: 2.5rem;
        filter: drop-shadow(0 0 10px var(--neon-green));
    }
    
    .glass-card-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.01em;
    }
    
    .glass-card-subtitle {
        font-size: 0.9rem;
        color: var(--text-muted);
        margin: 0.25rem 0 0 0;
        font-weight: 400;
    }
    
    /* ============================================
       📊 ELITE METRIC CARDS - Unified System
    ============================================ */
    .premium-metric {
        background: 
            linear-gradient(135deg,
                rgba(16, 185, 129, 0.06) 0%,
                rgba(6, 182, 212, 0.04) 100%),
            var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 18px;
        padding: 1.75rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: var(--elevation-1);
    }
    
    .premium-metric::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(16, 185, 129, 0.12) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .premium-metric:hover {
        transform: translateY(-3px);
        border-color: var(--border-medium);
        box-shadow: 
            var(--elevation-2),
            var(--glow-subtle);
    }
    
    .premium-metric:hover::before {
        opacity: 1;
    }
    
    .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.75rem;
        display: block;
        filter: drop-shadow(0 0 10px rgba(0, 255, 136, 0.5));
    }
    
    .metric-value {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, 
            var(--emerald-primary) 0%, 
            var(--teal-accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .metric-delta {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    /* ============================================
       🎯 RESULT CARDS - Base Luxury Styling
    ============================================ */
    .result-card {
        position: relative;
        background: 
            linear-gradient(135deg,
                rgba(16, 185, 129, 0.06) 0%,
                rgba(6, 182, 212, 0.03) 100%),
            var(--bg-card);
        border: 1px solid var(--border-medium);
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 
            var(--elevation-2),
            var(--glow-subtle);
        overflow: hidden;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        border-color: var(--emerald-primary);
        box-shadow: 
            var(--elevation-3),
            var(--glow-emerald);
    }
    
    .result-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .result-icon {
        font-size: 2.5rem;
        filter: drop-shadow(0 0 12px rgba(16, 185, 129, 0.4));
    }
    
    .result-title {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 0;
    }
    
    .result-value {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, 
            var(--emerald-primary) 0%, 
            var(--teal-accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
        letter-spacing: -0.02em;
    }
    
    .confidence-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.01em;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .confidence-high {
        background: linear-gradient(135deg, 
            rgba(16, 185, 129, 0.15) 0%, 
            rgba(16, 185, 129, 0.08) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: var(--emerald-light);
    }
    
    .confidence-medium {
        background: linear-gradient(135deg, 
            rgba(251, 191, 36, 0.15) 0%, 
            rgba(251, 191, 36, 0.08) 100%);
        border: 1px solid rgba(251, 191, 36, 0.3);
        color: #FCD34D;
    }
    
    .confidence-low {
        background: linear-gradient(135deg, 
            rgba(239, 68, 68, 0.15) 0%, 
            rgba(239, 68, 68, 0.08) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        color: #FCA5A5;
    }
    
    /* ============================================
       📦 INFO & SUCCESS BOXES - Luxury Notifications
    ============================================ */
    .success-box {
        background: 
            linear-gradient(135deg,
                rgba(16, 185, 129, 0.08) 0%,
                rgba(16, 185, 129, 0.04) 100%),
            var(--bg-card);
        border-left: 3px solid var(--emerald-primary);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: var(--text-primary);
        backdrop-filter: blur(10px);
        box-shadow: var(--elevation-1);
    }
    
    .success-box h4 {
        color: var(--emerald-primary);
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    .info-box {
        background: 
            linear-gradient(135deg,
                rgba(59, 130, 246, 0.08) 0%,
                rgba(59, 130, 246, 0.04) 100%),
            var(--bg-card);
        border-left: 3px solid var(--accent-info);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        color: var(--text-primary);
        backdrop-filter: blur(10px);
        box-shadow: var(--elevation-1);
    }
    
    .info-box p {
        margin: 0;
        color: var(--text-secondary);
    }
    
    .custom-card {
        background: 
            linear-gradient(135deg,
                rgba(16, 185, 129, 0.06) 0%,
                rgba(6, 182, 212, 0.03) 100%),
            var(--bg-card);
        border: 1px solid var(--border-subtle);
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: var(--elevation-1);
    }
    
    .custom-card h3 {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
        margin-top: 0;
        margin-bottom: 0.75rem;
        font-size: 1.5rem;
    }
    
    .custom-card p {
        color: var(--text-secondary);
        margin: 0;
    }
    
    /* ============================================
       🎯 ELITE AI RESULT CARDS - Elevated Intelligence
    ============================================ */
    .result-card-premium {
        position: relative;
        background: 
            linear-gradient(135deg,
                rgba(16, 185, 129, 0.08) 0%,
                rgba(6, 182, 212, 0.04) 100%),
            var(--bg-card);
        border: 1px solid var(--border-medium);
        border-radius: 18px;
        padding: 2.75rem;
        margin: 2.5rem 0;
        box-shadow: 
            var(--elevation-3),
            var(--glow-emerald),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        overflow: hidden;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .result-card-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(16, 185, 129, 0.12), 
            transparent);
        transition: left 0.7s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .result-card-premium:hover::before {
        left: 100%;
    }
    
    .result-card-premium:hover {
        transform: translateY(-4px);
        border-color: var(--emerald-primary);
        box-shadow: 
            var(--elevation-4),
            0 0 40px rgba(16, 185, 129, 0.25),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }
    
    .result-header-premium {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .result-icon-premium {
        font-size: 4rem;
        animation: float-icon 3s ease-in-out infinite;
        filter: drop-shadow(0 0 20px rgba(0, 255, 136, 0.6));
    }
    
    @keyframes float-icon {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .result-title-premium {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
        letter-spacing: -0.01em;
    }
    
    .result-value-premium {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--neon-green), var(--mint));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1.5rem 0;
        text-align: center;
        padding: 1.5rem;
        border-radius: 15px;
        background-color: rgba(0, 255, 136, 0.05);
        letter-spacing: -0.02em;
        text-shadow: 0 0 40px rgba(0, 255, 136, 0.3);
    }
    
    /* ============================================
       🏅 CONFIDENCE BADGES - Premium Status
    ============================================ */
    .confidence-badge-premium {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.25rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.02em;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .confidence-high-premium {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(16, 185, 129, 0.1));
        border: 1px solid var(--emerald);
        color: var(--neon-green);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
    }
    
    .confidence-medium-premium {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.1));
        border: 1px solid var(--amber-premium);
        color: #fbbf24;
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.3);
    }
    
    .confidence-low-premium {
        background: linear-gradient(135deg, rgba(244, 63, 94, 0.2), rgba(244, 63, 94, 0.1));
        border: 1px solid var(--rose-alert);
        color: #f87171;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
    }
    
    /* ============================================
       🔘 ELITE BUTTONS - Glowing Magnetic Interactions
    ============================================ */
    .stButton > button {
        background: linear-gradient(135deg, 
            var(--emerald-primary) 0%, 
            var(--emerald-dark) 100%);
        color: white;
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 16px;
        padding: 0.875rem 2.25rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 0.9375rem;
        letter-spacing: 0.01em;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 
            var(--elevation-1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.15);
        transform: translate(-50%, -50%);
        transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1), 
                    height 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stButton > button:hover::before {
        width: 320px;
        height: 320px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.6);
        box-shadow: 
            var(--elevation-2),
            var(--glow-emerald),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
        background: linear-gradient(135deg, 
            var(--emerald-bright) 0%, 
            var(--emerald-primary) 100%);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.99);
        box-shadow: 
            var(--elevation-1),
            inset 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    /* ============================================
       📝 ELITE INPUT FIELDS - Apple-Style Inset
    ============================================ */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 0.875rem 1.125rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9375rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 
            inset 0 1px 3px rgba(0, 0, 0, 0.3),
            0 1px 0 rgba(255, 255, 255, 0.03) !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--border-medium) !important;
        box-shadow: 
            inset 0 1px 3px rgba(0, 0, 0, 0.25),
            0 0 0 3px rgba(16, 185, 129, 0.12),
            var(--glow-subtle) !important;
        background: rgba(255, 255, 255, 0.06) !important;
        outline: none !important;
    }
    
    .stNumberInput label,
    .stTextInput label,
    .stTextArea label {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.01em !important;
    }
    
    /* ============================================
       🎨 PREMIUM INFO BOXES - Status Messages
    ============================================ */
    .info-box-premium {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
        border-left: 4px solid var(--electric-blue);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        color: var(--text-primary);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.15);
    }
    
    .success-box-premium {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(16, 185, 129, 0.05));
        border-left: 4px solid var(--neon-green);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        color: var(--text-primary);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);
    }
    
    .warning-box-premium {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.1), rgba(251, 191, 36, 0.05));
        border-left: 4px solid var(--amber-premium);
        padding: 1.25rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        color: var(--text-primary);
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(251, 191, 36, 0.15);
    }
    
    /* ============================================
       ⚡ SECTION DIVIDERS - Elite Vertical Rhythm
    ============================================ */
    .premium-divider {
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%,
            rgba(16, 185, 129, 0.3) 50%,
            transparent 100%);
        margin: 3.5rem 0;
        opacity: 0.4;
    }
    
    /* ============================================
       📊 STREAMLIT COMPONENT OVERRIDES
    ============================================ */
    .stExpander {
        background: var(--glass-bg) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .streamlit-expanderHeader {
        background: transparent !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        padding: 1rem 1.5rem !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(0, 255, 136, 0.05) !important;
    }
    
    
    /* ============================================
       🎭 PREMIUM SIDEBAR - Dark Mode Navigation
    ============================================ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            #0a0e12 0%,
            #111418 50%,
            #0d1117 100%);
        border-right: 1px solid var(--glass-border);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.5);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: var(--text-primary);
    }
    
    [data-testid="collapsedControl"] {
        color: var(--text-primary);
        background: var(--bg-card);
        border-radius: 50%;
    }
    
    /* ============================================
       📊 DATA TABLES - Modern Grid
    ============================================ */
    .dataframe {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        border-radius: 12px;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .dataframe thead tr th {
        background: rgba(16, 185, 129, 0.1) !important;
        color: var(--neon-green) !important;
        font-weight: 600 !important;
        padding: 1rem !important;
    }
    
    .dataframe tbody tr {
        background: rgba(255, 255, 255, 0.02) !important;
        color: var(--text-secondary) !important;
        transition: background 0.2s ease;
    }
    
    .dataframe tbody tr:hover {
        background: rgba(0, 255, 136, 0.05) !important;
    }
    
    /* ============================================
       🎬 ANIMATIONS & MICRO-INTERACTIONS
    ============================================ */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    .animate-slide-in {
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    
    .animate-fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }
    
    /* ============================================
       🔍 RESPONSIVE DESIGN - Mobile Optimization
    ============================================ */
    @media (max-width: 768px) {
        .premium-hero {
            padding: 2rem 1.5rem;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-subtitle {
            font-size: 1rem;
        }
        
        .glass-card {
            padding: 1.5rem;
        }
        
        .result-value-premium {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# Load environment variables from .env (local) and support Streamlit Cloud secrets
# First try default .env in current working directory
load_dotenv()
# Establish repository root (robustly) and ensure it's on sys.path so
# pickled models that reference top-level package imports (e.g. `models`)
# can be imported during unpickling.
try:
    current_file = os.path.abspath(__file__)
    # repo root is two levels up from streamlit_app/app.py
    repo_root = os.path.dirname(os.path.dirname(current_file))
except Exception:
    repo_root = os.path.abspath(os.curdir)

if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Also try loading .env from the project root (one level above models/frontend folders)
try:
    env_path = os.path.join(repo_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path, override=False)
except Exception:
    pass

# 🏆 PREMIUM HERO HEADER - World-Class Design
st.markdown("""
<div class="premium-hero">
    <div class="hero-content">
        <div class="hero-logo">🌱</div>
        <h1 class="hero-title">AgriTech</h1>
        <p class="hero-subtitle">AI-Powered Precision Agriculture | Enterprise Crop & Irrigation Intelligence</p>
        <span class="hero-badge">✨ Powered by Advanced Machine Learning</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 📡 IoT Live Data Section - Premium Glass Design ---
with st.expander("📡 Live Sensor Data (IoT Monitoring)", expanded=False):
    st.markdown("""
    <div class="glass-card">
        <div class="glass-card-header">
            <div>
                <h3 class="glass-card-title">Real-time Environmental Monitoring</h3>
                <p class="glass-card-subtitle">Fetch live IoT sensor data or load demo telemetry</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Supabase credentials (from .env or Streamlit secrets)
    SUPABASE_URL = os.getenv("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") else None)
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or (st.secrets.get("SUPABASE_SERVICE_KEY") if hasattr(st, "secrets") else None)
    
    # Button row
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 2])
    with btn_col1:
        refresh_btn = st.button("🔄 Refresh Data", disabled=(not SUPABASE_URL or not SUPABASE_KEY), use_container_width=True)
    with btn_col2:
        demo_btn = st.button("🎲 Demo Data", use_container_width=True)
    
    # Demo data function
    def generate_demo_data():
        """Generate demo sensor data for testing"""
        import numpy as np
        from datetime import datetime, timedelta
        
        # Generate 50 time points over last 24 hours
        now = datetime.now()
        times = [now - timedelta(hours=24-i*0.5) for i in range(50)]
        
        # Generate realistic sensor data with some variation
        np.random.seed(42)
        data = {
            'created_at': times,
            'temperature': 26.97 + np.random.normal(0, 2, 50),
            'humidity': 62.02 + np.random.normal(0, 5, 50),
            'soil_moisture': 35 + np.random.normal(0, 8, 50),
            'water_level': 50 + np.random.normal(0, 10, 50),
            'wind_speed': 8 + np.random.normal(0, 3, 50),
            'rainfall': np.random.exponential(2, 50)
        }
        
        # Store demo soil type in session state
        # Use global available_soil_types or fallback to defaults
        if 'demo_soil_type' not in st.session_state:
            global available_soil_types
            try:
                soil_options = available_soil_types if available_soil_types else ['clay', 'loamy', 'sandy', 'black', 'red']
            except:
                soil_options = ['clay', 'loamy', 'sandy', 'black', 'red']
            st.session_state.demo_soil_type = np.random.choice(soil_options)
        
        return pd.DataFrame(data)
    
    if SUPABASE_URL and SUPABASE_KEY:
        if refresh_btn:
            with st.spinner("Fetching sensor data..."):
                try:
                    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                    response = supabase.table("Sensor readings").select("*").order("created_at", desc=True).limit(100).execute()
                    data = response.data
                    if data:
                        df = pd.DataFrame(data)
                        df_sorted = df.sort_values("created_at")
                        
                        # Store IoT data in sensor_defaults for inputs to use
                        latest_row = df.iloc[0]  # Most recent data
                        st.session_state['sensor_defaults'] = {
                            'temperature': float(latest_row.get('temperature', 26.97)),
                            'humidity': float(latest_row.get('humidity', 62.02)),
                            'soil_moisture': float(latest_row.get('soil_moisture', 35.0)),
                            'wind_speed': float(latest_row.get('wind_speed', 8.0))
                        }
                        
                        # Quick Stats Section
                        st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)
                        st.markdown("#### 📊 Latest Sensor Readings")
                        cols = st.columns(4)
                        
                        if "temperature" in df.columns:
                            with cols[0]:
                                latest_temp = df.iloc[0].get("temperature", "N/A")
                                avg_temp = df["temperature"].mean()
                                st.markdown(f"""
                                <div class="premium-metric">
                                    <span class="metric-icon">🌡️</span>
                                    <div class="metric-label">Temperature</div>
                                    <div class="metric-value">{latest_temp:.1f}°C</div>
                                    <div class="metric-delta">Avg: {avg_temp:.1f}°C</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        if "humidity" in df.columns:
                            with cols[1]:
                                latest_hum = df.iloc[0].get("humidity", "N/A")
                                avg_hum = df["humidity"].mean()
                                st.markdown(f"""
                                <div class="premium-metric">
                                    <span class="metric-icon">💧</span>
                                    <div class="metric-label">Humidity</div>
                                    <div class="metric-value">{latest_hum:.1f}%</div>
                                    <div class="metric-delta">Avg: {avg_hum:.1f}%</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        if "soil_moisture" in df.columns:
                            with cols[2]:
                                latest_sm = df.iloc[0].get("soil_moisture", "N/A")
                                avg_sm = df["soil_moisture"].mean()
                                st.markdown(f"""
                                <div class="premium-metric">
                                    <span class="metric-icon">🌱</span>
                                    <div class="metric-label">Soil Moisture</div>
                                    <div class="metric-value">{latest_sm:.1f}%</div>
                                    <div class="metric-delta">Avg: {avg_sm:.1f}%</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        if "water_level" in df.columns:
                            with cols[3]:
                                latest_wl = df.iloc[0].get("water_level", "N/A")
                                avg_wl = df["water_level"].mean()
                                st.markdown(f"""
                                <div class="premium-metric">
                                    <span class="metric-icon">💦</span>
                                    <div class="metric-label">Water Level</div>
                                    <div class="metric-value">{latest_wl:.1f}</div>
                                    <div class="metric-delta">Avg: {avg_wl:.1f}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.divider()
                        
                        # Visualizations
                        st.subheader("📈 Sensor Data Visualization")
                        
                        # Temperature and Humidity Chart (2 separate lines with different colors)
                        if "temperature" in df.columns and "humidity" in df.columns:
                            fig1 = px.line(df_sorted, x="created_at", y="temperature", 
                                          title="🌡️ Temperature Over Time",
                                          labels={"created_at": "Time", "temperature": "Temperature (°C)"},
                                          markers=True)
                            fig1.update_traces(line_color='#FF6B6B', marker=dict(size=6))
                            fig1.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig1, use_container_width=True)
                            
                            fig2 = px.line(df_sorted, x="created_at", y="humidity",
                                          title="💧 Humidity Over Time",
                                          labels={"created_at": "Time", "humidity": "Humidity (%)"},
                                          markers=True)
                            fig2.update_traces(line_color='#4ECDC4', marker=dict(size=6))
                            fig2.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # Soil Moisture and Water Level Chart
                        if "soil_moisture" in df.columns:
                            fig3 = px.line(df_sorted, x="created_at", y="soil_moisture",
                                          title="🌱 Soil Moisture Over Time",
                                          labels={"created_at": "Time", "soil_moisture": "Soil Moisture (%)"},
                                          markers=True)
                            fig3.update_traces(line_color='#95E1D3', marker=dict(size=6))
                            fig3.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig3, use_container_width=True)
                        
                        if "water_level" in df.columns:
                            fig4 = px.line(df_sorted, x="created_at", y="water_level",
                                          title="💦 Water Level Over Time",
                                          labels={"created_at": "Time", "water_level": "Water Level"},
                                          markers=True)
                            fig4.update_traces(line_color='#3742FA', marker=dict(size=6))
                            fig4.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig4, use_container_width=True)
                        
                        # Additional sensors if available
                        if "wind_speed" in df.columns:
                            fig5 = px.line(df_sorted, x="created_at", y="wind_speed",
                                          title="🌬️ Wind Speed Over Time",
                                          labels={"created_at": "Time", "wind_speed": "Wind Speed (km/h)"},
                                          markers=True)
                            fig5.update_traces(line_color='#FFA502', marker=dict(size=6))
                            fig5.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig5, use_container_width=True)
                        
                        if "rainfall" in df.columns:
                            fig6 = px.bar(df_sorted, x="created_at", y="rainfall",
                                         title="🌧️ Rainfall Over Time",
                                         labels={"created_at": "Time", "rainfall": "Rainfall (mm)"})
                            fig6.update_traces(marker_color='#5F27CD')
                            fig6.update_layout(hovermode='x unified', height=350)
                            st.plotly_chart(fig6, use_container_width=True)
                        
                        # Data Table (collapsible)
                        with st.expander("📋 View Raw Data Table"):
                            st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No sensor data found in Supabase.")
                except Exception as e:
                    st.error(f"Error fetching data from Supabase: {e}")
                    st.info("💡 Try using Demo Data instead")
        elif not refresh_btn and not demo_btn:
            st.info("👆 Click 'Refresh Data' to load IoT sensor readings from Supabase")
    else:
        st.warning("⚠️ Supabase credentials not found. Use Demo Data button instead.")
    
    # Handle demo data button (works regardless of Supabase credentials)
    if demo_btn:
        with st.spinner("Generating demo data..."):
            try:
                df = generate_demo_data()
                df_sorted = df.sort_values("created_at")
                
                # Store demo data in sensor_defaults for inputs to use
                latest_row = df.iloc[-1]
                st.session_state['sensor_defaults'] = {
                    'temperature': float(latest_row['temperature']),
                    'humidity': float(latest_row['humidity']),
                    'soil_moisture': float(latest_row['soil_moisture']),
                    'wind_speed': float(latest_row['wind_speed'])
                }
                
                st.success("✅ Demo data loaded successfully!")
                
                # Display selected demo soil type
                if 'demo_soil_type' in st.session_state:
                    st.info(f"🌍 **Demo Soil Type**: {st.session_state.demo_soil_type.title()} (This will be auto-filled in inputs below)")
                
                # Quick Stats Section
                st.subheader("📊 Latest Sensor Readings (Demo)")
                cols = st.columns(4)
                
                with cols[0]:
                    latest_temp = df.iloc[-1]["temperature"]
                    avg_temp = df["temperature"].mean()
                    st.metric("🌡️ Temperature", f"{latest_temp:.1f}°C", delta=f"Avg: {avg_temp:.1f}°C")
                
                with cols[1]:
                    latest_hum = df.iloc[-1]["humidity"]
                    avg_hum = df["humidity"].mean()
                    st.metric("💧 Humidity", f"{latest_hum:.1f}%", delta=f"Avg: {avg_hum:.1f}%")
                
                with cols[2]:
                    latest_sm = df.iloc[-1]["soil_moisture"]
                    avg_sm = df["soil_moisture"].mean()
                    st.metric("🌱 Soil Moisture", f"{latest_sm:.1f}%", delta=f"Avg: {avg_sm:.1f}%")
                
                with cols[3]:
                    latest_wl = df.iloc[-1]["water_level"]
                    avg_wl = df["water_level"].mean()
                    st.metric("💦 Water Level", f"{latest_wl:.1f}", delta=f"Avg: {avg_wl:.1f}")
                
                st.divider()
                
                # Visualizations
                st.subheader("📈 Sensor Data Visualization")
                
                # Temperature Chart
                fig1 = px.line(df_sorted, x="created_at", y="temperature", 
                              title="🌡️ Temperature Over Time",
                              labels={"created_at": "Time", "temperature": "Temperature (°C)"},
                              markers=True)
                fig1.update_traces(line_color='#FF6B6B', marker=dict(size=6))
                fig1.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig1, use_container_width=True)
                
                # Humidity Chart
                fig2 = px.line(df_sorted, x="created_at", y="humidity",
                              title="💧 Humidity Over Time",
                              labels={"created_at": "Time", "humidity": "Humidity (%)"},
                              markers=True)
                fig2.update_traces(line_color='#4ECDC4', marker=dict(size=6))
                fig2.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig2, use_container_width=True)
                
                # Soil Moisture Chart
                fig3 = px.line(df_sorted, x="created_at", y="soil_moisture",
                              title="🌱 Soil Moisture Over Time",
                              labels={"created_at": "Time", "soil_moisture": "Soil Moisture (%)"},
                              markers=True)
                fig3.update_traces(line_color='#95E1D3', marker=dict(size=6))
                fig3.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig3, use_container_width=True)
                
                # Water Level Chart
                fig4 = px.line(df_sorted, x="created_at", y="water_level",
                              title="💦 Water Level Over Time",
                              labels={"created_at": "Time", "water_level": "Water Level"},
                              markers=True)
                fig4.update_traces(line_color='#3742FA', marker=dict(size=6))
                fig4.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig4, use_container_width=True)
                
                # Wind Speed Chart
                fig5 = px.line(df_sorted, x="created_at", y="wind_speed",
                              title="🌬️ Wind Speed Over Time",
                              labels={"created_at": "Time", "wind_speed": "Wind Speed (km/h)"},
                              markers=True)
                fig5.update_traces(line_color='#FFA502', marker=dict(size=6))
                fig5.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig5, use_container_width=True)
                
                # Rainfall Bar Chart
                fig6 = px.bar(df_sorted, x="created_at", y="rainfall",
                             title="🌧️ Rainfall Over Time",
                             labels={"created_at": "Time", "rainfall": "Rainfall (mm)"})
                fig6.update_traces(marker_color='#5F27CD')
                fig6.update_layout(hovermode='x unified', height=350)
                st.plotly_chart(fig6, use_container_width=True)
                
                # Data Table (collapsible)
                with st.expander("📋 View Raw Data Table"):
                    st.dataframe(df, use_container_width=True)
                    
            except Exception as e:
                st.error(f"❌ Error generating demo data: {e}")

# Global status tracker for all models
MODEL_STATUS = {
    'crop_model': False,
    'irrigation_model': False,
    'optimization_model': False,
    'soil_model': False
}

def load_crop_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root  
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(current_file))  # Two levels up from streamlit_app/app.py
    
    # Direct path to the crop model
    model_path = os.path.join(repo_root, "models", "crop_recommendation", "crop_model.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['crop_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading crop model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['crop_model'] = False
            return None
    else:
        st.error(f"❌ Crop model file not found at: {model_path}")
        MODEL_STATUS['crop_model'] = False
        return None

def load_irrigation_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(current_file))  # Two levels up from streamlit_app/app.py
    
    # Direct path to the irrigation model
    model_path = os.path.join(repo_root, "models", "irrigation_optimization", "catboost_classifier.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['irrigation_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading irrigation model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['irrigation_model'] = False
            return None
    else:
        st.error(f"❌ Irrigation model file not found at: {model_path}")
        MODEL_STATUS['irrigation_model'] = False
        return None

def load_optimization_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(current_file))  # Two levels up from streamlit_app/app.py
    
    # Direct path to the optimization model
    model_path = os.path.join(repo_root, "models", "irrigation_optimization", "catboost_irrigation_model.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['optimization_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading optimization model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['optimization_model'] = False
            return None
    else:
        st.error(f"❌ Optimization model file not found at: {model_path}")
        MODEL_STATUS['optimization_model'] = False
        return None

MODEL_STATUS = {'soil_model': False} 

def load_soil_model():
    """Load TensorFlow soil type classification model (supports .h5 and SavedModel)"""
    # يجب تعريف _file_ بشكل صحيح في بيئة Streamlit
    # سنستخدم اسم ملف وهمي لكي يعمل الكود هنا
    _file_ = __file__ # يجب أن يكون هذا السطر موجودًا في الملف الأصلي

    # Get the absolute path to the repository root
    current_file = os.path.abspath(_file_)
    repo_root = os.path.dirname(os.path.dirname(current_file))  # Two levels up from streamlit_app/app.py
    
    # Try loading .h5 file first (your model)
    h5_path = os.path.join(repo_root, "models", "soil_classification", "my_soil_model.h5")
    savedmodel_path = os.path.join(repo_root, "models", "soil_classification")
    
    # قائمة التسميات الصحيحة التي تدرب عليها النموذج (مستخلصة من إخراجك السابق)
    # هذا الترتيب يجب أن يطابق ترتيب الفئات في مجلدات التدريب: (0: Peat, 1: Sandy, 2: Silt)
    CORRECT_SOIL_LABELS = ["Peat Soil", "Sandy Soil", "Silt Soil"]
    
    # Try .h5 model first
    if os.path.exists(h5_path):
        try:
            # Use compile=False to avoid Keras 3 compatibility issues with custom layers
            model = tf.keras.models.load_model(h5_path, compile=False)
            MODEL_STATUS['soil_model'] = True
            
            # --- الإصلاح هنا: استخدام التسميات الصحيحة ---
            soil_labels = CORRECT_SOIL_LABELS
            
            return model, soil_labels
        except Exception as e:
            st.error(f"Error loading H5 model from {h5_path}: {type(e).__name__}: {e}")

    # Fallback to SavedModel
    elif os.path.exists(savedmodel_path):
        try:
            from tensorflow.keras.layers import TFSMLayer
            model = TFSMLayer(savedmodel_path, call_endpoint='serving_default')
            MODEL_STATUS['soil_model'] = True
            
            # --- الإصلاح هنا: استخدام التسميات الصحيحة ---
            soil_labels = CORRECT_SOIL_LABELS
            
            st.info(f"ℹ Using SavedModel from: {savedmodel_path}")
            return model, soil_labels
        except Exception as e:
            st.error(f"Error loading SavedModel from {savedmodel_path}: {type(e).__name__}: {e}")
    
    # No model found
    st.warning(f"⚠ Soil model not found. Tried:\n- {h5_path}\n- {savedmodel_path}")
    MODEL_STATUS['soil_model'] = False
    return None, None

# Load all models
crop_model = load_crop_model()
irrigation_model = load_irrigation_model()
optimization_model = load_optimization_model()
soil_model, soil_labels = load_soil_model()

# Load soil type encoder for crop recommendation
# Initialize with defaults first to avoid "not defined" errors
available_soil_types = ['clay', 'loamy', 'sandy', 'black', 'red']
soil_type_encoder = None

try:
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(current_file))  # Two levels up from streamlit_app/app.py
    encoder_path = os.path.join(repo_root, "models", "crop_recommendation", "soil_type_encoder.pkl")
    if os.path.exists(encoder_path):
        soil_type_encoder = joblib.load(encoder_path)
        # Get available soil types from encoder
        available_soil_types = list(soil_type_encoder.classes_)
except Exception as e:
    # Keep default soil types if encoder loading fails
    soil_type_encoder = None


def fetch_latest_iot_reading():
    """Fetch the latest sensor reading from Supabase (table: 'Sensor readings').
    Returns a dict with float values or None on failure.
    Converts soil_moisture from 0-1 to 0-100 automatically if needed.
    """
    SUPABASE_URL = os.getenv("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") else None)
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or (st.secrets.get("SUPABASE_SERVICE_KEY") if hasattr(st, "secrets") else None)
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table("Sensor readings").select("*").order("created_at", desc=True).limit(1).execute()
        data = response.data
        if not data:
            return None
        rec = data[0]

        def _f(key, default=None):
            v = rec.get(key)
            try:
                return float(v) if v is not None else default
            except Exception:
                return default

        result = {
            'temperature': _f('temperature', None),
            'humidity': _f('humidity', None),
            'soil_moisture': _f('soil_moisture', None),
            'wind_speed': _f('wind_speed', None),
            'pressure': _f('pressure', None),
            'rainfall': _f('rainfall', None),
        }

        # If soil_moisture looks normalized (0-1) convert to percent
        sm = result.get('soil_moisture')
        if sm is not None and sm <= 1.0:
            result['soil_moisture'] = sm * 100.0

        return result
    except Exception:
        return None

# Soil classification function
def predict_soil_type(image, soil_model, soil_labels):
    """Predict soil type from uploaded image using TensorFlow model"""
    if soil_model is None or soil_labels is None:
        return None, None, "Model not loaded", None
    
    try:
        # Enhanced preprocessing for better accuracy
        # 1. Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # 2. Resize to model input size (224x224)
        img = image.resize((224, 224), Image.Resampling.LANCZOS)
        
        # 3. Convert to array
        img_array = np.array(img, dtype=np.float32)
        
        # 4. Normalize to [0, 1] range (standard for most models)
        img_array = img_array / 255.0
        
        # 5. Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # 6. Predict using the model
        if hasattr(soil_model, 'predict'):
            # H5 model - use standard predict
            predictions = soil_model.predict(img_array, verbose=0)
            all_probs = predictions[0]
        else:
            # TFSMLayer - returns dictionary
            img_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)
            output = soil_model(img_tensor)
            
            # Extract predictions from output dictionary
            predictions = None
            for key in output.keys():
                predictions = output[key].numpy()
                break
            
            if predictions is None:
                return None, None, "Could not extract predictions from model output", None
            
            all_probs = predictions[0]
        
        # Apply softmax to normalize probabilities if they're not already normalized
        if not np.isclose(np.sum(all_probs), 1.0, rtol=0.1):
            exp_probs = np.exp(all_probs - np.max(all_probs))  # Numerical stability
            all_probs = exp_probs / np.sum(exp_probs)
        
        # Get predicted class and confidence
        predicted_class = np.argmax(all_probs)
        confidence = float(all_probs[predicted_class])
        
        # --- هذا السطر يستخدم القائمة المصححة ---
        soil_type = soil_labels[predicted_class]
        
        return soil_type, confidence, None, all_probs
    except Exception as e:
        return None, None, f"Prediction error: {e}", None

# Feature engineering functions
def create_irrigation_features(soil_moisture, temperature, humidity, ph, n, p, k, rainfall=0):
    """Create all required features for irrigation model"""
    import numpy as np
    
    # Basic features
    soil_humidity = humidity * 0.8  # Approximate soil humidity
    air_temperature = temperature
    
    # Derived features
    relative_soil_saturation = min(soil_moisture / 100.0, 1.0)
    temp_diff = abs(temperature - 25)  # Difference from optimal temp
    evapotranspiration = max(0, (temperature - 10) * 0.1 + (100 - humidity) * 0.05)
    rain_vs_soil = rainfall / max(soil_moisture, 1)
    ph_encoded = 1 if ph > 7 else 0  # Alkaline vs acidic
    
    # NPK ratios
    np_ratio = n / max(p, 1)
    nk_ratio = n / max(k, 1)
    npk_balance = (n + p + k) / 3
    
    # Additional derived features
    crop_encoded = 1  # Default crop type
    rain_3days = rainfall * 3  # Assume same rainfall for 3 days
    moisture_temp_ratio = soil_moisture / max(temperature, 1)
    evapo_ratio = evapotranspiration / max(rainfall, 0.1)
    rain_effect = min(rainfall / 10, 1.0)
    moisture_change_rate = 0.1  # Default change rate
    temp_scaled = temperature / 40  # Scale temperature
    wind_ratio = 0.5  # Default wind effect
    
    return np.array([[
        soil_moisture, temperature, soil_humidity, relative_soil_saturation,
        temp_diff, evapotranspiration, rain_vs_soil, rainfall, ph_encoded,
        n, p, k, np_ratio, nk_ratio, crop_encoded, rain_3days,
        moisture_temp_ratio, evapo_ratio, rain_effect, moisture_change_rate,
        temp_scaled, npk_balance, wind_ratio
    ]])

def create_optimization_features(soil_moisture, temperature, humidity, ph, n, p, k, rainfall=0):
    """Create all required features for optimization model"""
    import numpy as np
    
    # Basic environmental features
    soil_humidity = humidity * 0.8
    air_temperature = temperature
    wind_speed = 10  # Default wind speed
    wind_gust = wind_speed * 1.5
    pressure = 101.325  # Standard atmospheric pressure
    
    # Derived features
    soil_moisture_diff = 0.1  # Default change
    relative_soil_saturation = min(soil_moisture / 100.0, 1.0)
    temp_diff = abs(temperature - 25)
    wind_effect = wind_speed * 0.1
    evapotranspiration = max(0, (temperature - 10) * 0.1 + (100 - humidity) * 0.05)
    rain_3days = rainfall * 3
    rain_vs_soil = rainfall / max(soil_moisture, 1)
    
    # NPK features
    np_ratio = n / max(p, 1)
    nk_ratio = n / max(k, 1)
    npk_balance = (n + p + k) / 3
    
    # Encoded features
    ph_encoded = 1 if ph > 7 else 0
    crop_encoded = 1
    
    # Additional ratios
    moisture_temp_ratio = soil_moisture / max(temperature, 1)
    evapo_ratio = evapotranspiration / max(rainfall, 0.1)
    rain_effect = min(rainfall / 10, 1.0)
    moisture_change_rate = 0.1
    temp_scaled = temperature / 40
    wind_ratio = wind_speed / 50
    
    return np.array([[
        soil_moisture, temperature, soil_humidity, air_temperature,
        wind_speed, humidity, wind_gust, pressure, ph, rainfall,
        n, p, k, soil_moisture_diff, relative_soil_saturation,
        temp_diff, wind_effect, evapotranspiration, rain_3days,
        rain_vs_soil, np_ratio, nk_ratio, ph_encoded, crop_encoded,
        moisture_temp_ratio, evapo_ratio, rain_effect, moisture_change_rate,
        temp_scaled, npk_balance, wind_ratio
    ]])


def recommend_from_dataset(N, P, K, temperature, humidity, ph, rainfall, k=5):
    """Lightweight nearest-neighbour recommender that uses data/crop_data.csv.

    Returns (label, confidence) where confidence is fraction of the k nearest neighbors
    that agree with the predicted label.
    """
    import pandas as _pd
    import numpy as _np
    import os as _os

    cache_name = '_crop_dataset_cache'
    if cache_name not in globals():
        data_path = _os.path.join(repo_root, 'data', 'crop_data.csv')
        if not _os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found: {data_path}")
        df = _pd.read_csv(data_path)
        feats = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].values.astype(float)
        labels = df['label'].astype(str).values
        mean = feats.mean(axis=0)
        std = feats.std(axis=0)
        std[std == 0] = 1.0
        globals()[cache_name] = {'feats': feats, 'labels': labels, 'mean': mean, 'std': std}

    cache = globals()[cache_name]
    feat = _np.array([N, P, K, temperature, humidity, ph, rainfall], dtype=float)
    norm = (feat - cache['mean']) / cache['std']
    feats_norm = (cache['feats'] - cache['mean']) / cache['std']
    dists = _np.linalg.norm(feats_norm - norm, axis=1)
    idx = _np.argsort(dists)[:k]
    top_labels = cache['labels'][idx]
    uniques, counts = _np.unique(top_labels, return_counts=True)
    mode = uniques[counts.argmax()]
    conf = float(counts.max()) / float(k)
    return str(mode), conf


def call_gemini_chat(prompt, context=None, system_instruction=None):
    """Call the Gemini REST API and return a dict with text + metadata."""
    
    # Check for Service Account authentication first
    service_account_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.path.join(
        os.path.dirname(__file__), "service-account.json"
    )
    
    access_token = None
    api_key = None
    
    # Try Service Account authentication first
    if os.path.exists(service_account_path):
        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=['https://www.googleapis.com/auth/generative-language.retriever']
            )
            credentials.refresh(Request())
            access_token = credentials.token
        except Exception as e:
            st.warning(f"Service Account auth failed, trying API key: {e}")
    
    # Fall back to API key if Service Account not available
    if not access_token:
        api_key = os.getenv("GEMINI_API_KEY") or (st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") else None)
        if not api_key:
            raise ValueError("Neither GOOGLE_APPLICATION_CREDENTIALS nor GEMINI_API_KEY found. Please set one in .env or Streamlit secrets.")

    model_name = (os.getenv("GEMINI_MODEL", "gemini-1.5-flash") or "").strip() or "gemini-1.5-flash"
    endpoint_override = os.getenv("GEMINI_REST_URL")

    def _build_endpoint(model):
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    headers = {"Content-Type": "application/json"}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    user_parts = [
        {"text": prompt}
    ]
    if context:
        user_parts.append({"text": f"\nContext:\n{context}"})

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": user_parts
            }
        ]
    }

    if system_instruction:
        payload["system_instruction"] = {
            "parts": [{"text": system_instruction}]
        }

    attempt_log = []
    available_model_cache = {"names": None, "error": None}

    def _make_request(url):
        try:
            # Use Bearer token if available, otherwise use API key
            if access_token:
                return requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
            else:
                return requests.post(
                    url,
                    params={"key": api_key},
                    headers=headers,
                    json=payload,
                    timeout=30
                )
        except requests.RequestException as req_err:
            raise RuntimeError(f"Gemini request failed: {req_err}") from req_err

    def _call_model(target_model, reason=None):
        target_url = endpoint_override or _build_endpoint(target_model)
        response = _make_request(target_url)
        attempt_log.append({
            "model": target_model,
            "status": getattr(response, "status_code", None),
            "ok": getattr(response, "ok", False),
            "reason": reason or ("endpoint override" if endpoint_override else "default")
        })
        return response

    def _fetch_available_models():
        if available_model_cache["names"] is not None or available_model_cache["error"] is not None:
            return available_model_cache["names"]
        try:
            # Use Bearer token if available, otherwise use API key
            if access_token:
                resp = requests.get(
                    "https://generativelanguage.googleapis.com/v1beta/models",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=15
                )
            else:
                resp = requests.get(
                    "https://generativelanguage.googleapis.com/v1beta/models",
                    params={"key": api_key},
                    timeout=15
                )
            if resp.ok:
                data = resp.json()
                names = set()
                for model in data.get("models", []):
                    name = model.get("name")
                    if not name:
                        continue
                    short_name = name.split("/")[-1]
                    methods = model.get("supportedGenerationMethods", []) or []
                    if "generateContent" in methods:
                        names.add(short_name)
                available_model_cache["names"] = names
                return names
            else:
                available_model_cache["error"] = resp.text
        except requests.RequestException as fetch_err:
            available_model_cache["error"] = str(fetch_err)
        return None

    response = _call_model(model_name)
    used_model = model_name
    fallback_notice = None
    fallback_used = False

    if not response.ok and response.status_code == 404 and not endpoint_override:
        fallback_notice_parts = []
        fallback_chain = []

        if model_name.endswith("-latest"):
            trimmed = model_name.removesuffix("-latest")
            if trimmed and trimmed != model_name:
                fallback_chain.append((trimmed, "'-latest' alias unavailable"))

        preferred_order = [
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-2.5-flash-lite-preview-06-17"
        ]
        for candidate in preferred_order:
            if candidate and candidate != model_name:
                fallback_chain.append((candidate, "Primary model unavailable"))

        available_names = _fetch_available_models()

        def _allowed(candidate):
            if not available_names:
                return True
            return candidate in available_names

        filtered_chain = [(model, reason) for model, reason in fallback_chain if _allowed(model)]

        if available_names:
            missing_models = [model for model, _ in fallback_chain if model not in available_names]
            if missing_models:
                fallback_notice_parts.append(
                    "Models not in your account were skipped: " + ", ".join(missing_models)
                )

        for fallback_model, reason in filtered_chain:
            fallback_notice_parts.append(
                f"{reason}. Retrying with '{fallback_model}'. Update GEMINI_MODEL to pin a working model."
            )
            response = _call_model(fallback_model, reason=reason)
            if response.ok:
                used_model = fallback_model
                fallback_notice = " ".join(fallback_notice_parts)
                fallback_used = True
                break

    if not response.ok:
        try:
            err_payload = response.json()
            err_detail = err_payload.get("error", {}).get("message") or err_payload.get("error", {}).get("status")
        except ValueError:
            err_detail = response.text

        attempt_summary = ", ".join(
            f"{entry['model']}→{entry.get('status')}" if entry.get('status') else entry['model']
            for entry in attempt_log
        )
        if attempt_summary:
            err_detail = f"{err_detail} (attempts: {attempt_summary})"

        if available_model_cache["names"]:
            sorted_names = ", ".join(sorted(available_model_cache["names"]))
            err_detail = f"{err_detail} | Available models for key: {sorted_names}"
        elif available_model_cache["error"]:
            err_detail = f"{err_detail} | Unable to list models: {available_model_cache['error']}"

        extra_hint = ""
        if response.status_code == 404 and not endpoint_override:
            if model_name.endswith("-latest") and not fallback_used:
                extra_hint = " Tip: remove the '-latest' suffix or set GEMINI_REST_URL explicitly."
            else:
                extra_hint = " Ensure your GEMINI_MODEL matches an available model for your API key."
        elif endpoint_override:
            extra_hint = " Verify GEMINI_REST_URL is correct or unset it to allow automatic fallbacks."

        raise RuntimeError(f"Gemini API error ({response.status_code}): {err_detail}{extra_hint}")

    data = response.json()

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        text = ""

    if not text:
        text = "No response returned from Gemini."

    return {
        "text": text,
        "model_used": used_model,
        "notice": fallback_notice,
        "attempts": attempt_log
    }

# Check overall system status
def check_system_status():
    """Returns True only if ALL required models are loaded successfully"""
    all_loaded = all(MODEL_STATUS.values())
    if not all_loaded:
        failed_models = [model for model, status in MODEL_STATUS.items() if not status]
        st.error(f"🚨 **System Status: FAILED** - Models not loaded: {', '.join(failed_models)}")
        st.warning("⚠️ **Fail-Safe Mode**: All predictions will return 0/False due to missing models")
        return False
    else:
        st.success("✅ **System Status: OPERATIONAL** - All models loaded successfully")
        return True

# Check system status with styled output
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
system_operational = check_system_status()
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Try to auto-fill inputs from the latest IoT reading (if available)
sensor_defaults = fetch_latest_iot_reading() or {}

# Helper that treats explicit None as missing and falls back to default
def _safe_default(key, default):
    v = sensor_defaults.get(key, None)
    return default if v is None else v

# prepare defaults (fall back to previous hard-coded defaults)
temp_default = _safe_default('temperature', 23.0)
hum_default = _safe_default('humidity', 82.0)
soil_moisture_default = _safe_default('soil_moisture', 35.0)
wind_speed_default = _safe_default('wind_speed', 8.0)
pressure_default = _safe_default('pressure', 101.3)
rain_default = _safe_default('rainfall', 240.0)

# Create two columns layout with improved spacing
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="glass-card animate-slide-in">
        <div class="glass-card-header">
            <span class="glass-card-icon">📊</span>
            <div>
                <h3 class="glass-card-title">Input Parameters</h3>
                <p class="glass-card-subtitle">Configure soil nutrients and environmental conditions</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Option to auto-fill selected inputs from IoT and lock those widgets
    auto_fill = st.checkbox("🔁 Auto-fill from IoT Sensors", value=True, help="Automatically populate Temperature, Humidity, and Soil Moisture from live sensors")

    # Manual refresh button to fetch latest IoT values into session state
    if st.button("🔄 Fetch IoT Now"):
        new = fetch_latest_iot_reading()
        if new:
            st.session_state['sensor_defaults'] = new
        else:
            st.warning("No IoT data available or failed to fetch.")
        # `st.experimental_rerun()` is not present in all Streamlit builds/environments.
        # Try to call it if available; otherwise inform the user to refresh.
        try:
            if hasattr(st, 'experimental_rerun'):
                st.experimental_rerun()
            elif hasattr(st, 'rerun'):
                # some versions expose a different API
                st.rerun()
            else:
                st.success("IoT values fetched — please refresh the page to apply the new defaults.")
        except Exception:
            st.success("IoT values fetched — please refresh the page to apply the new defaults.")

    # Prefer session-cached sensor values if present (after manual refresh)
    current_sensor = st.session_state.get('sensor_defaults', sensor_defaults)
    
    # Soil Nutrients Section
    st.markdown("#### 🧪 Soil Nutrients (NPK)")
    ncol1, ncol2, ncol3 = st.columns(3)
    with ncol1:
        N = st.number_input("Nitrogen (N)", min_value=0, max_value=200, value=101, help="Nitrogen content in soil (mg/kg)")
    with ncol2:
        P = st.number_input("Phosphorus (P)", min_value=0, max_value=200, value=33, help="Phosphorus content in soil (mg/kg)")
    with ncol3:
        K = st.number_input("Potassium (K)", min_value=0, max_value=200, value=33, help="Potassium content in soil (mg/kg)")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Environmental Conditions Section
    st.markdown("#### 🌤️ Environmental Conditions")
    temp_val = current_sensor.get('temperature', temp_default)
    hum_val = current_sensor.get('humidity', hum_default)
    
    # Get demo soil type if available
    default_soil_type = st.session_state.get('demo_soil_type', available_soil_types[0])
    default_soil_index = available_soil_types.index(default_soil_type) if default_soil_type in available_soil_types else 0
    
    # Add Soil Type selector
    soil_type = st.selectbox(
        "🌍 Soil Type",
        options=available_soil_types,
        index=default_soil_index,
        help="Select the type of soil in your field"
    )
    
    ecol1, ecol2 = st.columns(2)
    with ecol1:
        temp = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=50.0, value=float(temp_val), help="Average temperature", disabled=auto_fill)
        ph = st.number_input("⚗️ Soil pH", min_value=0.0, max_value=14.0, value=6.91, help="Soil pH level (0-14)")
    with ecol2:
        hum = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=float(hum_val), help="Relative humidity", disabled=auto_fill)
        rain = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=300.0, value=142.86, help="Annual rainfall")
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Irrigation Parameters Section
    st.markdown("#### 💦 Irrigation Parameters")
    soil_val = current_sensor.get('soil_moisture', soil_moisture_default)
    
    icol1, icol2, icol3 = st.columns(3)
    with icol1:
        soil_moisture = st.number_input(
            "💧 Soil Moisture (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(soil_val),
            step=0.1,
            help="Volumetric water content (0-100%)",
            disabled=auto_fill,
        )
    with icol2:
        wind_speed = st.number_input("🌬️ Wind Speed (km/h)", min_value=0.0, max_value=50.0, value=float(wind_speed_default), help="Wind speed")
    with icol3:
        pressure = st.number_input("🌡️ Pressure (kPa)", min_value=80.0, max_value=110.0, value=float(pressure_default), help="Atmospheric pressure")
    
    # Input Summary Table
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    with st.expander("📋 View Input Summary", expanded=False):
        summary_data = {
            "Parameter": ["Soil Type", "Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "pH", "Rainfall", "Soil Moisture", "Wind Speed", "Pressure"],
            "Value": [f"{soil_type.title()}", f"{N} mg/kg", f"{P} mg/kg", f"{K} mg/kg", f"{temp}°C", f"{hum}%", f"{ph}", f"{rain} mm", f"{soil_moisture}%", f"{wind_speed} km/h", f"{pressure} kPa"],
            "Status": ["✅" if auto_fill else "✏️"] * 11
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)
    
    # === SOIL TYPE CLASSIFICATION SECTION ===
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-card">
        <h3>🏞️ Soil Type Classification</h3>
        <p style="color: #6c757d;">Upload an image to identify soil type using AI vision</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a soil image...", type=["jpg", "jpeg", "png"], help="Upload a clear image of the soil surface")
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
        with col_img2:
            st.image(image, caption="Uploaded Soil Image", use_container_width=True)
        
        # Classify button
        if st.button("🔍 Classify Soil Type", type="primary", use_container_width=True, key="classify_soil"):
            if not MODEL_STATUS.get('soil_model') or soil_model is None:
                st.error("❌ **SOIL CLASSIFIER NOT LOADED**: Cannot classify soil type")
                st.info("🔄 Please ensure soil_model_savedmodel is available in models/ directory")
            else:
                with st.spinner("🔄 Analyzing soil image..."):
                    # Get prediction with all probabilities
                    result = predict_soil_type(image, soil_model, soil_labels)
                    
                    if len(result) == 3:
                        soil_type, confidence, error = result
                        all_probs = None
                    else:
                        soil_type, confidence, error, all_probs = result
                    
                    if error:
                        st.error(f"❌ Classification failed: {error}")
                    else:
                        # Display result in a professional card
                        confidence_class = "confidence-high" if confidence >= 0.8 else ("confidence-medium" if confidence >= 0.6 else "confidence-low")
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-header">
                                <div class="result-icon">🌍</div>
                                <div>
                                    <div class="result-title">Soil Classification</div>
                                    <span class="confidence-badge {confidence_class}">Confidence: {confidence*100:.1f}%</span>
                                </div>
                            </div>
                            <div class="result-value">{soil_type}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Soil type information
                        soil_info = {
                            'Alluvial': '🌊 **Alluvial Soil**: Rich in minerals and nutrients, formed by river deposits. Excellent for agriculture with good water retention.',
                            'Black': '🖤 **Black Soil**: High in clay content, rich in calcium, iron, and magnesium. Ideal for cotton cultivation and retains moisture well.',
                            'Clay': '🧱 **Clay Soil**: Heavy texture with very fine particles. Good water retention but poor drainage. Needs proper management for cultivation.',
                            'Red': '🔴 **Red Soil**: Contains iron oxide giving it red color. Good for crops like groundnuts, potatoes, and pulses. Moderate fertility.'
                        }
                        
                        if soil_type in soil_info:
                            st.info(soil_info[soil_type])
                        
                        # Add interpretation help
                        if confidence < 0.6:
                            st.warning("⚠️ **Low Confidence**: The model is not very confident about this prediction. Consider taking a clearer photo with better lighting.")
                        elif confidence < 0.8:
                            st.info("ℹ️ **Medium Confidence**: The prediction is reasonably confident but could be improved with a better quality image.")
                        else:
                            st.success("💡 **High Confidence**: The model is very confident about this prediction!")
                        
                        st.success("💡 **Tip**: For best results, use clear, well-lit images showing the soil texture and color clearly.")

with col2:
    st.markdown("""
    <div class="glass-card animate-slide-in">
        <div class="glass-card-header">
            <span class="glass-card-icon">🎯</span>
            <div>
                <h3 class="glass-card-title">AI-Powered Recommendations</h3>
                <p class="glass-card-subtitle">Enterprise-grade crop and irrigation intelligence</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Developer debug toggle: show raw inputs/outputs on the page
    show_debug = st.checkbox("🔧 Debug Mode", value=False, key="show_debug", help="Show technical details and raw model outputs")
    
    # === CROP RECOMMENDATION SECTION ===
    st.markdown('<div class="premium-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🌱 Crop Recommendation")
    
    if st.button("🚀 Get Crop Recommendation", type="primary", width="stretch", key="crop_recommendation"):
        # Check if crop model is loaded
        if not MODEL_STATUS.get('crop_model') or crop_model is None:
            st.error("❌ **CROP MODEL NOT LOADED**: Cannot provide recommendations")
            st.info("🔄 Please ensure crop_model.pkl is available in models/crop_recommendation/")
        else:
            try:
                # Encode soil type using the encoder
                if soil_type_encoder is not None:
                    try:
                        soil_type_encoded = soil_type_encoder.transform([soil_type])[0]
                    except:
                        # If soil type not in encoder, use default (0)
                        soil_type_encoded = 0
                else:
                    soil_type_encoded = 0
                
                # Create DataFrame with proper column names including soil_type_encoded
                feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'soil_type_encoded']
                input_data = pd.DataFrame([[N, P, K, temp, hum, ph, rain, soil_type_encoded]], columns=feature_names)
                # Debug: log inputs to help trace behavior and optionally show on the page
                crop_inputs_dict = input_data.to_dict(orient='records')[0]
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"CROP_INPUTS: {crop_inputs_dict}\n")
                except Exception:
                    pass

                # Make prediction using crop_model
                prediction = None
                confidence = None

                try:
                    prediction = crop_model.predict(input_data)[0]
                    try:
                        confidence = crop_model.predict_proba(input_data).max()
                    except Exception:
                        confidence = None
                except Exception as pred_error:
                    st.error(f"❌ **PREDICTION FAILED**: {str(pred_error)}")
                    prediction = 'unknown'
                    confidence = None
                
                # Debug: log model outputs as well and (optionally) print them to the page
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"CROP_OUTPUT: pred={prediction}, conf={confidence}\n")
                except Exception:
                    pass

                if show_debug:
                    st.markdown("**Debug — crop model inputs**")
                    st.write(input_data)
                    st.markdown("**Debug — crop model outputs**")
                    st.write({"prediction": str(prediction), "confidence": float(confidence) if confidence is not None else None})

                # Display results only if prediction was successful
                if prediction != 'unknown':
                    # Professional result card
                    conf_value = confidence if confidence is not None else 0.0
                    confidence_class = "confidence-high" if conf_value >= 0.8 else ("confidence-medium" if conf_value >= 0.6 else "confidence-low")
                    
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">
                            <div class="result-icon">🌾</div>
                            <div>
                                <div class="result-title">Recommended Crop</div>
                                <span class="confidence-badge {confidence_class}">Confidence: {conf_value*100:.1f}%</span>
                            </div>
                        </div>
                        <div class="result-value">{prediction.title()}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Add crop information
                    crop_info = {
                        'rice': '🍚 Rice - High water requirement, suitable for humid conditions',
                        'maize': '🌽 Maize - Moderate water requirement, good for moderate climate',
                        'chickpea': '🫘 Chickpea - Low water requirement, drought tolerant',
                        'kidneybeans': '🫘 Kidney Beans - Nitrogen-fixing legume',
                        'pigeonpeas': '🫛 Pigeon Peas - Drought resistant pulse crop',
                        'mothbeans': '🫘 Moth Beans - Heat and drought tolerant',
                        'mungbean': '🫛 Mung Bean - Quick growing pulse crop',
                        'blackgram': '🫘 Black Gram - Protein-rich pulse crop',
                        'lentil': '🟤 Lentil - Cool season pulse crop',
                        'pomegranate': '🍎 Pomegranate - Antioxidant-rich fruit',
                        'banana': '🍌 Banana - Tropical fruit, high potassium needs',
                        'mango': '🥭 Mango - King of fruits, tropical climate',
                        'grapes': '🍇 Grapes - Mediterranean climate preferred',
                        'watermelon': '🍉 Watermelon - High water requirement in summer',
                        'muskmelon': '🍈 Muskmelon - Warm season crop',
                        'apple': '🍎 Apple - Temperate climate fruit',
                        'orange': '🍊 Orange - Citrus fruit, warm climate',
                        'papaya': '🥭 Papaya - Tropical fruit, year-round growing',
                        'coconut': '🥥 Coconut - Coastal tropical crop',
                        'cotton': '🌿 Cotton - Cash crop, moderate water needs',
                        'jute': '🌿 Jute - Fiber crop, high humidity required',
                        'coffee': '☕ Coffee - Shade-grown, specific climate needs'
                    }
                    
                    if prediction.lower() in crop_info:
                        st.info(crop_info[prediction.lower()])
                        
            except Exception as e:
                st.error(f"❌ **PREDICTION FAILED**: {str(e)}")
                st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")
    
    # === IRRIGATION DECISIONS SECTION ===
    st.divider()
    st.subheader("💧 Smart Irrigation Analysis")
    
    # Unified Irrigation Check & Optimization
    if st.button("🔍 Analyze Irrigation Needs", type="primary", width="stretch", key="irrigation_analysis"):
        if not system_operational or not MODEL_STATUS['irrigation_model']:
            st.error("❌ **FAIL-SAFE ACTIVATED**: Irrigation model unavailable")
            st.info("🔄 **Returned Value**: 0 (Safe failure mode)")
        else:
            try:
                # STEP 1: Smart Irrigation Check
                st.markdown("### 📊 Step 1: Irrigation Decision")
                
                # Create features for irrigation model
                irrigation_features = create_irrigation_features(
                    soil_moisture, temp, hum, ph, N, P, K, rain
                )
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"IRR_INPUTS: soil_moisture={soil_moisture}, temp={temp}, hum={hum}, ph={ph}, N={N}, P={P}, K={K}, rain={rain}\n")
                except Exception:
                    pass
                
                pred = irrigation_model.predict(irrigation_features)[0]
                
                # Get prediction probability if available
                try:
                    prob = irrigation_model.predict_proba(irrigation_features).max()
                except Exception:
                    prob = None
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"IRR_OUTPUT: pred={pred}, conf={prob}\n")
                except Exception:
                    pass

                if show_debug:
                    st.markdown("**Debug — irrigation model inputs**")
                    st.write(irrigation_features.tolist())
                    st.markdown("**Debug — irrigation model outputs**")
                    st.write({"prediction": str(pred), "confidence": float(prob) if prob is not None else None})

                # Display irrigation decision
                irrigation_needed = (pred == 1 or pred == 'irrigate')
                
                # Professional irrigation decision card
                prob_value = prob if prob is not None else 0.0
                confidence_class = "confidence-high" if prob_value >= 0.8 else ("confidence-medium" if prob_value >= 0.6 else "confidence-low")
                
                if irrigation_needed:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">
                            <div class="result-icon">💧</div>
                            <div>
                                <div class="result-title">Irrigation Decision</div>
                                <span class="confidence-badge {confidence_class}">Confidence: {prob_value*100:.1f}%</span>
                            </div>
                        </div>
                        <div class="result-value">Irrigation Needed</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # STEP 2: Calculate Optimal Irrigation Amount (only if irrigation is needed)
                    st.markdown("### ⚡ Step 2: Optimal Irrigation Amount")
                    
                    if not MODEL_STATUS['optimization_model']:
                        st.warning("⚠️ **Optimization model unavailable** - Cannot calculate optimal amount")
                    else:
                        try:
                            # Create features for optimization model
                            optimization_features = create_optimization_features(
                                soil_moisture, temp, hum, ph, N, P, K, rain
                            )
                            
                            try:
                                with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                                    _dbg.write(f"OPT_INPUTS: soil_moisture={soil_moisture}, temp={temp}, hum={hum}, ph={ph}, N={N}, P={P}, K={K}, rain={rain}\n")
                            except Exception:
                                pass
                            
                            optimization_pred = optimization_model.predict(optimization_features)[0]
                            
                            try:
                                with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                                    _dbg.write(f"OPT_OUTPUT: pred={optimization_pred}\n")
                            except Exception:
                                pass

                            if show_debug:
                                st.markdown("**Debug — optimization model inputs**")
                                st.write(optimization_features.tolist())
                                st.markdown("**Debug — optimization model outputs**")
                                st.write({"prediction": float(optimization_pred)})
                            
                            # Validation check
                            if optimization_pred < 0 or optimization_pred > 100:
                                st.error("❌ **INVALID OPTIMIZATION RESULT**")
                                st.info("🔄 **Returned Value**: 0 (Validation fail-safe)")
                            else:
                                # Display optimal amount in styled card
                                st.markdown(f"""
                                <div class="result-card">
                                    <div class="result-header">
                                        <div class="result-icon">💦</div>
                                        <div>
                                            <div class="result-title">Optimal Irrigation Amount</div>
                                        </div>
                                    </div>
                                    <div class="result-value">{optimization_pred:.2f} units</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Summary box with modern styling
                                st.markdown(f"""
                                <div class="success-box">
                                    <h4 style="margin-top: 0; color: var(--secondary-green);">🎯 Irrigation Summary</h4>
                                    <ul style="margin-bottom: 0;">
                                        <li><strong>Decision:</strong> Irrigation Required ✅</li>
                                        <li><strong>Optimal Amount:</strong> {optimization_pred:.2f} units</li>
                                        <li><strong>Confidence:</strong> {prob_value*100:.1f}%</li>
                                    </ul>
                                </div>
                                """, unsafe_allow_html=True)
                                
                        except Exception as e:
                            st.error(f"❌ **OPTIMIZATION FAILED**: {str(e)}")
                            st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")
                else:
                    # No irrigation needed card
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-header">
                            <div class="result-icon">✋</div>
                            <div>
                                <div class="result-title">Irrigation Decision</div>
                                <span class="confidence-badge {confidence_class}">Confidence: {prob_value*100:.1f}%</span>
                            </div>
                        </div>
                        <div class="result-value">No Irrigation Needed</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Info box
                    st.markdown("""
                    <div class="info-box">
                        <p style="margin: 0;"><strong>✅ Soil conditions are adequate</strong> - No irrigation required at this time</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Summary box
                    st.markdown(f"""
                    <div class="success-box">
                        <h4 style="margin-top: 0; color: var(--secondary-green);">🎯 Irrigation Summary</h4>
                        <ul style="margin-bottom: 0;">
                            <li><strong>Decision:</strong> No Irrigation Required ✅</li>
                            <li><strong>Recommended Amount:</strong> 0.00 units</li>
                            <li><strong>Confidence:</strong> {prob_value*100:.1f}%</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"❌ **IRRIGATION ANALYSIS FAILED**: {str(e)}")
                st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")

    # Gemini AI Section
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="custom-card">
        <h3>🤖 AI Assistant (Gemini)</h3>
        <p style="color: #6c757d;">Get expert agricultural advice and personalized recommendations</p>
    </div>
    """, unsafe_allow_html=True)

    gemini_prompt = st.text_area(
        "💬 Ask me anything about crops, irrigation, or farming",
        placeholder="Example: What's the best way to irrigate rice during a heat wave?",
        key="gemini_prompt",
        height=100
    )

    context_snippet = (
        f"Current soil inputs -> N:{N}, P:{P}, K:{K}, Temp:{temp}°C, Humidity:{hum}%, pH:{ph}, Rainfall:{rain}mm, "
        f"Soil moisture:{soil_moisture}, Wind:{wind_speed}km/h, Pressure:{pressure}kPa"
    )

    if st.button("✨ Ask Gemini", type="primary", key="gemini_button"):
        clean_prompt = gemini_prompt.strip()
        if not clean_prompt:
            st.warning("⚠️ Please type a question first.")
        else:
            with st.spinner("Contacting Gemini..."):
                try:
                    try:
                        with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                            _dbg.write(f"GEMINI_PROMPT: {clean_prompt}\n")
                    except Exception:
                        pass

                    system_instruction = (
                        "You are AgriTech Assistant (Gemini) that explains crop and irrigation guidance in concise, practical English. "
                        "Use the provided soil context when relevant and keep responses under 200 words."
                    )
                    gemini_result = call_gemini_chat(
                        clean_prompt,
                        context=context_snippet,
                        system_instruction=system_instruction
                    )

                    if isinstance(gemini_result, dict):
                        gemini_response = gemini_result.get("text", "")
                        gemini_notice = gemini_result.get("notice")
                        gemini_model_used = gemini_result.get("model_used")
                        gemini_attempts = gemini_result.get("attempts")
                    else:
                        gemini_response = gemini_result
                        gemini_notice = None
                        gemini_model_used = None
                        gemini_attempts = None

                    st.success("✅ Response from Gemini")
                    st.markdown(gemini_response)

                    if gemini_notice:
                        st.info(gemini_notice)
                    if gemini_model_used:
                        st.caption(f"Gemini model: {gemini_model_used}")
                    if show_debug and gemini_attempts:
                        st.markdown("**Debug — Gemini attempts**")
                        st.write(gemini_attempts)

                    try:
                        with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                            _dbg.write(
                                f"GEMINI_RESPONSE: model={gemini_model_used}, notice={gemini_notice}, attempts={gemini_attempts}, text={gemini_response}\n"
                            )
                    except Exception:
                        pass

                except Exception as e:
                    st.error(f"❌ Gemini API error: {str(e)}")
                    st.info("Please verify your API key and internet connection, then try again.")
                    st.caption("Troubleshooting: set GEMINI_API_KEY in .env, pin GEMINI_MODEL=gemini-1.5-flash, and restart Streamlit after edits.")
                    try:
                        with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                            _dbg.write(f"GEMINI_ERROR: {str(e)}\n")
                    except Exception:
                        pass

# Professional Footer
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #6c757d;">
    <h3 style="color: var(--primary-green); margin-bottom: 1rem;">🌱 AgriTech Smart Advisor</h3>
    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">Empowering farmers with AI-driven precision agriculture</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">💡 Intelligent Crop Recommendations • Smart Irrigation Management • Real-time IoT Monitoring</p>
</div>
""", unsafe_allow_html=True)

# Add sidebar with additional information
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <h2 style="color: white;">🌱 AgriTech</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Smart Agriculture Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: white;">
        <h3 style="color: #f4a535;">📊 System Features</h3>
        <ul style="color: rgba(255,255,255,0.9);">
            <li>🌾 AI Crop Recommendation</li>
            <li>💧 Smart Irrigation Analysis</li>
            <li>🏞️ Soil Type Classification</li>
            <li>📡 IoT Sensor Integration</li>
            <li>🤖 AI Agricultural Assistant</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: white;">
        <h3 style="color: #f4a535;">💡 Quick Tips</h3>
        <ul style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">
            <li>Enable IoT auto-fill for real-time data</li>
            <li>Upload clear soil images for accurate classification</li>
            <li>Adjust parameters to explore different scenarios</li>
            <li>Use the AI assistant for personalized advice</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Model Status in sidebar
    st.markdown("""
    <div style="color: white;">
        <h3 style="color: #f4a535;">🔧 Model Status</h3>
    </div>
    """, unsafe_allow_html=True)
    
    for model_name, status in MODEL_STATUS.items():
        status_icon = "✅" if status else "❌"
        status_color = "#4CAF50" if status else "#f44336"
        display_name = model_name.replace('_', ' ').title()
        st.markdown(f"""
        <div style="color: white; padding: 0.5rem 0; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.2rem;">{status_icon}</span>
            <span style="font-size: 0.9rem;">{display_name}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem; text-align: center; padding-top: 1rem;">
        <p>© 2025 AgriTech Platform</p>
        <p>Version 2.0</p>
    </div>
    """, unsafe_allow_html=True)
