#!/usr/bin/env python3
"""
미국 시장 수익률 데이터 수집기
Alpha Vantage API를 활용하여 실시간 섹터별 ETF 수익률 데이터를 수집합니다.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

class MarketReturnsCollector:
    def __init__(self):
        # Alpha Vantage API 키
        self.alpha_vantage_key = 'JVD34QT2NV8JVJYA'
        
        # 섹터별 ETF 심볼 매핑
        self.sector_etfs = {
            'technology': 'XLK',           # Technology Select Sector SPDR Fund
            'healthcare': 'XLV',           # Health Care Select Sector SPDR Fund
            'financial': 'XLF',            # Financial Select Sector SPDR Fund
            'consumerDiscretionary': 'XLY', # Consumer Discretionary Select Sector SPDR Fund
            'consumerStaples': 'XLP',      # Consumer Staples Select Sector SPDR Fund
            'utilities': 'XLU',            # Utilities Select Sector SPDR Fund
            'energy': 'XLE',               # Energy Select Sector SPDR Fund
            'industrials': 'XLI',          # Industrial Select Sector SPDR Fund
            'realEstate': 'XLRE',          # Real Estate Select Sector SPDR Fund
            'materials': 'XLB',            # Materials Select Sector SPDR Fund
            'communication': 'XLC'         # Communication Services Select Sector SPDR Fund
        }
        
        # 섹터별 한국어 이름
        self.sector_names = {
            'technology': '기술',
            'healthcare': '헬스케어',
            'financial': '금융',
            'consumerDiscretionary': '소비재(선택)',
            'consumerStaples': '소비재(필수)',
            'utilities': '유틸리티',
            'energy': '에너지',
            'industrials': '산업',
            'realEstate': '부동산',
            'materials': '소재',
            'communication': '통신'
        }

    def get_stock_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Alpha Vantage API에서 주식 시세를 가져옵니다."""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Global Quote' in data and data['Global Quote']:
                quote = data['Global Quote']
                return {
                    'symbol': symbol,
                    'price': float(quote['05. price']),
                    'change': float(quote['09. change']),
                    'change_percent': float(quote['10. change percent'].replace('%', '')),
                    'volume': int(quote['06. volume']),
                    'timestamp': quote['07. latest trading day']
                }
            return None
            
        except Exception as e:
            print(f"Alpha Vantage API 오류 ({symbol}): {e}")
            return None

    def get_time_series_data(self, symbol: str, period: str = '1Y') -> Optional[Dict[str, Any]]:
        """Alpha Vantage API에서 시계열 데이터를 가져옵니다."""
        try:
            # 기간에 따른 출력 크기 설정
            outputsize_map = {
                '3M': 'compact',
                '6M': 'compact', 
                '1Y': 'compact',
                '3Y': 'full'
            }
            
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'outputsize': outputsize_map.get(period, 'compact'),
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                time_series = data['Time Series (Daily)']
                
                # 날짜별로 정렬
                sorted_dates = sorted(time_series.keys(), reverse=True)
                
                # 기간에 따른 데이터 필터링
                if period == '3M':
                    cutoff_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
                elif period == '6M':
                    cutoff_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
                elif period == '1Y':
                    cutoff_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
                elif period == '3Y':
                    cutoff_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')
                else:
                    cutoff_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
                
                filtered_data = {date: values for date, values in time_series.items() if date >= cutoff_date}
                
                if filtered_data:
                    # 수익률 계산
                    dates = sorted(filtered_data.keys())
                    if len(dates) >= 2:
                        start_price = float(filtered_data[dates[-1]]['4. close'])
                        end_price = float(filtered_data[dates[0]]['4. close'])
                        return_percent = ((end_price - start_price) / start_price) * 100
                        
                        return {
                            'symbol': symbol,
                            'period': period,
                            'start_date': dates[-1],
                            'end_date': dates[0],
                            'start_price': start_price,
                            'end_price': end_price,
                            'return_percent': round(return_percent, 2),
                            'data_points': len(filtered_data)
                        }
            
            return None
            
        except Exception as e:
            print(f"Alpha Vantage 시계열 API 오류 ({symbol}): {e}")
            return None

    def collect_market_returns(self, period: str = '1Y') -> Dict[str, Any]:
        """모든 섹터의 시장 수익률을 수집합니다."""
        print(f"\n📊 미국 시장 수익률 데이터 수집 시작 (기간: {period})...")
        
        market_returns = {}
        successful_count = 0
        
        for sector, symbol in self.sector_etfs.items():
            try:
                print(f"\n🔍 {self.sector_names[sector]} ({symbol}) 데이터 수집 중...")
                
                # 시계열 데이터로 수익률 계산
                time_series_data = self.get_time_series_data(symbol, period)
                
                if time_series_data:
                    market_returns[sector] = {
                        'symbol': symbol,
                        'name': self.sector_names[sector],
                        'return_percent': time_series_data['return_percent'],
                        'period': period,
                        'start_date': time_series_data['start_date'],
                        'end_date': time_series_data['end_date'],
                        'start_price': time_series_data['start_price'],
                        'end_price': time_series_data['end_price'],
                        'data_points': time_series_data['data_points'],
                        'source': 'Alpha Vantage API',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    print(f"✅ {self.sector_names[sector]}: {time_series_data['return_percent']:.2f}% (Alpha Vantage)")
                    successful_count += 1
                else:
                    # 실패 시 현재 시세로 대체
                    quote_data = self.get_stock_quote(symbol)
                    if quote_data:
                        market_returns[sector] = {
                            'symbol': symbol,
                            'name': self.sector_names[sector],
                            'return_percent': quote_data['change_percent'],
                            'period': '1D',
                            'start_date': 'N/A',
                            'end_date': quote_data['timestamp'],
                            'start_price': 'N/A',
                            'end_price': quote_data['price'],
                            'data_points': 1,
                            'source': 'Alpha Vantage API (Current Quote)',
                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        print(f"✅ {self.sector_names[sector]}: {quote_data['change_percent']:.2f}% (현재 시세)")
                        successful_count += 1
                    else:
                        print(f"❌ {self.sector_names[sector]}: 데이터 수집 실패")
                
                # API 호출 제한을 위한 지연
                time.sleep(0.2)
                
            except Exception as e:
                print(f"❌ {self.sector_names[sector]} 데이터 수집 오류: {e}")
        
        print(f"\n📊 수집 완료: {successful_count}/{len(self.sector_etfs)}개 섹터")
        return market_returns

    def save_to_json(self, data: Dict[str, Any], filename: str = 'market_returns.json'):
        """데이터를 JSON 파일로 저장합니다."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 데이터가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"❌ 파일 저장 오류: {e}")

    def generate_web_dashboard_data(self, market_returns: Dict[str, Any]) -> Dict[str, Any]:
        """웹 대시보드용 데이터 형식으로 변환합니다."""
        dashboard_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'period': market_returns.get(list(market_returns.keys())[0], {}).get('period', '1Y') if market_returns else '1Y',
            'source': 'Alpha Vantage API',
            'sectors': {}
        }
        
        for sector, data in market_returns.items():
            dashboard_data['sectors'][sector] = {
                'name': data['name'],
                'symbol': data['symbol'],
                'return_percent': data['return_percent'],
                'source': data['source'],
                'timestamp': data['timestamp']
            }
        
        return dashboard_data

def main():
    """메인 실행 함수"""
    collector = MarketReturnsCollector()
    
    # 1년 수익률 데이터 수집
    market_returns = collector.collect_market_returns('1Y')
    
    if market_returns:
        # 원본 데이터 저장
        collector.save_to_json(market_returns, 'market_returns_full.json')
        
        # 웹 대시보드용 데이터 생성 및 저장
        dashboard_data = collector.generate_web_dashboard_data(market_returns)
        collector.save_to_json(dashboard_data, 'market_returns.json')
        
        print(f"\n🌐 웹 대시보드용 JSON:")
        print(json.dumps(dashboard_data, ensure_ascii=False, indent=2))
        
        # 수집 결과 요약
        print(f"\n📊 수집 결과 요약:")
        for sector, data in market_returns.items():
            print(f"  {data['name']}: {data['return_percent']:.2f}% ({data['source']})")
    else:
        print("❌ 시장 수익률 데이터 수집에 실패했습니다.")

if __name__ == "__main__":
    main()
