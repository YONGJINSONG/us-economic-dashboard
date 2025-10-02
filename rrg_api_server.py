#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RRG (Relative Rotation Graph) API Server
yfinance를 사용하여 실시간 ETF 데이터를 수집하고 RRG를 계산합니다.
"""

import sys
import io
# Windows 인코딩 문제 해결
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

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

class RRGCalculator:
    """RRG 계산 클래스"""
    
    def __init__(self):
        self.sector_symbols = ['XLB', 'XLC', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLRE', 'XLU', 'XLV', 'XLY']
        self.benchmark_symbol = 'SPY'
        
        self.sector_names = {
            'XLB': 'Materials',
            'XLC': 'Communication Services', 
            'XLE': 'Energy',
            'XLF': 'Financials',
            'XLI': 'Industrials',
            'XLK': 'Technology',
            'XLP': 'Consumer Staples',
            'XLRE': 'Real Estate',
            'XLU': 'Utilities',
            'XLV': 'Healthcare',
            'XLY': 'Consumer Discretionary'
        }
    
    def get_data(self, period_days=252):
        """yfinance를 사용하여 ETF 데이터 수집"""
        print(f"Fetching data for {period_days} days...")
        
        # 종료 날짜 (오늘)
        end_date = datetime.now()
        # 시작 날짜 (period_days만큼 이전)
        start_date = end_date - timedelta(days=period_days + 50)  # 여유분 추가
        
        print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        try:
            # 벤치마크 (SPY) 데이터
            print("Downloading SPY data...")
            spy = yf.download('SPY', start=start_date, end=end_date, progress=False)
            print(f"SPY data shape: {spy.shape}")
            if spy.empty:
                raise ValueError("SPY 데이터를 가져올 수 없습니다.")
            print("✓ SPY 데이터 수집 완료")
            
            # 섹터 ETF 데이터 수집
            sector_data = {}
            for symbol in self.sector_symbols:
                try:
                    print(f"Downloading {symbol} data...")
                    data = yf.download(symbol, start=start_date, end=end_date, progress=False)
                    print(f"{symbol} data shape: {data.shape}")
                    if not data.empty:
                        sector_data[symbol] = data
                        print(f"✓ {symbol} 데이터 수집 완료")
                    else:
                        print(f"✗ {symbol} 데이터 없음")
                except Exception as e:
                    print(f"✗ {symbol} 데이터 수집 실패: {e}")
            
            print(f"Total sectors collected: {len(sector_data)}")
            return spy, sector_data
            
        except Exception as e:
            print(f"데이터 수집 중 오류 발생: {e}")
            import traceback
            traceback.print_exc()
            return None, None
    
    def calculate_relative_strength(self, etf_data, benchmark_data, period=252):
        """상대 강도 계산 - rrg_blog.py 방식"""
        try:
            # 최근 period일 데이터만 사용
            etf_recent = etf_data.tail(period)
            benchmark_recent = benchmark_data.tail(period)
            
            # yfinance 데이터 구조 처리 (MultiIndex 컬럼)
            if isinstance(etf_recent.columns, pd.MultiIndex):
                etf_close = etf_recent[('Close', etf_recent.columns.get_level_values(1)[0])]
                benchmark_close = benchmark_recent[('Close', benchmark_recent.columns.get_level_values(1)[0])]
            else:
                etf_close = etf_recent['Close']
                benchmark_close = benchmark_recent['Close']
            
            # rrg_blog.py 방식: RS = 100 * (ETF 가격 / 벤치마크 가격)
            # 전체 시리즈에 대해 계산 (단일 값이 아닌)
            relative_strength = 100 * (etf_close / benchmark_close)
            
            return relative_strength
            
        except Exception as e:
            print(f"상대 강도 계산 오류: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def calculate_rrg_metrics(self, etf_data, benchmark_data, period=252):
        """RRG 메트릭 계산 - rrg_blog.py 방식"""
        try:
            # 최근 period일 데이터만 사용
            etf_recent = etf_data.tail(period)
            benchmark_recent = benchmark_data.tail(period)
            
            # yfinance 데이터 구조 처리 (MultiIndex 컬럼)
            if isinstance(etf_recent.columns, pd.MultiIndex):
                etf_close = etf_recent[('Close', etf_recent.columns.get_level_values(1)[0])]
                benchmark_close = benchmark_recent[('Close', benchmark_recent.columns.get_level_values(1)[0])]
            else:
                etf_close = etf_recent['Close']
                benchmark_close = benchmark_recent['Close']
            
            # rrg_blog.py 방식: RSR과 RSM 계산
            window = 14  # rrg_blog.py와 동일한 윈도우 크기
            
            # RS 계산 (Relative Strength)
            rs = 100 * (etf_close / benchmark_close)
            
            # RSR 계산 (Relative Strength Ratio) - Z-Score 방식
            actual_window = min(window, len(rs) - 1)
            if actual_window < 2:
                actual_window = 2
            
            rolling_mean = rs.rolling(window=actual_window, min_periods=1).mean()
            rolling_std = rs.rolling(window=actual_window, min_periods=1).std(ddof=0)
            
            # 표준편차가 0인 경우를 처리
            rolling_std = rolling_std.replace(0, 1)
            
            rsr = 100 + (rs - rolling_mean) / rolling_std
            rsr = rsr.dropna()
            
            if len(rsr) == 0:
                return None, None, None
            
            # RSR ROC 계산 (Rate of Change) - rrg_blog.py 방식: 첫 번째 값 대비 변화율
            rsr_roc = 100 * ((rsr / rsr.iloc[0]) - 1)
            rsr_roc = rsr_roc.dropna()
            
            if len(rsr_roc) == 0:
                return rsr.iloc[-1], None, rs.iloc[-1]
            
            # RSM 계산 (Relative Strength Momentum) - RSR ROC의 Z-Score
            rsm_actual_window = min(window, len(rsr_roc) - 1)
            if rsm_actual_window < 2:
                rsm_actual_window = 2
            
            rsm_rolling_mean = rsr_roc.rolling(window=rsm_actual_window, min_periods=1).mean()
            rsm_rolling_std = rsr_roc.rolling(window=rsm_actual_window, min_periods=1).std(ddof=0)
            
            # 표준편차가 0인 경우를 처리
            rsm_rolling_std = rsm_rolling_std.replace(0, 1)
            
            rsm = 101 + (rsr_roc - rsm_rolling_mean) / rsm_rolling_std
            rsm = rsm.dropna()
            
            if len(rsm) == 0:
                return rsr.iloc[-1], None, rs.iloc[-1]
            
            # 최신 값들 반환 (RSR, RSM, RS)
            return rsr.iloc[-1], rsm.iloc[-1], rs.iloc[-1]
            
        except Exception as e:
            print(f"RRG 메트릭 계산 오류: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None
    
    
    def determine_quadrant(self, x, y):
        """사분면 결정 - rrg_blog.py 방식"""
        # rrg_blog.py 방식: 100을 기준으로 사분면 결정
        if x < 100 and y < 100:
            return "Lagging (약세)"
        elif x > 100 and y > 100:
            return "Leading (강세)"
        elif x < 100 and y > 100:
            return "Improving (개선)"
        elif x > 100 and y < 100:
            return "Weakening (약화)"
        else:
            return "Neutral (중립)"
    
    def calculate_rrg_data(self, period_days=252):
        """전체 RRG 데이터 계산"""
        print(f"RRG 데이터 계산 시작 (기간: {period_days}일)")
        
        # 데이터 수집
        spy_data, sector_data = self.get_data(period_days)
        if spy_data is None or not sector_data:
            return None
        
        rrg_data = {}
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        for symbol in self.sector_symbols:
            if symbol in sector_data:
                try:
                    # RRG 메트릭 계산 (RSR, RSM, RS)
                    rsr, rsm, rs = self.calculate_rrg_metrics(sector_data[symbol], spy_data, period_days)
                    if rsr is None or rsm is None or rs is None:
                        print(f"✗ {symbol}: 메트릭 계산 실패")
                        continue
                    
                    # 사분면 결정
                    quadrant = self.determine_quadrant(rsr, rsm)
                    
                    # 데이터 저장
                    rrg_data[symbol] = {
                        "name": self.sector_names[symbol],
                        "x": round(rsr, 4),
                        "y": round(rsm, 4),
                        "rsr": round(rsr, 4),
                        "rsm": round(rsm, 4),
                        "relative_strength": round(rs, 4),
                        "momentum": round(rsm, 4),
                        "date": current_date,
                        "quadrant": quadrant,
                        "calculation_method": "rrg_blog.py"
                    }
                    
                    print(f"✓ {symbol} ({self.sector_names[symbol]}): RSR={rsr:.4f}, RSM={rsm:.4f}, RS={rs:.4f}, Quadrant={quadrant}")
                    
                except Exception as e:
                    print(f"✗ {symbol} 계산 실패: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
        
        print(f"RRG 데이터 계산 완료: {len(rrg_data)}개 섹터")
        return rrg_data
    
    def calculate_rrg_timeline_data(self, period_days=252):
        """RRG 타임라인 데이터 계산 (화살표 표시용) - rrg_blog.py 방식"""
        print(f"RRG 타임라인 데이터 계산 시작 (기간: {period_days}일)")
        
        # 데이터 수집
        spy_data, sector_data = self.get_data(period_days)
        if spy_data is None or not sector_data:
            return None
        
        timeline_data = {}
        
        # 타임라인 포인트 수 결정 (기간에 따라)
        if period_days <= 21:
            num_points = 3
        elif period_days <= 63:
            num_points = 4
        else:
            num_points = 5
        
        for symbol in self.sector_symbols:
            if symbol not in sector_data:
                continue
                
            try:
                timeline = []
                
                # rrg_blog.py 방식: 실제 데이터 포인트들을 사용하여 timeline 생성
                etf_data = sector_data[symbol]
                benchmark_data = spy_data
                
                # 전체 기간에 대해 RRG 메트릭 계산
                etf_recent = etf_data.tail(period_days)
                benchmark_recent = benchmark_data.tail(period_days)
                
                if isinstance(etf_recent.columns, pd.MultiIndex):
                    etf_close = etf_recent[('Close', etf_recent.columns.get_level_values(1)[0])]
                    benchmark_close = benchmark_recent[('Close', benchmark_recent.columns.get_level_values(1)[0])]
                else:
                    etf_close = etf_recent['Close']
                    benchmark_close = benchmark_recent['Close']
                
                # 상대 강도 계산
                rs = 100 * (etf_close / benchmark_close)
                
                # RSR 계산 (Z-score 방식)
                window = 14
                actual_window = min(window, len(rs) - 1)
                if actual_window < 2:
                    actual_window = 2
                
                rolling_mean = rs.rolling(window=actual_window, min_periods=1).mean()
                rolling_std = rs.rolling(window=actual_window, min_periods=1).std(ddof=0)
                rolling_std = rolling_std.replace(0, 1)
                rsr = 100 + (rs - rolling_mean) / rolling_std
                rsr = rsr.dropna()
                
                # RSM 계산 (rrg_blog.py 방식)
                if len(rsr) > 0:
                    # rrg_blog.py 방식: 첫 번째 값 대비 변화율
                    rsr_roc = 100 * ((rsr / rsr.iloc[0]) - 1)
                    rsr_roc = rsr_roc.dropna()
                    
                    if len(rsr_roc) > 0:
                        rsm_actual_window = min(window, len(rsr_roc) - 1)
                        if rsm_actual_window < 2:
                            rsm_actual_window = 2
                        
                        rsm_rolling_mean = rsr_roc.rolling(window=rsm_actual_window, min_periods=1).mean()
                        rsm_rolling_std = rsr_roc.rolling(window=rsm_actual_window, min_periods=1).std(ddof=0)
                        rsm_rolling_std = rsm_rolling_std.replace(0, 1)
                        rsm = 101 + (rsr_roc - rsm_rolling_mean) / rsm_rolling_std
                        rsm = rsm.dropna()
                        
                        # 타임라인 포인트 생성 (등간격으로 선택) - 현재 데이터와 일치하도록 수정
                        if len(rsr) >= num_points and len(rsm) >= num_points:
                            # 마지막 포인트는 현재 데이터와 정확히 일치해야 함
                            # 현재 데이터 계산
                            current_rsr, current_rsm, current_rs = self.calculate_rrg_metrics(etf_data, benchmark_data, period_days)
                            
                            if current_rsr is not None and current_rsm is not None and current_rs is not None:
                                # 마지막 포인트를 현재 데이터로 설정
                                timeline.append({
                                    'date': datetime.now().strftime('%Y-%m-%d'),
                                    'x': round(float(current_rsr), 4),
                                    'y': round(float(current_rsm), 4),
                                    'rsr': round(float(current_rsr), 4),
                                    'rsm': round(float(current_rsm), 4),
                                    'relative_strength': round(float(current_rs), 4)
                                })
                                
                                # 나머지 포인트들을 등간격으로 선택 (마지막 포인트 제외)
                                remaining_points = num_points - 1
                                if remaining_points > 0 and len(rsr) > remaining_points:
                                    step = len(rsr) // (remaining_points + 1)
                                    for i in range(remaining_points):
                                        idx = (i + 1) * step
                                        if idx < len(rsr) and idx < len(rsm):
                                            # 날짜 계산
                                            date_idx = rsr.index[idx]
                                            date_str = date_idx.strftime('%Y-%m-%d')
                                            
                                            timeline.insert(i, {
                                                'date': date_str,
                                                'x': round(float(rsr.iloc[idx]), 4),
                                                'y': round(float(rsm.iloc[idx]), 4),
                                                'rsr': round(float(rsr.iloc[idx]), 4),
                                                'rsm': round(float(rsm.iloc[idx]), 4),
                                                'relative_strength': round(float(rs.iloc[idx]), 4)
                                            })
                
                if timeline:
                    timeline_data[symbol] = {
                        'name': self.sector_names[symbol],
                        'timeline': timeline,
                        'current': timeline[-1] if timeline else None
                    }
                    print(f"✓ {symbol} 타임라인 생성: {len(timeline)} 포인트")
                else:
                    print(f"⚠️ {symbol} 타임라인 생성 실패: 데이터 부족")
                    
            except Exception as e:
                print(f"✗ {symbol} 타임라인 계산 실패: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"RRG 타임라인 데이터 계산 완료: {len(timeline_data)}개 섹터")
        return timeline_data

# RRG 계산기 인스턴스 생성
rrg_calculator = RRGCalculator()

@app.route('/api/rrg/generate', methods=['GET'])
def generate_rrg_data():
    """RRG 데이터 생성 API"""
    try:
        # URL 파라미터에서 기간 가져오기
        period = request.args.get('period', 252, type=int)
        
        # 유효한 기간인지 확인
        valid_periods = [5, 21, 63, 126, 252]
        if period not in valid_periods:
            return jsonify({
                'error': f'Invalid period. Valid periods: {valid_periods}',
                'status': 'error'
            }), 400
        
        print(f"API 요청: RRG 데이터 생성 (기간: {period}일)")
        
        # RRG 데이터 계산
        rrg_data = rrg_calculator.calculate_rrg_data(period)
        
        if rrg_data is None or len(rrg_data) == 0:
            return jsonify({
                'error': 'Failed to generate RRG data',
                'status': 'error'
            }), 500
        
        return jsonify({
            'data': rrg_data,
            'period': period,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'success'
        })
        
    except Exception as e:
        print(f"API 오류: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/rrg/status', methods=['GET'])
def get_status():
    """API 상태 확인"""
    return jsonify({
        'status': 'running',
        'message': 'RRG API Server is running',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/rrg/timeline', methods=['GET'])
def generate_rrg_timeline():
    """RRG 타임라인 데이터 생성 API (화살표 표시용)"""
    try:
        # URL 파라미터에서 기간 가져오기
        period = request.args.get('period', 252, type=int)
        
        # 유효한 기간인지 확인
        valid_periods = [5, 21, 63, 126, 252]
        if period not in valid_periods:
            return jsonify({
                'error': f'Invalid period. Valid periods: {valid_periods}',
                'status': 'error'
            }), 400
        
        print(f"API 요청: RRG 타임라인 데이터 생성 (기간: {period}일)")
        
        # RRG 타임라인 데이터 계산
        timeline_data = rrg_calculator.calculate_rrg_timeline_data(period)
        
        if timeline_data is None or len(timeline_data) == 0:
            return jsonify({
                'error': 'Failed to generate RRG timeline data',
                'status': 'error'
            }), 500
        
        return jsonify({
            'data': timeline_data,
            'period': period,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'success'
        })
        
    except Exception as e:
        print(f"API 오류: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

@app.route('/api/rrg/sectors', methods=['GET'])
def get_sectors():
    """지원하는 섹터 목록 반환"""
    return jsonify({
        'sectors': rrg_calculator.sector_names,
        'benchmark': rrg_calculator.benchmark_symbol,
        'status': 'success'
    })

if __name__ == '__main__':
    print("🚀 RRG API Server 시작 중...")
    print("📊 yfinance를 사용하여 실시간 ETF 데이터 수집")
    print("🌐 API 엔드포인트:")
    print("   - GET /api/rrg/generate?period=63")
    print("   - GET /api/rrg/timeline?period=63")
    print("   - GET /api/rrg/status")
    print("   - GET /api/rrg/sectors")
    print("=" * 50)
    
    app.run(host='127.0.0.1', port=5001, debug=True)
