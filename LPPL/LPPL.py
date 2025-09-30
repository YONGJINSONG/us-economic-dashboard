import numpy as np
import pandas as pd
import yfinance as yf
import datetime
from datetime import datetime as dt
import warnings
import matplotlib.pyplot as plt
from lppls import lppls

# matplotlib 백엔드를 설정하여 그래프가 표시되도록 함
import matplotlib
matplotlib.use('Agg')  # 백엔드 설정 (파일 저장용)
warnings.filterwarnings("ignore")

days_before = 365*10
from_date = datetime.datetime.today() - datetime.timedelta(days=days_before)
to_date = datetime.datetime.today()
ticker = 'QQQ'

data = yf.Ticker(ticker).history(start=from_date, end=to_date)

data['Date'] = data.index.strftime('%Y-%m-%d')
time = [pd.Timestamp.toordinal(dt.strptime(t1, '%Y-%m-%d')) for t1 in data['Date'].values]
price = np.log(data['Close'].values)

# create observations array (expected format for LPPLS observations)
observations = np.array([time, price])

# set the max number for searches to perform before giving-up
# the literature suggests 25
MAX_SEARCHES = 25

# instantiate a new LPPLS model with the Nasdaq Dot-com bubble dataset
lppls_model = lppls.LPPLS(observations=observations)

if __name__ == '__main__':

    # fit the model to the data and get back the params
    tc, m, w, a, b, c, c1, c2, O, D = lppls_model.fit(MAX_SEARCHES)

    # visualize the fit
    lppls_model.plot_fit()
    plt.savefig('lppls_fit.png', dpi=300, bbox_inches='tight')  # 첫 번째 그래프 저장
    print("첫 번째 그래프가 'lppls_fit.png'로 저장되었습니다.")

    # 1번 이미지 등장

    # define custom filter condition
    # compute the confidence indicator
    res = lppls_model.mp_compute_nested_fits(
        workers=8,
        window_size=120,
        smallest_window_size=30,
        outer_increment=1,
        inner_increment=5,
        max_searches=25,
        # filter_conditions_config={} # not implemented in 0.6.x
    )

    lppls_model.plot_confidence_indicators(res)
    plt.savefig('lppls_confidence.png', dpi=300, bbox_inches='tight')  # 두 번째 그래프 저장
    print("두 번째 그래프가 'lppls_confidence.png'로 저장되었습니다.")
    #  2번 이미지 등장