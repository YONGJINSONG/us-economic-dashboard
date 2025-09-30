# RRG Indicator v2.2 (Relative Rotation Graph)

SPDR 섹터 ETF들의 상대적 강도 회전 그래프를 시각화하는 프로그램입니다.

## 기능

- **11개 SPDR 섹터 ETF 분석**: XLB, XLC, XLE, XLF, XLI, XLK, XLP, XLRE, XLU, XLV, XLY
- **실시간 RRG 차트**: JdK RS Ratio vs JdK RS Momentum
- **움직임 방향 화살표**: 각 섹터의 움직임 방향을 화살표로 표시
- **동적 티커 관리**: 
  - 실시간 티커 추가/제거 기능
  - 자동 RRG 재계산
  - Yahoo Finance 데이터 자동 다운로드
  - 확인 대화상자로 실수 방지
  - 스크롤 지원으로 많은 티커 관리
- **인터랙티브 컨트롤**: 
  - 날짜 슬라이더로 시간 이동
  - Tail 슬라이더로 표시 기간 조절
  - Play/Pause 버튼으로 애니메이션 제어
  - 체크박스로 섹터 표시/숨김
- **상태별 색상 코딩**:
  - 🔴 빨간색: Lagging (후행)
  - 🟢 초록색: Leading (선행)
  - 🔵 파란색: Improving (개선)
  - 🟡 노란색: Weakening (약화)

## 설치 및 실행

### 방법 1: 자동 설치 및 실행 (권장)
1. `install_and_run.bat` 파일을 더블클릭
2. 필요한 패키지가 자동으로 설치되고 프로그램이 실행됩니다

### 방법 2: 수동 설치
1. 명령 프롬프트(cmd)를 관리자 권한으로 실행
2. 프로젝트 폴더로 이동
3. 다음 명령어 실행:
   ```
   pip install -r requirements.txt
   python RRGIndicator.py
   ```

### 방법 3: 간단 실행
- 패키지가 이미 설치되어 있다면 `run.bat` 파일을 더블클릭

## 시스템 요구사항

- Python 3.7 이상
- 인터넷 연결 (실시간 데이터 다운로드용)

## 필요한 패키지

- pandas: 데이터 처리
- numpy: 수치 계산
- yfinance: Yahoo Finance 데이터
- matplotlib: 그래프 시각화
- scipy: 과학 계산
- tkinter: GUI (Python 기본 포함)

## 사용법

1. 프로그램 실행 후 차트에서 각 섹터의 위치를 확인
2. 하단 슬라이더로 날짜와 표시 기간 조절
3. Play 버튼으로 애니메이션 시작/정지
4. 체크박스로 관심 있는 섹터만 선택하여 표시
5. 화살표로 각 섹터의 움직임 방향 파악

### 티커 관리 기능

**새 티커 추가하기**:
- "Add Ticker" 버튼 클릭
- 원하는 티커 심볼 입력 (예: AAPL, MSFT, GOOGL, TSLA)
- 자동으로 데이터 다운로드 및 RRG 계산

**티커 제거하기**:
- "Remove Ticker" 버튼 클릭
- 제거할 티커 선택
- 자동으로 차트에서 제거 및 RRG 재계산

**주의사항**:
- 최소 1개 티커는 반드시 유지되어야 함
- 새 티커 추가 시 인터넷 연결 필요
- 잘못된 티커 심볼 입력 시 오류 메시지 표시

## 문제 해결

- **패키지 설치 오류**: `pip install --upgrade pip` 후 재시도
- **프로그램 실행 오류**: Python 3.7 이상 버전 확인
- **데이터 로딩 오류**: 인터넷 연결 상태 확인

## 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제작되었습니다.
