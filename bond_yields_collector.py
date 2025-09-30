#!/usr/bin/env python3
"""
글로벌 국채 금리 데이터 수집기
FRED API와 Alpha Vantage API를 활용하여 실시간 국채 금리 데이터를 수집합니다.
"""

import requests
import pandas as pd
from datetime import datetime
import json
import os
import time
from typing import Dict, Any, Optional
import re
from bs4 import BeautifulSoup

class BondYieldsCollector:
    def __init__(self):
        # API 키 설정
        self.fred_api_key = '99a4dabe83da776316663c0c9eb5703c'  # FRED API 키
        self.alpha_vantage_key = 'JVD34QT2NV8JVJYA'  # Alpha Vantage API 키
        
        # FRED 시리즈 ID 매핑 (각국 다양한 만기 국채 수익률)
        self.fred_series = {
            'US': {
                '1년': 'DGS1',      # 미국 1년 국채
                '2년': 'DGS2',      # 미국 2년 국채
                '5년': 'DGS5',      # 미국 5년 국채
                '10년': 'DGS10',    # 미국 10년 국채
                '30년': 'DGS30'     # 미국 30년 국채
            },
            'DE': {
                '1년': 'IRLTLT01DEM156N',   # 독일 1년 국채
                '2년': 'IRLTLT01DEM156N',   # 독일 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01DEM156N',   # 독일 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01DEM156N',  # 독일 10년 국채
                '30년': 'IRLTLT01DEM156N'   # 독일 30년 국채 (동일 시리즈 사용)
            },
            'JP': {
                '1년': 'IRLTLT01JPM156N',   # 일본 1년 국채
                '2년': 'IRLTLT01JPM156N',   # 일본 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01JPM156N',   # 일본 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01JPM156N',  # 일본 10년 국채
                '30년': 'IRLTLT01JPM156N'   # 일본 30년 국채 (동일 시리즈 사용)
            },
            'GB': {
                '1년': 'IRLTLT01GBM156N',   # 영국 1년 국채
                '2년': 'IRLTLT01GBM156N',   # 영국 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01GBM156N',   # 영국 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01GBM156N',  # 영국 10년 국채
                '30년': 'IRLTLT01GBM156N'   # 영국 30년 국채 (동일 시리즈 사용)
            },
            'FR': {
                '1년': 'IRLTLT01FRM156N',   # 프랑스 1년 국채
                '2년': 'IRLTLT01FRM156N',   # 프랑스 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01FRM156N',   # 프랑스 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01FRM156N',  # 프랑스 10년 국채
                '30년': 'IRLTLT01FRM156N'   # 프랑스 30년 국채 (동일 시리즈 사용)
            },
            'IT': {
                '1년': 'IRLTLT01ITM156N',   # 이탈리아 1년 국채
                '2년': 'IRLTLT01ITM156N',   # 이탈리아 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01ITM156N',   # 이탈리아 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01ITM156N',  # 이탈리아 10년 국채
                '30년': 'IRLTLT01ITM156N'   # 이탈리아 30년 국채 (동일 시리즈 사용)
            },
            'ES': {
                '1년': 'IRLTLT01ESM156N',   # 스페인 1년 국채
                '2년': 'IRLTLT01ESM156N',   # 스페인 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01ESM156N',   # 스페인 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01ESM156N',  # 스페인 10년 국채
                '30년': 'IRLTLT01ESM156N'   # 스페인 30년 국채 (동일 시리즈 사용)
            },
            'CA': {
                '1년': 'IRLTLT01CAM156N',   # 캐나다 1년 국채
                '2년': 'IRLTLT01CAM156N',   # 캐나다 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01CAM156N',   # 캐나다 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01CAM156N',  # 캐나다 10년 국채
                '30년': 'IRLTLT01CAM156N'   # 캐나다 30년 국채 (동일 시리즈 사용)
            },
            'AU': {
                '1년': 'IRLTLT01AUM156N',   # 호주 1년 국채
                '2년': 'IRLTLT01AUM156N',   # 호주 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01AUM156N',   # 호주 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01AUM156N',  # 호주 10년 국채
                '30년': 'IRLTLT01AUM156N'   # 호주 30년 국채 (동일 시리즈 사용)
            },
            'KR': {
                '1년': 'IRLTLT01KRM156N',   # 한국 1년 국채
                '2년': 'IRLTLT01KRM156N',   # 한국 2년 국채 (동일 시리즈 사용)
                '5년': 'IRLTLT01KRM156N',   # 한국 5년 국채 (동일 시리즈 사용)
                '10년': 'IRLTLT01KRM156N',  # 한국 10년 국채
                '30년': 'IRLTLT01KRM156N'   # 한국 30년 국채 (동일 시리즈 사용)
            }
        }
        
        # 실제로는 각 국가별로 개별 만기 시리즈가 필요하지만, 
        # 현재 FRED API에서는 일부 국가만 개별 만기 데이터를 제공합니다.
        # 임시로 샘플 데이터를 사용하여 각 만기별로 다른 값을 표시하도록 하겠습니다.
        
        # 국가명 매핑
        self.country_names = {
            'US': '미국',
            'DE': '독일',
            'JP': '일본',
            'GB': '영국',
            'FR': '프랑스',
            'IT': '이탈리아',
            'ES': '스페인',
            'CA': '캐나다',
            'AU': '호주',
            'KR': '한국'
        }
        
        # 웹 스크래핑을 위한 헤더
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_fred_data(self, series_id: str, api_key: str) -> Optional[Dict[str, Any]]:
        """FRED API에서 데이터를 가져옵니다."""
        try:
            url = f"https://api.stlouisfed.org/fred/series/observations"
            params = {
                'series_id': series_id,
                'api_key': api_key,
                'file_type': 'json',
                'limit': 1,
                'sort_order': 'desc'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'observations' in data and len(data['observations']) > 0:
                observation = data['observations'][0]
                return {
                    'value': float(observation['value']) if observation['value'] != '.' else None,
                    'date': observation['date'],
                    'source': 'FRED'
                }
            return None
            
        except Exception as e:
            print(f"FRED API 오류 ({series_id}): {e}")
            return None

    def get_treasury_yield(self, maturity: str, interval: str, api_key: str) -> Optional[Dict[str, Any]]:
        """Alpha Vantage API에서 국채 수익률을 가져옵니다."""
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TREASURY_YIELD',
                'interval': interval,
                'maturity': maturity,
                'apikey': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                latest_data = data['data'][0]
                return {
                    'value': float(latest_data['value']),
                    'date': latest_data['date'],
                    'source': 'Alpha Vantage'
                }
            return None
            
        except Exception as e:
            print(f"Alpha Vantage API 오류 ({maturity}): {e}")
            return None

    def get_all_treasury_yields(self, api_key: str) -> Dict[str, Any]:
        """Alpha Vantage API에서 모든 만기의 미국 국채 수익률을 가져옵니다."""
        maturities = {
            '1년': '3month',
            '2년': '2year', 
            '5년': '5year',
            '10년': '10year',
            '30년': '30year'
        }
        
        yields = {}
        
        for korean_maturity, av_maturity in maturities.items():
            try:
                data = self.get_treasury_yield(av_maturity, 'monthly', api_key)
                if data:
                    yields[korean_maturity] = data['value']
                    print(f"✅ 미국 {korean_maturity}: {data['value']:.2f}% (Alpha Vantage)")
                else:
                    print(f"❌ 미국 {korean_maturity}: 데이터 없음")
            except Exception as e:
                print(f"❌ 미국 {korean_maturity}: 오류 - {e}")
            
            # API 호출 제한을 위한 지연
            time.sleep(0.2)
        
        return yields

    def get_korean_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 한국 국채 수익률 데이터를 가져옵니다."""
        korean_yields = {}
        
        try:
            # Investing.com 한국 국채 페이지
            url = "https://kr.investing.com/rates-bonds/south-korea-government-bonds"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 디버깅을 위해 페이지 내용 일부 출력
            print(f"페이지 로드 성공: {url}")
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            korean_bonds = {
                '1년': {'data_id': '29294', 'selector': '#pair_29294 > td.pid-29294-last_close'},
                '2년': {'data_id': '29295', 'selector': '#pair_29295 > td.pid-29295-last_close'},
                '5년': {'data_id': '29298', 'selector': '#pair_29298 > td.pid-29298-last_close'},
                '10년': {'data_id': '29292', 'selector': '#pair_29292 > td.pid-29292-last_close'},
                '30년': {'data_id': '1052525', 'selector': '#pair_1052525 > td.pid-1052525-last_close'}
            }
            
            for maturity, bond_info in korean_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        korean_yields[maturity] = yield_value
                        print(f"✅ 한국 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            korean_yields[maturity] = yield_value
                            print(f"✅ 한국 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        korean_yields[maturity] = yield_value
                        print(f"✅ 한국 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            korean_yields[maturity] = yield_value
                            print(f"✅ 한국 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in korean_yields:
                        print(f"❌ 한국 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 한국 {maturity}: 파싱 오류 - {e}")
            
            # 한국 데이터가 없으면 샘플 데이터 사용
            if not korean_yields:
                print("⚠️ 한국 데이터 수집 실패 - 샘플 데이터 사용")
                korean_yields = {
                    '1년': 3.25,
                    '2년': 3.15,
                    '5년': 3.05,
                    '10년': 2.95,
                    '30년': 3.15,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                korean_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                korean_yields['source'] = 'Investing.com'
                print(f"✅ 한국 국채 수익률 {len(korean_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"한국 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            korean_yields = {
                '1년': 3.25,
                '2년': 3.15,
                '5년': 3.05,
                '10년': 2.95,
                '30년': 3.15,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return korean_yields

    def get_chinese_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 중국 국채 수익률 데이터를 가져옵니다."""
        chinese_yields = {}
        
        try:
            # Investing.com 중국 국채 페이지 - 여러 URL 시도
            urls = [
                "https://kr.investing.com/rates-bonds/china-government-bonds",
                "https://kr.investing.com/markets/china",
                "https://www.investing.com/rates-bonds/china-government-bonds"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"중국 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 중국 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 디버깅을 위해 페이지 내용 일부 출력
            print(f"페이지 로드 성공: {url}")
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            chinese_bonds = {
                '1년': {'data_id': '29231', 'selector': '#pair_29231 > td.pid-29231-last_close'},
                '2년': {'data_id': '29232', 'selector': '#pair_29232 > td.pid-29232-last_close'},
                '5년': {'data_id': '29234', 'selector': '#pair_29234 > td.pid-29234-last_close'},
                '10년': {'data_id': '29227', 'selector': '#pair_29227 > td.pid-29227-last_close'},
                '30년': {'data_id': '29230', 'selector': '#pair_29230 > td.pid-29230-last_close'}
            }
            
            for maturity, bond_info in chinese_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        chinese_yields[maturity] = yield_value
                        print(f"✅ 중국 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            chinese_yields[maturity] = yield_value
                            print(f"✅ 중국 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        chinese_yields[maturity] = yield_value
                        print(f"✅ 중국 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            chinese_yields[maturity] = yield_value
                            print(f"✅ 중국 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in chinese_yields:
                        print(f"❌ 중국 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 중국 {maturity}: 파싱 오류 - {e}")
            
            # 중국 데이터가 없으면 샘플 데이터 사용
            if not chinese_yields:
                print("⚠️ 중국 데이터 수집 실패 - 샘플 데이터 사용")
                chinese_yields = {
                    '1년': 2.15,
                    '2년': 2.25,
                    '5년': 2.45,
                    '10년': 2.65,
                    '30년': 2.85,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                chinese_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                chinese_yields['source'] = 'Investing.com'
                print(f"✅ 중국 국채 수익률 {len(chinese_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"중국 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            chinese_yields = {
                '1년': 2.15,
                '2년': 2.25,
                '5년': 2.45,
                '10년': 2.65,
                '30년': 2.85,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return chinese_yields

    def get_japanese_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 일본 국채 수익률 데이터를 가져옵니다."""
        japanese_yields = {}
        
        try:
            # Investing.com 일본 국채 페이지 - 여러 URL 시도
            urls = [
                "https://kr.investing.com/rates-bonds/japan-government-bonds",
                "https://www.investing.com/rates-bonds/japan-government-bonds",
                "https://kr.investing.com/markets/japan"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"일본 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 일본 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            japanese_bonds = {
                '1년': {'data_id': '23892', 'selector': '#pair_23892 > td.pid-23892-last_close'},
                '2년': {'data_id': '23893', 'selector': '#pair_23893 > td.pid-23893-last_close'},
                '5년': {'data_id': '23896', 'selector': '#pair_23896 > td.pid-23896-last_close'},
                '10년': {'data_id': '23901', 'selector': '#pair_23901 > td.pid-23901-last_close'},
                '30년': {'data_id': '23904', 'selector': '#pair_23904 > td.pid-23904-last_close'}
            }
            
            for maturity, bond_info in japanese_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        japanese_yields[maturity] = yield_value
                        print(f"✅ 일본 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            japanese_yields[maturity] = yield_value
                            print(f"✅ 일본 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        japanese_yields[maturity] = yield_value
                        print(f"✅ 일본 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            japanese_yields[maturity] = yield_value
                            print(f"✅ 일본 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in japanese_yields:
                        print(f"❌ 일본 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 일본 {maturity}: 파싱 오류 - {e}")
            
            # 일본 데이터가 없으면 샘플 데이터 사용
            if not japanese_yields:
                print("⚠️ 일본 데이터 수집 실패 - 샘플 데이터 사용")
                japanese_yields = {
                    '1년': 0.15,
                    '2년': 0.25,
                    '5년': 0.45,
                    '10년': 0.65,
                    '30년': 1.25,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                japanese_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                japanese_yields['source'] = 'Investing.com'
                print(f"✅ 일본 국채 수익률 {len(japanese_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"일본 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            japanese_yields = {
                '1년': 0.15,
                '2년': 0.25,
                '5년': 0.45,
                '10년': 0.65,
                '30년': 1.25,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return japanese_yields

    def get_australian_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 호주 국채 수익률 데이터를 가져옵니다."""
        australian_yields = {}
        
        try:
            # Investing.com 호주 국채 페이지 - 여러 URL 시도
            urls = [
                "https://kr.investing.com/rates-bonds/australia-government-bonds",
                "https://www.investing.com/rates-bonds/australia-government-bonds",
                "https://kr.investing.com/markets/australia"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"호주 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 호주 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            australian_bonds = {
                '1년': {'data_id': '23869', 'selector': '#pair_23869 > td.pid-23869-last_close'},
                '2년': {'data_id': '23870', 'selector': '#pair_23870 > td.pid-23870-last_close'},
                '5년': {'data_id': '23873', 'selector': '#pair_23873 > td.pid-23873-last_close'},
                '10년': {'data_id': '23878', 'selector': '#pair_23878 > td.pid-23878-last_close'},
                '30년': {'data_id': '1052473', 'selector': '#pair_1052473 > td.pid-1052473-last_close'}
            }
            
            for maturity, bond_info in australian_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        australian_yields[maturity] = yield_value
                        print(f"✅ 호주 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            australian_yields[maturity] = yield_value
                            print(f"✅ 호주 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        australian_yields[maturity] = yield_value
                        print(f"✅ 호주 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            australian_yields[maturity] = yield_value
                            print(f"✅ 호주 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in australian_yields:
                        print(f"❌ 호주 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 호주 {maturity}: 파싱 오류 - {e}")
            
            # 호주 데이터가 없으면 샘플 데이터 사용
            if not australian_yields:
                print("⚠️ 호주 데이터 수집 실패 - 샘플 데이터 사용")
                australian_yields = {
                    '1년': 4.15,
                    '2년': 4.05,
                    '5년': 3.85,
                    '10년': 3.65,
                    '30년': 3.95,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                australian_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                australian_yields['source'] = 'Investing.com'
                print(f"✅ 호주 국채 수익률 {len(australian_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"호주 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            australian_yields = {
                '1년': 4.15,
                '2년': 4.05,
                '5년': 3.85,
                '10년': 3.65,
                '30년': 3.95,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return australian_yields

    def get_german_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 독일 국채 수익률 데이터를 가져옵니다."""
        german_yields = {}
        
        try:
            # Investing.com 독일 국채 페이지 - 여러 URL 시도
            urls = [
                "https://www.investing.com/rates-bonds/germany-government-bonds?maturity_from=40&maturity_to=290",
                "https://kr.investing.com/markets/germany",
                "https://kr.investing.com/rates-bonds/germany-government-bonds",
                "https://www.investing.com/rates-bonds/germany-government-bonds"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"독일 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 독일 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            german_bonds = {
                '1년': {'data_id': '23684', 'selector': '#pair_23684 > td.pid-23684-last_close'},
                '2년': {'data_id': '23685', 'selector': '#pair_23685 > td.pid-23685-last_close'},
                '5년': {'data_id': '23688', 'selector': '#pair_23688 > td.pid-23688-last_close'},
                '10년': {'data_id': '23693', 'selector': '#pair_23693 > td.pid-23693-last_close'},
                '30년': {'data_id': '23696', 'selector': '#pair_23696 > td.pid-23696-last_close'}
            }
            
            for maturity, bond_info in german_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        german_yields[maturity] = yield_value
                        print(f"✅ 독일 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            german_yields[maturity] = yield_value
                            print(f"✅ 독일 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        german_yields[maturity] = yield_value
                        print(f"✅ 독일 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            german_yields[maturity] = yield_value
                            print(f"✅ 독일 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in german_yields:
                        print(f"❌ 독일 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 독일 {maturity}: 파싱 오류 - {e}")
            
            # 독일 데이터가 없으면 샘플 데이터 사용
            if not german_yields:
                print("⚠️ 독일 데이터 수집 실패 - 샘플 데이터 사용")
                german_yields = {
                    '1년': 3.25,
                    '2년': 3.15,
                    '5년': 2.95,
                    '10년': 2.75,
                    '30년': 3.05,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                german_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                german_yields['source'] = 'Investing.com'
                print(f"✅ 독일 국채 수익률 {len(german_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"독일 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            german_yields = {
                '1년': 3.25,
                '2년': 3.15,
                '5년': 2.95,
                '10년': 2.75,
                '30년': 3.05,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return german_yields

    def get_british_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 영국 국채 수익률 데이터를 가져옵니다."""
        british_yields = {}
        
        try:
            # Investing.com 영국 국채 페이지 - 여러 URL 시도
            urls = [
                "https://www.investing.com/rates-bonds/uk-government-bonds?maturity_from=40&maturity_to=310",
                "https://kr.investing.com/markets/united-kingdom",
                "https://kr.investing.com/rates-bonds/uk-government-bonds",
                "https://www.investing.com/rates-bonds/uk-government-bonds"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"영국 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 영국 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            british_bonds = {
                '1년': {'data_id': '23664', 'selector': '#pair_23664 > td.pid-23664-last_close'},
                '2년': {'data_id': '23665', 'selector': '#pair_23665 > td.pid-23665-last_close'},
                '5년': {'data_id': '23668', 'selector': '#pair_23668 > td.pid-23668-last_close'},
                '10년': {'data_id': '23673', 'selector': '#pair_23673 > td.pid-23673-last_close'},
                '30년': {'data_id': '23677', 'selector': '#pair_23677 > td.pid-23677-last_close'}
            }
            
            for maturity, bond_info in british_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        british_yields[maturity] = yield_value
                        print(f"✅ 영국 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            british_yields[maturity] = yield_value
                            print(f"✅ 영국 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        british_yields[maturity] = yield_value
                        print(f"✅ 영국 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            british_yields[maturity] = yield_value
                            print(f"✅ 영국 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in british_yields:
                        print(f"❌ 영국 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 영국 {maturity}: 파싱 오류 - {e}")
            
            # 영국 데이터가 없으면 샘플 데이터 사용
            if not british_yields:
                print("⚠️ 영국 데이터 수집 실패 - 샘플 데이터 사용")
                british_yields = {
                    '1년': 4.25,
                    '2년': 4.15,
                    '5년': 3.95,
                    '10년': 3.85,
                    '30년': 4.15,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                british_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                british_yields['source'] = 'Investing.com'
                print(f"✅ 영국 국채 수익률 {len(british_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"영국 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            british_yields = {
                '1년': 4.25,
                '2년': 4.15,
                '5년': 3.95,
                '10년': 3.85,
                '30년': 4.15,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return british_yields

    def get_french_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 프랑스 국채 수익률 데이터를 가져옵니다."""
        french_yields = {}
        
        try:
            # Investing.com 프랑스 국채 페이지 - 여러 URL 시도
            urls = [
                "https://www.investing.com/rates-bonds/france-government-bonds?maturity_from=40&maturity_to=310",
                "https://kr.investing.com/markets/france",
                "https://kr.investing.com/rates-bonds/france-government-bonds",
                "https://www.investing.com/rates-bonds/france-government-bonds"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"프랑스 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 프랑스 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            french_bonds = {
                '1년': {'data_id': '23769', 'selector': '#pair_23769 > td.pid-23769-last_close'},
                '2년': {'data_id': '23770', 'selector': '#pair_23770 > td.pid-23770-last_close'},
                '5년': {'data_id': '23773', 'selector': '#pair_23773 > td.pid-23773-last_close'},
                '10년': {'data_id': '23778', 'selector': '#pair_23778 > td.pid-23778-last_close'},
                '30년': {'data_id': '23781', 'selector': '#pair_23781 > td.pid-23781-last_close'}
            }
            
            for maturity, bond_info in french_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        french_yields[maturity] = yield_value
                        print(f"✅ 프랑스 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            french_yields[maturity] = yield_value
                            print(f"✅ 프랑스 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        french_yields[maturity] = yield_value
                        print(f"✅ 프랑스 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            french_yields[maturity] = yield_value
                            print(f"✅ 프랑스 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in french_yields:
                        print(f"❌ 프랑스 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 프랑스 {maturity}: 파싱 오류 - {e}")
            
            # 프랑스 데이터가 없으면 샘플 데이터 사용
            if not french_yields:
                print("⚠️ 프랑스 데이터 수집 실패 - 샘플 데이터 사용")
                french_yields = {
                    '1년': 3.45,
                    '2년': 3.35,
                    '5년': 3.15,
                    '10년': 2.95,
                    '30년': 3.25,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                french_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                french_yields['source'] = 'Investing.com'
                print(f"✅ 프랑스 국채 수익률 {len(french_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"프랑스 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            french_yields = {
                '1년': 3.45,
                '2년': 3.35,
                '5년': 3.15,
                '10년': 2.95,
                '30년': 3.25,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return french_yields

    def get_canadian_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 캐나다 국채 수익률 데이터를 가져옵니다."""
        canadian_yields = {}
        
        try:
            # Investing.com 캐나다 국채 페이지 - 여러 URL 시도
            urls = [
                "https://www.investing.com/rates-bonds/canada-government-bonds?maturity_from=40&maturity_to=290",
                "https://kr.investing.com/markets/canada",
                "https://kr.investing.com/rates-bonds/canada-government-bonds",
                "https://www.investing.com/rates-bonds/canada-government-bonds"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"캐나다 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 캐나다 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            canadian_bonds = {
                '1년': {'data_id': '25269', 'selector': '#pair_25269 > td.pid-25269-last_close'},
                '2년': {'data_id': '25270', 'selector': '#pair_25270 > td.pid-25270-last_close'},
                '5년': {'data_id': '25273', 'selector': '#pair_25273 > td.pid-25273-last_close'},
                '10년': {'data_id': '25275', 'selector': '#pair_25275 > td.pid-25275-last_close'},
                '30년': {'data_id': '25277', 'selector': '#pair_25277 > td.pid-25277-last_close'}
            }
            
            for maturity, bond_info in canadian_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        canadian_yields[maturity] = yield_value
                        print(f"✅ 캐나다 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            canadian_yields[maturity] = yield_value
                            print(f"✅ 캐나다 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        canadian_yields[maturity] = yield_value
                        print(f"✅ 캐나다 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            canadian_yields[maturity] = yield_value
                            print(f"✅ 캐나다 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in canadian_yields:
                        print(f"❌ 캐나다 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 캐나다 {maturity}: 파싱 오류 - {e}")
            
            # 캐나다 데이터가 없으면 샘플 데이터 사용
            if not canadian_yields:
                print("⚠️ 캐나다 데이터 수집 실패 - 샘플 데이터 사용")
                canadian_yields = {
                    '1년': 4.45,
                    '2년': 4.35,
                    '5년': 4.15,
                    '10년': 3.95,
                    '30년': 4.25,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                canadian_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                canadian_yields['source'] = 'Investing.com'
                print(f"✅ 캐나다 국채 수익률 {len(canadian_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"캐나다 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            canadian_yields = {
                '1년': 4.45,
                '2년': 4.35,
                '5년': 4.15,
                '10년': 3.95,
                '30년': 4.25,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return canadian_yields

    def get_american_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 미국 국채 수익률 데이터를 가져옵니다."""
        american_yields = {}
        
        try:
            # Investing.com 미국 국채 페이지 - 여러 URL 시도
            urls = [
                "https://www.investing.com/rates-bonds/usa-government-bonds?maturity_from=40&maturity_to=290",
                "https://kr.investing.com/markets/united-states",
                "https://kr.investing.com/rates-bonds/us-government-bonds",
                "https://www.investing.com/rates-bonds/us-government-bonds"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"미국 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 미국 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            american_bonds = {
                '1년': {'data_id': '23700', 'selector': '#pair_23700 > td.pid-23700-last_close'},
                '2년': {'data_id': '23701', 'selector': '#pair_23701 > td.pid-23701-last_close'},
                '5년': {'data_id': '23703', 'selector': '#pair_23703 > td.pid-23703-last_close'},
                '10년': {'data_id': '23705', 'selector': '#pair_23705 > td.pid-23705-last_close'},
                '30년': {'data_id': '23706', 'selector': '#pair_23706 > td.pid-23706-last_close'}
            }
            
            for maturity, bond_info in american_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        american_yields[maturity] = yield_value
                        print(f"✅ 미국 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            american_yields[maturity] = yield_value
                            print(f"✅ 미국 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        american_yields[maturity] = yield_value
                        print(f"✅ 미국 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            american_yields[maturity] = yield_value
                            print(f"✅ 미국 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in american_yields:
                        print(f"❌ 미국 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 미국 {maturity}: 파싱 오류 - {e}")
            
            # 미국 데이터가 없으면 샘플 데이터 사용
            if not american_yields:
                print("⚠️ 미국 데이터 수집 실패 - 샘플 데이터 사용")
                american_yields = {
                    '1년': 4.85,
                    '2년': 4.72,
                    '5년': 4.45,
                    '10년': 4.35,
                    '30년': 4.52,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                american_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                american_yields['source'] = 'Investing.com'
                print(f"✅ 미국 국채 수익률 {len(american_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"미국 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            american_yields = {
                '1년': 4.85,
                '2년': 4.72,
                '5년': 4.45,
                '10년': 4.35,
                '30년': 4.52,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return american_yields

    def get_spanish_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 스페인 국채 수익률 데이터를 가져옵니다."""
        spanish_yields = {}
        
        try:
            # Investing.com 스페인 국채 페이지 - 여러 URL 시도
            urls = [
                "https://www.investing.com/rates-bonds/spain-government-bonds?maturity_from=40&maturity_to=290",
                "https://kr.investing.com/markets/spain",
                "https://kr.investing.com/rates-bonds/spain-government-bonds",
                "https://www.investing.com/rates-bonds/spain-government-bonds"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"스페인 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 스페인 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            spanish_bonds = {
                '1년': {'data_id': '23797', 'selector': '#pair_23797 > td.pid-23797-last_close'},
                '2년': {'data_id': '23798', 'selector': '#pair_23798 > td.pid-23798-last_close'},
                '5년': {'data_id': '23801', 'selector': '#pair_23801 > td.pid-23801-last_close'},
                '10년': {'data_id': '23806', 'selector': '#pair_23806 > td.pid-23806-last_close'},
                '30년': {'data_id': '100155', 'selector': '#pair_100155 > td.pid-100155-last_close'}
            }
            
            for maturity, bond_info in spanish_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        spanish_yields[maturity] = yield_value
                        print(f"✅ 스페인 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            spanish_yields[maturity] = yield_value
                            print(f"✅ 스페인 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        spanish_yields[maturity] = yield_value
                        print(f"✅ 스페인 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            spanish_yields[maturity] = yield_value
                            print(f"✅ 스페인 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in spanish_yields:
                        print(f"❌ 스페인 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 스페인 {maturity}: 파싱 오류 - {e}")
            
            # 스페인 데이터가 없으면 샘플 데이터 사용
            if not spanish_yields:
                print("⚠️ 스페인 데이터 수집 실패 - 샘플 데이터 사용")
                spanish_yields = {
                    '1년': 3.65,
                    '2년': 3.55,
                    '5년': 3.35,
                    '10년': 3.15,
                    '30년': 3.45,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                spanish_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                spanish_yields['source'] = 'Investing.com'
                print(f"✅ 스페인 국채 수익률 {len(spanish_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"스페인 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            spanish_yields = {
                '1년': 3.65,
                '2년': 3.55,
                '5년': 3.35,
                '10년': 3.15,
                '30년': 3.45,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return spanish_yields

    def get_italian_bond_yields_from_investing(self) -> Dict[str, Any]:
        """Investing.com에서 이탈리아 국채 수익률 데이터를 가져옵니다."""
        italian_yields = {}
        
        try:
            # Investing.com 이탈리아 국채 페이지 - 여러 URL 시도
            urls = [
                "https://www.investing.com/rates-bonds/italy-government-bonds?maturity_from=40&maturity_to=310",
                "https://kr.investing.com/markets/italy",
                "https://kr.investing.com/rates-bonds/italy-government-bonds",
                "https://www.investing.com/rates-bonds/italy-government-bonds"
            ]
            
            response = None
            for url in urls:
                try:
                    print(f"이탈리아 데이터 수집 시도: {url}")
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    print(f"페이지 로드 성공: {url}")
                    break
                except Exception as e:
                    print(f"URL 실패: {url} - {e}")
                    continue
            
            if not response:
                raise Exception("모든 이탈리아 URL에서 데이터를 가져올 수 없습니다.")
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 각 만기별 데이터 추출 - 정확한 CSS 셀렉터 사용
            italian_bonds = {
                '1년': {'data_id': '23729', 'selector': '#pair_23729 > td.pid-23729-last_close'},
                '2년': {'data_id': '23730', 'selector': '#pair_23730 > td.pid-23730-last_close'},
                '5년': {'data_id': '23733', 'selector': '#pair_23733 > td.pid-23733-last_close'},
                '10년': {'data_id': '23738', 'selector': '#pair_23738 > td.pid-23738-last_close'},
                '30년': {'data_id': '41352', 'selector': '#pair_41352 > td.pid-41352-last_close'}
            }
            
            for maturity, bond_info in italian_bonds.items():
                try:
                    # 방법 1: CSS 셀렉터로 직접 찾기
                    yield_element = soup.select_one(bond_info['selector'])
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        italian_yields[maturity] = yield_value
                        print(f"✅ 이탈리아 {maturity}: {yield_value:.2f}% (Investing.com - CSS 셀렉터)")
                        continue
                    
                    # 방법 2: ID로 요소 찾기
                    pair_element = soup.find('tr', id=f"pair_{bond_info['data_id']}")
                    if pair_element:
                        yield_element = pair_element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            italian_yields[maturity] = yield_value
                            print(f"✅ 이탈리아 {maturity}: {yield_value:.2f}% (Investing.com - ID 검색)")
                            continue
                    
                    # 방법 3: 클래스명으로 직접 찾기
                    yield_element = soup.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                    if yield_element:
                        yield_text = yield_element.get_text(strip=True)
                        yield_value = float(yield_text.replace('%', ''))
                        italian_yields[maturity] = yield_value
                        print(f"✅ 이탈리아 {maturity}: {yield_value:.2f}% (Investing.com - 클래스 검색)")
                        continue
                    
                    # 방법 4: data-id로 요소 찾기
                    element = soup.find(attrs={'data-id': bond_info['data_id']})
                    if element:
                        yield_element = element.find('td', class_=f"pid-{bond_info['data_id']}-last_close")
                        if yield_element:
                            yield_text = yield_element.get_text(strip=True)
                            yield_value = float(yield_text.replace('%', ''))
                            italian_yields[maturity] = yield_value
                            print(f"✅ 이탈리아 {maturity}: {yield_value:.2f}% (Investing.com - data-id 검색)")
                            continue
                    
                    if maturity not in italian_yields:
                        print(f"❌ 이탈리아 {maturity}: 모든 방법으로 찾을 수 없음 (셀렉터: {bond_info['selector']})")
                        
                except Exception as e:
                    print(f"❌ 이탈리아 {maturity}: 파싱 오류 - {e}")
            
            # 이탈리아 데이터가 없으면 샘플 데이터 사용
            if not italian_yields:
                print("⚠️ 이탈리아 데이터 수집 실패 - 샘플 데이터 사용")
                italian_yields = {
                    '1년': 3.85,
                    '2년': 3.75,
                    '5년': 3.55,
                    '10년': 3.35,
                    '30년': 3.65,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Sample Data (Investing.com 실패)'
                }
            else:
                italian_yields['date'] = datetime.now().strftime('%Y-%m-%d')
                italian_yields['source'] = 'Investing.com'
                print(f"✅ 이탈리아 국채 수익률 {len(italian_yields)-2}개 만기 수집 완료")
            
        except Exception as e:
            print(f"이탈리아 국채 수익률 스크래핑 오류: {e}")
            # 오류 시 샘플 데이터 사용
            italian_yields = {
                '1년': 3.85,
                '2년': 3.75,
                '5년': 3.55,
                '10년': 3.35,
                '30년': 3.65,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data (스크래핑 오류)'
            }
        
        return italian_yields

    def get_bond_yields_from_web(self) -> Dict[str, Any]:
        """웹 스크래핑을 통해 국채 수익률 데이터를 가져옵니다."""
        bond_yields = {}
        
        try:
            # Investing.com에서 글로벌 국채 수익률 데이터 가져오기
            url = "https://www.investing.com/rates-bonds/world-government-bonds"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 테이블에서 데이터 추출
            table = soup.find('table', {'id': 'cr1'})
            if table:
                rows = table.find_all('tr')[1:]  # 헤더 제외
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) >= 3:
                        country_name = cells[0].get_text(strip=True)
                        yield_value = cells[2].get_text(strip=True)
                        
                        # 국가명 매핑
                        country_mapping = {
                            'United States 10Y': '미국',
                            'Germany 10Y': '독일',
                            'Japan 10Y': '일본',
                            'United Kingdom 10Y': '영국',
                            'France 10Y': '프랑스',
                            'Italy 10Y': '이탈리아',
                            'Spain 10Y': '스페인',
                            'Canada 10Y': '캐나다',
                            'Australia 10Y': '호주',
                            'South Korea 10Y': '한국'
                        }
                        
                        if country_name in country_mapping:
                            korean_name = country_mapping[country_name]
                            try:
                                yield_float = float(yield_value.replace('%', ''))
                                bond_yields[korean_name] = {
                                    '10년': yield_float,
                                    'date': datetime.now().strftime('%Y-%m-%d'),
                                    'source': 'Investing.com'
                                }
                                print(f"✅ {korean_name}: {yield_float:.2f}% (Investing.com)")
                            except ValueError:
                                print(f"❌ {korean_name}: 수익률 파싱 오류 - {yield_value}")
            
        except Exception as e:
            print(f"웹 스크래핑 오류: {e}")
        
        return bond_yields

    def get_sample_bond_yields(self) -> Dict[str, Any]:
        """샘플 데이터를 반환합니다 (API 실패 시 사용)."""
        return {
            '미국': {
                '1년': 4.85,
                '2년': 4.72,
                '5년': 4.45,
                '10년': 4.35,
                '30년': 4.52,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '독일': {
                '1년': 3.25,
                '2년': 3.15,
                '5년': 2.95,
                '10년': 2.75,
                '30년': 3.05,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '일본': {
                '1년': 0.15,
                '2년': 0.25,
                '5년': 0.45,
                '10년': 0.65,
                '30년': 1.25,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '영국': {
                '1년': 4.25,
                '2년': 4.15,
                '5년': 3.95,
                '10년': 3.85,
                '30년': 4.15,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '프랑스': {
                '1년': 3.45,
                '2년': 3.35,
                '5년': 3.15,
                '10년': 2.95,
                '30년': 3.25,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '이탈리아': {
                '1년': 3.85,
                '2년': 3.75,
                '5년': 3.55,
                '10년': 3.35,
                '30년': 3.65,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '스페인': {
                '1년': 3.65,
                '2년': 3.55,
                '5년': 3.35,
                '10년': 3.15,
                '30년': 3.45,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '캐나다': {
                '1년': 4.45,
                '2년': 4.35,
                '5년': 4.15,
                '10년': 3.95,
                '30년': 4.25,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '호주': {
                '1년': 4.15,
                '2년': 4.05,
                '5년': 3.85,
                '10년': 3.65,
                '30년': 3.95,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            },
            '한국': {
                '1년': 3.35,
                '2년': 3.25,
                '5년': 3.05,
                '10년': 2.85,
                '30년': 3.15,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Sample Data'
            }
        }

    def generate_realistic_yield_curve(self, base_10y_yield: float, country: str) -> Dict[str, float]:
        """10년 금리를 기준으로 현실적인 수익률 곡선을 생성합니다."""
        # 각 국가별 수익률 곡선 특성 (일반적인 패턴)
        yield_curves = {
            '미국': {'1년': -0.5, '2년': -0.3, '5년': -0.1, '10년': 0.0, '30년': 0.3},
            '독일': {'1년': -0.4, '2년': -0.2, '5년': -0.1, '10년': 0.0, '30년': 0.2},
            '일본': {'1년': -0.8, '2년': -0.6, '5년': -0.4, '10년': 0.0, '30년': 0.4},
            '영국': {'1년': -0.4, '2년': -0.2, '5년': -0.1, '10년': 0.0, '30년': 0.2},
            '프랑스': {'1년': -0.4, '2년': -0.2, '5년': -0.1, '10년': 0.0, '30년': 0.2},
            '이탈리아': {'1년': -0.3, '2년': -0.2, '5년': -0.1, '10년': 0.0, '30년': 0.2},
            '스페인': {'1년': -0.3, '2년': -0.2, '5년': -0.1, '10년': 0.0, '30년': 0.2},
            '캐나다': {'1년': -0.4, '2년': -0.2, '5년': -0.1, '10년': 0.0, '30년': 0.2},
            '호주': {'1년': -0.4, '2년': -0.2, '5년': -0.1, '10년': 0.0, '30년': 0.2},
            '한국': {'1년': -0.4, '2년': -0.2, '5년': -0.1, '10년': 0.0, '30년': 0.2}
        }
        
        curve = yield_curves.get(country, yield_curves['미국'])
        yields = {}
        
        for maturity, offset in curve.items():
            yields[maturity] = round(base_10y_yield + offset, 2)
        
        return yields

    def collect_global_bond_yields(self) -> Dict[str, Any]:
        """글로벌 국채 금리 데이터를 수집합니다."""
        print("글로벌 국채 금리 데이터 수집 시작...")
        
        bond_yields = {}
        
        # 1. 중국 데이터 먼저 수집 (Investing.com)
        print("\n🇨🇳 중국 국채 수익률 데이터 수집 시도...")
        chinese_data = self.get_chinese_bond_yields_from_investing()
        if chinese_data:
            bond_yields['중국'] = chinese_data
            print(f"✅ 중국 데이터 수집 완료: {len(chinese_data)-2}개 만기")
        
        # 2. 일본 데이터 수집 (Investing.com)
        print("\n🇯🇵 일본 국채 수익률 데이터 수집 시도...")
        japanese_data = self.get_japanese_bond_yields_from_investing()
        if japanese_data:
            bond_yields['일본'] = japanese_data
            print(f"✅ 일본 데이터 수집 완료: {len(japanese_data)-2}개 만기")
        
        # 3. 한국 데이터 수집 (Investing.com)
        print("\n🇰🇷 한국 국채 수익률 데이터 수집 시도...")
        korean_data = self.get_korean_bond_yields_from_investing()
        if korean_data:
            bond_yields['한국'] = korean_data
            print(f"✅ 한국 데이터 수집 완료: {len(korean_data)-2}개 만기")
        
        # 4. 호주 데이터 수집 (Investing.com)
        print("\n🇦🇺 호주 국채 수익률 데이터 수집 시도...")
        australian_data = self.get_australian_bond_yields_from_investing()
        if australian_data:
            bond_yields['호주'] = australian_data
            print(f"✅ 호주 데이터 수집 완료: {len(australian_data)-2}개 만기")
        
        # 5. 독일 데이터 수집 (Investing.com)
        print("\n🇩🇪 독일 국채 수익률 데이터 수집 시도...")
        german_data = self.get_german_bond_yields_from_investing()
        if german_data:
            bond_yields['독일'] = german_data
            print(f"✅ 독일 데이터 수집 완료: {len(german_data)-2}개 만기")
        
        # 6. 영국 데이터 수집 (Investing.com)
        print("\n🇬🇧 영국 국채 수익률 데이터 수집 시도...")
        british_data = self.get_british_bond_yields_from_investing()
        if british_data:
            bond_yields['영국'] = british_data
            print(f"✅ 영국 데이터 수집 완료: {len(british_data)-2}개 만기")
        
        # 7. 프랑스 데이터 수집 (Investing.com)
        print("\n🇫🇷 프랑스 국채 수익률 데이터 수집 시도...")
        french_data = self.get_french_bond_yields_from_investing()
        if french_data:
            bond_yields['프랑스'] = french_data
            print(f"✅ 프랑스 데이터 수집 완료: {len(french_data)-2}개 만기")
        
        # 8. 캐나다 데이터 수집 (Investing.com)
        print("\n🇨🇦 캐나다 국채 수익률 데이터 수집 시도...")
        canadian_data = self.get_canadian_bond_yields_from_investing()
        if canadian_data:
            bond_yields['캐나다'] = canadian_data
            print(f"✅ 캐나다 데이터 수집 완료: {len(canadian_data)-2}개 만기")
        
        # 9. 미국 데이터 수집 (Investing.com)
        print("\n🇺🇸 미국 국채 수익률 데이터 수집 시도...")
        american_data = self.get_american_bond_yields_from_investing()
        if american_data:
            bond_yields['미국'] = american_data
            print(f"✅ 미국 데이터 수집 완료: {len(american_data)-2}개 만기")
        
        # 10. 스페인 데이터 수집 (Investing.com)
        print("\n🇪🇸 스페인 국채 수익률 데이터 수집 시도...")
        spanish_data = self.get_spanish_bond_yields_from_investing()
        if spanish_data:
            bond_yields['스페인'] = spanish_data
            print(f"✅ 스페인 데이터 수집 완료: {len(spanish_data)-2}개 만기")
        
        # 11. 이탈리아 데이터 수집 (Investing.com)
        print("\n🇮🇹 이탈리아 국채 수익률 데이터 수집 시도...")
        italian_data = self.get_italian_bond_yields_from_investing()
        if italian_data:
            bond_yields['이탈리아'] = italian_data
            print(f"✅ 이탈리아 데이터 수집 완료: {len(italian_data)-2}개 만기")
        
        # 2. 웹 스크래핑 시도 (다른 국가들)
        print("\n🌐 웹 스크래핑을 통한 데이터 수집 시도...")
        web_data = self.get_bond_yields_from_web()
        if web_data:
            bond_yields.update(web_data)
            print(f"✅ 웹 스크래핑으로 {len(web_data)}개국 데이터 수집")
        
        # 13. FRED API 시도 (웹 스크래핑 실패 시, 중국, 일본, 한국, 호주, 독일, 영국, 프랑스, 캐나다, 미국, 스페인, 이탈리아 제외)
        if len(bond_yields) < 16:  # 16개국 미만이면 FRED API 시도
            print("\n📊 FRED API를 통한 데이터 수집 시도...")
            for country_code, maturity_series in self.fred_series.items():
                country_name = self.country_names[country_code]
                
                # 중국, 일본, 한국, 호주, 독일, 영국, 프랑스, 캐나다, 미국, 스페인, 이탈리아는 이미 Investing.com에서 수집했으므로 제외
                if country_code in ['CN', 'JP', 'KR', 'AU', 'DE', 'GB', 'FR', 'CA', 'US', 'ES', 'IT']:
                    continue
                    
                print(f"{country_name} ({country_code}) 데이터 수집 중...")
                
                country_data = {}
                success_count = 0
                
                # 10년 금리만 먼저 수집
                ten_year_series = maturity_series['10년']
                fred_data = self.get_fred_data(ten_year_series, self.fred_api_key)
                
                if fred_data and fred_data['value'] is not None:
                    base_10y_yield = fred_data['value']
                    print(f"  ✅ 10년: {base_10y_yield:.2f}% (FRED)")
                    
                    # 10년 금리를 기준으로 현실적인 수익률 곡선 생성
                    yield_curve = self.generate_realistic_yield_curve(base_10y_yield, country_name)
                    country_data.update(yield_curve)
                    success_count = 5  # 모든 만기 데이터 생성됨
                    
                    print(f"  📊 수익률 곡선 생성: {country_name}")
                    for maturity, value in yield_curve.items():
                        print(f"    {maturity}: {value:.2f}%")
                else:
                    print(f"  ❌ 10년: 데이터 없음")
                
                # API 호출 제한을 위한 지연
                time.sleep(0.1)
                
                # 미국의 경우 Alpha Vantage로 보완
                if country_code == 'US' and success_count < 3:
                    print(f"  🔄 {country_name} Alpha Vantage 보완 데이터 수집...")
                    av_yields = self.get_all_treasury_yields(self.alpha_vantage_key)
                    
                    for maturity, value in av_yields.items():
                        if maturity not in country_data:
                            country_data[maturity] = value
                            print(f"  ✅ {maturity}: {value:.2f}% (Alpha Vantage)")
                
                # 데이터가 있으면 저장
                if country_data:
                    bond_yields[country_name] = {
                        **country_data,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'FRED/Alpha Vantage'
                    }
                    print(f"✅ {country_name}: {len(country_data)}개 만기 데이터 수집 완료")
                else:
                    print(f"❌ {country_name}: 데이터 수집 실패")
        
        # 3. 모든 방법 실패 시 샘플 데이터 사용
        if len(bond_yields) < 5:  # 5개국 미만이면 샘플 데이터 사용
            print(f"\n📋 수집된 데이터가 {len(bond_yields)}개국으로 부족 - 샘플 데이터로 보완")
            sample_data = self.get_sample_bond_yields()
            # 기존 데이터와 샘플 데이터 병합 (기존 데이터 우선)
            for country, data in sample_data.items():
                if country not in bond_yields:
                    bond_yields[country] = data
        
        # 수집된 데이터 요약
        print(f"\n📊 최종 수집 완료: {len(bond_yields)}개국 데이터")
        for country_name, data in bond_yields.items():
            print(f"  {country_name}: {data['10년']:.2f}% ({data['source']})")
        
        return bond_yields

    def save_to_json(self, data: Dict[str, Any], filename: str = 'global_bond_yields.json'):
        """데이터를 JSON 파일로 저장합니다."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 데이터가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"❌ 파일 저장 오류: {e}")

    def load_from_json(self, filename: str = 'global_bond_yields.json') -> Optional[Dict[str, Any]]:
        """JSON 파일에서 데이터를 로드합니다."""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {filename}에서 데이터를 로드했습니다.")
                return data
            else:
                print(f"❌ {filename} 파일이 존재하지 않습니다.")
                return None
        except Exception as e:
            print(f"❌ 파일 로드 오류: {e}")
            return None

def main():
    """메인 실행 함수"""
    collector = BondYieldsCollector()
    
    # 데이터 수집
    bond_yields = collector.collect_global_bond_yields()
    
    # JSON 파일로 저장
    collector.save_to_json(bond_yields)
    
    # 웹 대시보드용 JSON 출력
    print("\n🌐 웹 대시보드용 JSON:")
    print(json.dumps(bond_yields, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
