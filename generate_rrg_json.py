#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RRG 데이터 JSON 파일 생성 스크립트
GitHub Actions에서 자동 실행되어 rrg_data.json을 업데이트합니다.
"""

import json
import requests
import sys

def main():
    """
    로컬 RRG API 서버에서 데이터를 가져와 JSON 파일로 저장
    """
    print("=" * 60)
    print("RRG Data Generator for GitHub Actions")
    print("=" * 60)
    
    # 먼저 rrg_blog.py를 직접 실행하여 데이터 생성
    print("Running RRG calculation...")
    
    import subprocess
    
    # rrg_blog.py의 로직을 직접 실행
    script_code = '''
import pandas as pd
import yfinance as yf
import warnings
import datetime
import json

warnings.filterwarnings("ignore")

tickers = ['XLB', 'XLC', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY', 'XLRE']
days_before = 360
from_date = datetime.datetime.today() - datetime.timedelta(days=days_before)
to_date = datetime.datetime.today()
period = 5

# 섹터 이름 매핑
sector_names = {
    'XLB': 'Materials',
    'XLC': 'Communication Services',
    'XLE': 'Energy',
    'XLF': 'Financials',
    'XLI': 'Industrials',
    'XLK': 'Technology',
    'XLP': 'Consumer Staples',
    'XLU': 'Utilities',
    'XLV': 'Healthcare',
    'XLY': 'Consumer Discretionary',
    'XLRE': 'Real Estate'
}

benchmark = '^SPX'

# 데이터 다운로드
tickers_data_daily = yf.download(tickers, start=from_date, end=to_date, progress=False)
benchmark_data_daily = yf.download(benchmark, start=from_date, end=to_date, progress=False)

# Close 가격 추출
if isinstance(tickers_data_daily.columns, pd.MultiIndex):
    tickers_data_daily = tickers_data_daily['Close']
else:
    tickers_data_daily = tickers_data_daily['Close']

if isinstance(benchmark_data_daily.columns, pd.MultiIndex):
    benchmark_data_daily = benchmark_data_daily['Close']
else:
    benchmark_data_daily = benchmark_data_daily['Close']

# 데이터 필터링
latest_data_for_tickers = tickers_data_daily.iloc[::-1]
filtered_data_for_tickers = latest_data_for_tickers.iloc[::period]
tickers_data = filtered_data_for_tickers.iloc[::-1]

latest_data_for_benchmark = benchmark_data_daily.iloc[::-1]
filtered_data_for_benchmark = latest_data_for_benchmark.iloc[::period]
benchmark_data = filtered_data_for_benchmark.iloc[::-1]

# Relative Strength 계산
relative_strength_ratio = (tickers_data / benchmark_data.values.reshape(-1, 1)) * 100

# 이동평균 및 모멘텀 계산
window = 14
relative_strength_ma = relative_strength_ratio.rolling(window=window).mean()
relative_strength_momentum = relative_strength_ma.pct_change(periods=1) * 100

# 최신 값 추출
latest_rs = relative_strength_ratio.iloc[-1]
latest_momentum = relative_strength_momentum.iloc[-1]

# Z-score 정규화
rs_mean = latest_rs.mean()
rs_std = latest_rs.std()
if rs_std == 0:
    rs_std = 1
rsr_normalized = 100 + ((latest_rs - rs_mean) / rs_std)

momentum_mean = latest_momentum.mean()
momentum_std = latest_momentum.std()
if momentum_std == 0:
    momentum_std = 1
rsm_normalized = 100 + ((latest_momentum - momentum_mean) / momentum_std)

# JSON 데이터 생성
rrg_data = {}
today = datetime.datetime.now().strftime('%Y-%m-%d')

def get_quadrant_status(x, y):
    if x >= 100 and y >= 100:
        return "Leading (선도)"
    elif x < 100 and y >= 100:
        return "Improving (개선)"
    elif x < 100 and y < 100:
        return "Lagging (지연)"
    else:
        return "Weakening (약화)"

for ticker in tickers:
    if not pd.isna(rsr_normalized[ticker]) and not pd.isna(rsm_normalized[ticker]):
        x = float(rsr_normalized[ticker])
        y = float(rsm_normalized[ticker])
        rs = float(latest_rs[ticker])
        
        rrg_data[ticker] = {
            "name": sector_names[ticker],
            "x": round(x, 4),
            "y": round(y, 4),
            "rsr": round(x, 4),
            "rsm": round(y, 4),
            "relative_strength": round(rs, 4),
            "quadrant": get_quadrant_status(x, y),
            "date": today,
            "calculation_method": "rrg_blog.py"
        }

# JSON 파일로 저장
with open('rrg_data.json', 'w', encoding='utf-8') as f:
    json.dump(rrg_data, f, indent=4, ensure_ascii=False)

print(f"Total sectors: {len(rrg_data)}")
for symbol, data in rrg_data.items():
    print(f"{symbol}: RSR={data['rsr']:.2f}, RSM={data['rsm']:.2f}, {data['quadrant']}")
'''
    
    # 스크립트 실행
    result = subprocess.run([sys.executable, '-c', script_code], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        print("\n[SUCCESS] RRG data generation completed!")
        print("=" * 60)
    else:
        print("[ERROR] RRG data generation failed!")
        print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
