#!/usr/bin/env python3
"""
RRG 기간별 데이터 비교 테스트
"""

import requests
import json

def test_different_periods():
    """다른 기간의 RRG 데이터 비교"""
    base_url = "http://127.0.0.1:5000"
    periods = [5, 21, 63, 126, 252]
    
    print("🧪 RRG 기간별 데이터 비교 테스트...")
    
    results = {}
    
    for period in periods:
        print(f"\n📊 {period}일 기간 테스트...")
        try:
            response = requests.get(f"{base_url}/api/rrg/generate?period={period}")
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'success':
                    results[period] = data['data']
                    print(f"✅ {period}일 데이터 수집 성공")
                    
                    # XLB 섹터 데이터 출력
                    if 'XLB' in data['data']:
                        xlb = data['data']['XLB']
                        print(f"   XLB (Materials):")
                        print(f"     상대강도: {xlb['relative_strength']}")
                        print(f"     모멘텀: {xlb['momentum']}")
                        print(f"     사분면: {xlb['quadrant']}")
                else:
                    print(f"❌ {period}일 데이터 생성 실패: {data.get('error')}")
            else:
                print(f"❌ {period}일 요청 실패: {response.status_code}")
        except Exception as e:
            print(f"❌ {period}일 테스트 오류: {e}")
    
    # 결과 비교
    print("\n📈 기간별 데이터 비교:")
    print("=" * 80)
    print(f"{'기간':<8} {'XLB 상대강도':<12} {'XLB 모멘텀':<12} {'XLB 사분면':<20}")
    print("=" * 80)
    
    for period in periods:
        if period in results and 'XLB' in results[period]:
            xlb = results[period]['XLB']
            print(f"{period}일    {xlb['relative_strength']:<12.4f} {xlb['momentum']:<12.4f} {xlb['quadrant']:<20}")
        else:
            print(f"{period}일    {'N/A':<12} {'N/A':<12} {'N/A':<20}")
    
    print("=" * 80)
    
    # 모멘텀 변화 확인
    print("\n🔄 모멘텀 변화 확인:")
    momentums = []
    for period in periods:
        if period in results and 'XLB' in results[period]:
            momentums.append((period, results[period]['XLB']['momentum']))
    
    if len(momentums) > 1:
        print("XLB 섹터 모멘텀 변화:")
        for period, momentum in momentums:
            print(f"  {period}일: {momentum:.4f}")
        
        # 모멘텀이 모두 다른지 확인
        unique_momentums = set([m[1] for m in momentums])
        if len(unique_momentums) > 1:
            print("✅ 모멘텀 값이 기간별로 다릅니다!")
        else:
            print("❌ 모멘텀 값이 모든 기간에서 동일합니다.")
    else:
        print("❌ 충분한 데이터가 없습니다.")

if __name__ == "__main__":
    test_different_periods()
