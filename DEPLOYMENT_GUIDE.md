# 🚀 배포 가이드

## GitHub Pages 배포 (자동)

### 1. GitHub Pages 활성화

1. https://github.com/YONGJINSONG/us-economic-dashboard 접속
2. `Settings` → `Pages` 이동
3. 설정:
   - **Source**: Deploy from a branch
   - **Branch**: `main`
   - **Folder**: `/ (root)`
   - **Save** 클릭

### 2. 커스텀 도메인 설정

1. `Custom domain` 섹션에 `bareunsong.com` 입력
2. `Save` 클릭
3. DNS가 체크될 때까지 대기 (1-2분)

### 3. Cafe24 DNS 설정

Cafe24 도메인 관리에서:

```
타입: CNAME
호스트: www (또는 @)
값: yongjinsong.github.io
```

또는 A 레코드:
```
타입: A
호스트: @
값: 185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153
```

---

## Cafe24 FTP 수동 업로드

### 업로드할 파일:

**필수 파일:**
- `index.html`
- `app.js`
- `style.css`
- `rrg_data.json`

**추가 파일:**
- `dashboard_data.json`
- `global_bond_yields.json`
- `market_returns.json`
- `us_economic_data.json`

**업로드하지 말아야 할 파일:**
- `server.js` (Node.js 서버 - 로컬 전용)
- `rrg_blog_api_server.py` (Python API - 로컬 전용)
- `node_modules/` (의존성 - 서버에서 필요 없음)
- `__pycache__/` (Python 캐시)
- `backup_*` 폴더들

### FTP 업로드 경로:

일반적으로 Cafe24는:
```
/www 또는 /public_html
```

---

## 자동 업데이트 작동 방식

### GitHub Actions (매일 자동)

1. **매일 한국 시간 오전 9시** (UTC 0시) 자동 실행
2. `generate_rrg_json.py` 스크립트 실행
3. 최신 RRG 데이터 계산
4. `rrg_data.json` 파일 업데이트
5. 자동 커밋 & 푸시

### 수동 실행:

1. GitHub → `Actions` 탭
2. `Update RRG Data` 워크플로우 선택
3. `Run workflow` 버튼 클릭

---

## 배포 확인

### GitHub Pages:
```
https://yongjinsong.github.io/us-economic-dashboard/
```

### 커스텀 도메인:
```
http://bareunsong.com/index/
```

### 확인 사항:
- ✅ 모바일에서 FRED 그래프가 이미지로 표시되는지
- ✅ RRG 차트가 정상 작동하는지
- ✅ FED 금리 위젯이 로드되는지

---

## 문제 해결

### 변경사항이 반영되지 않는 경우:

1. **브라우저 캐시 삭제**:
   - Chrome: `Ctrl + Shift + Delete`
   - 강력 새로고침: `Ctrl + Shift + R`

2. **GitHub Pages 빌드 확인**:
   - Repository → `Actions` 탭
   - 최근 워크플로우 실행 상태 확인

3. **DNS 전파 대기**:
   - 커스텀 도메인 설정 시 최대 24-48시간 소요 가능

4. **Cafe24 설정 확인**:
   - 도메인 연결 설정이 올바른지 확인
   - FTP 파일이 최신인지 확인


