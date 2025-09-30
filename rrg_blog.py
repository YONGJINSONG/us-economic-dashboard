import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import warnings
import datetime

from curl_cffi import requests
session = requests.Session(impersonate="chrome")

warnings.filterwarnings("ignore")

tickers = ['XLB', 'XLC', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY', 'XLRE']

days_before = 360

from_date = datetime.datetime.today() - datetime.timedelta(days=days_before)
#from_date = '2023-12-29'
to_date = datetime.datetime.today()

period = 5

tickers_metadata_dict = {
    'symbol': [],
    'name': []
}

for i in range(len(tickers)):
    info = yf.Ticker(tickers[i]).info
    tickers_metadata_dict['symbol'].append(info['symbol'])
    tickers_metadata_dict['name'].append(info['longName'])

benchmark = '^SPX'

tickers_data_daily = yf.download(tickers, start=from_date, end=to_date)
benchmark_data_daily = yf.download(benchmark, start=from_date, end=to_date)

# MultiIndex인 경우 Close 컬럼 사용
if isinstance(tickers_data_daily.columns, pd.MultiIndex):
    tickers_data_daily = tickers_data_daily['Close']
else:
    tickers_data_daily = tickers_data_daily['Close']

if isinstance(benchmark_data_daily.columns, pd.MultiIndex):
    benchmark_data_daily = benchmark_data_daily['Close']
else:
    benchmark_data_daily = benchmark_data_daily['Close']

latest_data_for_tickers = tickers_data_daily.iloc[::-1]  # 데이터를 역순으로 정렬
filtered_data_for_tickers = latest_data_for_tickers.iloc[::period]  # x일 간격으로 선택
tickers_data = filtered_data_for_tickers.iloc[::-1]  # 원래 순서로 복원

latest_data_for_bm = benchmark_data_daily.iloc[::-1]  # 데이터를 역순으로 정렬
filtered_data_for_bm = latest_data_for_bm.iloc[::period]  # x일 간격으로 선택
benchmark_data = filtered_data_for_bm.iloc[::-1]  # 원래 순서로 복원

window = 14 #Z-Score 계산할 주기
tail = 7  # 그래프에 표시할 기간(최근 몇주)

rs_tickers = []
rsr_tickers = []
rsr_roc_tickers = []
rsm_tickers = []

for i in range(len(tickers)):
    # RS 계산 - 인덱스를 맞춰서 계산
    ticker_series = tickers_data[tickers[i]]
    benchmark_series = benchmark_data.iloc[:, 0]  # DataFrame에서 Series 추출
    
    # 인덱스 정렬
    common_index = ticker_series.index.intersection(benchmark_series.index)
    ticker_aligned = ticker_series.loc[common_index]
    benchmark_aligned = benchmark_series.loc[common_index]
    
    rs_tickers.append(100 * (ticker_aligned / benchmark_aligned))
    
    # RSR 계산 - rolling window를 데이터 길이에 맞게 조정
    actual_window = min(window, len(rs_tickers[i]) - 1)
    if actual_window < 2:
        actual_window = 2  # 최소 2개는 필요
    
    rolling_mean = rs_tickers[i].rolling(window=actual_window, min_periods=1).mean()
    rolling_std = rs_tickers[i].rolling(window=actual_window, min_periods=1).std(ddof=0)
    
    # 표준편차가 0인 경우를 처리 (모든 값이 같을 때)
    rolling_std = rolling_std.replace(0, 1)  # 0을 1로 대체하여 나누기 오류 방지
    
    rsr_calculation = 100 + (rs_tickers[i] - rolling_mean) / rolling_std
    rsr_tickers.append(rsr_calculation.dropna())
    
    # 안전한 인덱싱을 위해 데이터가 있는지 확인
    if len(rsr_tickers[i]) > 0:
        # RSR ROC 계산
        rsr_roc_tickers.append(100 * ((rsr_tickers[i] / rsr_tickers[i].iloc[0]) - 1))
        
        # RSM 계산 - rolling window를 데이터 길이에 맞게 조정
        rsm_actual_window = min(window, len(rsr_roc_tickers[i]) - 1)
        if rsm_actual_window < 2:
            rsm_actual_window = 2
        
        rsm_rolling_mean = rsr_roc_tickers[i].rolling(window=rsm_actual_window, min_periods=1).mean()
        rsm_rolling_std = rsr_roc_tickers[i].rolling(window=rsm_actual_window, min_periods=1).std(ddof=0)
        
        # 표준편차가 0인 경우를 처리
        rsm_rolling_std = rsm_rolling_std.replace(0, 1)
        
        rsm_tickers.append((101 + (rsr_roc_tickers[i] - rsm_rolling_mean) / rsm_rolling_std).dropna())
        
        # 인덱스 정렬
        rsr_tickers[i] = rsr_tickers[i][rsr_tickers[i].index.isin(rsm_tickers[i].index)]
        rsm_tickers[i] = rsm_tickers[i][rsm_tickers[i].index.isin(rsr_tickers[i].index)]

        # 최근 데이터 추출 (안전하게)
        if len(rsr_tickers[i]) >= tail:
            rsr_tickers[i] = rsr_tickers[i].iloc[-tail:]
            rsm_tickers[i] = rsm_tickers[i].iloc[-tail:]
    else:
        print(f"Warning: No data for {tickers[i]}")
        rsr_roc_tickers.append(pd.Series())
        rsm_tickers.append(pd.Series())

def get_status(x, y):
    if x < 100 and y < 100:
        return 'lagging'
    elif x > 100 and y > 100:
        return 'leading'
    elif x < 100 and y > 100:
        return 'improving'
    elif x > 100 and y < 100:
        return 'weakening'

def get_color(x, y):
    if get_status(x, y) == 'lagging':
        return 'red'
    elif get_status(x, y) == 'leading':
        return 'green'
    elif get_status(x, y) == 'improving':
        return 'blue'
    elif get_status(x, y) == 'weakening':
        return 'yellow'
        
# 그래프 설정
plt.figure(figsize=(15, 10))
plt.gca().set_facecolor('lightgray')

plt.fill_between([94, 100], [94, 94], [100, 100], color='red', alpha=0.2)
plt.fill_between([100, 106], [94, 94], [100, 100], color='yellow', alpha=0.2)
plt.fill_between([100, 106], [100, 100], [106, 106], color='green', alpha=0.2)
plt.fill_between([94, 100], [100, 100], [106, 106], color='blue', alpha=0.2)

# Add text labels in each corner
plt.text(97, 102, 'Improving', color='white', fontsize=20)
plt.text(102, 102, 'Leading', color='white', fontsize=20)
plt.text(102, 98, 'Weakening', color='white', fontsize=20)
plt.text(97, 98, 'Lagging', color='white', fontsize=20)


# 각 ticker마다 다른 색깔 정의
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan', 'magenta']

# 각 종목에 대해 RSR을 x축, RSM을 y축으로 선형 그래프 및 화살표 생성
for i in range(len(tickers)):
    # 데이터가 있는지 확인
    if len(rsr_tickers[i]) > 0 and len(rsm_tickers[i]) > 0:
        # 각 ticker마다 고유한 색깔 사용
        ticker_color = colors[i % len(colors)]
        bg_color = get_color(rsr_tickers[i].iloc[-1], rsm_tickers[i].iloc[-1])

        # 시작점을 네모로 표시 (상태 색깔 사용)
        plt.scatter(rsr_tickers[i].iloc[0], rsm_tickers[i].iloc[0], s=100, color=bg_color, marker='s')

        # 첫 데이터 지점에 종목명 레이블 추가
        plt.text(
            rsr_tickers[i].iloc[0], rsm_tickers[i].iloc[0],
            tickers[i], fontsize=10, color='gray', ha='left', va='center'
        )

        # 중간 데이터 포인트들을 작은 크기로 산점도 표시
        if len(rsr_tickers[i]) > 2:
            plt.scatter(rsr_tickers[i].iloc[1:-1], rsm_tickers[i].iloc[1:-1], s=20, color=ticker_color, label=tickers[i])

        # 마지막 데이터 포인트는 크게 표시 (상태 색깔 사용)
        plt.scatter(rsr_tickers[i].iloc[-1], rsm_tickers[i].iloc[-1], s=100, color=bg_color)

        # 마지막 데이터 지점에 종목명 레이블 추가
        plt.text(
            rsr_tickers[i].iloc[-1], rsm_tickers[i].iloc[-1],
            tickers[i], fontsize=12, color='black', ha='left', va='center'
        )

        # 연결선 그리기 (ticker 고유 색깔 사용)
        plt.plot(rsr_tickers[i], rsm_tickers[i], color=ticker_color, marker='o', linewidth=2)

        # 각 종목의 마지막 데이터 지점에 화살표 추가 (ticker 고유 색깔 사용)
        for j in range(1, len(rsr_tickers[i])):
            plt.annotate(
                '',
                xy=(rsr_tickers[i].iloc[j], rsm_tickers[i].iloc[j]),
                xytext=(rsr_tickers[i].iloc[j - 1], rsm_tickers[i].iloc[j - 1]),
                arrowprops=dict(arrowstyle='->', color=ticker_color, lw=2)
            )
    else:
        pass  # 데이터가 부족한 경우 건너뛰기

# x축과 y축 각각 100 위치에 점선 추가
plt.axhline(y=100, color='gray', linestyle='--', linewidth=0.8)  # y = 100에 수평 점선
plt.axvline(x=100, color='gray', linestyle='--', linewidth=0.8)  # x = 100에 수직 점선

# 축 범위 설정
range = 4
plt.xlim(100-range, 100+range)
plt.ylim(100-range, 100+range)

# 그래프 제목 및 축 레이블 설정
today_str = datetime.datetime.today().strftime('%Y-%m-%d')
plt.title(f"Relative Rotation Graph - {today_str}")
plt.xlabel("Relative Strength Ratio")
plt.ylabel("Relative Strength Momentum")

# 그래프 표시
plt.show()