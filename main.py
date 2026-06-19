# app.py

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(
page_title="MBTI 진로 탐색",
page_icon="🌈",
layout="wide"
)

# -----------------

# CSS

# -----------------

st.markdown("""

<style>

.main {
    background-color:#FFF9FB;
}

.title{
    text-align:center;
    font-size:45px;
    color:#7B6D8D;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:#A393BF;
    font-size:20px;
}

.box{
    background-color:#F6F0FF;
    padding:20px;
    border-radius:20px;
    border:2px solid #E6D5FF;
}

</style>

""", unsafe_allow_html=True)

# -----------------

# 데이터

# -----------------

mbti_data = {

```
"INTJ":{
    "strength":"논리적 사고와 전략 수립 능력이 뛰어남",
    "major":["컴퓨터공학","AI학과","경영학","데이터사이언스"],
    "jobs":["AI 엔지니어","연구원","데이터 과학자","전략기획가"],
    "ability":{
        "창의성":80,
        "리더십":85,
        "분석력":95,
        "의사소통":65
    },
    "relation":{
        "best":["ENFP","ENTP"],
        "friend":["INFJ","INTP"],
        "growth":["ENTJ","ISTJ"],
        "challenge":["ESFP","ISFP"]
    }
},

"ENFP":{
    "strength":"창의성과 공감 능력이 뛰어남",
    "major":["광고홍보학","심리학","교육학","미디어학"],
    "jobs":["유튜버","광고기획자","상담사","콘텐츠 크리에이터"],
    "ability":{
        "창의성":95,
        "리더십":75,
        "분석력":70,
        "의사소통":95
    },
    "relation":{
        "best":["INTJ","INFJ"],
        "friend":["ENFJ","ENTP"],
        "growth":["ISTJ","ESTJ"],
        "challenge":["ISTP","ISFP"]
    }
},

"INFJ":{
    "strength":"통찰력과 공감 능력이 뛰어남",
    "major":["심리학","교육학","사회복지학","상담학"],
    "jobs":["상담사","교사","심리학자","작가"],
    "ability":{
        "창의성":90,
        "리더십":70,
        "분석력":80,
        "의사소통":90
    },
    "relation":{
        "best":["ENFP","ENTP"],
        "friend":["INTJ","INFP"],
        "growth":["ENFJ","ISFJ"],
        "challenge":["ESTP","ESFP"]
    }
}
```

}

# -----------------

# 제목

# -----------------

st.markdown(
'<p class="title">🌈 MBTI 진로 탐색 플랫폼</p>',
unsafe_allow_html=True
)

st.markdown(
'<p class="subtitle">나의 성격유형으로 진로와 인간관계를 알아보자!</p>',
unsafe_allow_html=True
)

st.write("")

selected = st.selectbox(
"MBTI 선택",
list(mbti_data.keys())
)

# -----------------

# 인간관계 그래프 함수

# -----------------

def draw_graph(mbti):

```
relation = mbti_data[mbti]["relation"]

G = nx.Graph()

G.add_node(mbti)

color_map = {
    mbti:"#CDB4DB"
}

for x in relation["best"]:
    G.add_edge(mbti,x)
    color_map[x]="#A2D2FF"

for x in relation["friend"]:
    G.add_edge(mbti,x)
    color_map[x]="#BDE0FE"

for x in relation["growth"]:
    G.add_edge(mbti,x)
    color_map[x]="#CAFFBF"

for x in relation["challenge"]:
    G.add_edge(mbti,x)
    color_map[x]="#FFC8DD"

pos = nx.spring_layout(G, seed=42)

fig, ax = plt.subplots(figsize=(8,6))

nx.draw_networkx_nodes(
    G,
    pos,
    node_color=[color_map[n] for n in G.nodes()],
    node_size=2500
)

nx.draw_networkx_edges(
    G,
    pos,
    width=2
)

nx.draw_networkx_labels(
    G,
    pos,
    font_size=10,
    font_weight="bold"
)

plt.axis("off")

st.pyplot(fig)
```

# -----------------

# 결과 출력

# -----------------

if st.button("✨ 진로 분석하기"):

```
data = mbti_data[selected]

col1,col2 = st.columns(2)

with col1:

    st.subheader("💪 성격 강점")

    st.success(data["strength"])

    st.subheader("🎓 추천 학과")

    for major in data["major"]:
        st.write("✔", major)

    st.subheader("💼 추천 직업")

    for job in data["jobs"]:
        st.write("💼", job)

with col2:

    st.subheader("📊 핵심 역량")

    for k,v in data["ability"].items():

        st.progress(v/100)

        st.write(f"{k} : {v}%")

st.divider()

st.subheader("🤝 MBTI 인간관계 구조도")

draw_graph(selected)

st.info(
    '''
```

🔵 잘 맞는 유형

🟢 함께 성장하는 유형

🔷 편안한 친구 유형

🩷 갈등 가능성이 있는 유형
'''
)

```
st.success(
    "진로 추천은 참고용입니다. 자신의 흥미와 적성을 함께 고려하세요!"
)
```
