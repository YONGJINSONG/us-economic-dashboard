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
    
    # rrg_blog.py의 정확한 로직을 직접 실행
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

# 데이터 필터링 (rrg_blog.py와 동일)
latest_data_for_tickers = tickers_data_daily.iloc[::-1]
filtered_data_for_tickers = latest_data_for_tickers.iloc[::period]
tickers_data = filtered_data_for_tickers.iloc[::-1]

latest_data_for_bm = benchmark_data_daily.iloc[::-1]
filtered_data_for_bm = latest_data_for_bm.iloc[::period]
benchmark_data = filtered_data_for_bm.iloc[::-1]

window = 14  # Z-Score 계산할 주기
tail = 7  # 그래프에 표시할 기간(최근 몇주)

rs_tickers = []
rsr_tickers = []
rsr_roc_tickers = []
rsm_tickers = []

for i in range(len(tickers)):
    # RS 계산 (rrg_blog.py와 동일)
    ticker_series = tickers_data[tickers[i]]
    benchmark_series = benchmark_data.iloc[:, 0] if len(benchmark_data.shape) > 1 else benchmark_data
    
    # 인덱스 정렬
    common_index = ticker_series.index.intersection(benchmark_series.index)
    ticker_aligned = ticker_series.loc[common_index]
    benchmark_aligned = benchmark_series.loc[common_index]
    
    rs_tickers.append(100 * (ticker_aligned / benchmark_aligned))
    
    # RSR 계산 (rrg_blog.py와 동일)
    actual_window = min(window, len(rs_tickers[i]) - 1)
    if actual_window < 2:
        actual_window = 2
    
    rolling_mean = rs_tickers[i].rolling(window=actual_window, min_periods=1).mean()
    rolling_std = rs_tickers[i].rolling(window=actual_window, min_periods=1).std(ddof=0)
    rolling_std = rolling_std.replace(0, 1)
    
    rsr_calculation = 100 + (rs_tickers[i] - rolling_mean) / rolling_std
    rsr_tickers.append(rsr_calculation.dropna())
    
    # RSR ROC 계산
    if len(rsr_tickers[i]) > 0:
        rsr_roc_tickers.append(100 * ((rsr_tickers[i] / rsr_tickers[i].iloc[0]) - 1))
        
        # RSM 계산 (rrg_blog.py와 동일)
        rsm_actual_window = min(window, len(rsr_roc_tickers[i]) - 1)
        if rsm_actual_window < 2:
            rsm_actual_window = 2
        
        rsm_rolling_mean = rsr_roc_tickers[i].rolling(window=rsm_actual_window, min_periods=1).mean()
        rsm_rolling_std = rsr_roc_tickers[i].rolling(window=rsm_actual_window, min_periods=1).std(ddof=0)
        rsm_rolling_std = rsm_rolling_std.replace(0, 1)
        
        rsm_tickers.append((101 + (rsr_roc_tickers[i] - rsm_rolling_mean) / rsm_rolling_std).dropna())
        
        # 인덱스 정렬
        rsr_tickers[i] = rsr_tickers[i][rsr_tickers[i].index.isin(rsm_tickers[i].index)]
        rsm_tickers[i] = rsm_tickers[i][rsm_tickers[i].index.isin(rsr_tickers[i].index)]
        
        # 최근 tail개 데이터만 유지 (rrg_blog.py와 동일)
        if len(rsr_tickers[i]) >= tail:
            rsr_tickers[i] = rsr_tickers[i].iloc[-tail:]
            rsm_tickers[i] = rsm_tickers[i].iloc[-tail:]
    else:
        rsr_roc_tickers.append(pd.Series())
        rsm_tickers.append(pd.Series())

# JSON 데이터 생성
rrg_data = {}
rrg_timeline_data = {}
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

for i, ticker in enumerate(tickers):
    if len(rsr_tickers[i]) > 0 and len(rsm_tickers[i]) > 0:
        x = float(rsr_tickers[i].iloc[-1])
        y = float(rsm_tickers[i].iloc[-1])
        rs = float(rs_tickers[i].iloc[-1])
        
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
        
        # 타임라인 데이터 생성 (rrg_blog.py와 동일)
        timeline = []
        for j in range(len(rsr_tickers[i])):
            timeline.append({
                "date": rsr_tickers[i].index[j].strftime('%Y-%m-%d'),
                "x": round(float(rsr_tickers[i].iloc[j]), 4),
                "y": round(float(rsm_tickers[i].iloc[j]), 4)
            })
        
        rrg_timeline_data[ticker] = {
            "name": sector_names[ticker],
            "timeline": timeline,
            "current": timeline[-1] if timeline else None
        }

# JSON 파일로 저장
with open('rrg_data.json', 'w', encoding='utf-8') as f:
    json.dump(rrg_data, f, indent=4, ensure_ascii=False)

# 타임라인 데이터도 별도 파일로 저장
with open('rrg_timeline_data.json', 'w', encoding='utf-8') as f:
    json.dump(rrg_timeline_data, f, indent=4, ensure_ascii=False)

print(f"Total sectors: {len(rrg_data)}")
for symbol, data in rrg_data.items():
    timeline_count = len(rrg_timeline_data[symbol]['timeline']) if symbol in rrg_timeline_data else 0
    print(f"{symbol}: RSR={data['rsr']:.2f}, RSM={data['rsm']:.2f}, {data['quadrant']} (timeline: {timeline_count} points)")
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
