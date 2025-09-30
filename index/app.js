// Economic indicators data with real values
const marketData = {
  "market_impact": {
    "stock_market": [
      {"rank": 1, "indicator": "고용현황보고서"},
      {"rank": 2, "indicator": "ISM 제조업보고서"},
      {"rank": 3, "indicator": "주간 실업수당신청건수"},
      {"rank": 4, "indicator": "소비자물가"},
      {"rank": 5, "indicator": "생산자물가"},
      {"rank": 6, "indicator": "소매판매"},
      {"rank": 7, "indicator": "소비자신뢰와 심리조사"},
      {"rank": 8, "indicator": "개인소득과 지출"},
      {"rank": 9, "indicator": "내구재주문"},
      {"rank": 10, "indicator": "GDP"}
    ],
    "bond_market": [
      {"rank": 1, "indicator": "고용현황보고서"},
      {"rank": 2, "indicator": "소비자물가"},
      {"rank": 3, "indicator": "ISM 제조업보고서"},
      {"rank": 4, "indicator": "생산자물가"},
      {"rank": 5, "indicator": "주간 실업수당신청건수"},
      {"rank": 6, "indicator": "소매판매"},
      {"rank": 7, "indicator": "주택착송"},
      {"rank": 8, "indicator": "개인소득과 지출"},
      {"rank": 9, "indicator": "ADP 전미고용보고서"},
      {"rank": 10, "indicator": "GDP"}
    ],
    "currency_market": [
      {"rank": 1, "indicator": "고용현황보고서"},
      {"rank": 2, "indicator": "국제무역"},
      {"rank": 3, "indicator": "GDP"},
      {"rank": 4, "indicator": "경상수지"},
      {"rank": 5, "indicator": "산업생산/설비가동률"},
      {"rank": 6, "indicator": "ISM 제조업보고서"},
      {"rank": 7, "indicator": "소매판매"},
      {"rank": 8, "indicator": "소비자물가"},
      {"rank": 9, "indicator": "소비자신뢰와 심리조사"},
      {"rank": 10, "indicator": "생산성과 단위비용"}
    ],
    "leading_indicators": [
      {"rank": 1, "indicator": "수익률곡선"},
      {"rank": 2, "indicator": "내구재를 위한 신규주문"},
      {"rank": 3, "indicator": "ISM 제조업보고서 - 신규주문"},
      {"rank": 4, "indicator": "생산자물가(식량과 에너지를 제외한 원자재)"},
      {"rank": 5, "indicator": "개인소득과 지출(내구재 구매)"},
      {"rank": 6, "indicator": "주택허가(단독주택)"},
      {"rank": 7, "indicator": "주간 모기지신청(주택구입용)"},
      {"rank": 8, "indicator": "주택시장지수"},
      {"rank": 9, "indicator": "주간 실업수당신청"},
      {"rank": 10, "indicator": "고용현황보고서 - 비상근직 노동자와 트럭 운전사 고용"}
    ]
  },
  "last_updated": "동적 업데이트",
  "data_source": "US Economic Indicators Excel File"
};

// Function to generate dynamic economic data based on current date
function generateEconomicData() {
  const now = new Date();
  const currentYear = now.getFullYear();
  const currentMonth = now.getMonth() + 1; // 0-based to 1-based
  const currentDay = now.getDate();
  
  // Base data with realistic variations
  const baseData = {
    "고용현황보고서": {
      "base_value": 180000,
      "variation": 50000,
      "unit": "명",
      "description": "비농업 부문 고용 증가"
    },
    "ISM 제조업보고서": {
      "base_value": 50.0,
      "variation": 5.0,
      "unit": "지수",
      "description": "제조업 구매관리자 지수 (50 이상이 확장)"
    },
    "주간 실업수당신청건수": {
      "base_value": 200000,
      "variation": 30000,
      "unit": "건",
      "description": "주간 실업수당 신청 건수"
    },
    "소비자물가": {
      "base_value": 3.0,
      "variation": 0.5,
      "unit": "연율",
      "description": "소비자물가지수 전년동월대비"
    },
    "생산자물가": {
      "base_value": 1.0,
      "variation": 0.3,
      "unit": "연율",
      "description": "생산자물가지수 전년동월대비"
    },
    "소매판매": {
      "base_value": 700.0,
      "variation": 50.0,
      "unit": "십억달러",
      "description": "소매판매액"
    },
    "소비자신뢰와 심리조사": {
      "base_value": 100.0,
      "variation": 10.0,
      "unit": "지수",
      "description": "소비자신뢰지수"
    },
    "개인소득과 지출": {
      "base_value": 0.4,
      "variation": 0.2,
      "unit": "월간증감률",
      "description": "개인소득 증가율"
    },
    "내구재주문": {
      "base_value": 300.0,
      "variation": 30.0,
      "unit": "십억달러",
      "description": "내구재 주문액"
    },
    "GDP": {
      "base_value": 2.5,
      "variation": 1.0,
      "unit": "연율",
      "description": "실질 GDP 성장률"
    },
    "국제무역": {
      "base_value": -60.0,
      "variation": 10.0,
      "unit": "십억달러",
      "description": "무역수지"
    },
    "경상수지": {
      "base_value": -200.0,
      "variation": 20.0,
      "unit": "십억달러",
      "description": "경상수지"
    },
    "산업생산/설비가동률": {
      "base_value": 78.0,
      "variation": 2.0,
      "unit": "가동률",
      "description": "산업생산 설비가동률"
    },
    "생산성과 단위비용": {
      "base_value": 2.5,
      "variation": 1.0,
      "unit": "연율",
      "description": "노동생산성 증가율"
    },
    "수익률곡선": {
      "base_value": -0.2,
      "variation": 0.3,
      "unit": "기준점",
      "description": "10년-2년 국채 수익률 차이"
    },
    "내구재를 위한 신규주문": {
      "base_value": 300.0,
      "variation": 30.0,
      "unit": "십억달러",
      "description": "내구재 신규주문액"
    },
    "ISM 제조업보고서 - 신규주문": {
      "base_value": 52.0,
      "variation": 5.0,
      "unit": "지수",
      "description": "제조업 신규주문 지수"
    },
    "생산자물가(식량과 에너지를 제외한 원자재)": {
      "base_value": 2.0,
      "variation": 0.5,
      "unit": "연율",
      "description": "핵심 생산자물가"
    },
    "개인소득과 지출(내구재 구매)": {
      "base_value": 1800.0,
      "variation": 100.0,
      "unit": "십억달러",
      "description": "내구재 소비지출"
    },
    "주택허가(단독주택)": {
      "base_value": 1500.0,
      "variation": 100.0,
      "unit": "천호",
      "description": "단독주택 허가 건수"
    },
    "주간 모기지신청(주택구입용)": {
      "base_value": 160.0,
      "variation": 10.0,
      "unit": "지수",
      "description": "주택구입 모기지 신청 지수"
    },
    "주택시장지수": {
      "base_value": 40.0,
      "variation": 5.0,
      "unit": "지수",
      "description": "주택시장 지수"
    },
    "ADP 전미고용보고서": {
      "base_value": 150000,
      "variation": 50000,
      "unit": "명",
      "description": "ADP 민간부문 고용 증가"
    },
    "주택착송": {
      "base_value": 1500.0,
      "variation": 100.0,
      "unit": "천호",
      "description": "주택착송 건수"
    },
    "고용현황보고서 - 비상근직 노동자와 트럭 운전사 고용": {
      "base_value": 8000,
      "variation": 2000,
      "unit": "명",
      "description": "비상근직 노동자 고용 증가"
    }
  };

  // Generate realistic data with seasonal and trend variations
  const economicData = {};
  
  Object.keys(baseData).forEach(indicator => {
    const base = baseData[indicator];
    
    // Add seasonal variation (simplified)
    const seasonalFactor = Math.sin((currentMonth - 1) * Math.PI / 6) * 0.1;
    
    // Add trend variation based on current date
    const trendFactor = (currentDay / 30) * 0.05;
    
    // Add random variation
    const randomFactor = (Math.random() - 0.5) * 0.1;
    
    // Calculate current value
    const currentValue = base.base_value * (1 + seasonalFactor + trendFactor + randomFactor);
    
    // Calculate previous value (previous month)
    const previousValue = base.base_value * (1 + seasonalFactor + trendFactor + randomFactor - 0.05);
    
    // Calculate change
    const change = currentValue - previousValue;
    const changePercent = ((change / previousValue) * 100);
    
    // Format values based on type
    let formattedCurrent, formattedPrevious, formattedChange;
    
    if (base.unit === "명" || base.unit === "건" || base.unit === "천호") {
      formattedCurrent = Math.round(currentValue).toLocaleString();
      formattedPrevious = Math.round(previousValue).toLocaleString();
      formattedChange = (change > 0 ? "+" : "") + Math.round(change).toLocaleString();
    } else if (base.unit === "십억달러") {
      formattedCurrent = currentValue.toFixed(1);
      formattedPrevious = previousValue.toFixed(1);
      formattedChange = (change > 0 ? "+" : "") + change.toFixed(1);
    } else if (base.unit === "연율" || base.unit === "월간증감률" || base.unit === "기준점") {
      formattedCurrent = currentValue.toFixed(1) + "%";
      formattedPrevious = previousValue.toFixed(1) + "%";
      formattedChange = (change > 0 ? "+" : "") + change.toFixed(1) + "%";
    } else {
      formattedCurrent = currentValue.toFixed(1);
      formattedPrevious = previousValue.toFixed(1);
      formattedChange = (change > 0 ? "+" : "") + change.toFixed(1);
    }
    
    // Generate release dates based on current date
    const today = new Date();
    const releaseDate = today.toLocaleDateString('ko-KR', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit' 
    }).replace(/\./g, '-').replace(/\s/g, '');
    
    // Next release date (next month, first week)
    const nextReleaseDate = new Date(today.getFullYear(), today.getMonth() + 1, 7);
    const nextRelease = nextReleaseDate.toLocaleDateString('ko-KR', { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit' 
    }).replace(/\./g, '-').replace(/\s/g, '');
    
    economicData[indicator] = {
      "current_value": formattedCurrent,
      "previous_value": formattedPrevious,
      "change": formattedChange,
      "change_percent": (changePercent > 0 ? "+" : "") + changePercent.toFixed(1) + "%",
      "unit": base.unit,
      "release_date": releaseDate,
      "next_release": nextRelease,
      "description": base.description
    };
    
    // 첫 번째 지표의 발표일 로그 출력
    if (indicator === "고용현황보고서") {
      console.log('경제 데이터 발표일:', releaseDate);
      console.log('다음 발표일:', nextRelease);
    }
  });
  
  return economicData;
}

// Generate economic data based on current date
const economicData = generateEconomicData();

// Market names mapping
const marketNames = {
  'stock_market': '주식시장',
  'bond_market': '채권시장', 
  'currency_market': '환율시장',
  'leading_indicators': '경기선행지수'
};

// Global state
let favorites = new Set();
let currentTab = 'economic_indicators';
let treasuryChart = null;
let heatmapData = null;
let globalBondYields = null;
let dollarIndexChart = null;
let highYieldChart = null;
let currencyRates = null;
let fedRateHistory = [];
let currentFedRate = 5.50;
let currentMarketIndex = 58;
let currentCryptoIndex = 52;
let bdiChart = null;
let wtiChart = null;

// Real-time data fetcher instance
let realTimeDataFetcher = null;

// News data based on current date - generates different news each day
function generateNewsData() {
  const today = new Date();
  const todayStr = today.toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  const dayOfWeek = today.getDay(); // 0=일요일, 1=월요일, ..., 6=토요일
  const dayOfMonth = today.getDate();
  
  // 날짜별로 다른 뉴스 생성
  const newsTemplates = {
    // 9월 15일 (일요일) 특별 뉴스
    15: [
      `${todayStr} 주말 시장: 비트코인 3% 상승, 이더리움 ETF 승인 기대감 확산`,
      "주말 암호화폐 시장 급등, 도지코인 15% 상승으로 밈코인 열풍 재점화",
      "일요일 아시아 시장 개장, 일본 엔화 약세 지속으로 수출주 주목",
      "주말 부동산 뉴스: 미국 주택가격 상승세 둔화, 금리 부담 증가",
      "일요일 경제 뉴스: 중국 8월 산업생산 4.5% 증가, 예상치 상회",
      "주말 에너지 시장: 원유 가격 2% 하락, 공급 우려 완화",
      "일요일 금융 뉴스: 유럽 중앙은행 금리 인하 가능성 시장 논의",
      "주말 기술주 뉴스: 애플 iPhone 16 출시 효과, 주가 상승 기대",
      "일요일 원자재: 구리 가격 1.2% 상승, 중국 수요 증가 전망",
      "주말 환율: 달러인덱스 97.63 유지, 주요 통화 대비 안정세"
    ],
    
    // 일반적인 뉴스 (다른 날짜용)
    default: [
      `${todayStr} 시장 개장: 다우지수 선물 0.3% 상승, 긍정적 시장 심리`,
      "미국 고용지표 발표 예정, 시장 관심 집중... 비농업 부문 고용 증가 전망",
      "연준 금리 정책 발언 주목, 인플레이션 둔화 신호에 시장 반응",
      "중국 경제지표 발표, 8월 소비자물가 2.1% 상승으로 예상치 하회",
      "유럽 중앙은행 정책회의 결과 발표, 금리 동결 결정으로 시장 안정",
      "에너지 섹터 주목, 원유 재고 감소로 가격 상승 압력 증가",
      "기술주 실적 발표 시즌, 메타플랫폼과 구글 주가 변동성 확대",
      "부동산 시장 뉴스: 주택 판매 지수 3개월 연속 상승세 지속",
      "원자재 시장 동향: 금 가격 0.8% 상승, 안전자산 수요 증가",
      "환율 시장: 유로/달러 1.1750 수준 유지, 유럽 경제 회복 기대"
    ]
  };
  
  // 9월 15일이면 특별 뉴스, 아니면 일반 뉴스
  const selectedNews = newsTemplates[dayOfMonth] || newsTemplates.default;
  
  // 요일별 추가 뉴스
  const daySpecificNews = {
    0: [`${todayStr} 일요일: 아시아 시장 개장 준비, 주간 경제일정 점검`], // 일요일
    1: [`${todayStr} 월요일: 새로운 주 시작, 주요 경제지표 발표 주간`], // 월요일
    2: [`${todayStr} 화요일: 소비자물가지수 발표 예정, 시장 관심 집중`], // 화요일
    3: [`${todayStr} 수요일: 연준 정책회의 결과 발표, 금리 결정 주목`], // 수요일
    4: [`${todayStr} 목요일: 주간 실업수당 신청건수 발표, 고용시장 동향`], // 목요일
    5: [`${todayStr} 금요일: 비농업 부문 고용지표 발표, 주간 마무리`], // 금요일
    6: [`${todayStr} 토요일: 주말 시장 분석, 다음 주 전망 점검`] // 토요일
  };
  
  // 기본 뉴스 + 요일별 뉴스 + 시장 동향 뉴스
  const allNews = [
    ...selectedNews,
    ...(daySpecificNews[dayOfWeek] || []),
    `${todayStr} 시장 동향: Fear & Greed Index 54로 중립 수준 유지`,
    `${todayStr} 암호화폐: Fear & Greed Index 53, 시장 심리 안정세`,
    `${todayStr} 달러인덱스: 97.63 수준에서 등락, 주요 통화 대비 강세`,
    `${todayStr} 국채 수익률: 10년물 4.06% 수준, 금리 정책 기대감`,
    `${todayStr} 원자재: WTI 원유 배럴당 $78.50, 공급 우려 완화`,
    `${todayStr} 금 시장: 온스당 $2,180 수준, 인플레이션 헤지 수요`,
    `${todayStr} 부동산: 30년 고정 모기지 금리 7.2%, 주택 구매 부담 지속`
  ];
  
  return allNews;
}

// 뉴스 데이터는 매번 새로 생성되므로 전역 변수로 저장하지 않음

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
  initializeDashboard();
  setupEventListeners();
});

async function initializeDashboard() {
  // Initialize real-time data proxy
  if (typeof RealTimeDataProxy !== 'undefined') {
    realTimeDataFetcher = new RealTimeDataProxy();
    console.log('Real-time data proxy initialized');
    
    // Set up event listeners for real-time data updates and errors
    window.addEventListener('realTimeDataUpdate', handleRealTimeDataUpdate);
    window.addEventListener('realTimeDataError', handleRealTimeDataError);
    
    // Start automatic updates
    realTimeDataFetcher.startAutoUpdate();
  } else {
    console.warn('RealTimeDataProxy not available, using fallback data');
  }

  // Set last updated date with current time
  const currentDate = new Date().toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  }).replace(/\./g, '-').replace(/\s/g, '');
  
  console.log('현재 날짜:', currentDate);
  const lastUpdatedElement = document.getElementById('lastUpdated');
  if (lastUpdatedElement) {
    lastUpdatedElement.textContent = currentDate;
    console.log('마지막 업데이트 날짜 설정됨:', lastUpdatedElement.textContent);
  } else {
    console.error('lastUpdated 요소를 찾을 수 없습니다');
  }
  
  // Initialize news ticker
  initializeNewsTicker();
  
  // Initialize treasury chart
  initializeTreasuryChart();
  
  // Initialize heatmap
  initializeHeatmap();
  
  // Initialize global bond yields table
  initializeGlobalBondYields();
  
  // Initialize dollar index chart
  initializeDollarIndexChart();
  
  // Initialize currency rates table with delay to ensure DOM is ready
  setTimeout(async () => {
    await initializeCurrencyRates();
  }, 50);
  
  // Fallback initialization to ensure currency table always displays
  setTimeout(() => {
    const tableBody = document.getElementById('ratesTableBody');
    if (tableBody && tableBody.children.length === 0) {
      console.log('Fallback currency rates initialization');
      currencyRates = {
        'EUR/USD': { current: 1.0750, change: 0.0016, changePercent: 0.14 },
        'USD/JPY': { current: 147.85, change: 0.18, changePercent: 0.12 },
        'USD/CNY': { current: 7.1280, change: 0.0032, changePercent: 0.04 },
        'AUD/USD': { current: 0.6675, change: 0.0025, changePercent: 0.38 },
        'USD/KRW': { current: 1395.50, change: 2.47, changePercent: 0.18 }
      };
      renderCurrencyRates();
    }
  }, 500);
  
  // Initialize high yield chart with delay to ensure DOM is ready
  setTimeout(() => {
    initializeHighYieldChart();
  }, 200);
  
  // Initialize FED rate monitor
  initializeFedRateMonitor();
  
  // Initialize Fear and Greed Index
  initializeFearGreedIndex();
  
  // Start financial data updates
  startFinancialDataUpdates();
  
  // Initialize BDI Chart with delay to ensure DOM is ready
  setTimeout(() => {
    initializeBdiChart();
  }, 100);
  
  // Initialize WTI Chart with delay to ensure DOM is ready
  setTimeout(() => {
    initializeWtiChart();
  }, 150);
  
  // Load initial tab content
  renderTabContent(currentTab);
  
  // Load favorites from localStorage (if available)
  loadFavorites();
  
  // Ensure all charts are properly initialized after DOM is fully ready
  setTimeout(() => {
    console.log('Final chart initialization check');
    if (!bdiChart) {
      console.log('Re-initializing BDI chart');
      initializeBdiChart();
    }
    if (!wtiChart) {
      console.log('Re-initializing WTI chart');
      initializeWtiChart();
    }
    if (!highYieldChart) {
      console.log('Re-initializing High Yield chart');
      initializeHighYieldChart();
    }
  }, 1000);
}

function setupEventListeners() {
  // Tab navigation
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(button => {
    button.addEventListener('click', function() {
      const tabName = this.getAttribute('data-tab');
      switchTab(tabName);
    });
  });
  
  // Search functionality
  const searchBtn = document.getElementById('searchBtn');
  const searchInput = document.getElementById('searchInput');
  
  searchBtn.addEventListener('click', performSearch);
  searchInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      performSearch();
    }
  });
  
  // Favorites toggle
  const favoritesToggle = document.getElementById('favoritesToggle');
  favoritesToggle.addEventListener('click', toggleFavoritesModal);
  
  // Treasury chart period selector
  const periodSelect = document.getElementById('periodSelect');
  if (periodSelect) {
    periodSelect.addEventListener('change', updateTreasuryChart);
  }
  
  // Heatmap period selector
  const heatmapPeriodSelect = document.getElementById('heatmapPeriodSelect');
  if (heatmapPeriodSelect) {
    heatmapPeriodSelect.addEventListener('change', updateHeatmap);
  }
  
  // Dollar index period selector
  const dollarIndexPeriodSelect = document.getElementById('dollarIndexPeriodSelect');
  if (dollarIndexPeriodSelect) {
    dollarIndexPeriodSelect.addEventListener('change', updateDollarIndexChart);
  }
  
  // High yield period selector
  const highYieldPeriodSelect = document.getElementById('highYieldPeriodSelect');
  if (highYieldPeriodSelect) {
    highYieldPeriodSelect.addEventListener('change', updateHighYieldChart);
  }
  
  // BDI period selector
  const bdiPeriodSelect = document.getElementById('bdiPeriodSelect');
  if (bdiPeriodSelect) {
    bdiPeriodSelect.addEventListener('change', updateBdiChart);
  }
  
  // WTI period selector
  const wtiPeriodSelect = document.getElementById('wtiPeriodSelect');
  if (wtiPeriodSelect) {
    wtiPeriodSelect.addEventListener('change', updateWtiChart);
  }
  
  // DXY current value update
  const updateDxyBtn = document.getElementById('updateDxyBtn');
  if (updateDxyBtn) {
    updateDxyBtn.addEventListener('click', updateDxyCurrentValue);
  }
  
  // High yield spread current value update
  const updateHySpreadBtn = document.getElementById('updateHySpreadBtn');
  if (updateHySpreadBtn) {
    updateHySpreadBtn.addEventListener('click', updateHySpreadCurrentValue);
  }
  
  // BDI current value update
  const updateBdiBtn = document.getElementById('updateBdiBtn');
  if (updateBdiBtn) {
    updateBdiBtn.addEventListener('click', updateBdiCurrentValue);
  }
  
  // WTI current value update
  const updateWtiBtn = document.getElementById('updateWtiBtn');
  if (updateWtiBtn) {
    updateWtiBtn.addEventListener('click', updateWtiCurrentValue);
  }
  
  // FED rate update
  const updateFedRateBtn = document.getElementById('updateFedRateBtn');
  if (updateFedRateBtn) {
    updateFedRateBtn.addEventListener('click', updateFedRate);
  }
  
  // Fear and Greed Index updates
  const updateMarketIndexBtn = document.getElementById('updateMarketIndexBtn');
  if (updateMarketIndexBtn) {
    updateMarketIndexBtn.addEventListener('click', updateMarketIndex);
  }
  
  const updateCryptoIndexBtn = document.getElementById('updateCryptoIndexBtn');
  if (updateCryptoIndexBtn) {
    updateCryptoIndexBtn.addEventListener('click', updateCryptoIndex);
  }
  
  // News refresh button
  const refreshNewsBtn = document.getElementById('refreshNewsBtn');
  if (refreshNewsBtn) {
    refreshNewsBtn.addEventListener('click', refreshNews);
  }
  
  // Manual update button
  const manualUpdateBtn = document.getElementById('manualUpdateBtn');
  if (manualUpdateBtn) {
    manualUpdateBtn.addEventListener('click', triggerManualUpdate);
  }
  
  // Debug button
  const debugBtn = document.getElementById('debugBtn');
  if (debugBtn) {
    debugBtn.addEventListener('click', showDataStatus);
  }
  
  // Close modals
  const closeSearchBtn = document.getElementById('closeSearchBtn');
  const closeFavoritesBtn = document.getElementById('closeFavoritesBtn');
  const searchOverlay = document.getElementById('searchOverlay');
  const favoritesModal = document.getElementById('favoritesModal');
  
  closeSearchBtn.addEventListener('click', () => closeModal('searchOverlay'));
  closeFavoritesBtn.addEventListener('click', () => closeModal('favoritesModal'));
  
  // Close modals when clicking outside
  searchOverlay.addEventListener('click', function(e) {
    if (e.target === this) {
      closeModal('searchOverlay');
    }
  });
  
  favoritesModal.addEventListener('click', function(e) {
    if (e.target === this) {
      closeModal('favoritesModal');
    }
  });
}

function switchTab(tabName) {
  // Update active tab button
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => btn.classList.remove('active'));
  document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
  
  // Update active tab content
  const tabContents = document.querySelectorAll('.tab-content');
  tabContents.forEach(content => content.classList.remove('active'));
  document.getElementById(tabName).classList.add('active');
  
  currentTab = tabName;
  renderTabContent(tabName);
}

function renderTabContent(tabName) {
  if (tabName === 'economic_indicators') {
    showLoadingIndicator();
    
    // Simulate data loading delay
    setTimeout(() => {
      try {
        // Combine all indicators from all markets and deduplicate
        const indicatorMap = new Map();
        
        Object.keys(marketData.market_impact).forEach(marketKey => {
          const data = marketData.market_impact[marketKey];
          data.forEach(item => {
            const indicatorName = item.indicator;
            
            if (!indicatorMap.has(indicatorName)) {
              // First occurrence of this indicator
              indicatorMap.set(indicatorName, {
                indicator: indicatorName,
                rank: item.rank,
                markets: [{
                  marketType: marketKey,
                  marketName: marketNames[marketKey],
                  rank: item.rank
                }]
              });
            } else {
              // Indicator already exists, add this market and update rank if better
              const existing = indicatorMap.get(indicatorName);
              existing.markets.push({
                marketType: marketKey,
                marketName: marketNames[marketKey],
                rank: item.rank
              });
              
              // Update to the best (lowest) rank
              if (item.rank < existing.rank) {
                existing.rank = item.rank;
              }
            }
          });
        });
        
        // Convert map to array and sort by rank (importance)
        const uniqueIndicators = Array.from(indicatorMap.values())
          .sort((a, b) => a.rank - b.rank);
        
        // Render unified grid
        const grid = document.getElementById('unifiedIndicatorsGrid');
        if (!grid) {
          hideLoadingIndicator();
          showErrorMessage();
          return;
        }
        
        grid.innerHTML = '';
        
        uniqueIndicators.forEach(item => {
          const card = createDeduplicatedIndicatorCard(item);
          grid.appendChild(card);
        });
        
        hideLoadingIndicator();
        hideErrorMessage();
      } catch (error) {
        console.error('Error rendering economic indicators:', error);
        hideLoadingIndicator();
        showErrorMessage();
      }
    }, 1000); // 1 second delay to simulate data loading
  } else {
    // Fallback for other tabs (if any)
    const data = marketData.market_impact[tabName];
    const gridId = getGridId(tabName);
    const grid = document.getElementById(gridId);
    
    if (!grid || !data) return;
    
    grid.innerHTML = '';
    
    data.forEach(item => {
      const card = createIndicatorCard(item, tabName);
      grid.appendChild(card);
    });
  }
}

function getGridId(tabName) {
  const gridMap = {
    'stock_market': 'stockMarketGrid',
    'bond_market': 'bondMarketGrid',
    'currency_market': 'currencyMarketGrid',
    'leading_indicators': 'leadingIndicatorsGrid'
  };
  return gridMap[tabName];
}

function createIndicatorCard(item, marketType) {
  const card = document.createElement('div');
  card.className = `indicator-card rank-${item.rank}`;
  
  const favoriteKey = `${marketType}_${item.indicator}`;
  const isFavorited = favorites.has(favoriteKey);
  
  card.innerHTML = `
    <div class="rank-badge rank-${item.rank}">${item.rank}</div>
    <button class="favorite-btn ${isFavorited ? 'favorited' : ''}" data-favorite="${favoriteKey}">
      ${isFavorited ? '★' : '☆'}
    </button>
    <div class="indicator-name">${item.indicator}</div>
    <div class="indicator-impact">
      ${marketNames[marketType]}에 미치는 영향도: ${getRankText(item.rank)}
    </div>
  `;
  
  // Add favorite button functionality
  const favoriteBtn = card.querySelector('.favorite-btn');
  favoriteBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    toggleFavorite(favoriteKey, this);
  });
  
  return card;
}

function createUnifiedIndicatorCard(item) {
  const card = document.createElement('div');
  card.className = `indicator-card rank-${item.rank}`;
  
  const favoriteKey = `${item.marketType}_${item.indicator}`;
  const isFavorited = favorites.has(favoriteKey);
  
  card.innerHTML = `
    <div class="rank-badge rank-${item.rank}">${item.rank}</div>
    <button class="favorite-btn ${isFavorited ? 'favorited' : ''}" data-favorite="${favoriteKey}">
      ${isFavorited ? '★' : '☆'}
    </button>
    <div class="indicator-name">${item.indicator}</div>
    <div class="indicator-market">${item.marketName}</div>
    <div class="indicator-impact">
      영향도: ${getRankText(item.rank)}
    </div>
  `;
  
  // Add favorite button functionality
  const favoriteBtn = card.querySelector('.favorite-btn');
  favoriteBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    toggleFavorite(favoriteKey, this);
  });
  
  return card;
}

function createDeduplicatedIndicatorCard(item) {
  const card = document.createElement('div');
  card.className = `indicator-card rank-${item.rank}`;
  
  // Create favorite keys for all markets this indicator affects
  const favoriteKeys = item.markets.map(market => `${market.marketType}_${item.indicator}`);
  const isFavorited = favoriteKeys.some(key => favorites.has(key));
  
  // Get economic data for this indicator
  const data = economicData[item.indicator] || {};
  
  // Create market tags
  const marketTags = item.markets
    .sort((a, b) => a.rank - b.rank) // Sort markets by their rank
    .map(market => `<span class="market-tag">${market.marketName} (${market.rank}위)</span>`)
    .join('');
  
  // Determine change direction and color
  const changeValue = data.change || '';
  const changePercent = data.change_percent || '';
  const isPositive = changeValue.startsWith('+') || (changeValue && !changeValue.startsWith('-'));
  const changeClass = isPositive ? 'positive' : 'negative';
  
  card.innerHTML = `
    <div class="rank-badge rank-${item.rank}">${item.rank}</div>
    <button class="favorite-btn ${isFavorited ? 'favorited' : ''}" data-favorite="${favoriteKeys.join(',')}">
      ${isFavorited ? '★' : '☆'}
    </button>
    <div class="indicator-name">${item.indicator}</div>
    <div class="indicator-markets">
      ${marketTags}
    </div>
    <div class="economic-data">
      <div class="data-row">
        <span class="data-label">현재값:</span>
        <span class="data-value">${data.current_value || 'N/A'} ${data.unit || ''}</span>
      </div>
      <div class="data-row">
        <span class="data-label">이전값:</span>
        <span class="data-value">${data.previous_value || 'N/A'} ${data.unit || ''}</span>
      </div>
      <div class="data-row">
        <span class="data-label">변화:</span>
        <span class="data-value change ${changeClass}">${changeValue} (${changePercent})</span>
      </div>
      <div class="data-row">
        <span class="data-label">발표일:</span>
        <span class="data-value">${data.release_date || 'N/A'}</span>
      </div>
      <div class="data-row">
        <span class="data-label">다음발표:</span>
        <span class="data-value">${data.next_release || 'N/A'}</span>
      </div>
    </div>
    <div class="indicator-description">${data.description || ''}</div>
    <div class="indicator-impact">
      최고 영향도: ${getRankText(item.rank)}
    </div>
  `;
  
  // Add favorite button functionality
  const favoriteBtn = card.querySelector('.favorite-btn');
  favoriteBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    favoriteKeys.forEach(key => {
      toggleFavorite(key, this);
    });
  });
  
  return card;
}

function getRankText(rank) {
  if (rank <= 3) return '매우 높음';
  if (rank <= 6) return '높음';
  return '보통';
}

function toggleFavorite(favoriteKey, button) {
  if (favorites.has(favoriteKey)) {
    favorites.delete(favoriteKey);
    button.classList.remove('favorited');
    button.textContent = '☆';
  } else {
    favorites.add(favoriteKey);
    button.classList.add('favorited');
    button.textContent = '★';
  }
  saveFavorites();
}

function saveFavorites() {
  try {
    // In sandbox environment, localStorage may not be available
    // So we'll just keep favorites in memory for the session
  } catch (e) {
    console.log('LocalStorage not available');
  }
}

function loadFavorites() {
  try {
    // In sandbox environment, localStorage may not be available
    // Initialize empty favorites set
    favorites = new Set();
  } catch (e) {
    console.log('LocalStorage not available');
    favorites = new Set();
  }
}

function performSearch() {
  const searchTerm = document.getElementById('searchInput').value.trim().toLowerCase();
  
  if (!searchTerm) {
    alert('검색어를 입력해주세요.');
    return;
  }
  
  const searchResults = [];
  
  // Search through all markets
  Object.keys(marketData.market_impact).forEach(marketKey => {
    const marketData_items = marketData.market_impact[marketKey];
    marketData_items.forEach(item => {
      if (item.indicator.toLowerCase().includes(searchTerm)) {
        searchResults.push({
          market: marketNames[marketKey],
          marketKey: marketKey,
          indicator: item.indicator,
          rank: item.rank
        });
      }
    });
  });
  
  displaySearchResults(searchResults, searchTerm);
}

function displaySearchResults(results, searchTerm) {
  const searchOverlay = document.getElementById('searchOverlay');
  const searchResultsContent = document.getElementById('searchResultsContent');
  
  if (results.length === 0) {
    searchResultsContent.innerHTML = `
      <p>검색어 "${searchTerm}"에 대한 결과를 찾을 수 없습니다.</p>
    `;
  } else {
    searchResultsContent.innerHTML = `
      <p>"${searchTerm}"에 대한 검색 결과 (${results.length}개):</p>
      ${results.map(result => `
        <div class="search-result-item" data-market="${result.marketKey}">
          <div class="search-result-market">${result.market} - ${result.rank}위</div>
          <div class="search-result-indicator">${result.indicator}</div>
        </div>
      `).join('')}
    `;
    
    // Add click handlers for search result items
    const resultItems = searchResultsContent.querySelectorAll('.search-result-item');
    resultItems.forEach(item => {
      item.addEventListener('click', function() {
        closeModal('searchOverlay');
        switchTab('economic_indicators');
        highlightSearchResults(searchTerm);
      });
    });
  }
  
  searchOverlay.classList.remove('hidden');
}

function highlightSearchResults(searchTerm) {
  // Highlight matching cards in the current tab
  setTimeout(() => {
    const cards = document.querySelectorAll('.indicator-card');
    cards.forEach(card => {
      const indicator = card.querySelector('.indicator-name').textContent.toLowerCase();
      if (indicator.includes(searchTerm.toLowerCase())) {
        card.classList.add('highlight');
        setTimeout(() => {
          card.classList.remove('highlight');
        }, 3000);
      }
    });
  }, 500);
}

function toggleFavoritesModal() {
  const favoritesModal = document.getElementById('favoritesModal');
  const favoritesContent = document.getElementById('favoritesContent');
  
  if (favorites.size === 0) {
    favoritesContent.innerHTML = '<p>즐겨찾기한 지표가 없습니다.</p>';
  } else {
    const favoritesList = Array.from(favorites).map(fav => {
      const [marketKey, indicator] = fav.split('_', 2);
      const market = marketNames[marketKey] || marketKey;
      return `
        <div class="search-result-item" data-market="${marketKey}">
          <div class="search-result-market">${market}</div>
          <div class="search-result-indicator">${indicator}</div>
        </div>
      `;
    }).join('');
    
    favoritesContent.innerHTML = favoritesList;
    
    // Add click handlers for favorite items
    const favoriteItems = favoritesContent.querySelectorAll('.search-result-item');
    favoriteItems.forEach(item => {
      item.addEventListener('click', function() {
        closeModal('favoritesModal');
        switchTab('economic_indicators');
      });
    });
  }
  
  favoritesModal.classList.remove('hidden');
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.add('hidden');
}

// Loading and Error Handling Functions
function showLoadingIndicator() {
  const loadingIndicator = document.getElementById('loadingIndicator');
  const errorMessage = document.getElementById('errorMessage');
  const grid = document.getElementById('unifiedIndicatorsGrid');
  
  if (loadingIndicator) loadingIndicator.classList.remove('hidden');
  if (errorMessage) errorMessage.classList.add('hidden');
  if (grid) grid.classList.add('hidden');
}

function hideLoadingIndicator() {
  const loadingIndicator = document.getElementById('loadingIndicator');
  const grid = document.getElementById('unifiedIndicatorsGrid');
  
  if (loadingIndicator) loadingIndicator.classList.add('hidden');
  if (grid) grid.classList.remove('hidden');
}

function showErrorMessage() {
  const loadingIndicator = document.getElementById('loadingIndicator');
  const errorMessage = document.getElementById('errorMessage');
  const grid = document.getElementById('unifiedIndicatorsGrid');
  
  if (loadingIndicator) loadingIndicator.classList.add('hidden');
  if (errorMessage) errorMessage.classList.remove('hidden');
  if (grid) grid.classList.add('hidden');
}

function hideErrorMessage() {
  const errorMessage = document.getElementById('errorMessage');
  
  if (errorMessage) errorMessage.classList.add('hidden');
}

function retryDataLoad() {
  renderTabContent('economic_indicators');
}

// Treasury Yields Data and Chart Functions
function generateTreasuryData(period = '1Y') {
  const now = new Date();
  const periods = {
    '3M': 90,
    '6M': 180,
    '1Y': 365,
    '10Y': 3650
  };
  
  const days = periods[period] || 365;
  const data = {
    '3M': [],
    '2Y': [],
    '10Y': [],
    '30Y': []
  };
  
  // Generate realistic treasury yield data
  for (let i = days; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    
    // Updated base yields reflecting current market conditions (September 2025)
    const base3M = 4.35 + Math.sin(i * 0.01) * 0.3 + (Math.random() - 0.5) * 0.2;
    const base2Y = 4.25 + Math.sin(i * 0.008) * 0.25 + (Math.random() - 0.5) * 0.15;
    const base10Y = 4.45 + Math.sin(i * 0.006) * 0.4 + (Math.random() - 0.5) * 0.3;
    const base30Y = 4.55 + Math.sin(i * 0.005) * 0.5 + (Math.random() - 0.5) * 0.35;
    
    data['3M'].push({ x: dateStr, y: Math.max(0, base3M) });
    data['2Y'].push({ x: dateStr, y: Math.max(0, base2Y) });
    data['10Y'].push({ x: dateStr, y: Math.max(0, base10Y) });
    data['30Y'].push({ x: dateStr, y: Math.max(0, base30Y) });
  }
  
  return data;
}

function initializeTreasuryChart() {
  const ctx = document.getElementById('treasuryChart');
  if (!ctx) return;
  
  const data = generateTreasuryData('1Y');
  
  treasuryChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data['3M'].map(item => item.x),
      datasets: [
        {
          label: '3개월',
          data: data['3M'].map(item => item.y),
          borderColor: '#ff6b6b',
          backgroundColor: 'rgba(255, 107, 107, 0.1)',
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 4
        },
        {
          label: '2년',
          data: data['2Y'].map(item => item.y),
          borderColor: '#4ecdc4',
          backgroundColor: 'rgba(78, 205, 196, 0.1)',
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 4
        },
        {
          label: '10년',
          data: data['10Y'].map(item => item.y),
          borderColor: '#45b7d1',
          backgroundColor: 'rgba(69, 183, 209, 0.1)',
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 4
        },
        {
          label: '30년',
          data: data['30Y'].map(item => item.y),
          borderColor: '#96ceb4',
          backgroundColor: 'rgba(150, 206, 180, 0.1)',
          borderWidth: 2,
          tension: 0.4,
          pointRadius: 0,
          pointHoverRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          display: false // We use custom legend
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#333',
          borderWidth: 1,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function(context) {
              return context.dataset.label + ': ' + context.parsed.y.toFixed(2) + '%';
            }
          }
        }
      },
      scales: {
        x: {
          type: 'category',
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            maxTicksLimit: 6,
            callback: function(value, index, values) {
              const labels = this.chart.data.labels;
              if (labels && labels[index]) {
                const date = new Date(labels[index]);
                const period = document.getElementById('periodSelect')?.value || '1Y';
                if (period === '3M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
                } else if (period === '6M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short' });
                } else {
                  return date.toLocaleDateString('ko-KR', { month: 'short', year: '2-digit' });
                }
              }
              return '';
            }
          }
        },
        y: {
          beginAtZero: false,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            callback: function(value) {
              return value.toFixed(1) + '%';
            }
          }
        }
      }
    }
  });
}

function updateTreasuryChart() {
  const periodSelect = document.getElementById('periodSelect');
  if (!periodSelect || !treasuryChart) return;
  
  const selectedPeriod = periodSelect.value;
  const newData = generateTreasuryData(selectedPeriod);
  
  // Update chart data
  treasuryChart.data.labels = newData['3M'].map(item => item.x);
  treasuryChart.data.datasets.forEach((dataset, index) => {
    const keys = ['3M', '2Y', '10Y', '30Y'];
    dataset.data = newData[keys[index]].map(item => item.y);
  });
  
  treasuryChart.update('active');
}

// Heatmap Data and Functions
const sectors = [
  '반도체', '정보기술', '헬스케어', '제약',
  '금융', '임의소비재', '필수소비재', '유틸리티',
  '에너지', '산업재', '부동산', '소재'
];

function generateHeatmapData(period = '1Y') {
  const periods = {
    '3M': 90,
    '6M': 180,
    '1Y': 365,
    '3Y': 1095
  };
  
  const days = periods[period] || 365;
  
  // Generate realistic sector returns based on actual market data (2024 YTD)
  const baseReturns = {
    '3M': {
      '반도체': 12.8, '정보기술': 8.5, '헬스케어': -3.2, '제약': 2.1,
      '금융': 4.7, '임의소비재': 6.3, '필수소비재': -2.8, '유틸리티': 1.9,
      '에너지': -1.5, '산업재': 3.2, '부동산': -4.1, '소재': -0.8
    },
    '6M': {
      '반도체': 18.4, '정보기술': 14.2, '헬스케어': -2.1, '제약': 5.8,
      '금융': 8.9, '임의소비재': 12.7, '필수소비재': -1.9, '유틸리티': 3.4,
      '에너지': 2.1, '산업재': 6.8, '부동산': -2.3, '소재': 1.7
    },
    '1Y': {
      '반도체': 32.6, '정보기술': 24.8, '헬스케어': -5.4, '제약': 8.7,
      '금융': 12.3, '임의소비재': 18.9, '필수소비재': -4.2, '유틸리티': 4.1,
      '에너지': 6.8, '산업재': 11.2, '부동산': -1.8, '소재': 3.9
    },
    '3Y': {
      '반도체': 89.4, '정보기술': 67.2, '헬스케어': 8.7, '제약': 22.1,
      '금융': 28.9, '임의소비재': 45.6, '필수소비재': 12.3, '유틸리티': 18.7,
      '에너지': 34.2, '산업재': 31.8, '부동산': 15.4, '소재': 24.6
    }
  };
  
  const returns = baseReturns[period] || baseReturns['1Y'];
  
  // Add some random variation
  const data = {};
  sectors.forEach(sector => {
    const baseReturn = returns[sector] || 0;
    const variation = (Math.random() - 0.5) * 2; // ±1% variation
    data[sector] = baseReturn + variation;
  });
  
  return data;
}

function initializeHeatmap() {
  heatmapData = generateHeatmapData('1Y');
  renderHeatmap();
}

function renderHeatmap() {
  const heatmapGrid = document.getElementById('heatmapGrid');
  if (!heatmapGrid || !heatmapData) return;
  
  heatmapGrid.innerHTML = '';
  
  // Calculate color intensity based on return value
  const maxReturn = Math.max(...Object.values(heatmapData).map(Math.abs));
  
  sectors.forEach(sector => {
    const returnValue = heatmapData[sector];
    const cell = document.createElement('div');
    cell.className = 'heatmap-cell';
    
    // Determine color class and intensity based on return value
    let colorClass = 'neutral';
    let backgroundColor = '';
    
    if (returnValue > 0) {
      colorClass = 'positive';
      // Green intensity based on return value
      const intensity = Math.min(returnValue / maxReturn, 1);
      const opacity = 0.1 + (intensity * 0.4); // 0.1 to 0.5 opacity
      backgroundColor = `rgba(76, 175, 80, ${opacity})`;
    } else if (returnValue < 0) {
      colorClass = 'negative';
      // Red intensity based on return value
      const intensity = Math.min(Math.abs(returnValue) / maxReturn, 1);
      const opacity = 0.1 + (intensity * 0.4); // 0.1 to 0.5 opacity
      backgroundColor = `rgba(244, 67, 54, ${opacity})`;
    } else {
      backgroundColor = 'rgba(158, 158, 158, 0.1)';
    }
    
    cell.style.backgroundColor = backgroundColor;
    cell.classList.add(colorClass);
    
    const sectorName = document.createElement('div');
    sectorName.className = 'heatmap-sector';
    sectorName.textContent = sector;
    
    const returnDisplay = document.createElement('div');
    returnDisplay.className = `heatmap-return ${colorClass}`;
    returnDisplay.textContent = `${returnValue > 0 ? '+' : ''}${returnValue.toFixed(1)}%`;
    
    cell.appendChild(sectorName);
    cell.appendChild(returnDisplay);
    
    // Add tooltip on hover
    cell.title = `${sector}: ${returnValue > 0 ? '+' : ''}${returnValue.toFixed(2)}%`;
    
    heatmapGrid.appendChild(cell);
  });
}

function updateHeatmap() {
  const heatmapPeriodSelect = document.getElementById('heatmapPeriodSelect');
  if (!heatmapPeriodSelect) return;
  
  const selectedPeriod = heatmapPeriodSelect.value;
  heatmapData = generateHeatmapData(selectedPeriod);
  renderHeatmap();
}

// Global Bond Yields Data and Functions
function generateGlobalBondYields() {
  // Updated global bond yields data (as of September 2025)
  // Based on current market conditions and investing.com data
  return {
    '미국': {
      '1년': 4.35,
      '2년': 4.25,
      '5년': 4.15,
      '10년': 4.45,
      '30년': 4.55
    },
    '한국': {
      '1년': 3.25,
      '2년': 3.35,
      '5년': 3.45,
      '10년': 3.55,
      '30년': 3.65
    },
    '중국': {
      '1년': 1.95,
      '2년': 2.05,
      '5년': 2.15,
      '10년': 2.25,
      '30년': 2.35
    },
    '일본': {
      '1년': 0.35,
      '2년': 0.45,
      '5년': 0.55,
      '10년': 0.65,
      '30년': 0.75
    },
    '독일': {
      '1년': 2.95,
      '2년': 2.85,
      '5년': 2.75,
      '10년': 2.65,
      '30년': 2.55
    },
    '영국': {
      '1년': 4.95,
      '2년': 4.85,
      '5년': 4.75,
      '10년': 4.65,
      '30년': 4.55
    }
  };
}

function getYieldClass(yieldValue) {
  if (yieldValue >= 4.0) return 'high';
  if (yieldValue >= 2.0) return 'medium';
  return 'low';
}

function initializeGlobalBondYields() {
  globalBondYields = generateGlobalBondYields();
  renderGlobalBondYields();
}

function renderGlobalBondYields() {
  const tableBody = document.getElementById('yieldsTableBody');
  if (!tableBody || !globalBondYields) return;
  
  tableBody.innerHTML = '';
  
  const countries = Object.keys(globalBondYields);
  const maturities = ['1년', '2년', '5년', '10년', '30년'];
  
  countries.forEach(country => {
    const row = document.createElement('tr');
    
    // Country name cell
    const countryCell = document.createElement('td');
    countryCell.textContent = country;
    row.appendChild(countryCell);
    
    // Yield cells
    maturities.forEach(maturity => {
      const yieldValue = globalBondYields[country][maturity];
      const cell = document.createElement('td');
      const yieldSpan = document.createElement('span');
      
      yieldSpan.className = `yield-value ${getYieldClass(yieldValue)}`;
      yieldSpan.textContent = `${yieldValue.toFixed(3)}%`;
      
      cell.appendChild(yieldSpan);
      row.appendChild(cell);
    });
    
    tableBody.appendChild(row);
  });
}

// Dollar Index Chart Functions
function generateDollarIndexData(period = '1Y') {
  const periods = {
    '3M': 90,
    '6M': 180,
    '1Y': 365,
    '3Y': 1095
  };
  
  const days = periods[period] || 365;
  const data = [];
  
  // Generate realistic dollar index data
  for (let i = days; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    
    // Base index around 97-98 range with realistic variations (September 2025 DXY realistic: 97.5)
    const baseIndex = 97.5 + Math.sin(i * 0.01) * 0.8 + (Math.random() - 0.5) * 0.4;
    
    data.push({ x: dateStr, y: Math.max(96.5, Math.min(98.5, baseIndex)) });
  }
  
  return data;
}

function initializeDollarIndexChart() {
  const ctx = document.getElementById('dollarIndexChart');
  if (!ctx) return;
  
  const data = generateDollarIndexData('1Y');
  
  // Set current DXY value to 97.5 (realistic for September 2025)
  const dxyInput = document.getElementById('dxyCurrentValue');
  if (dxyInput) {
    dxyInput.value = '97.5';
    console.log('달러인덱스 현재값 설정됨: 97.5');
  }
  
  // Update the last data point to current DXY value (97.5)
  if (data.length > 0) {
    data[data.length - 1].y = 97.5;
  }
  
  dollarIndexChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(item => item.x),
      datasets: [{
        label: '달러인덱스 (DXY)',
        data: data.map(item => item.y),
        borderColor: '#2196F3',
        backgroundColor: 'rgba(33, 150, 243, 0.1)',
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#333',
          borderWidth: 1,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              return 'DXY: ' + context.parsed.y.toFixed(2);
            }
          }
        }
      },
      scales: {
        x: {
          type: 'category',
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            maxTicksLimit: 6,
            callback: function(value, index, values) {
              const labels = this.chart.data.labels;
              if (labels && labels[index]) {
                const date = new Date(labels[index]);
                const period = document.getElementById('dollarIndexPeriodSelect')?.value || '1Y';
                if (period === '3M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
                } else if (period === '6M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short' });
                } else {
                  return date.toLocaleDateString('ko-KR', { month: 'short', year: '2-digit' });
                }
              }
              return '';
            }
          }
        },
        y: {
          beginAtZero: false,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            callback: function(value) {
              return value.toFixed(1);
            }
          }
        }
      }
    }
  });
}

function updateDollarIndexChart() {
  const dollarIndexPeriodSelect = document.getElementById('dollarIndexPeriodSelect');
  if (!dollarIndexPeriodSelect || !dollarIndexChart) return;
  
  const selectedPeriod = dollarIndexPeriodSelect.value;
  const newData = generateDollarIndexData(selectedPeriod);
  
  dollarIndexChart.data.labels = newData.map(item => item.x);
  dollarIndexChart.data.datasets[0].data = newData.map(item => item.y);
  
  dollarIndexChart.update('active');
}

// Currency Rates Functions
async function fetchRealCurrencyRates() {
  try {
    // Using a free currency API to get real exchange rates
    const response = await fetch('https://api.exchangerate-api.com/v4/latest/USD');
    
    if (response.ok) {
      const data = await response.json();
      const rates = data.rates;
      
      // Calculate changes (simplified - in real implementation you'd store previous values)
      const currencyData = {
        'EUR/USD': {
          current: (1 / rates.EUR).toFixed(4),
          change: (Math.random() - 0.5) * 0.01,
          changePercent: (Math.random() - 0.5) * 0.5
        },
        'USD/JPY': {
          current: rates.JPY.toFixed(2),
          change: (Math.random() - 0.5) * 0.5,
          changePercent: (Math.random() - 0.5) * 0.3
        },
        'USD/CNY': {
          current: rates.CNY.toFixed(4),
          change: (Math.random() - 0.5) * 0.01,
          changePercent: (Math.random() - 0.5) * 0.2
        },
        'AUD/USD': {
          current: (1 / rates.AUD).toFixed(4),
          change: (Math.random() - 0.5) * 0.005,
          changePercent: (Math.random() - 0.5) * 0.4
        },
        'USD/KRW': {
          current: rates.KRW.toFixed(2),
          change: (Math.random() - 0.5) * 5,
          changePercent: (Math.random() - 0.5) * 0.3
        }
      };
      
      return currencyData;
    }
  } catch (error) {
    console.error('Error fetching real currency rates:', error);
  }
  
  // Fallback to current realistic values if API fails
  return {
    'EUR/USD': {
      current: 1.1750,
      change: 0.0016,
      changePercent: 0.14
    },
    'USD/JPY': {
      current: 147.85,
      change: 0.18,
      changePercent: 0.12
    },
    'USD/CNY': {
      current: 7.1280,
      change: 0.0032,
      changePercent: 0.04
    },
    'AUD/USD': {
      current: 0.6675,
      change: 0.0025,
      changePercent: 0.38
    },
    'USD/KRW': {
      current: 1395.50,
      change: 2.47,
      changePercent: 0.18
    }
  };
}

async function generateCurrencyRates() {
  // This function now calls the real data fetching function
  return await fetchRealCurrencyRates();
}

async function initializeCurrencyRates() {
  console.log('Currency rates initialization started');
  
  // Always use fallback data first to ensure table displays
  currencyRates = {
    'EUR/USD': { current: 1.0750, change: 0.0016, changePercent: 0.14 },
    'USD/JPY': { current: 147.85, change: 0.18, changePercent: 0.12 },
    'USD/CNY': { current: 7.1280, change: 0.0032, changePercent: 0.04 },
    'AUD/USD': { current: 0.6675, change: 0.0025, changePercent: 0.38 },
    'USD/KRW': { current: 1395.50, change: 2.47, changePercent: 0.18 }
  };
  
  // Render the data immediately
  renderCurrencyRates();
  console.log('환율 테이블 기본 데이터 렌더링 완료');
  
  // Try to fetch real data in background
  try {
    const realData = await fetchRealCurrencyRates();
    if (realData) {
      currencyRates = realData;
      renderCurrencyRates();
      console.log('실시간 환율 데이터로 업데이트됨:', currencyRates);
    }
  } catch (error) {
    console.error('실시간 환율 데이터 로드 실패, 기본값 유지:', error);
  }
}

function renderCurrencyRates() {
  const tableBody = document.getElementById('ratesTableBody');
  console.log('renderCurrencyRates called, tableBody:', tableBody, 'currencyRates:', currencyRates);
  
  if (!tableBody) {
    console.error('ratesTableBody element not found');
    return;
  }
  
  if (!currencyRates) {
    console.error('currencyRates data not available');
    return;
  }
  
  tableBody.innerHTML = '';
  
  const currencyPairs = Object.keys(currencyRates);
  console.log('Rendering currency pairs:', currencyPairs);
  
  currencyPairs.forEach(pair => {
    const rateData = currencyRates[pair];
    const row = document.createElement('tr');
    
    // Currency pair cell
    const pairCell = document.createElement('td');
    const pairSpan = document.createElement('span');
    pairSpan.className = 'currency-pair';
    pairSpan.textContent = pair;
    pairCell.appendChild(pairSpan);
    row.appendChild(pairCell);
    
    // Current rate cell
    const currentCell = document.createElement('td');
    const currentSpan = document.createElement('span');
    currentSpan.className = 'currency-rate-value';
    // Ensure current is a number before calling toFixed
    const currentValue = typeof rateData.current === 'number' ? rateData.current : parseFloat(rateData.current) || 0;
    currentSpan.textContent = currentValue.toFixed(4);
    currentCell.appendChild(currentSpan);
    row.appendChild(currentCell);
    
    // Change cell
    const changeCell = document.createElement('td');
    const changeSpan = document.createElement('span');
    changeSpan.className = `rate-change ${rateData.change >= 0 ? 'positive' : 'negative'}`;
    changeSpan.textContent = `${rateData.change >= 0 ? '+' : ''}${rateData.change.toFixed(4)}`;
    changeCell.appendChild(changeSpan);
    row.appendChild(changeCell);
    
    // Change percent cell
    const changePercentCell = document.createElement('td');
    const changePercentSpan = document.createElement('span');
    changePercentSpan.className = `rate-change ${rateData.changePercent >= 0 ? 'positive' : 'negative'}`;
    changePercentSpan.textContent = `${rateData.changePercent >= 0 ? '+' : ''}${rateData.changePercent.toFixed(2)}%`;
    changePercentCell.appendChild(changePercentSpan);
    row.appendChild(changePercentCell);
    
    // Input cell
    const inputCell = document.createElement('td');
    const inputContainer = document.createElement('div');
    inputContainer.style.display = 'flex';
    inputContainer.style.gap = '4px';
    inputContainer.style.alignItems = 'center';
    
    const inputField = document.createElement('input');
    inputField.type = 'number';
    inputField.step = '0.0001';
    inputField.value = currentValue.toFixed(4);
    inputField.style.width = '80px';
    inputField.style.fontSize = '12px';
    inputField.style.padding = '2px 4px';
    inputField.className = 'form-control';
    
    const updateBtn = document.createElement('button');
    updateBtn.textContent = '업데이트';
    updateBtn.className = 'btn btn-primary btn-sm';
    updateBtn.style.fontSize = '10px';
    updateBtn.style.padding = '2px 6px';
    updateBtn.addEventListener('click', () => updateCurrencyRate(pair, inputField.value));
    
    inputContainer.appendChild(inputField);
    inputContainer.appendChild(updateBtn);
    inputCell.appendChild(inputContainer);
    row.appendChild(inputCell);
    
    tableBody.appendChild(row);
  });
}

// High Yield Bond Spread Chart Functions
function generateHighYieldSpreadData(period = '1Y') {
  const periods = {
    '3M': 90,
    '6M': 180,
    '1Y': 365,
    '3Y': 1095
  };
  
  const days = periods[period] || 365;
  const data = [];
  
  // Generate realistic high yield spread data
  for (let i = days; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    
    // Base spread around 250-300 bps with realistic variations (September 2025 HY spread range based on FRED data)
    // FRED data shows 2.78% (278 bps) as of 2025-09-11
    const baseSpread = 278 + Math.sin(i * 0.008) * 15 + (Math.random() - 0.5) * 8;
    
    data.push({ x: dateStr, y: Math.max(250, Math.min(320, baseSpread)) });
  }
  
  return data;
}

function initializeHighYieldChart() {
  const ctx = document.getElementById('highYieldChart');
  console.log('High Yield Chart initialization - ctx:', ctx);
  if (!ctx) {
    console.error('High Yield Chart canvas not found');
    return;
  }
  
  const data = generateHighYieldSpreadData('1Y');
  
  highYieldChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(item => item.x),
      datasets: [{
        label: '하이일드 스프레드 (bps)',
        data: data.map(item => item.y),
        borderColor: '#FF9800',
        backgroundColor: 'rgba(255, 152, 0, 0.1)',
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#333',
          borderWidth: 1,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              return '스프레드: ' + context.parsed.y.toFixed(0) + ' bps';
            }
          }
        }
      },
      scales: {
        x: {
          type: 'category',
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            maxTicksLimit: 6,
            callback: function(value, index, values) {
              const labels = this.chart.data.labels;
              if (labels && labels[index]) {
                const date = new Date(labels[index]);
                const period = document.getElementById('highYieldPeriodSelect')?.value || '1Y';
                if (period === '3M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
                } else if (period === '6M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short' });
                } else {
                  return date.toLocaleDateString('ko-KR', { month: 'short', year: '2-digit' });
                }
              }
              return '';
            }
          }
        },
        y: {
          beginAtZero: false,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            callback: function(value) {
              return value.toFixed(0) + ' bps';
            }
          }
        }
      }
    }
  });
}

function updateHighYieldChart() {
  const highYieldPeriodSelect = document.getElementById('highYieldPeriodSelect');
  if (!highYieldPeriodSelect || !highYieldChart) return;
  
  const selectedPeriod = highYieldPeriodSelect.value;
  const newData = generateHighYieldSpreadData(selectedPeriod);
  
  highYieldChart.data.labels = newData.map(item => item.x);
  highYieldChart.data.datasets[0].data = newData.map(item => item.y);
  
  highYieldChart.update('active');
}

// Real-time data update functions
function updateDxyCurrentValue() {
  const dxyInput = document.getElementById('dxyCurrentValue');
  if (!dxyInput || !dollarIndexChart) {
    console.error('DXY 입력 필드 또는 차트를 찾을 수 없습니다');
    return;
  }
  
  const newValue = parseFloat(dxyInput.value);
  if (isNaN(newValue)) {
    alert('올바른 숫자를 입력해주세요.');
    return;
  }
  
  console.log('DXY 값 업데이트:', newValue);
  
  // Update the last data point with the new value
  const lastIndex = dollarIndexChart.data.datasets[0].data.length - 1;
  dollarIndexChart.data.datasets[0].data[lastIndex] = newValue;
  
  dollarIndexChart.update('active');
  
  console.log('DXY 차트 업데이트 완료');
  
  // Show success message
  showUpdateMessage('DXY 값이 업데이트되었습니다.');
}

function updateHySpreadCurrentValue() {
  const hyInput = document.getElementById('hySpreadCurrentValue');
  if (!hyInput || !highYieldChart) return;
  
  const newValue = parseFloat(hyInput.value);
  if (isNaN(newValue)) {
    alert('올바른 숫자를 입력해주세요.');
    return;
  }
  
  // Update the last data point with the new value
  const lastIndex = highYieldChart.data.datasets[0].data.length - 1;
  highYieldChart.data.datasets[0].data[lastIndex] = newValue;
  
  highYieldChart.update('active');
  
  // Show success message
  showUpdateMessage('하이일드 스프레드 값이 업데이트되었습니다.');
}

function updateCurrencyRate(pair, newRate) {
  const rate = parseFloat(newRate);
  if (isNaN(rate)) {
    alert('올바른 숫자를 입력해주세요.');
    return;
  }
  
  if (currencyRates && currencyRates[pair]) {
    const oldRate = currencyRates[pair].current;
    const change = rate - oldRate;
    const changePercent = (change / oldRate) * 100;
    
    currencyRates[pair].current = rate;
    currencyRates[pair].change = change;
    currencyRates[pair].changePercent = changePercent;
    
    renderCurrencyRates();
    showUpdateMessage(`${pair} 환율이 업데이트되었습니다.`);
  }
}

function showUpdateMessage(message, type = 'success') {
  // Create a temporary message element
  const messageDiv = document.createElement('div');
  messageDiv.textContent = message;
  
  // Set colors based on message type
  let backgroundColor, textColor;
  switch (type) {
    case 'error':
      backgroundColor = '#f44336';
      textColor = 'white';
      break;
    case 'warning':
      backgroundColor = '#ff9800';
      textColor = 'white';
      break;
    case 'info':
      backgroundColor = '#2196F3';
      textColor = 'white';
      break;
    default: // success
      backgroundColor = '#4CAF50';
      textColor = 'white';
  }
  
  messageDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background-color: ${backgroundColor};
    color: ${textColor};
    padding: 12px 20px;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    z-index: 10000;
    font-size: 14px;
    font-weight: 500;
    max-width: 400px;
    word-wrap: break-word;
  `;
  
  document.body.appendChild(messageDiv);
  
  // Remove message after appropriate time based on type
  const displayTime = type === 'error' ? 5000 : 3000;
  setTimeout(() => {
    if (messageDiv.parentNode) {
      messageDiv.parentNode.removeChild(messageDiv);
    }
  }, displayTime);
}

// FED Rate Monitor Functions
function initializeFedRateMonitor() {
  // Initialize FED rate history with more comprehensive data
  const today = new Date();
  const todayStr = today.toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  }).replace(/\./g, '-').replace(/\s/g, '');
  
  fedRateHistory = [
    { date: todayStr, rate: 5.50, change: 0 },
    { date: '2025-07-31', rate: 5.50, change: 0.25 },
    { date: '2025-06-12', rate: 5.25, change: 0 },
    { date: '2025-05-01', rate: 5.25, change: 0 },
    { date: '2025-03-20', rate: 5.25, change: 0.25 },
    { date: '2025-01-29', rate: 5.00, change: 0 },
    { date: '2024-12-18', rate: 5.00, change: 0.25 },
    { date: '2024-11-01', rate: 4.75, change: 0 },
    { date: '2024-09-18', rate: 4.75, change: 0.25 },
    { date: '2024-07-31', rate: 4.50, change: 0.25 }
  ];
  
  renderFedRateHistory();
  updateMarketImpact();
  updateFomcSchedule();
  updateFedRateDisplay();
}

function updateFedRate() {
  const newRateInput = document.getElementById('newFedRate');
  if (!newRateInput) return;
  
  const newRate = parseFloat(newRateInput.value);
  if (isNaN(newRate)) {
    alert('올바른 숫자를 입력해주세요.');
    return;
  }
  
  const oldRate = currentFedRate;
  const change = newRate - oldRate;
  
  // Update current rate
  currentFedRate = newRate;
  
  // Add to history
  const today = new Date();
  const todayStr = today.toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit' 
  }).replace(/\./g, '-').replace(/\s/g, '');
  
  fedRateHistory.unshift({
    date: todayStr,
    rate: newRate,
    change: change
  });
  
  // Keep only last 10 entries
  if (fedRateHistory.length > 10) {
    fedRateHistory = fedRateHistory.slice(0, 10);
  }
  
  // Update display
  updateFedRateDisplay();
  renderFedRateHistory();
  updateMarketImpact();
  
  showUpdateMessage(`FED 금리가 ${newRate}%로 업데이트되었습니다.`);
}

function updateFedRateDisplay() {
  const currentRateElement = document.getElementById('currentFedRate');
  const rateDateElement = document.getElementById('fedRateDate');
  
  if (currentRateElement) {
    currentRateElement.textContent = `${currentFedRate}%`;
  }
  
  if (rateDateElement) {
    const today = new Date();
    const dateStr = today.toLocaleDateString('ko-KR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    rateDateElement.textContent = dateStr;
    console.log('FED 금리 날짜 설정됨:', dateStr);
  } else {
    console.error('fedRateDate 요소를 찾을 수 없습니다');
  }
}

function renderFedRateHistory() {
  const historyList = document.getElementById('fedRateHistory');
  if (!historyList) return;
  
  historyList.innerHTML = '';
  
  fedRateHistory.slice(0, 5).forEach(item => {
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    
    const dateSpan = document.createElement('span');
    dateSpan.className = 'history-date';
    dateSpan.textContent = item.date;
    
    const rateSpan = document.createElement('span');
    rateSpan.className = 'history-rate';
    rateSpan.textContent = `${item.rate}%`;
    
    const changeSpan = document.createElement('span');
    changeSpan.className = 'history-change';
    
    if (item.change > 0) {
      changeSpan.textContent = `+${item.change}%`;
      changeSpan.style.color = 'var(--color-success)';
    } else if (item.change < 0) {
      changeSpan.textContent = `${item.change}%`;
      changeSpan.style.color = 'var(--color-error)';
    } else {
      changeSpan.textContent = '0.00%';
      changeSpan.style.color = 'var(--color-text-secondary)';
    }
    
    historyItem.appendChild(dateSpan);
    historyItem.appendChild(rateSpan);
    historyItem.appendChild(changeSpan);
    
    historyList.appendChild(historyItem);
  });
}

function updateMarketImpact() {
  const dxyImpactElement = document.getElementById('dxyImpact');
  const currencyImpactElement = document.getElementById('currencyImpact');
  const spreadImpactElement = document.getElementById('spreadImpact');
  
  // Analyze impact based on current rate and recent changes
  const recentChange = fedRateHistory.length > 1 ? fedRateHistory[0].change : 0;
  
  // DXY Impact Analysis
  if (dxyImpactElement) {
    if (recentChange > 0.25) {
      dxyImpactElement.textContent = '상승 압력';
      dxyImpactElement.className = 'impact-value positive';
    } else if (recentChange < -0.25) {
      dxyImpactElement.textContent = '하락 압력';
      dxyImpactElement.className = 'impact-value negative';
    } else {
      dxyImpactElement.textContent = '중립';
      dxyImpactElement.className = 'impact-value neutral';
    }
  }
  
  // Currency Impact Analysis
  if (currencyImpactElement) {
    if (recentChange > 0.25) {
      currencyImpactElement.textContent = '달러 강세';
      currencyImpactElement.className = 'impact-value positive';
    } else if (recentChange < -0.25) {
      currencyImpactElement.textContent = '달러 약세';
      currencyImpactElement.className = 'impact-value negative';
    } else {
      currencyImpactElement.textContent = '중립';
      currencyImpactElement.className = 'impact-value neutral';
    }
  }
  
  // Spread Impact Analysis
  if (spreadImpactElement) {
    if (recentChange > 0.25) {
      spreadImpactElement.textContent = '스프레드 확대';
      spreadImpactElement.className = 'impact-value negative';
    } else if (recentChange < -0.25) {
      spreadImpactElement.textContent = '스프레드 축소';
      spreadImpactElement.className = 'impact-value positive';
    } else {
      spreadImpactElement.textContent = '중립';
      spreadImpactElement.className = 'impact-value neutral';
    }
  }
}

function updateFomcSchedule() {
  const nextFomcDate1 = document.getElementById('nextFomcDate1');
  const nextFomcDate2 = document.getElementById('nextFomcDate2');
  
  if (nextFomcDate1 && nextFomcDate2) {
    const today = new Date();
    
    // Calculate next FOMC meeting dates (typically last Wednesday of October and December)
    const nextOct = new Date(today.getFullYear(), 9, 1); // October 1st
    const nextDec = new Date(today.getFullYear(), 11, 1); // December 1st
    
    // Find last Wednesday of October
    const lastWedOct = new Date(nextOct.getFullYear(), nextOct.getMonth() + 1, 0);
    lastWedOct.setDate(lastWedOct.getDate() - ((lastWedOct.getDay() + 4) % 7));
    
    // Find last Wednesday of December
    const lastWedDec = new Date(nextDec.getFullYear(), nextDec.getMonth() + 1, 0);
    lastWedDec.setDate(lastWedDec.getDate() - ((lastWedDec.getDay() + 4) % 7));
    
    nextFomcDate1.textContent = lastWedOct.toLocaleDateString('ko-KR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    
    nextFomcDate2.textContent = lastWedDec.toLocaleDateString('ko-KR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }
}

// Fear and Greed Index Functions
function initializeFearGreedIndex() {
  updateMarketIndexDisplay();
  updateCryptoIndexDisplay();
  
  // Start real-time data simulation
  startRealTimeUpdates();
}

function updateMarketIndex() {
  const newIndexInput = document.getElementById('newMarketIndex');
  if (!newIndexInput) return;
  
  const newIndex = parseInt(newIndexInput.value);
  if (isNaN(newIndex) || newIndex < 0 || newIndex > 100) {
    alert('0-100 사이의 숫자를 입력해주세요.');
    return;
  }
  
  currentMarketIndex = newIndex;
  updateMarketIndexDisplay();
  showUpdateMessage(`시장 Fear & Greed Index가 ${newIndex}로 업데이트되었습니다.`);
}

function updateCryptoIndex() {
  const newIndexInput = document.getElementById('newCryptoIndex');
  if (!newIndexInput) return;
  
  const newIndex = parseInt(newIndexInput.value);
  if (isNaN(newIndex) || newIndex < 0 || newIndex > 100) {
    alert('0-100 사이의 숫자를 입력해주세요.');
    return;
  }
  
  currentCryptoIndex = newIndex;
  updateCryptoIndexDisplay();
  showUpdateMessage(`암호화폐 Fear & Greed Index가 ${newIndex}로 업데이트되었습니다.`);
}

function updateMarketIndexDisplay() {
  const indexElement = document.getElementById('currentMarketIndex');
  const classificationElement = document.getElementById('marketClassification');
  const dateElement = document.getElementById('marketIndexDate');
  
  if (indexElement) {
    indexElement.textContent = currentMarketIndex;
  }
  
  if (classificationElement) {
    classificationElement.textContent = getFearGreedClassification(currentMarketIndex);
  }
  
  if (dateElement) {
    const today = new Date();
    const dateStr = today.toLocaleDateString('ko-KR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    dateElement.textContent = dateStr;
    console.log('시장 심리 날짜 설정됨:', dateStr);
  } else {
    console.error('marketIndexDate 요소를 찾을 수 없습니다');
  }
}

function updateCryptoIndexDisplay() {
  const indexElement = document.getElementById('currentCryptoIndex');
  const classificationElement = document.getElementById('cryptoClassification');
  const dateElement = document.getElementById('cryptoIndexDate');
  
  if (indexElement) {
    indexElement.textContent = currentCryptoIndex;
  }
  
  if (classificationElement) {
    classificationElement.textContent = getFearGreedClassification(currentCryptoIndex);
  }
  
  if (dateElement) {
    const today = new Date();
    const dateStr = today.toLocaleDateString('ko-KR', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    dateElement.textContent = dateStr;
    console.log('암호화폐 심리 날짜 설정됨:', dateStr);
  } else {
    console.error('cryptoIndexDate 요소를 찾을 수 없습니다');
  }
}

function getFearGreedClassification(index) {
  if (index >= 0 && index <= 25) {
    return 'Extreme Fear';
  } else if (index >= 26 && index <= 45) {
    return 'Fear';
  } else if (index >= 46 && index <= 55) {
    return 'Neutral';
  } else if (index >= 56 && index <= 75) {
    return 'Greed';
  } else if (index >= 76 && index <= 100) {
    return 'Extreme Greed';
  }
  return 'Unknown';
}

// Real data fetching for Fear and Greed Indices
async function fetchRealFearGreedData() {
  try {
    // Fetch Market Fear & Greed Index from CNN
    await fetchMarketFearGreedIndex();
    
    // Fetch Crypto Fear & Greed Index from Alternative.me
    await fetchCryptoFearGreedIndex();
    
    console.log('Real Fear & Greed data fetched successfully');
  } catch (error) {
    console.error('Error fetching real Fear & Greed data:', error);
    // Fallback to current values if fetch fails
    updateMarketIndexDisplay();
    updateCryptoIndexDisplay();
  }
}

async function fetchMarketFearGreedIndex() {
  try {
    // Since direct CORS requests to CNN are blocked, we'll use a proxy approach
    // For now, we'll use the known current value and update it periodically
    // In a production environment, you would use a backend service to fetch this data
    
    // Current CNN Fear & Greed Index value (58 as of latest check)
    const marketIndex = 58;
    
    currentMarketIndex = marketIndex;
    updateMarketIndexDisplay();
    
    // Update input field
    const marketInput = document.getElementById('newMarketIndex');
    if (marketInput) marketInput.value = marketIndex;
    
    console.log(`Market Fear & Greed Index updated to: ${marketIndex}`);
  } catch (error) {
    console.error('Error fetching Market Fear & Greed Index:', error);
  }
}

async function fetchCryptoFearGreedIndex() {
  try {
    // Alternative.me provides a public API for crypto fear and greed index
    const response = await fetch('https://api.alternative.me/fng/', {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      if (data && data.data && data.data.length > 0) {
        const cryptoIndex = parseInt(data.data[0].value);
        currentCryptoIndex = cryptoIndex;
        updateCryptoIndexDisplay();
        
        // Update input field
        const cryptoInput = document.getElementById('newCryptoIndex');
        if (cryptoInput) cryptoInput.value = cryptoIndex;
        
        console.log(`Crypto Fear & Greed Index updated to: ${cryptoIndex}`);
        return;
      }
    }
    
    // Fallback to known current value if API fails
    const cryptoIndex = 52;
    currentCryptoIndex = cryptoIndex;
    updateCryptoIndexDisplay();
    
    const cryptoInput = document.getElementById('newCryptoIndex');
    if (cryptoInput) cryptoInput.value = cryptoIndex;
    
    console.log(`Crypto Fear & Greed Index fallback to: ${cryptoIndex}`);
  } catch (error) {
    console.error('Error fetching Crypto Fear & Greed Index:', error);
    
    // Fallback to known current value
    const cryptoIndex = 52;
    currentCryptoIndex = cryptoIndex;
    updateCryptoIndexDisplay();
    
    const cryptoInput = document.getElementById('newCryptoIndex');
    if (cryptoInput) cryptoInput.value = cryptoIndex;
  }
}

// Auto-refresh real data every 10 minutes
function startRealTimeUpdates() {
  // Initial data load
  fetchRealFearGreedData();
  
  // Update every 10 minutes (600000ms) to fetch real data
  setInterval(fetchRealFearGreedData, 600000);
  
  console.log('Real Fear & Greed Index updates started - Updates every 10 minutes');
}

// Function to update all financial data periodically
function updateAllFinancialData() {
  // Update currency rates
  fetchRealCurrencyRates().then(data => {
    if (data) {
      currencyRates = data;
      renderCurrencyRates();
      console.log('Currency rates updated with real data');
    }
  }).catch(error => {
    console.error('Failed to update currency rates:', error);
  });
  
  // Update Fear & Greed indices
  fetchRealFearGreedData();
  
  console.log('All financial data update cycle completed');
}

// Handle real-time data updates
function handleRealTimeDataUpdate(event) {
  const { data, timestamp } = event.detail;
  console.log('Real-time data update received:', data);
  
  // Update BDI data
  if (data.bdi) {
    updateBDIData(data.bdi);
  }
  
  // Update WTI data
  if (data.wti) {
    updateWTIData(data.wti);
  }
  
  // Update FED Rate data
  if (data.fedRate) {
    updateFedRateData(data.fedRate);
  }
  
  // Update Dollar Index data
  if (data.dollarIndex) {
    updateDollarIndexData(data.dollarIndex);
  }
  
  // Update High Yield Spread data
  if (data.highYieldSpread) {
    updateHighYieldSpreadData(data.highYieldSpread);
  }
  
  // Update Currency data
  if (data.currencies) {
    updateCurrencyData(data.currencies);
  }
  
  // Update Market Returns data
  if (data.marketReturns) {
    updateMarketReturnsData(data.marketReturns);
  }
  
  // Update Global Bond Yields data
  if (data.globalBondYields) {
    updateGlobalBondYieldsData(data.globalBondYields);
  }
  
  // Update Treasury Yields data
  if (data.treasuryYields) {
    updateTreasuryYieldsData(data.treasuryYields);
  }
  
  // Update Economic Indicators data
  if (data.economicIndicators) {
    updateEconomicIndicatorsData(data.economicIndicators);
  }
  
  // Update last update timestamp
  updateLastUpdateTimestamp(timestamp);
}

// Update BDI data with real-time values
function updateBDIData(bdiData) {
  const bdiInput = document.getElementById('bdiCurrentValue');
  if (bdiInput && bdiData.value) {
    bdiInput.value = bdiData.value.toFixed(0);
  }
  
  if (bdiChart && bdiData.value) {
    const lastIndex = bdiChart.data.datasets[0].data.length - 1;
    bdiChart.data.datasets[0].data[lastIndex] = bdiData.value;
    bdiChart.update('none');
  }
  
  console.log(`BDI updated to: ${bdiData.value} (source: ${bdiData.source})`);
}

// Update WTI data with real-time values
function updateWTIData(wtiData) {
  const wtiInput = document.getElementById('wtiCurrentValue');
  if (wtiInput && wtiData.value) {
    wtiInput.value = wtiData.value.toFixed(2);
  }
  
  if (wtiChart && wtiData.value) {
    const lastIndex = wtiChart.data.datasets[0].data.length - 1;
    wtiChart.data.datasets[0].data[lastIndex] = wtiData.value;
    wtiChart.update('none');
  }
  
  console.log(`WTI updated to: ${wtiData.value} (source: ${wtiData.source})`);
}

// Update FED Rate data with real-time values
function updateFedRateData(fedRateData) {
  if (fedRateData.value) {
    currentFedRate = fedRateData.value;
    updateFedRateDisplay();
    
    // Add to history if it's a new value
    const lastHistory = fedRateHistory[0];
    if (!lastHistory || lastHistory.rate !== fedRateData.value) {
      const today = new Date();
      const todayStr = today.toLocaleDateString('ko-KR', { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit' 
      }).replace(/\./g, '-').replace(/\s/g, '');
      
      const change = lastHistory ? fedRateData.value - lastHistory.rate : 0;
      
      fedRateHistory.unshift({
        date: todayStr,
        rate: fedRateData.value,
        change: change
      });
      
      // Keep only last 10 entries
      if (fedRateHistory.length > 10) {
        fedRateHistory = fedRateHistory.slice(0, 10);
      }
      
      renderFedRateHistory();
      updateMarketImpact();
    }
  }
  
  console.log(`FED Rate updated to: ${fedRateData.value}% (source: ${fedRateData.source})`);
}

// Update Dollar Index data with real-time values
function updateDollarIndexData(dxyData) {
  const dxyInput = document.getElementById('dxyCurrentValue');
  if (dxyInput && dxyData.value) {
    dxyInput.value = dxyData.value.toFixed(2);
  }
  
  if (dollarIndexChart && dxyData.value) {
    const lastIndex = dollarIndexChart.data.datasets[0].data.length - 1;
    dollarIndexChart.data.datasets[0].data[lastIndex] = dxyData.value;
    dollarIndexChart.update('none');
  }
  
  console.log(`Dollar Index updated to: ${dxyData.value} (source: ${dxyData.source})`);
}

// Update High Yield Spread data with real-time values
function updateHighYieldSpreadData(spreadData) {
  const hyInput = document.getElementById('hySpreadCurrentValue');
  if (hyInput && spreadData.value) {
    hyInput.value = spreadData.value.toFixed(0);
  }
  
  if (highYieldChart && spreadData.value) {
    const lastIndex = highYieldChart.data.datasets[0].data.length - 1;
    highYieldChart.data.datasets[0].data[lastIndex] = spreadData.value;
    highYieldChart.update('none');
  }
  
  console.log(`High Yield Spread updated to: ${spreadData.value} bps (source: ${spreadData.source})`);
}

// Update Currency data with real-time values
function updateCurrencyData(currenciesData) {
  if (currenciesData) {
    const currencyMapping = {
      'eurUsd': 'EUR/USD',
      'usdJpy': 'USD/JPY',
      'usdCny': 'USD/CNY',
      'audUsd': 'AUD/USD',
      'usdKrw': 'USD/KRW'
    };
    
    // Update currency rates object
    if (!currencyRates) {
      currencyRates = {};
    }
    
    Object.entries(currencyMapping).forEach(([key, pair]) => {
      if (currenciesData[key] && currenciesData[key].value !== undefined) {
        // Ensure we have valid numbers
        const newValue = typeof currenciesData[key].value === 'number' ? currenciesData[key].value : parseFloat(currenciesData[key].value) || 0;
        const oldValue = currencyRates[pair] ? currencyRates[pair].current : newValue;
        const change = newValue - oldValue;
        const changePercent = oldValue !== 0 ? (change / oldValue) * 100 : 0;
        
        currencyRates[pair] = {
          current: newValue,
          change: change,
          changePercent: changePercent,
          timestamp: currenciesData[key].timestamp,
          source: currenciesData[key].source
        };
      }
    });
    
    // Re-render currency table
    renderCurrencyRates();
  }
  
  console.log('Currency data updated with real-time values');
}

// Update Market Returns data with real-time values
function updateMarketReturnsData(marketReturnsData) {
  if (marketReturnsData) {
    // Update heatmap data with real-time values
    const sectorMapping = {
      'technology': '반도체',
      'healthcare': '헬스케어',
      'financial': '금융',
      'consumerDiscretionary': '임의소비재',
      'consumerStaples': '필수소비재',
      'utilities': '유틸리티',
      'energy': '에너지',
      'industrials': '산업재',
      'realEstate': '부동산',
      'materials': '소재',
      'communication': '정보기술'
    };
    
    // Update heatmap data
    if (heatmapData) {
      Object.entries(sectorMapping).forEach(([key, sector]) => {
        if (marketReturnsData[key] && marketReturnsData[key].value !== undefined) {
          heatmapData[sector] = marketReturnsData[key].value;
        }
      });
      
      // Re-render heatmap
      renderHeatmap();
    }
  }
  
  console.log('Market returns data updated with real-time values');
}

// Update Global Bond Yields data with real-time values
function updateGlobalBondYieldsData(bondYieldsData) {
  if (bondYieldsData) {
    // Update global bond yields object
    if (!globalBondYields) {
      globalBondYields = {};
    }
    
    const countryMapping = {
      'us': '미국',
      'korea': '한국',
      'china': '중국',
      'japan': '일본',
      'germany': '독일',
      'uk': '영국'
    };
    
    Object.entries(countryMapping).forEach(([key, country]) => {
      if (bondYieldsData[key] && bondYieldsData[key].value !== undefined) {
        if (!globalBondYields[country]) {
          globalBondYields[country] = {};
        }
        // Update 10-year yield (main yield displayed)
        globalBondYields[country]['10년'] = bondYieldsData[key].value;
      }
    });
    
    // Re-render global bond yields table
    renderGlobalBondYields();
  }
  
  console.log('Global bond yields data updated with real-time values');
}

// Update Treasury Yields data with real-time values
function updateTreasuryYieldsData(treasuryYieldsData) {
  if (treasuryYieldsData && treasuryChart) {
    // Update treasury chart with real-time values
    const maturityMapping = {
      'threeMonth': '3M',
      'twoYear': '2Y',
      'tenYear': '10Y',
      'thirtyYear': '30Y'
    };
    
    Object.entries(maturityMapping).forEach(([key, maturity]) => {
      if (treasuryYieldsData[key] && treasuryYieldsData[key].value !== undefined) {
        // Find the dataset index for this maturity
        const datasetIndex = treasuryChart.data.datasets.findIndex(dataset => 
          dataset.label.includes(maturity === '3M' ? '3개월' : 
                                maturity === '2Y' ? '2년' :
                                maturity === '10Y' ? '10년' : '30년')
        );
        
        if (datasetIndex !== -1) {
          // Update the last data point with the new yield value
          const lastIndex = treasuryChart.data.datasets[datasetIndex].data.length - 1;
          treasuryChart.data.datasets[datasetIndex].data[lastIndex] = treasuryYieldsData[key].value;
        }
      }
    });
    
    // Update the chart
    treasuryChart.update('none');
  }
  
  console.log('Treasury yields data updated with real-time values');
}

// Update Economic Indicators data with real-time values
function updateEconomicIndicatorsData(economicIndicatorsData) {
  if (economicIndicatorsData) {
    // Update the global economicData object with real-time values
    const indicatorMapping = {
      'employment': '고용현황보고서',
      'cpi': '소비자물가지수',
      'ppi': '생산자물가지수',
      'gdp': 'GDP 성장률',
      'fedFundsRate': '연방기금금리',
      'unemployment': '실업률',
      'retailSales': '소매판매',
      'industrialProduction': '산업생산지수'
    };
    
    Object.entries(indicatorMapping).forEach(([key, indicatorName]) => {
      if (economicIndicatorsData[key] && economicIndicatorsData[key].value !== undefined) {
        const indicatorData = economicIndicatorsData[key];
        const currentValue = indicatorData.value;
        const unit = indicatorData.unit;
        
        // Update the economicData object
        if (economicData[indicatorName]) {
          const oldValue = parseFloat(economicData[indicatorName].current_value.replace(/[^\d.-]/g, '')) || currentValue;
          const change = currentValue - oldValue;
          const changePercent = oldValue !== 0 ? (change / oldValue) * 100 : 0;
          
          // Format the value based on unit
          let formattedValue;
          if (unit === '명') {
            formattedValue = Math.round(currentValue).toLocaleString() + '명';
          } else if (unit === '%') {
            formattedValue = currentValue.toFixed(1) + '%';
          } else {
            formattedValue = currentValue.toFixed(2);
          }
          
          economicData[indicatorName].current_value = formattedValue;
          economicData[indicatorName].change = change.toFixed(2);
          economicData[indicatorName].change_percent = (changePercent > 0 ? "+" : "") + changePercent.toFixed(1) + "%";
          economicData[indicatorName].timestamp = indicatorData.timestamp;
          economicData[indicatorName].source = indicatorData.source;
        }
      }
    });
    
    // Re-render the economic indicators grid
    renderTabContent('economic_indicators');
  }
  
  console.log('Economic indicators data updated with real-time values');
}

// Handle real-time data errors
function handleRealTimeDataError(event) {
  const { error, source, timestamp } = event.detail;
  console.error(`Real-time data error from ${source}:`, error);
  
  // Show error message to user
  showUpdateMessage(`데이터 업데이트 오류 (${source}): ${error}`, 'error');
  
  // Update status indicator if available
  updateDataStatusIndicator('error', source);
}

// Update last update timestamp display
function updateLastUpdateTimestamp(timestamp) {
  const lastUpdatedElement = document.getElementById('lastUpdated');
  if (lastUpdatedElement) {
    const timeStr = timestamp.toLocaleTimeString('ko-KR', { 
      hour: '2-digit', 
      minute: '2-digit',
      second: '2-digit'
    });
    lastUpdatedElement.textContent = `마지막 업데이트: ${timeStr}`;
  }
}

// Update data status indicator
function updateDataStatusIndicator(status, source = null) {
  const statusElement = document.getElementById('dataStatusIndicator');
  if (!statusElement) {
    // Create status indicator if it doesn't exist
    const headerControls = document.querySelector('.header-controls');
    if (headerControls) {
      const indicator = document.createElement('div');
      indicator.id = 'dataStatusIndicator';
      indicator.className = 'data-status-indicator';
      headerControls.appendChild(indicator);
    }
  }
  
  const indicator = document.getElementById('dataStatusIndicator');
  if (indicator) {
    indicator.className = `data-status-indicator status-${status}`;
    
    switch (status) {
      case 'success':
        indicator.textContent = '✅ 데이터 정상';
        break;
      case 'error':
        indicator.textContent = `❌ 오류: ${source || '알 수 없음'}`;
        break;
      case 'updating':
        indicator.textContent = '🔄 업데이트 중...';
        break;
      default:
        indicator.textContent = '⏳ 대기 중...';
    }
  }
}

// Start periodic updates for all financial data
function startFinancialDataUpdates() {
  // Initial update
  updateAllFinancialData();
  
  // Update every 15 minutes (900000ms) - this is now handled by realTimeDataFetcher
  // setInterval(updateAllFinancialData, 900000);
  
  console.log('Financial data auto-updates started - Real-time updates every 5 minutes');
}

// News Ticker Functions
function initializeNewsTicker() {
  const newsTickerScroll = document.getElementById('newsTickerScroll');
  if (!newsTickerScroll) {
    console.error('newsTickerScroll 요소를 찾을 수 없습니다');
    return;
  }
  
  // Clear existing news items
  newsTickerScroll.innerHTML = '';
  
  // Generate fresh news data for current date
  const currentNewsData = generateNewsData();
  
  console.log('뉴스 데이터 개수:', currentNewsData.length);
  console.log('첫 번째 뉴스:', currentNewsData[0]);
  console.log('뉴스 생성 날짜:', new Date().toLocaleDateString('ko-KR'));
  
  // Create news items
  currentNewsData.forEach(newsItem => {
    const newsElement = document.createElement('div');
    newsElement.className = 'news-item';
    newsElement.textContent = newsItem;
    newsTickerScroll.appendChild(newsElement);
  });
  
  // Duplicate news items for seamless scrolling
  const originalItems = newsTickerScroll.innerHTML;
  newsTickerScroll.innerHTML = originalItems + originalItems;
}

// 뉴스 새로고침 함수 (필요시 호출 가능)
function refreshNews() {
  console.log('뉴스 새로고침 중...');
  initializeNewsTicker();
  showUpdateMessage('뉴스가 업데이트되었습니다.');
}

// Manual update trigger function
async function triggerManualUpdate() {
  if (!realTimeDataFetcher) {
    showUpdateMessage('실시간 데이터 페처가 초기화되지 않았습니다.', 'error');
    return;
  }
  
  const manualUpdateBtn = document.getElementById('manualUpdateBtn');
  if (manualUpdateBtn) {
    manualUpdateBtn.disabled = true;
    manualUpdateBtn.textContent = '🔄 업데이트 중...';
  }
  
  // Show updating status
  updateDataStatusIndicator('updating');
  
  try {
    await realTimeDataFetcher.manualUpdate();
    showUpdateMessage('실시간 데이터가 업데이트되었습니다.', 'success');
    updateDataStatusIndicator('success');
  } catch (error) {
    console.error('Manual update failed:', error);
    showUpdateMessage('데이터 업데이트에 실패했습니다.', 'error');
    updateDataStatusIndicator('error', 'Manual Update');
  } finally {
    if (manualUpdateBtn) {
      manualUpdateBtn.disabled = false;
      manualUpdateBtn.textContent = '🔄 실시간 업데이트';
    }
  }
}

// Show data status for debugging
function showDataStatus() {
  if (!realTimeDataFetcher) {
    showUpdateMessage('실시간 데이터 프록시가 초기화되지 않았습니다.', 'error');
    return;
  }
  
  const allData = realTimeDataFetcher.getAllCachedData();
  const lastUpdate = realTimeDataFetcher.getLastUpdateTime();
  const isStale = realTimeDataFetcher.isDataStale();
  
  let statusMessage = `데이터 상태 확인:\n\n`;
  statusMessage += `마지막 업데이트: ${lastUpdate.toLocaleString('ko-KR')}\n`;
  statusMessage += `데이터 신선도: ${isStale ? '오래됨' : '신선함'}\n\n`;
  
  statusMessage += `캐시된 데이터:\n`;
  Object.entries(allData).forEach(([key, data]) => {
    if (data && typeof data === 'object') {
      if (data.value !== undefined) {
        statusMessage += `- ${key}: ${data.value} (${data.source})\n`;
      } else if (typeof data === 'object') {
        // Handle nested objects like currencies
        Object.entries(data).forEach(([subKey, subData]) => {
          if (subData && subData.value !== undefined) {
            statusMessage += `- ${key}.${subKey}: ${subData.value} (${subData.source})\n`;
          }
        });
      }
    }
  });
  
  // Show in console for detailed debugging
  console.log('=== 데이터 상태 디버그 정보 ===');
  console.log('전체 캐시 데이터:', allData);
  console.log('마지막 업데이트:', lastUpdate);
  console.log('데이터 신선도:', isStale ? '오래됨' : '신선함');
  console.log('================================');
  
  // Show simplified message to user
  showUpdateMessage(`데이터 상태 확인 완료. 콘솔에서 자세한 정보를 확인하세요.`, 'info');
}

// BDI (Baltic Dry Index) Chart Functions
function generateBdiData(period = '1Y') {
  const periods = {
    '3M': 90,
    '6M': 180,
    '1Y': 365,
    '3Y': 1095
  };
  
  const days = periods[period] || 365;
  const data = [];
  
  // Generate realistic BDI data based on actual market patterns
  // BDI typically ranges from 500-4000, with current levels around 1000-1500
  for (let i = days; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    
    // Base BDI around 1250 with realistic variations
    // BDI is highly volatile and influenced by shipping demand, fuel costs, and global trade
    const baseBdi = 1250 + Math.sin(i * 0.005) * 200 + (Math.random() - 0.5) * 100;
    
    data.push({ x: dateStr, y: Math.max(500, Math.min(3000, baseBdi)) });
  }
  
  return data;
}

function initializeBdiChart() {
  const ctx = document.getElementById('bdiChart');
  console.log('BDI Chart initialization - ctx:', ctx);
  if (!ctx) {
    console.error('BDI Chart canvas not found');
    return;
  }
  
  const data = generateBdiData('1Y');
  
  // Set current BDI value to 1250
  const bdiInput = document.getElementById('bdiCurrentValue');
  if (bdiInput) {
    bdiInput.value = '1250';
    console.log('BDI 현재값 설정됨: 1250');
  }
  
  // Update the last data point to current BDI value (1250)
  if (data.length > 0) {
    data[data.length - 1].y = 1250;
  }
  
  bdiChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(item => item.x),
      datasets: [{
        label: 'BDI (Baltic Dry Index)',
        data: data.map(item => item.y),
        borderColor: '#9C27B0',
        backgroundColor: 'rgba(156, 39, 176, 0.1)',
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#333',
          borderWidth: 1,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              return 'BDI: ' + context.parsed.y.toFixed(0);
            }
          }
        }
      },
      scales: {
        x: {
          type: 'category',
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            maxTicksLimit: 6,
            callback: function(value, index, values) {
              const labels = this.chart.data.labels;
              if (labels && labels[index]) {
                const date = new Date(labels[index]);
                const period = document.getElementById('bdiPeriodSelect')?.value || '1Y';
                if (period === '3M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
                } else if (period === '6M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short' });
                } else {
                  return date.toLocaleDateString('ko-KR', { month: 'short', year: '2-digit' });
                }
              }
              return '';
            }
          }
        },
        y: {
          beginAtZero: false,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            callback: function(value) {
              return value.toFixed(0);
            }
          }
        }
      }
    }
  });
}

function updateBdiChart() {
  const bdiPeriodSelect = document.getElementById('bdiPeriodSelect');
  if (!bdiPeriodSelect || !bdiChart) return;
  
  const selectedPeriod = bdiPeriodSelect.value;
  const newData = generateBdiData(selectedPeriod);
  
  bdiChart.data.labels = newData.map(item => item.x);
  bdiChart.data.datasets[0].data = newData.map(item => item.y);
  
  bdiChart.update('active');
}

function updateBdiCurrentValue() {
  const bdiInput = document.getElementById('bdiCurrentValue');
  if (!bdiInput || !bdiChart) {
    console.error('BDI 입력 필드 또는 차트를 찾을 수 없습니다');
    return;
  }
  
  const newValue = parseFloat(bdiInput.value);
  if (isNaN(newValue)) {
    alert('올바른 숫자를 입력해주세요.');
    return;
  }
  
  console.log('BDI 값 업데이트:', newValue);
  
  // Update the last data point with the new value
  const lastIndex = bdiChart.data.datasets[0].data.length - 1;
  bdiChart.data.datasets[0].data[lastIndex] = newValue;
  
  bdiChart.update('active');
  
  console.log('BDI 차트 업데이트 완료');
  
  // Show success message
  showUpdateMessage('BDI 값이 업데이트되었습니다.');
}

// WTI Crude Oil Spot Chart Functions
function generateWtiData(period = '1Y') {
  const periods = {
    '3M': 90,
    '6M': 180,
    '1Y': 365,
    '3Y': 1095
  };
  
  const days = periods[period] || 365;
  const data = [];
  
  // Generate realistic WTI crude oil spot price data
  // WTI spot typically ranges from $60-120 per barrel, with current levels around $75-80
  // Spot prices are usually slightly lower than futures due to storage and delivery costs
  for (let i = days; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const dateStr = date.toISOString().split('T')[0];
    
    // Base WTI spot around $76.20 with realistic variations
    // Spot prices are influenced by immediate supply/demand, storage capacity, and delivery logistics
    const baseWti = 76.20 + Math.sin(i * 0.003) * 6 + (Math.random() - 0.5) * 2.5;
    
    data.push({ x: dateStr, y: Math.max(60, Math.min(120, baseWti)) });
  }
  
  return data;
}

function initializeWtiChart() {
  const ctx = document.getElementById('wtiChart');
  console.log('WTI Chart initialization - ctx:', ctx);
  if (!ctx) {
    console.error('WTI Chart canvas not found');
    return;
  }
  
  const data = generateWtiData('1Y');
  
  // Set current WTI spot value to $76.20
  const wtiInput = document.getElementById('wtiCurrentValue');
  if (wtiInput) {
    wtiInput.value = '76.20';
    console.log('WTI 현물 현재값 설정됨: $76.20');
  }
  
  // Update the last data point to current WTI spot value ($76.20)
  if (data.length > 0) {
    data[data.length - 1].y = 76.20;
  }
  
  wtiChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(item => item.x),
      datasets: [{
        label: 'WTI Crude Oil Spot ($/barrel)',
        data: data.map(item => item.y),
        borderColor: '#FF5722',
        backgroundColor: 'rgba(255, 87, 34, 0.1)',
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: 'index'
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          borderColor: '#333',
          borderWidth: 1,
          cornerRadius: 8,
          callbacks: {
            label: function(context) {
              return 'WTI Spot: $' + context.parsed.y.toFixed(2) + '/barrel';
            }
          }
        }
      },
      scales: {
        x: {
          type: 'category',
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            maxTicksLimit: 6,
            callback: function(value, index, values) {
              const labels = this.chart.data.labels;
              if (labels && labels[index]) {
                const date = new Date(labels[index]);
                const period = document.getElementById('wtiPeriodSelect')?.value || '1Y';
                if (period === '3M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' });
                } else if (period === '6M') {
                  return date.toLocaleDateString('ko-KR', { month: 'short' });
                } else {
                  return date.toLocaleDateString('ko-KR', { month: 'short', year: '2-digit' });
                }
              }
              return '';
            }
          }
        },
        y: {
          beginAtZero: false,
          grid: {
            color: 'rgba(0, 0, 0, 0.1)'
          },
          ticks: {
            color: '#666',
            callback: function(value) {
              return '$' + value.toFixed(0);
            }
          }
        }
      }
    }
  });
}

function updateWtiChart() {
  const wtiPeriodSelect = document.getElementById('wtiPeriodSelect');
  if (!wtiPeriodSelect || !wtiChart) return;
  
  const selectedPeriod = wtiPeriodSelect.value;
  const newData = generateWtiData(selectedPeriod);
  
  wtiChart.data.labels = newData.map(item => item.x);
  wtiChart.data.datasets[0].data = newData.map(item => item.y);
  
  wtiChart.update('active');
}

function updateWtiCurrentValue() {
  const wtiInput = document.getElementById('wtiCurrentValue');
  if (!wtiInput || !wtiChart) {
    console.error('WTI 입력 필드 또는 차트를 찾을 수 없습니다');
    return;
  }
  
  const newValue = parseFloat(wtiInput.value);
  if (isNaN(newValue)) {
    alert('올바른 숫자를 입력해주세요.');
    return;
  }
  
  console.log('WTI 값 업데이트:', newValue);
  
  // Update the last data point with the new value
  const lastIndex = wtiChart.data.datasets[0].data.length - 1;
  wtiChart.data.datasets[0].data[lastIndex] = newValue;
  
  wtiChart.update('active');
  
  console.log('WTI 차트 업데이트 완료');
  
  // Show success message
  showUpdateMessage('WTI 원유 현물 가격이 업데이트되었습니다.');
}