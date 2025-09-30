#!/usr/bin/env python3
"""
yfinance 테스트 스크립트
"""

import yfinance as yf
from datetime import datetime, timedelta

def test_yfinance():
    """yfinance 기본 테스트"""
    print("🧪 yfinance 테스트 시작...")
    
    try:
        # 간단한 데이터 다운로드 테스트
        print("1. SPY 데이터 다운로드 테스트...")
        spy = yf.download('SPY', period='1mo', progress=False)
        print(f"   SPY 데이터 형태: {spy.shape}")
        print(f"   SPY 컬럼: {list(spy.columns)}")
        print(f"   SPY 최근 3일 데이터:")
        print(spy.tail(3))
        
        print("\n2. 섹터 ETF 데이터 다운로드 테스트...")
        symbols = ['XLB', 'XLC', 'XLE', 'XLF', 'XLI']
        for symbol in symbols:
            try:
                data = yf.download(symbol, period='1mo', progress=False)
                print(f"   {symbol}: {data.shape}")
            except Exception as e:
                print(f"   {symbol}: 오류 - {e}")
        
        print("\n3. 특정 기간 데이터 다운로드 테스트...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        spy_period = yf.download('SPY', start=start_date, end=end_date, progress=False)
        print(f"   SPY (30일): {spy_period.shape}")
        
        print("\n✅ yfinance 테스트 완료!")
        
    except Exception as e:
        print(f"❌ yfinance 테스트 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_yfinance()
