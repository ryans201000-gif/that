
import streamlit as st
import random

st.set_page_config(
    page_title="포켓몬 가챠 배틀",
    page_icon="⚡",
    layout="wide"
)

# -----------------------------
# 포켓몬 데이터
# -----------------------------

POKEMON = [
    {"name": "피카츄", "emoji": "⚡", "grade": "일반", "hp": 100, "atk": 25},
    {"name": "파이리", "emoji": "🔥", "grade": "일반", "hp": 90, "atk": 30},
    {"name": "꼬부기", "emoji": "🐢", "grade": "일반", "hp": 120, "atk": 20},
    {"name": "이상해씨", "emoji": "🌱", "grade": "일반", "hp": 110, "atk": 22},
    {"name": "구구", "emoji": "🐦", "grade": "일반", "hp": 85, "atk": 24},
    {"name": "이브이", "emoji": "🦊", "grade": "일반", "hp": 95, "atk": 24},

    {"name": "팬텀", "emoji": "👻", "grade": "희귀", "hp": 120, "atk": 38},
    {"name": "갸라도스", "emoji": "🐉", "grade": "희귀", "hp": 150, "atk": 35},
    {"name": "루카리오", "emoji": "🥊", "grade": "희귀", "hp": 130, "atk": 40},

    {"name": "뮤", "emoji": "✨", "grade": "전설", "hp": 160, "atk": 48},
    {"name": "프리져", "emoji": "❄️", "grade": "전설", "hp": 170, "atk": 45},
    {"name": "썬더", "emoji": "⚡", "grade": "전설", "hp": 155, "atk": 52},
    {"name": "파이어", "emoji": "🔥", "grade": "전설", "hp": 165, "atk": 50},

    {"name": "뮤츠", "emoji": "🧬", "grade": "초전설", "hp": 220, "atk": 65},
    {"name": "아르세우스", "emoji": "🌟", "grade": "초전설", "hp": 250, "atk": 70},
]

RATES = {
    "일반": 70,
    "희귀": 20,
    "전설": 9,
    "초전설": 1
}

GRADE_COLORS = {
    "일반": "#777777",
    "희귀": "#1686dc",
    "전설": "#9b45d6",
    "초전설": "#e5a000"
}

# -----------------------------
# 세션 초기화
# -----------------------------

defaults = {
    "coins": 500,
    "collection": [],
    "last_pull": None,
    "battle": None,
    "battle_message": "대결할 포켓몬을 선택하세요!",
    "wins": 0,
    "losses": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# -----------------------------
# 가챠 함수
# -----------------------------

def draw_pokemon():
    grade = random.choices(
        list(RATES.keys()),
        weights=list(RATES.values()),
        k=1
    )[0]

    candidates = [
        p for p in POKEMON
        if p["grade"] == grade
    ]

    pokemon = random.choice(candidates).copy()
    return pokemon


def pull():
    if st.session_state.coins < 100:
        st.warning("코인이 부족합니다!")
        return

    st.session_state.coins -= 100

    pokemon = draw_pokemon()
    st.session_state.collection.append(pokemon)
    st.session_state.last_pull = pokemon


# -----------------------------
# 배틀 함수
# -----------------------------

def start_battle(index):
    player = st.session_state.collection[index].copy()
    enemy = random.choice(POKEMON).copy()

    st.session_state.battle = {
        "player": player,
        "enemy": enemy,
        "player_hp": player["hp"],
        "enemy_hp": enemy["hp"],
        "finished": False
    }

    st.session_state.battle_message = (
        f"AI의 {enemy['name']}이(가) 등장했다!"
    )


def attack():
    battle = st.session_state.battle

    if not battle or battle["finished"]:
        return

    player = battle["player"]
    enemy = battle["enemy"]

    # 내 공격
    damage = random.randint(
        max(1, player["atk"] - 5),
        player["atk"] + 10
    )

    # 급소 공격
    critical = random.random() < 0.15

    if critical:
        damage = int(damage * 1.5)

    battle["enemy_hp"] = max(
        0, battle["enemy_hp"] - damage
    )

    message = f"{player['name']}의 공격! {damage} 데미지!"

    if critical:
        message += " 💥 급소 공격!"

    # 승리 확인
    if battle["enemy_hp"] <= 0:
        battle["finished"] = True
        st.session_state.wins += 1
        st.session_state.coins += 80
        st.session_state.battle_message = (
            message + "\n🎉 승리! 코인 80개 획득!"
        )
        return

    # AI 반격
    enemy_damage = random.randint(
        max(1, enemy["atk"] - 5),
        enemy["atk"] + 10
    )

    battle["player_hp"] = max(
        0, battle["player_hp"] - enemy_damage
    )

    message += (
        f"\n{enemy['name']}의 반격! "
        f"{enemy_damage} 데미지를 받았다!"
    )

    # 패배 확인
    if battle["player_hp"] <= 0:
        battle["finished"] = True
        st.session_state.losses += 1
        st.session_state.coins += 20
        message += "\n💀 패배... 참가 보상 20코인 획득!"

    st.session_state.battle_message = message


# -----------------------------
# CSS
# -----------------------------

st.markdown("""
<style>
.stApp {
    background-color: #a8dcf5;
    color: black;
}

h1, h2, h3, p, label {
    color: black !important;
}

.main .block-container {
    max-width: 1100px;
}

.stButton button {
    background-color: white;
    color: black;
    border: 2px solid #222;
    border-radius: 12px;
    font-weight: bold;
    min-height: 45px;
}

.stButton button:hover {
    background-color: #d9f1ff;
    color: black;
}

.pokemon-card {
    background-color: white;
    border: 3px solid #222;
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    margin: 8px 0;
}

.pokemon-emoji {
    font-size: 65px;
}

.pokemon-name {
    font-size: 24px;
    font-weight: bold;
}

.gacha-result {
    background-color: white;
    border: 3px solid #e5a000;
    border-radius: 20px;
    padding: 25px;
    text-align: center;
}

.battle-message {
    background: white;
    border: 2px solid black;
    border-radius: 15px;
    padding: 18px;
    text-align: center;
    font-size: 19px;
    font-weight: bold;
    white-space: pre-line;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 상단 화면
# -----------------------------

st.title("⚡ POKEMON GACHA BATTLE")
st.subheader("포켓몬을 수집하고 AI 트레이너에게 도전하라!")

c1, c2, c3 = st.columns(3)

c1.metric("💰 보유 코인", st.session_state.coins)
c2.metric("🏆 승리", st.session_state.wins)
c3.metric("💀 패배", st.session_state.losses)

st.divider()


# -----------------------------
# 메뉴
# -----------------------------

tab1, tab2, tab3 = st.tabs([
    "🎰 포켓몬 뽑기",
    "📖 포켓몬 도감",
    "⚔️ AI 대결"
])


# -----------------------------
# 가챠 화면
# -----------------------------

with tab1:

    st.header("🎰 랜덤 포켓몬 뽑기")

    st.markdown("### 뽑기 확률")

    cols = st.columns(4)

    for col, (grade, rate) in zip(cols, RATES.items()):
        color = GRADE_COLORS[grade]

        col.markdown(
            f"""
            <div class="pokemon-card">
                <b style="color:{color}">{grade}</b>
                <h2>{rate}%</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### 포켓몬 뽑기 비용: 100 코인")

    if st.button("🎁 포켓몬 뽑기!", use_container_width=True):
        pull()
        st.rerun()

    if st.session_state.last_pull:

        p = st.session_state.last_pull
        color = GRADE_COLORS[p["grade"]]

        st.markdown(f"""
        <div class="gacha-result">
            <h2>🎉 새로운 포켓몬 등장!</h2>
            <div style="font-size:100px">{p['emoji']}</div>
            <h1>{p['name']}</h1>
            <h2 style="color:{color}">{p['grade']}</h2>
            <p>HP: {p['hp']} | 공격력: {p['atk']}</p>
        </div>
        """, unsafe_allow_html=True)


# -----------------------------
# 도감 화면
# -----------------------------

with tab2:

    st.header("📖 나의 포켓몬 도감")

    collection = st.session_state.collection

    if not collection:
        st.info("아직 포켓몬이 없습니다. 가챠에서 포켓몬을 뽑아보세요!")

    else:

        st.write(f"현재 보유 포켓몬: {len(collection)}마리")

        grade_count = {
            grade: sum(
                1 for p in collection
                if p["grade"] == grade
            )
            for grade in RATES
        }

        cols = st.columns(4)

        for col, (grade, count) in zip(cols, grade_count.items()):
            col.metric(grade, f"{count}마리")

        st.divider()

        for i, p in enumerate(collection):

            color = GRADE_COLORS[p["grade"]]

            st.markdown(f"""
            <div class="pokemon-card">
                <div class="pokemon-emoji">{p['emoji']}</div>
                <div class="pokemon-name">{p['name']}</div>
                <h4 style="color:{color}">{p['grade']}</h4>
                HP: {p['hp']} | 공격력: {p['atk']}
                <p>보유 번호: #{i+1}</p>
            </div>
            """, unsafe_allow_html=True)


# -----------------------------
# AI 대결 화면
# -----------------------------

with tab3:

    st.header("⚔️ AI 트레이너와 대결")

    if not st.session_state.collection:

        st.warning("먼저 가챠에서 포켓몬을 뽑아주세요!")

    else:

        collection = st.session_state.collection

        options = list(range(len(collection)))

        selected = st.selectbox(
            "대결에 사용할 포켓몬 선택",
            options,
            format_func=lambda i: (
                f"{collection[i]['name']} "
                f"({collection[i]['grade']}) - #{i+1}"
            )
        )

        p = collection[selected]

        st.markdown(f"""
        <div class="pokemon-card">
            <div class="pokemon-emoji">{p['emoji']}</div>
            <div class="pokemon-name">{p['name']}</div>
            HP: {p['hp']} | 공격력: {p['atk']}
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔥 AI에게 대결 신청!", use_container_width=True):
            start_battle(selected)
            st.rerun()

        battle = st.session_state.battle

        if battle:

            st.divider()
            st.subheader("🔥 BATTLE START!")

            player = battle["player"]
            enemy = battle["enemy"]

            left, right = st.columns(2)

            with left:

                st.markdown(f"""
                <div class="pokemon-card">
                    <h3>🧑 내 포켓몬</h3>
                    <div class="pokemon-emoji">{player['emoji']}</div>
                    <div class="pokemon-name">{player['name']}</div>
                </div>
                """, unsafe_allow_html=True)

                st.write(
                    f"체력: {battle['player_hp']} / {player['hp']}"
                )

                st.progress(
                    battle["player_hp"] / player["hp"]
                )

            with right:

                st.markdown(f"""
                <div class="pokemon-card">
                    <h3>🤖 AI 포켓몬</h3>
                    <div class="pokemon-emoji">{enemy['emoji']}</div>
                    <div class="pokemon-name">{enemy['name']}</div>
                </div>
                """, unsafe_allow_html=True)

                st.write(
                    f"체력: {battle['enemy_hp']} / {enemy['hp']}"
                )

                st.progress(
                    battle["enemy_hp"] / enemy["hp"]
                )

            st.markdown(
                f"""
                <div class="battle-message">
                    {st.session_state.battle_message}
                </div>
                """,
                unsafe_allow_html=True
            )

            if not battle["finished"]:

                if st.button(
                    "⚔️ 공격하기!",
                    use_container_width=True
                ):
                    attack()
                    st.rerun()

            else:

                if st.button(
                    "🔄 다시 대결하기",
                    use_container_width=True
                ):
                    st.session_state.battle = None
                    st.session_state.battle_message = (
                        "새로운 포켓몬을 선택하세요!"
                    )
                    st.rerun()
