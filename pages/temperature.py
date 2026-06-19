import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="서울 120년 기후 변화 탐험기",
    page_icon="🌡️",
    layout="wide"
)

# --------------------------------------------------
# 데이터 로드
# --------------------------------------------------
@st.cache_data
def load_data():

    file_name = "ta_20260619190504.csv"

    try:
        df = pd.read_csv(file_name, encoding="utf-8")
    except:
        try:
            df = pd.read_csv(file_name, encoding="cp949")
        except:
            df = pd.read_csv(file_name, encoding="euc-kr")

    df.columns = df.columns.astype(str).str.strip()

    # 날짜 컬럼 찾기
    date_col = None
    for col in df.columns:
        if "일시" in col or "날짜" in col:
            date_col = col
            break

    if date_col is None:
        date_col = df.columns[0]

    # 기온 컬럼 찾기
    avg_col = next((c for c in df.columns if "평균기온" in c), None)
    min_col = next((c for c in df.columns if "최저기온" in c), None)
    max_col = next((c for c in df.columns if "최고기온" in c), None)

    if avg_col is None or min_col is None or max_col is None:
        st.error("기온 컬럼을 찾을 수 없습니다.")
        st.write(df.columns.tolist())
        st.stop()

    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    df = df.rename(columns={
        date_col: "날짜",
        avg_col: "평균기온",
        min_col: "최저기온",
        max_col: "최고기온"
    })

    for col in ["평균기온", "최저기온", "최고기온"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["평균기온"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month

    season_map = {
        12: "겨울", 1: "겨울", 2: "겨울",
        3: "봄", 4: "봄", 5: "봄",
        6: "여름", 7: "여름", 8: "여름",
        9: "가을", 10: "가을", 11: "가을"
    }

    df["계절"] = df["월"].map(season_map)

    return df


# --------------------------------------------------
# 데이터
# --------------------------------------------------
df = load_data()

if len(df) == 0:
    st.error("데이터가 없습니다.")
    st.stop()

# --------------------------------------------------
# 사이드바
# --------------------------------------------------
st.sidebar.title("⚙️ 설정")

min_year = int(df["연도"].min())
max_year = int(df["연도"].max())

year_range = st.sidebar.slider(
    "분석 기간",
    min_year,
    max_year,
    (min_year, max_year)
)

df = df[
    (df["연도"] >= year_range[0]) &
    (df["연도"] <= year_range[1])
]

# --------------------------------------------------
# 연평균 데이터
# --------------------------------------------------
annual = (
    df.groupby("연도")[["평균기온", "최저기온", "최고기온"]]
    .mean()
    .reset_index()
)

if len(annual) < 2:
    st.error("분석 가능한 데이터가 부족합니다.")
    st.stop()

# --------------------------------------------------
# 상단
# --------------------------------------------------
st.title("🌡️ 서울 120년 기후 변화 탐험기")

first_temp = annual.iloc[0]["평균기온"]
last_temp = annual.iloc[-1]["평균기온"]

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("분석기간", f"{year_range[0]}~{year_range[1]}")
c2.metric("평균기온", f"{df['평균기온'].mean():.2f}℃")
c3.metric("역대 최고", f"{df['최고기온'].max():.1f}℃")
c4.metric("역대 최저", f"{df['최저기온'].min():.1f}℃")
c5.metric("상승폭", f"{last_temp-first_temp:+.2f}℃")

# --------------------------------------------------
# 탭
# --------------------------------------------------
tabs = st.tabs([
    "📈 추세",
    "🔥 온난화",
    "🎂 출생연도",
    "🥵 더운 해",
    "🥶 추운 해",
    "☀️ 폭염",
    "❄️ 한파",
    "🌍 계절",
    "📅 Heatmap",
    "🔮 예측",
    "🤖 리포트"
])

# --------------------------------------------------
# 추세
# --------------------------------------------------
with tabs[0]:

    annual["10년이동평균"] = annual["평균기온"].rolling(10).mean()

    model = LinearRegression()
    model.fit(annual[["연도"]], annual["평균기온"])

    annual["추세선"] = model.predict(annual[["연도"]])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=annual["연도"],
            y=annual["평균기온"],
            name="연평균기온"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=annual["연도"],
            y=annual["10년이동평균"],
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

# --------------------------------------------------
# 온난화
# --------------------------------------------------
with tabs[1]:

    st.metric(
        "1907년 이후 상승폭",
        f"{last_temp-first_temp:+.2f}℃"
    )

# --------------------------------------------------
# 출생연도
# --------------------------------------------------
with tabs[2]:

    birth = st.number_input(
        "출생연도",
        min_value=min_year,
        max_value=max_year,
        value=1990
    )

    if birth in annual["연도"].values:

        birth_temp = annual.loc[
            annual["연도"] == birth,
            "평균기온"
        ].iloc[0]

        st.metric(
            "현재와 차이",
            f"{last_temp-birth_temp:+.2f}℃"
        )

# --------------------------------------------------
# 더운 해
# --------------------------------------------------
with tabs[3]:

    st.dataframe(
        annual.nlargest(20, "평균기온"),
        use_container_width=True
    )

# --------------------------------------------------
# 추운 해
# --------------------------------------------------
with tabs[4]:

    st.dataframe(
        annual.nsmallest(20, "평균기온"),
        use_container_width=True
    )

# --------------------------------------------------
# 폭염
# --------------------------------------------------
with tabs[5]:

    heat = (
        df[df["최고기온"] >= 33]
        .groupby("연도")
        .size()
        .reset_index(name="폭염일수")
    )

    if len(heat):
        st.plotly_chart(
            px.line(
                heat,
                x="연도",
                y="폭염일수"
            ),
            use_container_width=True
        )

# --------------------------------------------------
# 한파
# --------------------------------------------------
with tabs[6]:

    cold = (
        df[df["최저기온"] <= -12]
        .groupby("연도")
        .size()
        .reset_index(name="한파일수")
    )

    if len(cold):
        st.plotly_chart(
            px.line(
                cold,
                x="연도",
                y="한파일수"
            ),
            use_container_width=True
        )

# --------------------------------------------------
# 계절
# --------------------------------------------------
with tabs[7]:

    season_df = (
        df.groupby(["연도", "계절"])["평균기온"]
        .mean()
        .reset_index()
    )

    st.plotly_chart(
        px.line(
            season_df,
            x="연도",
            y="평균기온",
            color="계절"
        ),
        use_container_width=True
    )

# --------------------------------------------------
# 히트맵
# --------------------------------------------------
with tabs[8]:

    heatmap = pd.pivot_table(
        df,
        index="연도",
        columns="월",
        values="평균기온"
    )

    st.plotly_chart(
        px.imshow(
            heatmap,
            aspect="auto"
        ),
        use_container_width=True
    )

# --------------------------------------------------
# 예측
# --------------------------------------------------
with tabs[9]:

    model = LinearRegression()

    model.fit(
        annual[["연도"]],
        annual["평균기온"]
    )

    future_years = np.arange(
        max_year + 1,
        max_year + 21
    )

    preds = model.predict(
        future_years.reshape(-1, 1)
    )

    future = pd.DataFrame({
        "연도": future_years,
        "예측기온": preds
    })

    st.dataframe(
        future,
        use_container_width=True
    )

# --------------------------------------------------
# 리포트
# --------------------------------------------------
with tabs[10]:

    hottest = annual.loc[
        annual["평균기온"].idxmax(),
        "연도"
    ]

    coldest = annual.loc[
        annual["평균기온"].idxmin(),
        "연도"
    ]

    st.markdown(f"""
### 서울 기후 리포트

- 평균기온 상승폭: **{last_temp-first_temp:+.2f}℃**
- 가장 더운 해: **{int(hottest)}년**
- 가장 추운 해: **{int(coldest)}년**
- 서울은 장기적으로 온난화 추세를 보이고 있습니다.
""")
