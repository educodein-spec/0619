import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


# 페이지 설정
st.set_page_config(
    page_title="MBTI 진로 추천",
    page_icon="🌈",
    layout="centered"
)

# 파스텔톤 CSS
st.markdown("""
<style>
.main {
    background-color: #FFF9FB;
}

.title {
    text-align:center;
    color:#7B6D8D;
    font-size:42px;
    font-weight:bold;
}

.subtitle {
    text-align:center;
    color:#A393BF;
    font-size:20px;
}

.result-box {
    background-color:#F6F0FF;
    padding:20px;
    border-radius:20px;
    border:2px solid #E3D5FF;
    margin-top:20px;
}

.job-card {
    background-color:#FFFFFF;
    padding:15px;
    border-radius:15px;
    margin-bottom:10px;
    border-left:5px solid #CDB4DB;
}

.stButton>button {
    background-color:#CDB4DB;
    color:white;
    border:none;
    border-radius:12px;
    padding:10px 20px;
    font-size:16px;
}

.stButton>button:hover {
    background-color:#B8A0D9;
}
</style>
""", unsafe_allow_html=True)

# MBTI 데이터
mbti_jobs = {
    "INTJ": {
        "jobs": ["데이터 과학자", "연구원", "전략기획가", "AI 엔지니어"],
        "reason": "논리적이고 미래지향적인 사고를 활용할 수 있습니다."
    },
    "INTP": {
        "jobs": ["프로그래머", "과학자", "대학교수", "시스템 분석가"],
        "reason": "창의적인 문제 해결 능력이 뛰어납니다."
    },
    "ENTJ": {
        "jobs": ["CEO", "변호사", "경영컨설턴트", "프로젝트 매니저"],
        "reason": "리더십과 조직 관리 능력이 우수합니다."
    },
    "ENTP": {
        "jobs": ["창업가", "마케팅 전문가", "기획자", "발명가"],
        "reason": "새로운 아이디어를 만드는 것을 좋아합니다."
    },
    "INFJ": {
        "jobs": ["상담사", "심리학자", "교사", "작가"],
        "reason": "타인의 성장과 발전을 돕는 능력이 뛰어납니다."
    },
    "INFP": {
        "jobs": ["작가", "디자이너", "예술가", "사회복지사"],
        "reason": "창의성과 공감 능력이 풍부합니다."
    },
    "ENFJ": {
        "jobs": ["교사", "인사담당자", "코치", "교육컨설턴트"],
        "reason": "사람들을 이끌고 동기를 부여하는 능력이 있습니다."
    },
    "ENFP": {
        "jobs": ["광고기획자", "유튜버", "기자", "콘텐츠 크리에이터"],
        "reason": "열정적이고 창의적인 성향을 가지고 있습니다."
    },
    "ISTJ": {
        "jobs": ["공무원", "회계사", "품질관리자", "행정전문가"],
        "reason": "책임감과 정확성이 뛰어납니다."
    },
    "ISFJ": {
        "jobs": ["간호사", "초등교사", "사회복지사", "행정직"],
        "reason": "세심하고 배려심이 많습니다."
    },
    "ESTJ": {
        "jobs": ["경영자", "군인", "경찰", "프로젝트 관리자"],
        "reason": "체계적이고 리더십이 강합니다."
    },
    "ESFJ": {
        "jobs": ["간호사", "교사", "서비스 관리자", "HR 전문가"],
        "reason": "협력과 소통 능력이 뛰어납니다."
    },
    "ISTP": {
        "jobs": ["기계공학자", "파일럿", "자동차 정비사", "개발자"],
        "reason": "실용적이고 문제 해결에 강합니다."
    },
    "ISFP": {
        "jobs": ["그래픽 디자이너", "사진작가", "패션 디자이너", "플로리스트"],
        "reason": "예술적 감각과 섬세함을 가지고 있습니다."
    },
    "ESTP": {
        "jobs": ["영업전문가", "기업가", "스포츠 코치", "이벤트 기획자"],
        "reason": "도전적이고 실행력이 뛰어납니다."
    },
    "ESFP": {
        "jobs": ["방송인", "배우", "관광가이드", "행사기획자"],
        "reason": "사람들과 소통하며 에너지를 얻습니다."
    }
}

# 제목
st.markdown('<p class="title">🌈 MBTI 진로 추천</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">나의 MBTI로 알아보는 미래 직업 탐색</p>',
    unsafe_allow_html=True
)

st.write("")
st.write("### 📝 MBTI를 선택하세요")

selected_mbti = st.selectbox(
    "MBTI 유형",
    list(mbti_jobs.keys())
)

if st.button("✨ 추천 직업 보기"):

    data = mbti_jobs[selected_mbti]

    st.markdown(
        f"""
        <div class="result-box">
            <h2>🎯 {selected_mbti} 추천 직업</h2>
            <p><b>추천 이유:</b> {data['reason']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    for job in data["jobs"]:
        st.markdown(
            f"""
            <div class="job-card">
                💼 {job}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.success("진로 탐색은 참고 자료이며, 자신의 관심사와 적성을 함께 고려해 보세요!")

st.write("---")

st.subheader("🌟 MBTI 인간관계 구조도")

mbti_relationships = {
"INTJ": {
"best": ["ENFP", "ENTP"],
"friend": ["INFJ", "INTP"],
"challenge": ["ESFP", "ISFP"]
},
"INTP": {
"best": ["ENTJ", "ENFJ"],
"friend": ["INTJ", "INFJ"],
"challenge": ["ESFP", "ESTP"]
},
"ENTJ": {
"best": ["INTP", "INFP"],
"friend": ["ENTP", "INTJ"],
"challenge": ["ISFP", "ESFP"]
},
"ENTP": {
"best": ["INFJ", "INTJ"],
"friend": ["ENFP", "ENTJ"],
"challenge": ["ISFJ", "ISTJ"]
},
"INFJ": {
"best": ["ENFP", "ENTP"],
"friend": ["INTJ", "INFP"],
"challenge": ["ESTP", "ESFP"]
},
"INFP": {
"best": ["ENFJ", "ENTJ"],
"friend": ["INFJ", "ENFP"],
"challenge": ["ESTJ", "ISTJ"]
},
"ENFJ": {
"best": ["INFP", "ISFP"],
"friend": ["ENFP", "INFJ"],
"challenge": ["ISTP", "INTP"]
},
"ENFP": {
"best": ["INTJ", "INFJ"],
"friend": ["ENTP", "ENFJ"],
"challenge": ["ISTJ", "ESTJ"]
}
}
