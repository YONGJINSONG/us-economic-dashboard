#!/usr/bin/env python3
"""
RRG Blog API Server
rrg_blog.py의 계산 방식을 기반으로 한 정확한 RRG API 서버
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)  # CORS 활성화

class RRGBlogCalculator:
    """rrg_blog.py 방식의 RRG 계산 클래스"""
    
    def __init__(self):
        self.sector_symbols = ['XLB', 'XLC', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY', 'XLRE']
        self.benchmark_symbol = '^SPX'  # SPX 인덱스 사용 (SPY 대신)
        
        self.sector_names = {
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
        
        # rrg_blog.py의 설정값들
        self.window = 14  # Z-Score 계산할 주기
        self.tail = 7     # 그래프에 표시할 기간(최근 몇주)
    
    def get_data(self, period_days=63):
        """yfinance를 사용하여 ETF 데이터 수집 (rrg_blog.py 방식)"""
        print(f"Fetching data for {period_days} days using rrg_blog.py method...")
        
        # 종료 날짜 (오늘)
        end_date = datetime.now()
        # 시작 날짜 (period_days + 여유분)
        start_date = end_date - timedelta(days=period_days + 50)
        
        print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        try:
            # ETF 데이터 다운로드
            tickers_data = yf.download(self.sector_symbols, start=start_date, end=end_date)
            benchmark_data = yf.download(self.benchmark_symbol, start=start_date, end=end_date)
            
            # MultiIndex 처리
            if isinstance(tickers_data.columns, pd.MultiIndex):
                tickers_data = tickers_data['Close']
            else:
                tickers_data = tickers_data['Close']
                
            if isinstance(benchmark_data.columns, pd.MultiIndex):
                benchmark_data = benchmark_data['Close']
            else:
                benchmark_data = benchmark_data['Close']
            
            print(f"✓ Downloaded {len(tickers_data)} days of data")
            return tickers_data, benchmark_data
            
        except Exception as e:
            print(f"❌ Error downloading data: {e}")
            return None, None
    
    def calculate_rsr_rsm(self, tickers_data, benchmark_data, period=5):
        """rrg_blog.py 방식으로 RSR과 RSM 계산"""
        print("Calculating RSR and RSM using rrg_blog.py method...")
        
        # 데이터 필터링 (rrg_blog.py 방식)
        latest_data_for_tickers = tickers_data.iloc[::-1]  # 데이터를 역순으로 정렬
        filtered_data_for_tickers = latest_data_for_tickers.iloc[::period]  # x일 간격으로 선택
        tickers_filtered = filtered_data_for_tickers.iloc[::-1]  # 원래 순서로 복원
        
        latest_data_for_bm = benchmark_data.iloc[::-1]  # 데이터를 역순으로 정렬
        filtered_data_for_bm = latest_data_for_bm.iloc[::period]  # x일 간격으로 선택
        benchmark_filtered = filtered_data_for_bm.iloc[::-1]  # 원래 순서로 복원
        
        rs_tickers = []
        rsr_tickers = []
        rsr_roc_tickers = []
        rsm_tickers = []
        
        for i, ticker in enumerate(self.sector_symbols):
            try:
                # RS 계산
                ticker_series = tickers_filtered[ticker]
                benchmark_series = benchmark_filtered.iloc[:, 0]  # DataFrame에서 Series 추출
                
                # 인덱스 정렬
                common_index = ticker_series.index.intersection(benchmark_series.index)
                ticker_aligned = ticker_series.loc[common_index]
                benchmark_aligned = benchmark_series.loc[common_index]
                
                rs = 100 * (ticker_aligned / benchmark_aligned)
                rs_tickers.append(rs)
                
                # RSR 계산
                actual_window = min(self.window, len(rs) - 1)
                if actual_window < 2:
                    actual_window = 2
                
                rolling_mean = rs.rolling(window=actual_window, min_periods=1).mean()
                rolling_std = rs.rolling(window=actual_window, min_periods=1).std(ddof=0)
                
                # 표준편차가 0인 경우를 처리
                rolling_std = rolling_std.replace(0, 1)
                
                rsr = 100 + (rs - rolling_mean) / rolling_std
                rsr_tickers.append(rsr.dropna())
                
                if len(rsr_tickers[i]) > 0:
                    # RSR ROC 계산
                    rsr_roc = 100 * ((rsr_tickers[i] / rsr_tickers[i].iloc[0]) - 1)
                    rsr_roc_tickers.append(rsr_roc)
                    
                    # RSM 계산
                    rsm_actual_window = min(self.window, len(rsr_roc) - 1)
                    if rsm_actual_window < 2:
                        rsm_actual_window = 2
                    
                    rsm_rolling_mean = rsr_roc.rolling(window=rsm_actual_window, min_periods=1).mean()
                    rsm_rolling_std = rsr_roc.rolling(window=rsm_actual_window, min_periods=1).std(ddof=0)
                    
                    rsm_rolling_std = rsm_rolling_std.replace(0, 1)
                    
                    rsm = (101 + (rsr_roc - rsm_rolling_mean) / rsm_rolling_std).dropna()
                    rsm_tickers.append(rsm)
                    
                    # 인덱스 정렬
                    rsr_tickers[i] = rsr_tickers[i][rsr_tickers[i].index.isin(rsm.index)]
                    rsm_tickers[i] = rsm[rsm.index.isin(rsr_tickers[i].index)]
                    
                    # 최근 데이터 추출
                    if len(rsr_tickers[i]) >= self.tail:
                        rsr_tickers[i] = rsr_tickers[i].iloc[-self.tail:]
                        rsm_tickers[i] = rsm_tickers[i].iloc[-self.tail:]
                else:
                    rsr_roc_tickers.append(pd.Series())
                    rsm_tickers.append(pd.Series())
                    
            except Exception as e:
                print(f"❌ Error calculating for {ticker}: {e}")
                rs_tickers.append(pd.Series())
                rsr_tickers.append(pd.Series())
                rsr_roc_tickers.append(pd.Series())
                rsm_tickers.append(pd.Series())
        
        return rsr_tickers, rsm_tickers
    
    def get_quadrant_status(self, x, y):
        """rrg_blog.py 방식의 사분면 분류"""
        if x < 100 and y < 100:
            return 'Lagging (지연)'
        elif x > 100 and y > 100:
            return 'Leading (선도)'
        elif x < 100 and y > 100:
            return 'Improving (개선)'
        elif x > 100 and y < 100:
            return 'Weakening (약화)'
        else:
            return 'Neutral (중립)'
    
    def generate_rrg_timeline_data(self, period_days=63):
        """시간별 RRG 데이터 생성 (화살표용)"""
        try:
            print(f"Generating RRG timeline data for {period_days} days...")
            
            # 데이터 수집
            tickers_data, benchmark_data = self.get_data(period_days)
            if tickers_data is None or benchmark_data is None:
                return None
            
            # RSR과 RSM 계산
            rsr_tickers, rsm_tickers = self.calculate_rsr_rsm(tickers_data, benchmark_data, period_days)
            
            # 시간별 데이터 생성
            timeline_data = {}
            
            for i, symbol in enumerate(self.sector_symbols):
                if i < len(rsr_tickers) and len(rsr_tickers[i]) > 0:
                    rsr_series = rsr_tickers[i]
                    rsm_series = rsm_tickers[i]
                    
                    # 시간별 포인트 생성
                    timeline_points = []
                    for j in range(len(rsr_series)):
                        timeline_points.append({
                            'date': rsr_series.index[j].strftime('%Y-%m-%d'),
                            'x': round(float(rsr_series.iloc[j]), 4),  # 정밀도 향상
                            'y': round(float(rsm_series.iloc[j]), 4)   # 정밀도 향상
                        })
                    
                    timeline_data[symbol] = {
                        'name': self.sector_names[symbol],
                        'timeline': timeline_points,
                        'current': timeline_points[-1] if timeline_points else None,
                        '_source': 'rrg_blog_api'
                    }
            
            return timeline_data
            
        except Exception as e:
            print(f"Error generating RRG timeline data: {e}")
            return None
    
    def generate_rrg_data(self, period_days=63):
        """RRG 데이터 생성"""
        print(f"Generating RRG data for {period_days} days...")
        
        # 데이터 수집
        tickers_data, benchmark_data = self.get_data(period_days)
        if tickers_data is None or benchmark_data is None:
            return None
        
        # RSR, RSM 계산
        rsr_tickers, rsm_tickers = self.calculate_rsr_rsm(tickers_data, benchmark_data)
        
        # 결과 데이터 구성
        result = {}
        for i, ticker in enumerate(self.sector_symbols):
            try:
                if len(rsr_tickers[i]) > 0 and len(rsm_tickers[i]) > 0:
                    # 최신 값들
                    latest_rsr = rsr_tickers[i].iloc[-1]
                    latest_rsm = rsm_tickers[i].iloc[-1]
                    
                    # 상대강도 (Relative Strength) - RS 값
                    rs_value = 100 * (tickers_data[ticker].iloc[-1] / benchmark_data.iloc[-1, 0])
                    
                    result[ticker] = {
                        'name': self.sector_names[ticker],
                        'relative_strength': round(rs_value, 4),
                        'rsr': round(latest_rsr, 4),
                        'rsm': round(latest_rsm, 4),
                        'x': round(latest_rsr, 4),
                        'y': round(latest_rsm, 4),
                        'quadrant': self.get_quadrant_status(latest_rsr, latest_rsm),
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'calculation_method': 'rrg_blog.py'
                    }
                    
                    print(f"✓ {ticker} ({self.sector_names[ticker]}): RSR={latest_rsr:.4f}, RSM={latest_rsm:.4f}, Quadrant={self.get_quadrant_status(latest_rsr, latest_rsm)}")
                else:
                    print(f"❌ {ticker}: No data available")
                    
            except Exception as e:
                print(f"❌ Error processing {ticker}: {e}")
        
        return result

# Flask 라우트
@app.route('/api/rrg/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'running',
        'message': 'RRG Blog API Server is running',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/rrg/sectors', methods=['GET'])
def sectors():
    calculator = RRGBlogCalculator()
    return jsonify({
        'benchmark': calculator.benchmark_symbol,
        'sectors': calculator.sector_names,
        'sector_count': len(calculator.sector_symbols)
    })

@app.route('/api/rrg/generate', methods=['GET'])
def generate_rrg():
    try:
        period = request.args.get('period', 63, type=int)
        print(f"API request: RRG data generation (period: {period} days)")
        
        calculator = RRGBlogCalculator()
        data = calculator.generate_rrg_data(period)
        
        if data:
            return jsonify({
                'status': 'success',
                'data': data,
                'period': period,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'method': 'rrg_blog.py'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to generate RRG data'
            }), 500
            
    except Exception as e:
        print(f"Error in generate_rrg: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/rrg/timeline', methods=['GET'])
def generate_rrg_timeline():
    try:
        period = request.args.get('period', 63, type=int)
        print(f"API request: RRG timeline data generation (period: {period} days)")
        
        calculator = RRGBlogCalculator()
        timeline_data = calculator.generate_rrg_timeline_data(period)
        
        if timeline_data:
            return jsonify({
                'status': 'success',
                'data': timeline_data,
                'period': period,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'method': 'rrg_blog.py_timeline'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to generate RRG timeline data'
            }), 500
            
    except Exception as e:
        print(f"Error in generate_rrg_timeline: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 RRG Blog API Server starting...")
    print("📊 Using rrg_blog.py calculation method with SPX benchmark")
    print("🌐 API endpoints:")
    print("   - GET /api/rrg/generate?period=63")
    print("   - GET /api/rrg/status")
    print("   - GET /api/rrg/sectors")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=5001, debug=True)
