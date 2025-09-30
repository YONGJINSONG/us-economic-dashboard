#!/usr/bin/env python3
"""
RRG API Server - 웹에서 RRG 데이터를 생성할 수 있는 API 서버
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import json
import os
import sys
from datetime import datetime

app = Flask(__name__)
CORS(app)  # CORS 허용

@app.route('/api/rrg/generate', methods=['POST'])
def generate_rrg_data():
    """선택된 기간으로 RRG 데이터를 생성합니다."""
    try:
        data = request.get_json()
        period = data.get('period', 252)
        
        print(f"Generating RRG data with period: {period} days")
        
        # Python 스크립트 실행
        result = subprocess.run([
            sys.executable, '-c', 
            f'from rrg_plotter import RRGPlotter; rrg = RRGPlotter(period={period}); rrg.run_full_analysis()'
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode != 0:
            return jsonify({
                'success': False,
                'error': f'Python script failed: {result.stderr}'
            }), 500
        
        # 생성된 JSON 파일 읽기
        try:
            with open('rrg_data.json', 'r', encoding='utf-8') as f:
                rrg_data = json.load(f)
            
            return jsonify({
                'success': True,
                'data': rrg_data,
                'period': period,
                'timestamp': datetime.now().isoformat()
            })
            
        except FileNotFoundError:
            return jsonify({
                'success': False,
                'error': 'RRG data file not found'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/rrg/status', methods=['GET'])
def get_status():
    """API 서버 상태를 확인합니다."""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting RRG API Server...")
    print("API Endpoints:")
    print("  POST /api/rrg/generate - Generate RRG data with specified period")
    print("  GET /api/rrg/status - Check server status")
    app.run(host='127.0.0.1', port=5000, debug=True)
