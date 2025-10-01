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
        """상대 강도 계산"""
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
            
            # 상대 강도 = (ETF 가격 / 벤치마크 가격) * 100
            relative_strength = (etf_close.iloc[-1] / benchmark_close.iloc[-1]) * 100
            
            return relative_strength
            
        except Exception as e:
            print(f"상대 강도 계산 오류: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def calculate_momentum(self, etf_data, benchmark_data, period=252):
        """상대 강도 모멘텀 계산"""
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
            
            # 현재 상대 강도
            current_rs = (etf_close.iloc[-1] / benchmark_close.iloc[-1]) * 100
            
            # 기간에 따른 모멘텀 계산
            # 짧은 기간일수록 더 적은 일수로 모멘텀 계산
            if period <= 5:  # 1주일 이하
                lookback_days = min(2, len(etf_close) - 1)
            elif period <= 21:  # 1개월 이하
                lookback_days = min(5, len(etf_close) - 1)
            elif period <= 63:  # 3개월 이하
                lookback_days = min(8, len(etf_close) - 1)
            else:  # 6개월 이상
                lookback_days = min(12, len(etf_close) - 1)
            
            if len(etf_close) > lookback_days:
                past_rs = (etf_close.iloc[-lookback_days] / benchmark_close.iloc[-lookback_days]) * 100
                momentum = current_rs - past_rs
            else:
                momentum = 0
            
            return momentum
            
        except Exception as e:
            print(f"모멘텀 계산 오류: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def calculate_rrg_coordinates(self, relative_strength, momentum):
        """RRG 좌표 계산"""
        try:
            # RRG 좌표 변환
            # X축: 상대 강도 (100을 기준으로 한 상대적 값)
            # Y축: 모멘텀 (변화율)
            x = relative_strength - 100  # X축: 상대 강도 (100 기준)
            y = momentum                 # Y축: 모멘텀 (변화율)
            
            return x, y
            
        except Exception as e:
            print(f"RRG 좌표 계산 오류: {e}")
            return None, None
    
    def determine_quadrant(self, x, y):
        """사분면 결정"""
        if x >= 0 and y >= 0:
            return "Leading (강세)"
        elif x < 0 and y >= 0:
            return "Weakening (약화)"
        elif x < 0 and y < 0:
            return "Improving (개선)"
        else:  # x >= 0 and y < 0
            return "Lagging (약세)"
    
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
                    # 상대 강도 계산
                    rs = self.calculate_relative_strength(sector_data[symbol], spy_data, period_days)
                    if rs is None:
                        continue
                    
                    # 모멘텀 계산
                    momentum = self.calculate_momentum(sector_data[symbol], spy_data, period_days)
                    if momentum is None:
                        continue
                    
                    # RRG 좌표 계산
                    x, y = self.calculate_rrg_coordinates(rs, momentum)
                    if x is None or y is None:
                        continue
                    
                    # 사분면 결정
                    quadrant = self.determine_quadrant(x, y)
                    
                    # 데이터 저장
                    rrg_data[symbol] = {
                        "name": self.sector_names[symbol],
                        "x": round(x, 4),
                        "y": round(y, 4),
                        "relative_strength": round(rs, 4),
                        "momentum": round(momentum, 4),
                        "date": current_date,
                        "quadrant": quadrant
                    }
                    
                    print(f"✓ {symbol} ({self.sector_names[symbol]}): RS={rs:.4f}, Momentum={momentum:.4f}, Quadrant={quadrant}")
                    
                except Exception as e:
                    print(f"✗ {symbol} 계산 실패: {e}")
                    continue
        
        print(f"RRG 데이터 계산 완료: {len(rrg_data)}개 섹터")
        return rrg_data
    
    def calculate_rrg_timeline_data(self, period_days=252):
        """RRG 타임라인 데이터 계산 (화살표 표시용)"""
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
                
                # 기간을 나누어 여러 시점의 데이터 계산
                for i in range(num_points):
                    # 각 시점의 기간 계산
                    point_period = period_days * (i + 1) // num_points
                    
                    # 상대 강도 계산
                    rs = self.calculate_relative_strength(sector_data[symbol], spy_data, point_period)
                    if rs is None:
                        continue
                    
                    # 모멘텀 계산
                    momentum = self.calculate_momentum(sector_data[symbol], spy_data, point_period)
                    if momentum is None:
                        continue
                    
                    # RRG 좌표 계산
                    x, y = self.calculate_rrg_coordinates(rs, momentum)
                    if x is None or y is None:
                        continue
                    
                    # 날짜 계산 (오늘부터 역순으로)
                    days_ago = period_days - point_period
                    date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
                    
                    timeline.append({
                        'date': date,
                        'x': round(x, 4),
                        'y': round(y, 4),
                        'rsr': round(x + 100, 4),  # RSR = x + 100
                        'rsm': round(y + 100, 4)   # RSM = y + 100
                    })
                
                if timeline:
                    timeline_data[symbol] = {
                        'name': self.sector_names[symbol],
                        'timeline': timeline
                    }
                    print(f"✓ {symbol} 타임라인 생성: {len(timeline)} 포인트")
                    
            except Exception as e:
                print(f"✗ {symbol} 타임라인 계산 실패: {e}")
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
