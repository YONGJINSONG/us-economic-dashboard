# 실시간 데이터 업데이트 시스템

## 개요

미국 경제지표 대시보드에 실시간 데이터 업데이트 기능을 추가했습니다. 이 시스템은 다음과 같은 데이터 소스에서 실시간 정보를 가져와 대시보드를 자동으로 업데이트합니다:

## 지원되는 데이터 소스

### 1. BDI (Baltic Dry Index)
- **소스**: https://kr.investing.com/indices/baltic-dry
- **설명**: 발틱 드라이 인덱스 - 해상 운송 시장의 주요 지표
- **업데이트 주기**: 5분마다 자동 업데이트

### 2. WTI 원유 현물
- **소스**: https://www.investing.com/commodities/crude-oil
- **설명**: 미국 서부 텍사스 중질유 현물 가격
- **업데이트 주기**: 5분마다 자동 업데이트

### 3. FED 금리 모니터링
- **소스**: https://kr.investing.com/central-banks/fed-rate-monitor
- **설명**: 연방준비제도 기준금리
- **업데이트 주기**: 5분마다 자동 업데이트

### 4. 달러인덱스 (DXY)
- **소스**: https://www.investing.com/indices/usdollar?cid=1224074
- **설명**: 달러 강세/약세를 나타내는 지수
- **업데이트 주기**: 5분마다 자동 업데이트

### 5. 주요 통화간 환율
- **소스**: https://www.investing.com/currencies/
- **지원 통화쌍**:
  - EUR/USD
  - USD/JPY
  - USD/CNY
  - AUD/USD
  - USD/KRW
- **업데이트 주기**: 5분마다 자동 업데이트

### 6. 하이일드 채권 스프레드
- **소스**: https://fred.stlouisfed.org/series/BAMLH0A0HYM2
- **설명**: ICE BofA US High Yield Index Option-Adjusted Spread
- **업데이트 주기**: 5분마다 자동 업데이트

### 7. 미국 시장 수익률 (섹터별)
- **소스**: https://www.investing.com/etfs/ (Sector ETFs)
- **지원 섹터**:
  - Technology (반도체/정보기술)
  - Healthcare (헬스케어)
  - Financial (금융)
  - Consumer Discretionary (임의소비재)
  - Consumer Staples (필수소비재)
  - Utilities (유틸리티)
  - Energy (에너지)
  - Industrials (산업재)
  - Real Estate (부동산)
  - Materials (소재)
  - Communication Services (정보기술)
- **업데이트 주기**: 5분마다 자동 업데이트

### 8. 글로벌 국채 금리
- **소스**: https://www.investing.com/rates-bonds/
- **지원 국가**:
  - 미국 (10년 국채)
  - 한국 (10년 국채)
  - 중국 (10년 국채)
  - 일본 (10년 국채)
  - 독일 (10년 국채)
  - 영국 (10년 국채)
- **업데이트 주기**: 5분마다 자동 업데이트

### 9. 미국 국채 수익률
- **소스**: https://www.investing.com/rates-bonds/
- **지원 만기**:
  - 3개월 국채
  - 2년 국채
  - 10년 국채
  - 30년 국채
- **업데이트 주기**: 5분마다 자동 업데이트

## 시스템 아키텍처

### RealTimeDataFetcher 클래스
```javascript
class RealTimeDataFetcher {
  constructor() {
    this.updateInterval = 5 * 60 * 1000; // 5분
    this.dataCache = new Map();
    this.isUpdating = false;
  }
}
```

### 주요 기능
1. **자동 업데이트**: 5분마다 모든 데이터 소스에서 최신 정보를 가져옴
2. **수동 업데이트**: 사용자가 원할 때 즉시 데이터를 새로고침
3. **에러 처리**: 네트워크 오류나 데이터 소스 문제 시 폴백 데이터 사용
4. **상태 표시**: 실시간 데이터 상태를 시각적으로 표시

## 사용법

### 자동 업데이트
시스템이 시작되면 자동으로 5분마다 데이터를 업데이트합니다.

### 수동 업데이트
헤더의 "🔄 실시간 업데이트" 버튼을 클릭하여 즉시 데이터를 새로고침할 수 있습니다.

### 상태 표시
- ✅ **데이터 정상**: 모든 데이터가 정상적으로 업데이트됨
- 🔄 **업데이트 중**: 데이터 업데이트 진행 중
- ❌ **오류**: 데이터 업데이트 중 오류 발생

## 에러 처리 및 폴백

### 1. 네트워크 오류
- CORS 문제나 네트워크 연결 실패 시 폴백 데이터 사용
- 사용자에게 오류 메시지 표시

### 2. 데이터 파싱 오류
- HTML 구조 변경으로 인한 파싱 실패 시 폴백 데이터 사용
- 콘솔에 상세한 오류 로그 출력

### 3. API 제한
- FRED API 호출 제한 시 폴백 데이터 사용
- 재시도 로직 구현

## 폴백 데이터

시스템이 실시간 데이터를 가져올 수 없을 때 사용하는 기본값:

- **BDI**: 1,250
- **WTI**: $76.20/배럴
- **FED 금리**: 5.50%
- **달러인덱스**: 97.5
- **하이일드 스프레드**: 278 bps
- **EUR/USD**: 1.0750
- **USD/JPY**: 147.85
- **USD/CNY**: 7.1280
- **AUD/USD**: 0.6675
- **USD/KRW**: 1395.50

### 시장 수익률 (섹터별)
- **Technology**: +8.7%
- **Healthcare**: -3.1%
- **Financial**: +4.9%
- **Consumer Discretionary**: +6.5%
- **Consumer Staples**: -2.6%
- **Utilities**: +2.1%
- **Energy**: -1.3%
- **Industrials**: +3.4%
- **Real Estate**: -4.3%
- **Materials**: -0.6%
- **Communication Services**: +2.3%

### 글로벌 국채 금리 (10년)
- **미국**: 4.47%
- **한국**: 3.57%
- **중국**: 2.27%
- **일본**: 0.67%
- **독일**: 2.67%
- **영국**: 4.67%

### 미국 국채 수익률
- **3개월**: 4.37%
- **2년**: 4.27%
- **10년**: 4.47%
- **30년**: 4.57%

## 기술적 구현

### 1. 이벤트 기반 아키텍처
```javascript
// 데이터 업데이트 이벤트
window.addEventListener('realTimeDataUpdate', handleRealTimeDataUpdate);

// 에러 이벤트
window.addEventListener('realTimeDataError', handleRealTimeDataError);
```

### 2. 데이터 캐싱
```javascript
this.dataCache.set('bdi', {
  value: bdiValue,
  timestamp: new Date(),
  source: 'investing.com'
});
```

### 3. 차트 업데이트
```javascript
// 차트의 마지막 데이터 포인트를 실시간 값으로 업데이트
const lastIndex = bdiChart.data.datasets[0].data.length - 1;
bdiChart.data.datasets[0].data[lastIndex] = newValue;
bdiChart.update('none');
```

## 성능 최적화

1. **병렬 처리**: 모든 데이터 소스를 동시에 가져옴
2. **캐싱**: 이전 데이터를 메모리에 저장하여 빠른 접근
3. **차트 최적화**: 전체 차트를 다시 그리지 않고 마지막 포인트만 업데이트
4. **에러 복구**: 개별 데이터 소스 실패가 전체 시스템에 영향을 주지 않음

## 보안 고려사항

1. **CORS 정책**: 브라우저의 CORS 정책으로 인해 직접적인 웹 스크래핑이 제한됨
2. **프록시 서버**: 프로덕션 환경에서는 백엔드 프록시 서버 사용 권장
3. **API 키**: FRED API 사용 시 적절한 API 키 설정 필요

## 향후 개선 사항

1. **백엔드 프록시**: CORS 문제 해결을 위한 백엔드 서버 구현
2. **WebSocket**: 실시간 데이터 스트리밍을 위한 WebSocket 연결
3. **데이터베이스**: 히스토리컬 데이터 저장을 위한 데이터베이스 연동
4. **알림 시스템**: 중요한 데이터 변화 시 사용자 알림
5. **모바일 최적화**: 모바일 환경에서의 성능 최적화

## 문제 해결

### 자주 발생하는 문제

1. **데이터가 업데이트되지 않음**
   - 네트워크 연결 확인
   - 브라우저 콘솔에서 오류 메시지 확인
   - 수동 업데이트 버튼 클릭

2. **CORS 오류**
   - 개발 환경에서는 정상적인 현상
   - 프로덕션에서는 백엔드 프록시 서버 필요

3. **차트가 업데이트되지 않음**
   - 차트 초기화 상태 확인
   - 데이터 형식 확인

## 로그 및 디버깅

시스템은 상세한 로그를 콘솔에 출력합니다:

```javascript
console.log('Real-time data fetcher initialized');
console.log('Starting real-time data fetch...');
console.log('BDI updated to: 1247 (source: investing.com)');
```

브라우저 개발자 도구의 콘솔 탭에서 실시간 데이터 업데이트 상태를 모니터링할 수 있습니다.
