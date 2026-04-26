import streamlit as st
import httpx
import pandas as pd
import plotly.express as px
import json
import time
from datetime import datetime
from streamlit_agraph import agraph, Node, Edge, Config
import subprocess
import sys
import socket

@st.cache_resource
def start_backend():
    def is_port_in_use(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    if not is_port_in_use(8000):
        subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"])
        for _ in range(10):
            if is_port_in_use(8000):
                break
            time.sleep(0.5)
    return True

start_backend()

# Page Config
st.set_page_config(
    page_title="AI Learning Coach",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern/Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #4f46e5;
        --primary-hover: #4338ca;
        --bg: #f8fafc;
        --card-bg: #ffffff;
        --text-main: #1e293b;
        --text-muted: #64748b;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }
    
    .main {
        background-color: var(--bg);
    }
    
    /* Horizontal Menu Style */
    .stButton > button {
        border-radius: 10px;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    /* Card Style */
    .st-emotion-cache-12w0qpk {
        border-radius: 20px;
        padding: 2rem;
        background: var(--card-bg);
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--primary);
        font-weight: 700;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    .sidebar-user-card {
        padding: 1.5rem;
        background: #f1f5f9;
        border-radius: 15px;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Sidebar - User Demographics & Q&A
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/brain.png", width=60)
    st.title("Öğrenme Koçu")
    st.markdown("*Geliştirici: Ali İhsan Çetin*")
    st.markdown("---")
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if st.session_state.user_id:
        if not st.session_state.user_data:
            try:
                res = httpx.get(f"{API_BASE_URL}/get-profile?user_id={st.session_state.user_id}")
                if res.status_code == 200:
                    st.session_state.user_data = res.json()
            except:
                pass
        
        user = st.session_state.user_data
        if user:
            xp = user.get('xp', 0)
            level = (xp // 100) + 1
            xp_progress = xp % 100
            streak = user.get('streak_days', 0)
            
            st.markdown(f"""
            <div class="sidebar-user-card">
                <small style="color: var(--text-muted)">Hoş geldin,</small>
                <div style="font-weight: 700; font-size: 1.1rem; color: var(--primary)">{user['full_name']}</div>
                <div style="font-size: 0.85rem; margin-top: 5px;">🎯 {user['goal']}</div>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid #e2e8f0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span style="font-weight: 600; font-size: 0.9rem; color: #4f46e5;">⭐ Seviye {level}</span>
                    <span style="font-weight: 600; font-size: 0.9rem; color: #f97316;">🔥 {streak} Seri</span>
                </div>
                <div style="width: 100%; background-color: #e2e8f0; border-radius: 10px; height: 8px;">
                    <div style="width: {xp_progress}%; background-color: #4f46e5; height: 8px; border-radius: 10px;"></div>
                </div>
                <div style="text-align: right; font-size: 0.75rem; color: var(--text-muted); margin-top: 3px;">
                    {xp_progress}/100 XP
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 💬 Koça Sor")
        # Use a simple chat interface in sidebar
        for msg in st.session_state.chat_history[-3:]: # Show last 3
            role = "user" if msg["role"] == "user" else "assistant"
            with st.chat_message(role):
                st.markdown(msg["content"])
        
        q_input = st.chat_input("Bir şey sor...")
        if q_input:
            st.session_state.chat_history.append({"role": "user", "content": q_input})
            with st.spinner("Düşünüyorum..."):
                try:
                    res = httpx.post(f"{API_BASE_URL}/ask-question", json={"user_id": st.session_state.user_id, "question": q_input})
                    data = res.json()
                    answer = data.get("coach_feedback", "Yanıt alınamadı.")
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    st.rerun()
                except Exception as e:
                    st.error(f"Hata: {e}")
        
        st.markdown("---")
        if st.button("🚪 Oturumu Sıfırla", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.user_data = None
            st.session_state.chat_history = []
            st.rerun()
    else:
        st.info("👋 Merhaba! Başlamak için lütfen profilini oluştur.")

# Navigation (Horizontal Buttons)
if 'page' not in st.session_state:
    st.session_state.page = "Profil"

def render_nav():
    st.markdown("### 🧭 Gezinti")
    cols = st.columns(4)
    pages = ["Profil", "Plan", "İlerleme", "Analiz"]
    icons = ["👤", "📅", "📝", "📊"]

    for i, p in enumerate(pages):
        btn_type = "secondary" if st.session_state.page != p else "primary"
        if cols[i].button(f"{icons[i]} {p}", key=f"nav_{p}", use_container_width=True, type=btn_type):
            st.session_state.page = p
            st.rerun()
    st.markdown("---")

render_nav()

# Functions
def create_profile(data):
    try:
        response = httpx.post(f"{API_BASE_URL}/create-profile", json=data)
        if response.status_code != 200:
            st.error(f"Hata ({response.status_code}): {response.text}")
            return None
        return response.json()
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

def generate_plan(user_id):
    try:
        response = httpx.post(f"{API_BASE_URL}/generate-plan?user_id={user_id}", timeout=60.0)
        data = response.json()
        if data.get("error"):
            st.error(f"AI Hatası: {data.get('message')}")
            return None
        return data
    except Exception as e:
        st.error(f"Hata: {e}")
        return None

def get_plan(user_id):
    try:
        response = httpx.get(f"{API_BASE_URL}/get-plan?user_id={user_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

def submit_progress(user_id, content):
    try:
        response = httpx.post(f"{API_BASE_URL}/submit-progress", json={"user_id": user_id, "content": content}, timeout=60.0)
        data = response.json()
        if data.get("error"):
            st.error(f"AI Hatası: {data.get('message')}")
            return None
        return data
    except Exception as e:
        st.error(f"Hata: {e}")
        return None

def get_history(user_id):
    try:
        response = httpx.get(f"{API_BASE_URL}/performance-history?user_id={user_id}")
        return response.json()
    except Exception as e:
        return []

def generate_quiz(progress_id):
    try:
        response = httpx.post(f"{API_BASE_URL}/generate-quiz?progress_id={progress_id}", timeout=60.0)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Sunucu Hatası ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")
        return None

def submit_quiz(user_id, quiz_id, answers):
    try:
        data = {"user_id": user_id, "quiz_id": quiz_id, "answers": answers}
        response = httpx.post(f"{API_BASE_URL}/submit-quiz", json=data)
        return response.json()
    except Exception as e:
        st.error(f"Gönderim Hatası: {e}")
        return None

def get_reports(user_id):
    try:
        response = httpx.get(f"{API_BASE_URL}/reports?user_id={user_id}")
        return response.json()
    except Exception as e:
        return []

def create_report(user_id):
    try:
        response = httpx.post(f"{API_BASE_URL}/generate-weekly-report?user_id={user_id}", timeout=60.0)
        return response.json()
    except Exception as e:
        st.error(f"Rapor Hatası: {e}")
        return None

# App Logic
if st.session_state.page == "Profil":
    st.header("👤 Profil ve Hedef Belirleme")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Ad Soyad", placeholder="Örn: Ali Yılmaz")
            age = st.number_input("Yaş", 5, 100, 25)
            gender = st.selectbox("Cinsiyet", ["Belirtmek İstemiyorum", "Erkek", "Kadın"])
        with col2:
            goal = st.text_input("Öğrenme Hedefi", placeholder="Örn: Modern React Geliştirme")
            level = st.selectbox("Seviye", ["Başlangıç", "Orta", "İleri"])
            daily_time = st.slider("Günlük Süre (dk)", 15, 240, 60)
            style = st.selectbox("Öğrenme Stili", ["Görsel", "İşitsel", "Okuma/Yazma", "Kinestetik"])

        if st.button("🌟 Yolculuğu Başlat", type="primary"):
            if goal and full_name:
                data = {
                    "full_name": full_name,
                    "age": age,
                    "gender": gender,
                    "goal": goal,
                    "level": level,
                    "daily_time": daily_time,
                    "learning_style": style
                }
                with st.spinner("Koçunuz planınızı hazırlıyor..."):
                    profile = create_profile(data)
                    if profile:
                        st.session_state.user_id = profile['id']
                        generate_plan(profile['id'])
                        st.success("Harika! Planınız hazırlandı.")
                        st.session_state.page = "Plan"
                        st.rerun()
            else:
                st.warning("Lütfen ad ve hedef alanlarını doldurun.")

elif st.session_state.page == "Plan":
    st.header("📅 Öğrenme Planınız")
    if not st.session_state.user_id:
        st.info("Lütfen önce profilinizi oluşturun.")
    else:
        plan = get_plan(st.session_state.user_id)
        if plan:
            p_data = plan['plan_data']
            st.subheader(p_data.get('plan_name', 'Haftalık Plan'))
            st.info(f"💡 {p_data.get('overview', '')}")
            
            tab_list, tab_tree = st.tabs(["📋 Liste Görünümü", "🌳 Yetenek Ağacı"])
            
            with tab_list:
                for week in p_data.get('weeks', []):
                    st.markdown(f"### 🗓️ {week.get('week_name', 'Hafta')}")
                    for day in week['days']:
                        with st.container(border=True):
                            c1, c2 = st.columns([3, 1])
                            with c1:
                                st.markdown(f"#### Gün {day['day']}: {day['topic']}")
                                st.markdown("**Görevler:**")
                                for t in day['tasks']: st.markdown(f"- {t}")
                            with c2:
                                st.markdown("**Kaynaklar:**")
                                for r in day['resources']: st.markdown(f"- {r}")
                                st.markdown(f"⏱️ **{day['estimated_minutes']} dk**")
                            
                            # Add a small progress indicator or style it
                            st.markdown('<div style="height: 5px; background: #e2e8f0; border-radius: 10px; margin-top: 10px;"></div>', unsafe_allow_html=True)
                            
            with tab_tree:
                nodes = []
                edges = []
                
                goal_id = "goal"
                nodes.append(Node(id=goal_id, label=p_data.get('plan_name', 'Hedef'), size=30, shape="star", color="#4f46e5"))
                
                for w_idx, week in enumerate(p_data.get('weeks', [])):
                    week_id = f"w_{w_idx}"
                    nodes.append(Node(id=week_id, label=week.get('week_name', f"Hafta {w_idx+1}"), size=25, shape="hexagon", color="#10b981"))
                    edges.append(Edge(source=goal_id, target=week_id))
                    
                    for d_idx, day in enumerate(week['days']):
                        day_id = f"w_{w_idx}_d_{d_idx}"
                        day_label = f"Gün {day['day']}"
                        nodes.append(Node(id=day_id, label=day_label, size=20, shape="dot", color="#3b82f6"))
                        edges.append(Edge(source=week_id, target=day_id))
                        
                        topic_id = f"w_{w_idx}_d_{d_idx}_t"
                        nodes.append(Node(id=topic_id, label=day['topic'], size=15, shape="box", color="#f59e0b"))
                        edges.append(Edge(source=day_id, target=topic_id))

                config = Config(width=800, height=500, directed=True, physics=True, hierarchical=True)
                agraph(nodes=nodes, edges=edges, config=config)
        else:
            st.warning("Henüz bir planınız yok.")
            if st.button("Planı Şimdi Oluştur"):
                generate_plan(st.session_state.user_id)
                st.rerun()

elif st.session_state.page == "İlerleme":
    st.header("📝 Bugün Neler Yaptın?")
    if not st.session_state.user_id:
        st.info("Lütfen önce profilinizi oluşturun.")
    else:
        col_form, col_info = st.columns([2, 1])
        
        with col_info:
            st.markdown("""
            <div style="background: #eef2ff; padding: 1.5rem; border-radius: 15px; border-left: 5px solid var(--primary); margin-bottom: 1rem;">
                <h4 style="margin-top:0">⏱️ Odaklanma Sayacı</h4>
            </div>
            """, unsafe_allow_html=True)
            
            pomo_cols = st.columns(2)
            if pomo_cols[0].button("25 Dk Başlat", use_container_width=True):
                st.session_state.pomodoro_target = 25 * 60
                st.session_state.pomodoro_active = True
            if pomo_cols[1].button("Test (10s)", use_container_width=True):
                st.session_state.pomodoro_target = 10
                st.session_state.pomodoro_active = True
                
            if st.session_state.get('pomodoro_active', False):
                ph = st.empty()
                t = st.session_state.pomodoro_target
                while t > 0:
                    mins, secs = divmod(t, 60)
                    ph.metric("Kalan Süre", f"{mins:02d}:{secs:02d}")
                    time.sleep(1)
                    t -= 1
                ph.success("⏰ Süre Doldu! Hemen raporunu yaz.")
                st.session_state.pomodoro_active = False
                st.balloons()
            
            st.markdown("""
            <div style="background: #f8fafc; padding: 1.5rem; border-radius: 15px; margin-top: 1rem;">
                <h4 style="margin-top:0">✨ Günün Motivasyonu</h4>
                <p style="font-style: italic; color: #4338ca">"Öğrenmek, akıntıya karşı kürek çekmeye benzer; durduğunuz an gerilersiniz."</p>
                <small>- Benjamin Britten</small>
            </div>
            """, unsafe_allow_html=True)
            st.image("https://img.icons8.com/bubbles/200/000000/learning.png")

        with col_form:
            if 'report_key' not in st.session_state:
                st.session_state.report_key = 0
                
            content = st.text_area(
                "Çalışma özetini buraya yaz...", 
                height=200, 
                placeholder="Bugün neler öğrendin? Hangi konuları bitirdin? Zorlandığın yerler oldu mu?",
                key=f"report_content_{st.session_state.report_key}"
            )
            
            if 'last_progress_id' not in st.session_state:
                st.session_state.last_progress_id = None
            if 'current_quiz' not in st.session_state:
                st.session_state.current_quiz = None
            if 'quiz_submitted' not in st.session_state:
                st.session_state.quiz_submitted = False
    
            if st.button("🚀 Analiz Et ve Kaydet", type="primary", use_container_width=True):
                if content:
                    with st.spinner("Koçunuz değerlendiriyor..."):
                        res = submit_progress(st.session_state.user_id, content)
                        if res:
                            st.balloons()
                            st.session_state.last_progress_id = res['progress']['id']
                            st.session_state.current_quiz = None # Reset quiz
                            st.session_state.quiz_submitted = False
                            
                            fb = res['coach_feedback']
                            st.success("Değerlendirme Tamamlandı!")
                            st.markdown(f"### 🤖 Geri Bildirim\n{fb.get('coach_feedback')}")
                            st.info(f"🎯 **Motivasyon:** {fb.get('motivation_message')}")
                else:
                    st.warning("İçerik boş olamaz.")
        
        # Quiz Section Removed as requested

elif st.session_state.page == "Analiz":
    st.header("📊 Performans Analizi")
    if not st.session_state.user_id:
        st.info("Henüz analiz edilecek veri bulunmuyor. Lütfen profilinizi oluşturun.")
    else:
        history = get_history(st.session_state.user_id)
        
        tab1, tab2 = st.tabs(["📈 Performans Grafikleri", "📋 Haftalık Raporlar"])
        
        with tab1:
            if history:
                df = pd.DataFrame(history)
                df['date'] = pd.to_datetime(df['date']).dt.date
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("🎯 Performans Gelişimi")
                    # Line Chart for Performance
                    fig_line = px.line(
                        df, 
                        x='date', 
                        y='performance_score',
                        title="Puan Geçmişi",
                        markers=True,
                        labels={'performance_score': 'Performans Puanı', 'date': 'Tarih'},
                        template="plotly_white"
                    )
                    fig_line.update_traces(line_color='#3b82f6', line_width=3)
                    st.plotly_chart(fig_line, use_container_width=True)
                
                with col2:
                    st.subheader("📊 Dağılım")
                    # Kategorilere ayır
                    df['category'] = pd.cut(df['performance_score'], bins=[0, 50, 80, 100], labels=['Geliştirilmeli', 'İyi', 'Mükemmel'])
                    cat_counts = df['category'].value_counts().reset_index()
                    cat_counts.columns = ['Durum', 'Adet']
                    
                    # Pasta grafiği oluştur
                    fig_pie = px.pie(
                        cat_counts, 
                        values='Adet', 
                        names='Durum', 
                        hole=.4, 
                        color_discrete_sequence=px.colors.sequential.RdBu,
                        template="plotly_white"
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.markdown("""
                <div style="text-align: center; padding: 3rem;">
                    <img src="https://img.icons8.com/bubbles/200/000000/empty-box.png" width="150">
                    <h3>Henüz veri bulunmuyor</h3>
                    <p>Öğrenme yolculuğuna başlamak için ilk ilerleme raporunu 'İlerleme' sekmesinden gönderebilirsin.</p>
                </div>
                """, unsafe_allow_html=True)

        with tab2:
            st.subheader("📝 AI Haftalık Değerlendirmeler")
            if st.button("✨ Yeni Haftalık Rapor Oluştur", type="primary"):
                with st.spinner("Yapay zeka haftanızı analiz ediyor..."):
                    new_report = create_report(st.session_state.user_id)
                    if new_report:
                        st.success("Raporunuz başarıyla oluşturuldu!")
            
            reports = get_reports(st.session_state.user_id)
            if reports:
                for r in reports:
                    with st.expander(f"📅 Rapor: {pd.to_datetime(r['created_at']).strftime('%d.%m.%Y')}"):
                        st.markdown(f"**Özet:**\n{r['summary']}")
                        st.markdown("**Metrikler:**")
                        cols = st.columns(len(r['metrics']))
                        for i, (k, v) in enumerate(r['metrics'].items()):
                            cols[i].metric(k.replace('_', ' ').title(), v)
                        
                        st.markdown("**Öneriler:**")
                        for s in r['suggestions']:
                            st.markdown(f"- {s}")
            else:
                st.markdown("""
                <div style="text-align: center; padding: 2rem; background: #f8fafc; border-radius: 15px;">
                    <img src="https://img.icons8.com/bubbles/100/000000/document.png" width="80">
                    <p>Henüz oluşturulmuş bir haftalık rapor bulunmuyor.</p>
                </div>
                """, unsafe_allow_html=True)

