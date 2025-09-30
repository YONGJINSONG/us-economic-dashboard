import pandas as pd
import numpy as np
import requests
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import warnings
import json
import os
warnings.filterwarnings('ignore')

class RRGPlotter:
    """
    Relative Rotation Graph (RRG) 생성 클래스
    11개 S&P 섹터 ETF의 상대 회전 그래프를 생성합니다.
    """

    def __init__(self, start_date='2023-01-01', end_date=None, period=252):
        self.start_date = start_date
        # 현재 날짜를 기본값으로 사용
        if end_date is None:
            self.end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            self.end_date = end_date
        self.period = period
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

    def download_data(self):
        """모든 ETF 데이터 다운로드"""
        print("데이터 다운로드 중...")
        self.all_data = {}

        # 벤치마크 다운로드
        spy_url = f"https://perplexity.ai/rest/finance/history/{self.benchmark_symbol}/csv?start_date={self.start_date}&end_date={self.end_date}"
        response = requests.get(spy_url)
        spy_data = pd.read_csv(StringIO(response.text))
        spy_data['date'] = pd.to_datetime(spy_data['date'], utc=True)
        self.all_data['SPY'] = spy_data.sort_values('date')

        # 섹터 ETF 다운로드
        for symbol in self.sector_symbols:
            url = f"https://perplexity.ai/rest/finance/history/{symbol}/csv?start_date={self.start_date}&end_date={self.end_date}"
            response = requests.get(url)
            data = pd.read_csv(StringIO(response.text))
            data['date'] = pd.to_datetime(data['date'], utc=True)
            self.all_data[symbol] = data.sort_values('date')

        print("데이터 다운로드 완료!")

    def calculate_relative_strength(self, symbol, period=None):
        """상대 강도 계산 (RS = Price / Benchmark Price)"""
        if period is None:
            period = self.period
            
        if symbol not in self.all_data or 'SPY' not in self.all_data:
            return None
        
        data = self.all_data[symbol].copy()
        spy_data = self.all_data['SPY'].copy()
        
        # 날짜 기준으로 병합
        merged = pd.merge(data, spy_data, on='date', suffixes=('_sector', '_spy'))
        
        # 상대 강도 계산
        merged['relative_strength'] = merged['close_sector'] / merged['close_spy']
        
        # 이동평균 계산
        merged['rs_ma'] = merged['relative_strength'].rolling(window=period).mean()
        
        return merged[['date', 'relative_strength', 'rs_ma']].dropna()

    def calculate_relative_strength_momentum(self, rs_data, period=None):
        """상대 강도 모멘텀 계산 (RSM = (RS_t / RS_t-n) - 1)"""
        if period is None:
            period = self.period
            
        rs_data = rs_data.copy()
        rs_data['rsm'] = (rs_data['relative_strength'] / rs_data['relative_strength'].shift(period)) - 1
        return rs_data

    def calculate_rrg_coordinates(self, period=None):
        """RRG 좌표 계산"""
        if period is None:
            period = self.period
            
        rrg_data = {}
        
        for symbol in self.sector_symbols:
            rs_data = self.calculate_relative_strength(symbol, period)
            if rs_data is not None and len(rs_data) > 0:
                rs_data = self.calculate_relative_strength_momentum(rs_data, period)
                
                # 최신 데이터 포인트
                latest = rs_data.iloc[-1]
                
                # RRG 좌표 계산
                # X축: 상대 강도 (RS)
                # Y축: 상대 강도 모멘텀 (RSM)
                x_coord = (latest['relative_strength'] - 1) * 100  # 백분율로 변환
                y_coord = latest['rsm'] * 100  # 백분율로 변환
                
                rrg_data[symbol] = {
                    'name': self.sector_names[symbol],
                    'x': x_coord,
                    'y': y_coord,
                    'relative_strength': latest['relative_strength'],
                    'momentum': latest['rsm'],
                    'date': latest['date']
                }
        
        return rrg_data

    def create_rrg_plot(self, rrg_data, save_path='rrg_plot.png'):
        """RRG 플롯 생성"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 사분면 구분선 그리기
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        
        # 사분면 라벨
        ax.text(0.02, 0.98, 'Leading\n(강세)', transform=ax.transAxes, 
                fontsize=12, fontweight='bold', color='green', va='top')
        ax.text(0.98, 0.98, 'Weakening\n(약화)', transform=ax.transAxes, 
                fontsize=12, fontweight='bold', color='orange', va='top', ha='right')
        ax.text(0.02, 0.02, 'Improving\n(개선)', transform=ax.transAxes, 
                fontsize=12, fontweight='bold', color='blue', va='bottom')
        ax.text(0.98, 0.02, 'Lagging\n(약세)', transform=ax.transAxes, 
                fontsize=12, fontweight='bold', color='red', va='bottom', ha='right')
        
        # 섹터별 포인트 그리기
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
                 '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9', '#F8C471']
        
        for i, (symbol, data) in enumerate(rrg_data.items()):
            x, y = data['x'], data['y']
            
            # 포인트 그리기
            ax.scatter(x, y, c=colors[i % len(colors)], s=100, alpha=0.7, edgecolors='black', linewidth=1)
            
            # 라벨 추가
            ax.annotate(f"{symbol}\n{data['name']}", 
                       (x, y), 
                       xytext=(5, 5), 
                       textcoords='offset points',
                       fontsize=9,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
        
        # 축 설정
        ax.set_xlabel('Relative Strength (상대 강도)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Relative Strength Momentum (상대 강도 모멘텀)', fontsize=12, fontweight='bold')
        ax.set_title('Relative Rotation Graph (RRG) - S&P 500 Sectors', fontsize=14, fontweight='bold')
        
        # 그리드 추가
        ax.grid(True, alpha=0.3)
        
        # 축 범위 설정
        max_range = max(max(abs(data['x']) for data in rrg_data.values()),
                       max(abs(data['y']) for data in rrg_data.values())) * 1.2
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        
        # 레전드 추가
        legend_elements = []
        for i, (symbol, data) in enumerate(rrg_data.items()):
            legend_elements.append(plt.Line2D([0], [0], marker='o', color='w', 
                                            markerfacecolor=colors[i % len(colors)], 
                                            markersize=8, label=f"{symbol} - {data['name']}"))
        
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1, 0.5))
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"RRG 플롯이 {save_path}에 저장되었습니다.")

    def generate_rrg_data_json(self, rrg_data, save_path='rrg_data.json'):
        """RRG 데이터를 JSON 형태로 저장"""
        # 날짜를 문자열로 변환
        json_data = {}
        for symbol, data in rrg_data.items():
            json_data[symbol] = {
                'name': data['name'],
                'x': round(data['x'], 4),
                'y': round(data['y'], 4),
                'relative_strength': round(data['relative_strength'], 4),
                'momentum': round(data['momentum'], 4),
                'date': data['date'].strftime('%Y-%m-%d'),
                'quadrant': self.get_quadrant(data['x'], data['y'])
            }
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        
        print(f"RRG 데이터가 {save_path}에 저장되었습니다.")

    def get_quadrant(self, x, y):
        """사분면 결정"""
        if x >= 0 and y >= 0:
            return "Leading (강세)"
        elif x < 0 and y >= 0:
            return "Weakening (약화)"
        elif x < 0 and y < 0:
            return "Improving (개선)"
        else:
            return "Lagging (약세)"

    def run_full_analysis(self, period=None):
        """전체 분석 실행"""
        if period is not None:
            self.period = period
            
        print(f"=== Relative Rotation Graph (RRG) 분석 시작 (기간: {self.period}일) ===")
        
        # 데이터 다운로드
        self.download_data()
        
        # RRG 좌표 계산
        rrg_data = self.calculate_rrg_coordinates()
        
        if not rrg_data:
            print("RRG 데이터를 계산할 수 없습니다.")
            return
        
        # 결과 출력
        print("\n=== RRG 분석 결과 ===")
        for symbol, data in rrg_data.items():
            print(f"{symbol} ({data['name']}):")
            print(f"  상대 강도: {data['relative_strength']:.4f}")
            print(f"  모멘텀: {data['momentum']:.4f}")
            print(f"  사분면: {self.get_quadrant(data['x'], data['y'])}")
            print()
        
        # 플롯 생성
        self.create_rrg_plot(rrg_data)
        
        # JSON 데이터 저장
        self.generate_rrg_data_json(rrg_data)
        
        print("=== RRG 분석 완료 ===")

if __name__ == "__main__":
    # RRG 분석 실행
    rrg = RRGPlotter()
    rrg.run_full_analysis()
