#!/usr/bin/env python3
"""
Simple RRG Server - CGI 스타일로 RRG 데이터를 생성하는 간단한 서버
"""

import cgi
import json
import sys
import os
from datetime import datetime
from rrg_plotter import RRGPlotter

def main():
    """CGI 스타일로 RRG 데이터를 생성합니다."""
    try:
        # Content-Type 헤더 설정
        print("Content-Type: application/json")
        print("Access-Control-Allow-Origin: *")
        print("Access-Control-Allow-Methods: POST, GET, OPTIONS")
        print("Access-Control-Allow-Headers: Content-Type")
        print()
        
        # POST 데이터 읽기
        if os.environ.get('REQUEST_METHOD') == 'POST':
            content_length = int(os.environ.get('CONTENT_LENGTH', 0))
            post_data = sys.stdin.read(content_length)
            
            try:
                data = json.loads(post_data)
                period = data.get('period', 252)
            except json.JSONDecodeError:
                period = 252
        else:
            period = 252
        
        print(f"Generating RRG data with period: {period} days", file=sys.stderr)
        
        # RRG 데이터 생성
        rrg = RRGPlotter(period=period)
        rrg.run_full_analysis()
        
        # 생성된 JSON 파일 읽기
        try:
            with open('rrg_data.json', 'r', encoding='utf-8') as f:
                rrg_data = json.load(f)
            
            response = {
                'success': True,
                'data': rrg_data,
                'period': period,
                'timestamp': datetime.now().isoformat()
            }
            
            print(json.dumps(response, ensure_ascii=False, indent=2))
            
        except FileNotFoundError:
            response = {
                'success': False,
                'error': 'RRG data file not found'
            }
            print(json.dumps(response))
            
    except Exception as e:
        response = {
            'success': False,
            'error': str(e)
        }
        print(json.dumps(response))

if __name__ == '__main__':
    main()
