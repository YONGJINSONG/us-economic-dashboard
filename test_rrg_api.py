#!/usr/bin/env python3
"""
RRG API 테스트 스크립트
"""

import requests
import json
import time

def test_rrg_api():
    """RRG API 테스트"""
    base_url = "http://127.0.0.1:5000"
    
    print("🧪 RRG API 테스트 시작...")
    
    # 1. 상태 확인
    print("\n1. API 상태 확인...")
    try:
        response = requests.get(f"{base_url}/api/rrg/status")
        if response.status_code == 200:
            print("✅ API 서버 정상 작동")
            print(f"   응답: {response.json()}")
        else:
            print(f"❌ API 서버 오류: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ API 서버 연결 실패: {e}")
        return
    
    # 2. 섹터 목록 확인
    print("\n2. 섹터 목록 확인...")
    try:
        response = requests.get(f"{base_url}/api/rrg/sectors")
        if response.status_code == 200:
            data = response.json()
            print("✅ 섹터 목록 조회 성공")
            print(f"   벤치마크: {data['benchmark']}")
            print(f"   섹터 수: {len(data['sectors'])}")
        else:
            print(f"❌ 섹터 목록 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 섹터 목록 조회 오류: {e}")
    
    # 3. RRG 데이터 생성 테스트 (1년)
    print("\n3. RRG 데이터 생성 테스트 (1년)...")
    try:
        response = requests.get(f"{base_url}/api/rrg/generate?period=252")
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print("✅ RRG 데이터 생성 성공")
                print(f"   기간: {data['period']}일")
                print(f"   날짜: {data['date']}")
                print(f"   섹터 수: {len(data['data'])}")
                
                # 첫 번째 섹터 데이터 출력
                first_sector = list(data['data'].keys())[0]
                sector_data = data['data'][first_sector]
                print(f"   예시 - {first_sector} ({sector_data['name']}):")
                print(f"     상대강도: {sector_data['relative_strength']}")
                print(f"     모멘텀: {sector_data['momentum']}")
                print(f"     사분면: {sector_data['quadrant']}")
            else:
                print(f"❌ RRG 데이터 생성 실패: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ RRG 데이터 생성 요청 실패: {response.status_code}")
            print(f"   응답: {response.text}")
    except Exception as e:
        print(f"❌ RRG 데이터 생성 오류: {e}")
    
    # 4. 다른 기간 테스트 (1주일)
    print("\n4. RRG 데이터 생성 테스트 (1주일)...")
    try:
        response = requests.get(f"{base_url}/api/rrg/generate?period=5")
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                print("✅ 1주일 RRG 데이터 생성 성공")
                print(f"   섹터 수: {len(data['data'])}")
            else:
                print(f"❌ 1주일 RRG 데이터 생성 실패: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ 1주일 RRG 데이터 생성 요청 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ 1주일 RRG 데이터 생성 오류: {e}")
    
    print("\n🏁 테스트 완료!")

if __name__ == "__main__":
    # API 서버가 시작될 때까지 잠시 대기
    print("⏳ API 서버 시작 대기 중...")
    time.sleep(3)
    
    test_rrg_api()
