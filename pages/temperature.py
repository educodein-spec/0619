import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="서울 120년 기후 변화 탐험기", page_icon="🌡️", layout="wide")

@st.cache_data
def load_data():

    df = pd.read_csv(
        "ta_20260619190504.csv",
        encoding="utf-8"
    )

    st.write(df.head())
    st.write(df.columns)

    return df

df = load_data()

st.title("🌡️ 서울 120년 기후 변화 탐험기")

min_year = int(df["연도"].min())
max_year = int(df["연도"].max())

st.sidebar.header("설정")
year_range = st.sidebar.slider("분석 기간", min_year, max_year, (min_year, max_year))

df = df[(df["연도"] >= year_range[0]) & (df["연도"] <= year_range[1])]

annual = df.groupby("연도")[["평균기온","최저기온","최고기온"]].mean().reset_index()

first_temp = annual.iloc[0]["평균기온"]
last_temp = annual.iloc[-1]["평균기온"]

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("분석기간", f"{year_range[0]}~{year_range[1]}")
c2.metric("평균기온", f"{df['평균기온'].mean():.2f}℃")
c3.metric("역대 최고", f"{df['최고기온'].max():.1f}℃")
c4.metric("역대 최저", f"{df['최저기온'].min():.1f}℃")
c5.metric("상승폭", f"{last_temp-first_temp:+.2f}℃")

tabs = st.tabs([
    "📈 추세","🔥 온난화","🎂 출생연도","🥵 더운 해",
    "🥶 추운 해","☀️ 폭염","❄️ 한파","🌍 계절",
    "📅 Heatmap","🔮 예측","🤖 리포트"
])

with tabs[0]:
    annual["10년이동평균"] = annual["평균기온"].rolling(10).mean()
    model = LinearRegression().fit(annual[["연도"]], annual["평균기온"])
    annual["추세선"] = model.predict(annual[["연도"]])

    fig = go.Figure()
    fig.add_scatter(x=annual["연도"], y=annual["평균기온"], name="평균기온")
    fig.add_scatter(x=annual["연도"], y=annual["10년이동평균"], name="10년 이동평균")
    fig.add_scatter(x=annual["연도"], y=annual["추세선"], name="추세선")
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.metric("1907→최근 상승폭", f"{last_temp-first_temp:+.2f}℃")

with tabs[2]:
    birth = st.number_input("출생연도", min_value=min_year, max_value=max_year, value=1990)
    if birth in annual["연도"].values:
        bt = annual.loc[annual["연도"]==birth,"평균기온"].iloc[0]
        st.metric("현재와 차이", f"{last_temp-bt:+.2f}℃")

with tabs[3]:
    st.dataframe(annual.nlargest(20,"평균기온")[["연도","평균기온"]])

with tabs[4]:
    st.dataframe(annual.nsmallest(20,"평균기온")[["연도","평균기온"]])

with tabs[5]:
    heat = df[df["최고기온"]>=33].groupby("연도").size().reset_index(name="폭염일수")
    st.plotly_chart(px.line(heat,x="연도",y="폭염일수"), use_container_width=True)

with tabs[6]:
    cold = df[df["최저기온"]<=-12].groupby("연도").size().reset_index(name="한파일수")
    st.plotly_chart(px.line(cold,x="연도",y="한파일수"), use_container_width=True)

with tabs[7]:
    season = df.groupby(["연도","계절"])["평균기온"].mean().reset_index()
    st.plotly_chart(px.line(season,x="연도",y="평균기온",color="계절"), use_container_width=True)

with tabs[8]:
    heatmap = pd.pivot_table(df,index="연도",columns="월",values="평균기온")
    st.plotly_chart(px.imshow(heatmap,aspect="auto"), use_container_width=True)

with tabs[9]:
    model = LinearRegression().fit(annual[["연도"]], annual["평균기온"])
    future_years = np.arange(max_year+1, max_year+21)
    preds = model.predict(future_years.reshape(-1,1))
    future = pd.DataFrame({"연도":future_years,"예측기온":preds})
    st.dataframe(future)

with tabs[10]:
    hottest = annual.loc[annual["평균기온"].idxmax(),"연도"]
    coldest = annual.loc[annual["평균기온"].idxmin(),"연도"]
    st.markdown(f"""
    ### 서울 기후 리포트
    - 평균기온 상승폭: **{last_temp-first_temp:+.2f}℃**
    - 가장 더운 해: **{int(hottest)}년**
    - 가장 추운 해: **{int(coldest)}년**
    - 서울은 장기적으로 온난화 추세를 보입니다.
    """)
