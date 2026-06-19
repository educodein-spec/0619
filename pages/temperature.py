import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression

# -----------------------------------

# 페이지 설정

# -----------------------------------

st.set_page_config(
page_title="서울 120년 기후 변화 탐험기",
page_icon="🌡️",
layout="wide"
)

# -----------------------------------

# 데이터 로드

# -----------------------------------

@st.cache_data
def load_data():

```
df = pd.read_csv("ta_20260619190504.csv", encoding="utf-8")

df.columns = [
    "날짜",
    "지점",
    "평균기온",
    "최저기온",
    "최고기온"
]

df["날짜"] = pd.to_datetime(df["날짜"])

df["연도"] = df["날짜"].dt.year
df["월"] = df["날짜"].dt.month
df["일"] = df["날짜"].dt.day

def season(month):
    if month in [3,4,5]:
        return "봄"
    elif month in [6,7,8]:
        return "여름"
    elif month in [9,10,11]:
        return "가을"
    return "겨울"

df["계절"] = df["월"].apply(season)

return df
```

df = load_data()

# -----------------------------------

# Sidebar

# -----------------------------------

st.sidebar.title("⚙️ 설정")

min_year = int(df["연도"].min())
max_year = int(df["연도"].max())

year_range = st.sidebar.slider(
"분석 기간",
min_year,
max_year,
(min_year, max_year)
)

temp_type = st.sidebar.selectbox(
"기온 선택",
["평균기온", "최저기온", "최고기온"]
)

df = df[
(df["연도"] >= year_range[0]) &
(df["연도"] <= year_range[1])
]

# -----------------------------------

# 타이틀

# -----------------------------------

st.title("🌡️ 서울 120년 기후 변화 탐험기")
st.caption("1907 ~ 2026 서울 기온 데이터 분석")

# -----------------------------------

# KPI

# -----------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
st.metric(
"분석 기간",
f"{year_range[0]}~{year_range[1]}"
)

with c2:
st.metric(
"평균 기온",
f"{df['평균기온'].mean():.2f}℃"
)

with c3:
st.metric(
"역대 최고",
f"{df['최고기온'].max():.1f}℃"
)

with c4:
st.metric(
"역대 최저",
f"{df['최저기온'].min():.1f}℃"
)

# -----------------------------------

# 연평균 기온

# -----------------------------------

st.header("📈 연평균 기온 추세")

annual = (
df.groupby("연도")[temp_type]
.mean()
.reset_index()
)

annual["10년 이동평균"] = (
annual[temp_type]
.rolling(10)
.mean()
)

X = annual["연도"].values.reshape(-1,1)
y = annual[temp_type].values

model = LinearRegression()
model.fit(X,y)

annual["추세선"] = model.predict(X)

fig = go.Figure()

fig.add_trace(
go.Scatter(
x=annual["연도"],
y=annual[temp_type],
name="연평균"
)
)

fig.add_trace(
go.Scatter(
x=annual["연도"],
y=annual["10년 이동평균"],
name="10년 이동평균"
)
)

fig.add_trace(
go.Scatter(
x=annual["연도"],
y=annual["추세선"],
name="추세선"
)
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------

# 온난화 분석

# -----------------------------------

st.header("🔥 서울은 얼마나 따뜻해졌을까?")

first_year = annual.iloc[0]
last_year = annual.iloc[-1]

change = (
last_year[temp_type]
- first_year[temp_type]
)

c1, c2, c3 = st.columns(3)

c1.metric(
f"{int(first_year['연도'])}년",
f"{first_year[temp_type]:.2f}℃"
)

c2.metric(
f"{int(last_year['연도'])}년",
f"{last_year[temp_type]:.2f}℃"
)

c3.metric(
"변화량",
f"{change:+.2f}℃"
)

# -----------------------------------

# 출생연도 비교

# -----------------------------------

st.header("🎂 내가 태어난 해와 비교")

birth_year = st.number_input(
"출생연도",
min_value=min_year,
max_value=max_year,
value=1990
)

if birth_year in annual["연도"].values:

```
birth_temp = annual[
    annual["연도"] == birth_year
][temp_type].iloc[0]

recent_temp = annual.iloc[-1][temp_type]

diff = recent_temp - birth_temp

c1, c2, c3 = st.columns(3)

c1.metric(
    f"{birth_year}년",
    f"{birth_temp:.2f}℃"
)

c2.metric(
    f"{int(last_year['연도'])}년",
    f"{recent_temp:.2f}℃"
)

c3.metric(
    "변화",
    f"{diff:+.2f}℃"
)
```

# -----------------------------------

# 더운 해 TOP20

# -----------------------------------

st.header("🥵 가장 더운 해 TOP20")

hot_years = (
annual
.sort_values(temp_type, ascending=False)
.head(20)
)

st.dataframe(
hot_years[["연도", temp_type]],
use_container_width=True
)

fig = px.bar(
hot_years,
x="연도",
y=temp_type
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------

# 추운 해 TOP20

# -----------------------------------

st.header("🥶 가장 추운 해 TOP20")

cold_years = (
annual
.sort_values(temp_type)
.head(20)
)

st.dataframe(
cold_years[["연도", temp_type]],
use_container_width=True
)

# -----------------------------------

# 폭염 분석

# -----------------------------------

st.header("☀️ 폭염 분석")

heatwave = (
df[df["최고기온"] >= 33]
.groupby("연도")
.size()
.reset_index(name="폭염일수")
)

fig = px.line(
heatwave,
x="연도",
y="폭염일수"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------

# 한파 분석

# -----------------------------------

st.header("❄️ 한파 분석")

coldwave = (
df[df["최저기온"] <= -12]
.groupby("연도")
.size()
.reset_index(name="한파일수")
)

fig = px.line(
coldwave,
x="연도",
y="한파일수"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------

# 월별 히트맵

# -----------------------------------

st.header("📅 월별 기온 히트맵")

pivot = pd.pivot_table(
df,
values="평균기온",
index="연도",
columns="월",
aggfunc="mean"
)

fig = px.imshow(
pivot,
aspect="auto"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------

# 미래 예측

# -----------------------------------

st.header("🔮 미래 기온 예측")

future_years = np.arange(
annual["연도"].max()+1,
annual["연도"].max()+21
)

future_pred = model.predict(
future_years.reshape(-1,1)
)

future_df = pd.DataFrame({
"연도":future_years,
"예측기온":future_pred
})

fig = go.Figure()

fig.add_trace(
go.Scatter(
x=annual["연도"],
y=annual[temp_type],
name="실제"
)
)

fig.add_trace(
go.Scatter(
x=future_df["연도"],
y=future_df["예측기온"],
name="예측"
)
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(
future_df,
use_container_width=True
)

# -----------------------------------

# AI 인사이트

# -----------------------------------

st.header("🤖 자동 인사이트")

hottest_year = hot_years.iloc[0]["연도"]
coldest_year = cold_years.iloc[0]["연도"]

st.info(
f"""
• 분석 기간 동안 평균 변화량 : {change:+.2f}℃

```
• 가장 더운 해 : {int(hottest_year)}년

• 가장 추운 해 : {int(coldest_year)}년

• 서울은 장기적으로 뚜렷한 온난화 경향을 보이고 있습니다.

• 최근 수십 년간 상승 속도가 더욱 가파르게 나타납니다.
"""
```

)
