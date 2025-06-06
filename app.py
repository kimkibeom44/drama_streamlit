import streamlit as st
import json
import random
from collections import defaultdict
from datetime import datetime, timedelta

# 1. 페이지 설정 및 스타일
st.set_page_config(
    page_title="할머니의 드라마 정원",
    layout="wide",
    initial_sidebar_state="collapsed"
)
base_size = 24
st.markdown(f"""
<style>
html, body, [class*="css"] {{
    font-family: "Nanum Gothic", sans-serif;
    background-color: #FFFDF8;
    color: #333;
    font-size: {base_size}px !important;
}}
.title {{ font-size: {base_size*2.5}px; font-weight: bold; text-align: center; color: #7B3F00; margin: 20px 0 10px; }}
.subtitle {{ font-size: {base_size*1.2}px; text-align: center; color: #555; margin-bottom: 20px; }}
.section-header {{ font-size: {base_size*1.8}px; font-weight: bold; color: #8B3F00; margin: 20px 0 10px; }}
.card-wrapper {{ position: relative; display: inline-block; margin: 10px; }}
.card-img {{ width: 200px; height: auto; border-radius: 8px; }}
.card-title-overlay {{ position: absolute; top: 8px; left: 8px; background: rgba(0,0,0,0.6); color: white; padding: 4px 8px; border-radius: 4px; font-size: {base_size*1.2}px; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">할머니의 드라마 정원</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">원하는 기능 탭을 눌러주세요~ 🌸</div>', unsafe_allow_html=True)

# 2. 데이터 로드
with open("grandma_dramas_100.json", encoding="utf-8") as f:
    data = json.load(f)
with open("final_drama_schedule_updated.json", encoding="utf-8") as f:
    live_schedule = json.load(f)
with open("upcoming_dramas_schedule.json", encoding="utf-8") as f:
    upcoming_schedule = json.load(f)
with open("popular_dramas_updated.json", encoding="utf-8") as f:
    popular_list = json.load(f)
with open("drama_image_urls.json", encoding="utf-8") as f:
    image_map = json.load(f)


for d in all_dramas:
    d["image_url"] = image_map.get(d["programName"])

# 날짜 계산
now = datetime.now()
wd_today = now.strftime("%A")
wd_tomorrow = (now + timedelta(days=1)).strftime("%A")

# 이미지 + 제목 오버레이 함수
def image_with_title(title, url):
    html = f'''<div class="card-wrapper">\
    <img src="{url}" class="card-img"/><div class="card-title-overlay">{title}</div></div>'''
    st.markdown(html, unsafe_allow_html=True)

# 3. 방송사/연령/유형별 데이터 가공
broadcaster_map = defaultdict(list)
for d in all_dramas:
    broadcaster_map[d["broadcaster"]].append(d)

def is_60s(d): return any(g in d["genre"] for g in ["가족", "로맨스", "힐링", "일상", "휴먼", "감동"])
def is_70s(d): return any(g in d["genre"] for g in ["막장", "복수", "욕망", "정치", "격정", "복수극"])
def is_80s(d): return any(g in d["genre"] for g in ["전통", "역사", "농촌", "사극"])

age_group_rankings = {
    "60대": [d for d in all_dramas if is_60s(d)][:20],
    "70대": [d for d in all_dramas if is_70s(d)][:20],
    "80대": [d for d in all_dramas if is_80s(d)][:20]
}

typeA = [d for d in all_dramas if "막장" in d["genre"] or "복수" in d["genre"] or "욕망" in d["genre"]][:5]
typeB = [d for d in all_dramas if "힐링" in d["genre"] or "가족" in d["genre"] or "감동" in d["genre"] or "일상" in d["genre"]][:5]
typeC = [d for d in all_dramas if "전통" in d["genre"] or "역사" in d["genre"] or "사극" in d["genre"] or "농촌" in d["genre"]][:5]
grandma_types = {
    "막장 드라마 좋아하는 A할머니": typeA,
    "힐링 드라마 좋아하는 B할머니": typeB,
    "전통 드라마 좋아하는 C할머니": typeC
}

# 4. 탭 구성
tabs = st.tabs([
    "오늘·내일 방송",
    "장르별 추천",
    "배우 검색",
    "키워드 검색",
    "랜덤 4편 추천",
    "🔥 인기 드라마",
    "🎤 트로트 예능",
    "📺 방송사별 드라마",
    "🎂 연령별 추천",
    "👵 할머니 유형별 추천"
])

# 오늘·내일 방송
with tabs[0]:
    st.subheader("🗓 오늘·내일 방송", divider=True)
    col1, col2 = st.columns(2)

    # 오늘 방송 중에서 랜덤으로 하나 골라 별표
    today = [d for d in live_schedule if wd_today in d["dayOfWeek"]]
    star_today = random.choice(today) if today else None

    with col1:
        st.markdown("✅ 오늘 방송")
        if today:
            for t in today:
                star = " ⭐" if star_today and t['programName'] == star_today['programName'] else ""
                st.markdown(f"- {t['programName']}{star} ({t['startTime']})")
        else:
            st.write("오늘 방송이 없어요.")

    # 내일 방송 중에서 랜덤으로 하나 골라 별표
    tm = [d for d in live_schedule if wd_tomorrow in d["dayOfWeek"]]
    star_tm = random.choice(tm) if tm else None

    with col2:
        st.markdown("⏰ 내일 방송")
        if tm:
            for t in tm:
                star = " ⭐" if star_tm and t['programName'] == star_tm['programName'] else ""
                st.markdown(f"- {t['programName']}{star} ({t['startTime']})")
        else:
            st.write("내일 방송이 없어요.")
# 장르별 추천
with tabs[1]:
    st.subheader("🎭 장르별 추천", divider=True)
    genres = sorted({g.strip() for d in all_dramas for g in d["genre"].split(",")})
    sel = st.selectbox("장르 선택", ["전체"] + genres)
    lst = all_dramas if sel == "전체" else [d for d in all_dramas if sel in d["genre"]]
    for d in lst:
        img = d.get("image_url")
        if img:
            image_with_title(d["programName"], img)
        st.markdown(f"**줄거리:** {d.get('summary','')}")
        st.markdown(f"**출연진:** {', '.join(d['actors'])}")

# 배우 검색
with tabs[2]:
    st.subheader("🎬 배우 검색", divider=True)
    q = st.text_input("배우 이름 입력")
    if q:
        found = [d for d in all_dramas if q in " ".join(d['actors'])]
        if found:
            for d in found:
                img = d.get("image_url")
                if img:
                    image_with_title(d["programName"], img)
                st.markdown(f"**줄거리:** {d.get('summary','')}")
        else:
            st.write("해당 배우 드라마가 없어요.")

# 키워드 검색
with tabs[3]:
    st.subheader("🔖 키워드 검색", divider=True)
    q = st.text_input("키워드 입력")
    if q:
        found = [d for d in all_dramas if q.lower() in d['programName'].lower()
                  or q.lower() in d['summary'].lower()
                  or q.lower() in d['genre'].lower()
                  or q in " ".join(d['actors'])]
        if found:
            for d in found:
                img = d.get("image_url")
                if img:
                    image_with_title(d["programName"], img)
                st.markdown(f"**줄거리:** {d.get('summary','')}")
        else:
            st.write("검색 결과가 없어요.")

# 랜덤 4편 추천
with tabs[4]:
    st.subheader("🌟 랜덤 4편 추천", divider=True)
    sample = random.sample(all_dramas, 4)
    for d in sample:
        img = d.get("image_url")
        if img:
            image_with_title(d["programName"], img)

# 인기 드라마
with tabs[5]:
    st.subheader("🔥 인기 드라마", divider=True)
    for rec in popular_list:
        d = next((x for x in all_dramas if x['programName'] == rec['programName']), None)
        if d:
            img = d.get('image_url')
            if img:
                image_with_title(d['programName'], img)

# 트로트 예능
with tabs[6]:
    st.subheader("🎤 트로트 예능", divider=True)
    trot = [d for d in all_dramas if '트로트' in d['genre'] or '예능' in d['genre']]
    if trot:
        for d in trot:
            img = d.get('image_url')
            if img:
                image_with_title(d['programName'], img)
    else:
        st.write("트로트 예능이 없어요.")

# 방송사별 드라마
with tabs[7]:
    st.subheader("📺 방송사별 드라마", divider=True)
    sel_bc = st.selectbox("방송사 선택", list(broadcaster_map.keys()))
    for d in broadcaster_map[sel_bc]:
        st.markdown(f"**{d['programName']}** ({d['genre']})")
        st.markdown(f"- 줄거리: {d['summary']}")
        st.markdown(f"- 출연진: {', '.join(d['actors'])}")
        img = d.get("image_url")
        if img:
            st.image(img, width=220)
        st.markdown("---")

# 연령별 추천
with tabs[8]:
    st.subheader("🎂 연령별 인기 드라마", divider=True)
    sel_age = st.radio("연령대를 선택하세요", ["60대", "70대", "80대"], horizontal=True)
    for d in age_group_rankings[sel_age]:
        st.markdown(f"**{d['programName']}** ({d['genre']})")
        st.markdown(f"- 줄거리: {d['summary']}")
        st.markdown(f"- 출연진: {', '.join(d['actors'])}")
        img = d.get("image_url")
        if img:
            st.image(img, width=220)
        st.markdown("---")

# 할머니 유형별 추천
with tabs[9]:
    st.subheader("👵 할머니 유형별 추천", divider=True)
    sel_type = st.selectbox("어떤 할머니이신가요?", list(grandma_types.keys()))
    for d in grandma_types[sel_type]:
        st.markdown(f"**{d['programName']}** ({d['genre']})")
        st.markdown(f"- 줄거리: {d['summary']}")
        st.markdown(f"- 출연진: {', '.join(d['actors'])}")
        img = d.get("image_url")
        if img:
            st.image(img, width=220)
        st.markdown("---")
