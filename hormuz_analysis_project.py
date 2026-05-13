#!/usr/bin/env python3
"""
====================================================
 Strait of Hormuz Shipping Disruption 2026
 Data Analytics Project
 Tool: Python (IBM Cognos-equivalent analysis)
 Dataset: Kaggle - Strait of Hormuz 2026
====================================================
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ─── PHASE 1: DATA COLLECTION ───────────────────────────────────────────────
# Dataset downloaded from Kaggle:
# https://www.kaggle.com/datasets/strait-of-hormuz-shipping-disruption-2026
RAW_FILE = 'strait_of_hormuz_shipping_disruption_2026__1_.csv'
df_raw = pd.read_csv(RAW_FILE)
print(f"Loaded: {df_raw.shape[0]} rows × {df_raw.shape[1]} columns")

# ─── PHASE 2: DATA CLEANING & PREPROCESSING ─────────────────────────────────
df = df_raw.copy()

# Fix date column
df['date'] = pd.to_datetime(df['date'])

# Create readable period label
df['period_label'] = df['period_type'].map({'pre_war': 'Pre-War', 'war_crisis': 'War Crisis'})

# Create month column
df['month'] = df['date'].dt.to_period('M').astype(str)

# Round float columns
float_cols = df.select_dtypes(include='float64').columns
df[float_cols] = df[float_cols].round(2)

# Trim carrier status columns
status_cols = ['maersk_status','cma_cgm_status','hapag_lloyd_status','cosco_status','msc_status']
for col in status_cols:
    df[col] = df[col].str.strip()

# Encode crisis severity
def severity(pct):
    if pct >= 80: return 'Normal'
    elif pct >= 40: return 'Moderate'
    elif pct >= 10: return 'Severe'
    else: return 'Critical'
df['crisis_severity'] = df['transit_pct_of_prewar_avg'].apply(severity)

# Save cleaned file
df.to_csv('hormuz_clean.csv', index=False)
print("Cleaned dataset saved: hormuz_clean.csv")
print(f"Null values after cleaning: {df.isnull().sum().sum()}")

# ─── PHASE 3: ANALYSIS ───────────────────────────────────────────────────────
pre = df[df['period_label'] == 'Pre-War']
war = df[df['period_label'] == 'War Crisis']

print("\n=== KEY FINDINGS ===")
print(f"Ship transits dropped: {pre['daily_ship_transits'].mean():.0f} → {war['daily_ship_transits'].mean():.0f} per day")
print(f"Oil throughput dropped: {pre['oil_throughput_mbpd'].mean():.1f} → {war['oil_throughput_mbpd'].mean():.1f} mbpd")
print(f"Brent crude rose: ${pre['brent_crude_usd_bbl'].mean():.2f} → ${war['brent_crude_usd_bbl'].mean():.2f}")
print(f"War risk insurance: {pre['war_risk_insurance_pct'].mean():.2f}% → {war['war_risk_insurance_pct'].mean():.2f}%")
print(f"Vessels attacked (total): {war['vessels_attacked_cumulative'].max()}")

print("\nProject complete. All outputs saved.")
