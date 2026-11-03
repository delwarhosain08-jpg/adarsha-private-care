import streamlit as st
from pathlib import Path
from datetime import datetime
from html import escape
import google.generativeai as genai
import pandas as pd
import plotly.express as px

# ============================================================
# OPTIONAL SUPABASE IMPORT
# ============================================================

try:
    from supabase import create_client, Client
except ImportError:
    create_client = None
    Client = None

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="আদর্শ প্রাইভেট কেয়ার",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ব্রাউজার টাইটেল এবং আইকন পুরোপুরি সেট করার জন্য অতিরিক্ত এইচটিএমএল ট্যাগ
st.markdown("""
    <script>
        document.title = "আদর্শ প্রাইভেট কেয়ার";
    </script>
""", unsafe_allow_html=True)

# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "logo.png"
BANNER_PATH = BASE_DIR / "banner.jpg"

# ============================================================
# COACHING INFORMATION
# ============================================================

COACHING_NAME = "আদর্শ প্রাইভেট কেয়ার"
TAGLINE = "গুণগত শিক্ষা, উজ্জ্বল ভবিষ্যৎ"
EMAIL = "delwarhosain08@gmail.com"
PHONE = "01563148910"
FACEBOOK_URL = "https://www.facebook.com/share/1J55ZjGBqT/"
YOUTUBE_URL = "https://www.youtube.com/@teach.20accademy"
WHATSAPP_URL = "https://wa.me/8801734165721"

# জেমিনি এপিআই কি
GEMINI_API_KEY = "AQ.Ab8RN6Km-jxlHJqpZDHCAt6uYT-VyFnc8ZyYvBSc0_8xtz0KBQ"

# ============================================================
# SUPABASE CONFIGURATION
# ============================================================

DEFAULT_SUPABASE_URL = "https://esjxmccsgttshrlwtljl.supabase.co"
DEFAULT_SUPABASE_KEY = "sb_publishable_Vq8VcCEfjROHeE7PNsT3kw_Nx0aNvvq"

def get_supabase_config():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        if url and key:
            return str(url), str(key)
    except Exception:
        pass
    return DEFAULT_SUPABASE_URL, DEFAULT_SUPABASE_KEY

SUPABASE_URL, SUPABASE_KEY = get_supabase_config()

# ============================================================
# SUPABASE CLIENT
# ============================================================

supabase = None
SUPABASE_CONNECTED = False
SUPABASE_ERROR = None

def initialize_supabase():
    if create_client is None:
        return None, False, "supabase package পাওয়া যায়নি।"
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None, False, "Supabase URL অথবা Key পাওয়া যায়নি।"
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return client, True, None
    except Exception as error:
        return None, False, str(error)

supabase, SUPABASE_CONNECTED, SUPABASE_ERROR = initialize_supabase()

# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state():
    defaults = {
        "logged_in": False,
        "user_role": "guest",
        "user_name": "",
        "user_id": None,
        "selected_class": None,
        "selected_subject": None,
        "page": "🏠 হোম",
        "admin_mode": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# ============================================================
# COMMON HELPERS
# ============================================================

def safe_text(value, default=""):
    if value is None:
        return default
    return escape(str(value))

def format_date(value):
    if not value:
        return ""
    try:
        if isinstance(value, datetime):
            return value.strftime("%d-%m-%Y")
        text = str(value)
        return text[:10]
    except Exception:
        return str(value)

def database_available():
    return supabase is not None and SUPABASE_CONNECTED

# ============================================================
# DATABASE HELPER FUNCTIONS
# ============================================================

def fetch_table(table_name, columns="*", limit=100, order_column=None, descending=True):
    if not database_available():
        return []
    try:
        query = supabase.table(table_name).select(columns)
        if order_column:
            query = query.order(order_column, desc=descending)
        if limit:
            query = query.limit(limit)
        response = query.execute()
        return response.data or []
    except Exception:
        return []

def insert_row(table_name, data):
    if not database_available():
        return False, [], "Supabase connection নেই।"
    try:
        response = supabase.table(table_name).insert(data).execute()
        return True, response.data or [], None
    except Exception as error:
        return False, [], str(error)

# ============================================================
# CUSTOM CSS - ADARSHA PRIVATE CARE
# ============================================================

st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"], .stApp {
        background: #F5F7FB !important;
        background-image: none !important;
        color: #1E293B !important;
    }
    .main { padding-top: 1rem; }
    [data-testid="stHeader"] { background: #F5F7FB !important; }
    [data-testid="stMain"] h1, [data-testid="stMain"] h2, [data-testid="stMain"] h3 {
        color: #172554 !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] {
        background: #202B5C !important;
    }
    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }
    .hero {
        background: linear-gradient(135deg, #243B80, #5145CD, #7C3AED) !important;
        padding: 42px 25px;
        border-radius: 24px;
        color: #FFFFFF !important;
        box-shadow: 0 12px 30px rgba(36, 59, 128, 0.20);
        margin-bottom: 25px;
        text-align: center;
    }
    .hero-title { color: #FFFFFF !important; font-size: 42px; font-weight: 800; margin-bottom: 10px; }
    .hero-subtitle { color: #F8FAFC !important; font-size: 20px; margin: 8px 0; }
    .card, .notice, .info-box {
        background: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #DBE3EF;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
        margin-bottom: 20px;
    }
    .social-button {
        display: block;
        text-align: center;
        padding: 14px;
        margin: 8px 0;
        border-radius: 12px;
        background: #4338CA !important;
        color: #FFFFFF !important;
        text-decoration: none;
        font-weight: 700;
    }
    .social-button:hover { background: #312E81 !important; }
    .stat-card { text-align: center; background: #FFFFFF; padding: 20px; border-radius: 15px; border: 1px solid #DBE3EF; }
    .stat-number { font-size: 32px; font-weight: 800; color: #4338CA !important; }
    .stat-label { color: #475569 !important; font-size: 14px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    if LOGO_PATH.exists():
        try:
            st.image(str(LOGO_PATH), width=150)
        except Exception:
            st.markdown('<div style="text-align:center; font-size:70px;">🎓</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="text-align:center; font-size:70px;">🎓</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <h2 style="color:white !important; text-align:center; font-size:22px;">
            {safe_text(COACHING_NAME)}
        </h2>
        <p style="color:#e0e7ff !important; text-align:center; font-size:14px;">
            {safe_text(TAGLINE)}
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    if SUPABASE_CONNECTED:
        st.success("🟢 Database Connected")
    else:
        st.warning("🟡 Database Offline")

    st.markdown("---")

    menu = st.radio(
        "📌 প্রধান মেনু",
        [
            "🏠 হোম",
            "📚 ক্লাসসমূহ",
            "👨‍🎓 শিক্ষার্থী",
            "👨‍🏫 শিক্ষক",
            "📢 নোটিশ",
            "💬 ছাত্র-ছাত্রী চ্যাট",
            "🤖 এআই লার্নিং কর্নার (EduMagiX)",
            "ℹ আমাদের সম্পর্কে",
            "📞 যোগাযোগ"
        ],
        index=0
    )

    st.session_state["page"] = menu

    st.markdown("---")
    st.markdown('<p style="text-align:center; color:#ffffff !important; font-weight:bold; font-size:13px;">🔗 Quick Links</p>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <a class="social-button" href="{FACEBOOK_URL}" target="_blank">📘 Facebook</a>
        <a class="social-button" href="{YOUTUBE_URL}" target="_blank">▶️ YouTube</a>
        <a class="social-button" href="{WHATSAPP_URL}" target="_blank">💬 WhatsApp</a>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# EDUCATIONAL DATA
# ============================================================

CLASS_DATA = {
    "৬ষ্ঠ শ্রেণি": {
        "icon": "📘",
        "subjects": ["বাংলা", "ইংরেজি", "গণিত", "বিজ্ঞান", "বাংলাদেশ ও বিশ্বপরিচয়", "তথ্য ও যোগাযোগ প্রযুক্তি", "ইসলাম শিক্ষা"],
    },
    "৭ম শ্রেণি": {
        "icon": "📗",
        "subjects": ["বাংলা", "ইংরেজি", "গণিত", "বিজ্ঞান", "বাংলাদেশ ও বিশ্বপরিচয়", "তথ্য ও যোগাযোগ প্রযুক্তি", "ইসলাম শিক্ষা"],
    },
    "৮ম শ্রেণি": {
        "icon": "📙",
        "subjects": ["বাংলা", "ইংরেজি", "গণিত", "বিজ্ঞান", "বাংলাদেশ ও বিশ্বপরিচয়", "তথ্য ও যোগাযোগ প্রযুক্তি", "ইসলাম শিক্ষা"],
    },
    "৯ম শ্রেণি": {
        "icon": "📕",
        "subjects": ["বাংলা", "ইংরেজি", "গণিত", "বিজ্ঞান", "ব্যবসায় উদ্যোগ", "হিসাববিজ্ঞান", "ফিন্যান্স ও ব্যাংকিং", "তথ্য ও যোগাযোগ প্রযুক্তি", "ইসলাম শিক্ষা"],
    },
    "১০ম শ্রেণি": {
        "icon": "📚",
        "subjects": ["বাংলা", "ইংরেজি", "গণিত", "বিজ্ঞান", "ব্যবসায় উদ্যোগ", "হিসাববিজ্ঞান", "ফিন্যান্স ও ব্যাংকিং", "তথ্য ও যোগাযোগ প্রযুক্তি", "ইসলাম শিক্ষা"],
    },
    "SSC": {
        "icon": "🎓",
        "subjects": ["বাংলা", "ইংরেজি", "গণিত", "বিজ্ঞান", "ব্যবসায় উদ্যোগ", "হিসাববিজ্ঞান", "ফিন্যান্স ও ব্যাংকিং", "তথ্য ও যোগাযোগ প্রযুক্তি", "ইসলাম শিক্ষা"],
    },
}

# ============================================================
# PAGE ROUTING
# ============================================================

if menu == "🏠 হোম":
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-title">🎓 {safe_text(COACHING_NAME)}</div>
            <div class="hero-subtitle">{safe_text(TAGLINE)}</div>
            <div class="hero-description">মুখস্থ নয় — বুঝে পড়ার আধুনিক শিক্ষা প্ল্যাটফর্ম</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if BANNER_PATH.exists():
        try:
            st.image(str(BANNER_PATH), use_container_width=True)
        except Exception:
            pass

    st.markdown("## 📊 প্ল্যাটফর্মের তথ্য")
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

    total_classes = len(CLASS_DATA)
    total_subjects = sum(len(item["subjects"]) for item in CLASS_DATA.values())
    student_count = len(fetch_table("students", limit=1000)) if database_available() else 0
    teacher_count = len(fetch_table("teachers", limit=1000)) if database_available() else 0

    with stat_col1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_classes}</div><div class="stat-label">📚 শ্রেণি</div></div>', unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{total_subjects}</div><div class="stat-label">📖 বিষয়</div></div>', unsafe_allow_html=True)
    with stat_col3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{student_count}</div><div class="stat-label">👨‍🎓 শিক্ষার্থী</div></div>', unsafe_allow_html=True)
    with stat_col4:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{teacher_count}</div><div class="stat-label">👨‍🏫 শিক্ষক</div></div>', unsafe_allow_html=True)

elif menu == "📚 ক্লাসসমূহ":
    st.markdown("## 📚 আমাদের ক্লাসসমূহ ও সিলেবাস")
    st.markdown("আদর্শ প্রাইভেট কেয়ারে ৬ষ্ঠ থেকে ১০ম শ্রেণি এবং এসএসসি পর্যন্ত প্রতিটি বিষয়ের জন্য অভিজ্ঞ শিক্ষক দ্বারা পাঠদান করা হয়।")
    st.markdown("---")

    selected_class_name = st.selectbox("একটি শ্রেণি নির্বাচন করুন:", list(CLASS_DATA.keys()))

    if selected_class_name in CLASS_DATA:
        class_info = CLASS_DATA[selected_class_name]
        st.markdown(
            f"""
            <div class="card">
                <h3>{class_info['icon']} {safe_text(selected_class_name)}</h3>
                <p><b>অন্তর্ভুক্ত বিষয়সমূহ:</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )

        subjects = class_info["subjects"]
        cols = st.columns(3)
        for idx, subj in enumerate(subjects):
            with cols[idx % 3]:
                st.info(f"📖 {subj}")

elif menu == "👨‍🎓 শিক্ষার্থী":
    st.markdown("## 👨‍🎓 শিক্ষার্থী তালিকা")
    students = fetch_table("students", limit=50)
    if students:
        df_students = pd.DataFrame(students)
        st.dataframe(df_students, use_container_width=True)
    else:
        st.info("কোনো শিক্ষার্থীর তথ্য পাওয়া যায়নি।")

elif menu == "👨‍🏫 শিক্ষক":
    st.markdown("## 👨‍🏫 শিক্ষক পরিচিতি")
    if Path("111111.jpg").exists():
        st.image("111111.jpg", width=220, caption="আদর্শ প্রাইভেট কেয়ার")
    else:
        st.warning("ছবির ফাইলটি খুঁজে পাওয়া যায়নি।")
    st.markdown("---")
    st.markdown("**শিক্ষকের নাম:** Delwar Hosain")
    st.markdown("**শিক্ষাগত যোগ্যতা:** MBA")
    st.markdown("**প্রতিষ্ঠানের নাম:** আদর্শ প্রাইভেট কেয়ার")

elif menu == "📢 নোটিশ":
    st.markdown("## 📢 প্রাতিষ্ঠানিক নোটিশ বোর্ড")
    notices = fetch_table("notices", order_column="created_at", descending=True)
    if notices:
        for notice in notices:
            st.markdown(
                f"""
                <div class="notice">
                    <h4>{safe_text(notice.get('title'))}</h4>
                    <p>{safe_text(notice.get('content'))}</p>
                    <small style="color: gray;">প্রকাশের তারিখ: {format_date(notice.get('created_at'))}</small>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("এই মুহূর্তে কোনো নতুন নোটিশ নেই।")

elif menu == "💬 ছাত্র-ছাত্রী চ্যাট":
    st.markdown("## 💬 চ্যাট কর্নার")
    st.caption("👨‍🎓 শিক্ষার্থী • 👨‍🏫 শিক্ষক • 👥 বন্ধু")

    col1, col2 = st.columns(2)
    with col1:
        sender_name = st.text_input("👤 আপনার নাম", placeholder="যেমন: আব্দুল্লাহ", key="chat_sender_name")
        sender_role = st.selectbox(
            "আপনার ভূমিকা",
            ["student", "teacher"],
            format_func=lambda x: "👨‍🎓 শিক্ষার্থী" if x == "student" else "👨‍🏫 শিক্ষক",
            key="chat_sender_role"
        )

    with col2:
        recipient_type = st.radio(
            "🎯 প্রাপকের ধরন",
            ["👨‍🏫 শিক্ষক", "👥 বন্ধু"],
            horizontal=True,
            key="chat_recipient_type"
        )
        if recipient_type == "👨‍🏫 শিক্ষক":
            recipient_role = "teacher"
            recipient_name = st.text_input("শিক্ষকের নাম", placeholder="যেমন: করিম স্যার", key="chat_teacher_name").strip()
        else:
            recipient_role = "student"
            recipient_name = st.text_input("বন্ধুর নাম", placeholder="যেমন: রাকিব", key="chat_friend_name").strip()

    sender_clean = sender_name.strip()
    recipient_clean = recipient_name.strip()

    if sender_clean and recipient_clean:
        users = sorted([
            sender_clean.lower().replace(" ", ""),
            recipient_clean.lower().replace(" ", "")
        ])
        conversation_id = f"chat_{users[0]}_{users[1]}"
    else:
        conversation_id = None

    st.markdown("---")

    if not sender_clean or not recipient_clean:
        st.info("ℹ️ চ্যাট দেখতে প্রথমে ওপরের বক্সে **আপনার নাম** এবং **যার সাথে কথা বলবেন তার নাম** লিখুন।")
    else:
        st.markdown(f"### 💬 কথোপকথন: {sender_clean} ⇄ {recipient_clean}")
        
        try:
            result = (
                supabase
                .table("messages")
                .select("*")
                .eq("conversation_id", conversation_id)
                .order("created_at", desc=False)
                .execute()
            )
            messages = result.data or []
        except Exception as e:
            messages = []
            st.error(f"❌ কথোপকথন লোড করতে সমস্যা হয়েছে: {e}")

        chat_box = st.container()
        with chat_box:
            if messages:
                for m in messages:
                    message_sender = str(m.get("sender_name") or m.get("student_name") or "অজানা")
                    message_text = str(m.get("message") or "")
                    message_time = str(m.get("created_at") or "")[:16].replace("T", " ")

                    if message_sender.strip().lower() == sender_clean.lower():
                        st.markdown(f"""
                            <div style="background: #0084ff; color: white; padding: 12px 16px; border-radius: 18px 18px 4px 18px; margin: 4px 0 4px 25%;">
                                <div style="font-size: 15px;">{message_text}</div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.8); text-align: right; margin-top: 4px;">আপনি • {message_time}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        icon = "👨‍🏫" if m.get("sender_role") == "teacher" else "👨‍🎓"
                        st.markdown(f"""
                            <div style="background: #f0f2f5; color: #1c1e21; padding: 12px 16px; border-radius: 18px 18px 18px 4px; margin: 4px 25% 4px 0;">
                                <div style="font-size: 12px; font-weight: bold; color: #444; margin-bottom: 2px;">{icon} {message_sender}</div>
                                <div style="font-size: 15px;">{message_text}</div>
                                <div style="font-size: 10px; color: #65676b; margin-top: 4px;">{message_time}</div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='text-align: center; color: gray;'>এখনো কোনো বার্তা আদান-প্রদান হয়নি। প্রথম বার্তাটি পাঠিয়ে শুরু করুন!</p>", unsafe_allow_html=True)

    st.markdown("---")
    with st.form(key="chat_form", clear_on_submit=True):
        msg = st.text_area("✍️ নতুন বার্তা লিখুন", placeholder="আপনার বার্তা এখানে টাইপ করুন...", height=80, key="chat_message_input")
        submit_btn = st.form_submit_button("📤 বার্তা পাঠান", use_container_width=True)

        if submit_btn:
            if not sender_clean:
                st.warning("⚠️ অনুগ্রহ করে আপনার নাম লিখুন।")
            elif not recipient_clean:
                st.warning("⚠️ যার কাছে পাঠাবেন তার নাম লিখুন।")
            elif not msg.strip():
                st.warning("⚠️ মেসেজ খালি রাখা যাবে না।")
            elif not conversation_id:
                st.error("❌ চ্যাট আইডি তৈরি করা যায়নি।")
            else:
                message_data = {
                    "conversation_id": conversation_id,
                    "student_name": sender_clean if sender_role == "student" else recipient_clean,
                    "sender_name": sender_clean,
                    "sender_role": sender_role,
                    "recipient_name": recipient_clean,
                    "recipient_role": recipient_role,
                    "message": msg.strip()
                }
                try:
                    success, data, err = insert_row("messages", message_data)
                    if success:
                        st.success("✅ বার্তা পাঠানো হয়েছে!")
                        st.rerun()
                    else:
                        st.error(f"❌ পাঠাতে সমস্যা হয়েছে: {err}")
                except Exception as e:
                    st.error(f"❌ সমস্যা হয়েছে: {e}")

eelif menu == "🤖 এআই লার্নিং কর্নার (EduMagiX)":
    st.markdown("## ✨ EduMagiX: কঠিন পড়াশোনা হোক পানির মতো সহজ")
    st.markdown("### পাঠ্যবইয়ের যেকোনো জটিল বিষয়, থিওরি বা সমীকরণ এখানে লিখুন—আপনার পছন্দমতো মোডে এআই সেটি বুঝিয়ে দেবে।")
    
    # আপনার জেমিনি এপিআই কি এখানে বসিয়ে দিন (AIzaSy দিয়ে শুরু হওয়া সঠিক কি)
    GEMINI_API_KEY = "AQ.Ab8RN6Km-jxlHJqpZDHCAt6uYT-VyFnc8ZyYvBSc0_8xtz0KBQ"

    # ৫টি ভিন্ন মোডের জন্য ট্যাব
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📖 গল্পের ছলে (Story Mode)", 
        "📊 গ্রাফ ও চার্ট (Visuals)", 
        "🔍 গভীর বিশ্লেষণ (Analysis)", 
        "📝 সারসংক্ষেপ (Summary)", 
        "⚡ ম্যাথ শর্টকাট (Logic)"
    ])

    # ----------------- ট্যাব ১: গল্পের ছলে শিক্ষা -----------------
    with tab1:
        st.subheader("📖 গল্পের মাধ্যমে যেকোনো জটিল বিষয় বুঝুন")
        topic_story = st.text_area("কোন বিষয়টি গল্প আকারে জানতে চান?", placeholder="যেমন: নিউটনের গতির তৃতীয় সূত্র বা সালোকসংশ্লেষণ...", key="story_input")
        
        if st.button("গল্প তৈরি করুন 🚀", key="btn_story"):
            if topic_story.strip() != "":
                with st.spinner("এআই চমৎকার একটি গল্প বুনছে... ⏳"):
                    try:
                        genai.configure(api_key=GEMINI_API_KEY)
                        model = genai.GenerativeModel('gemini-3.8-flash')
                        prompt = f"Explain '{topic_story}' as a very engaging, simple storytelling format (ELI5) for students in fluent Bengali."
                        response = model.generate_content(prompt)
                        st.success("✅ গল্পের ছলে ব্যাখ্যা:")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"ত্রুটি দেখা দিয়েছে: {e}")
            else:
                st.warning("দয়া করে কিছু একটা লিখুন!")

    # ----------------- ট্যাব ২: গ্রাফ ও ভিজ্যুয়াল চার্ট -----------------
    with tab2:
        st.subheader("📊 ডেটা, গ্রাফ ও ভিজ্যুয়াল চার্টের মাধ্যমে প্রদর্শন")
        topic_chart = st.text_input("কোন বিষয়ের গ্রাফ বা ভিজ্যুয়াল ডেটা দেখতে চান?", placeholder="যেমন: জনসংখ্যার বৃদ্ধি বা গতি বনাম সময়...", key="chart_input")
        
        if st.button("গ্রাফ ও চার্ট জেনারেট করুন 📈", key="btn_chart"):
            if topic_chart.strip() != "":
                with st.spinner("গ্রাফ ও ভিজ্যুয়াল তৈরি হচ্ছে... ⏳"):
                    st.success(f"🎯 **{topic_chart}** এর ভিজ্যুয়াল রিপ্রেজেন্টেশন:")
                    
                    df = pd.DataFrame({
                        'ধাপ বা সময় (Step/Time)': ['ধাপ ১', 'ধাপ ২', 'ধাপ ৩', 'ধাপ ৪', 'ধাপ ৫'],
                        'প্রভাব বা মান (Impact Value)': [20, 45, 70, 90, 100]
                    })
                    
                    fig = px.bar(df, x='ধাপ বা সময় (Step/Time)', y='প্রভাব বা মান (Impact Value)', 
                                 title=f"{topic_chart} - বিশ্লেষণ চার্ট",
                                 color='প্রভাব বা মান (Impact Value)',
                                 color_continuous_scale='sunset')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.info("💡 ইন্টারঅ্যাক্টিভ চার্টের মাধ্যমে বিষয়টি দৃশ্যমান করা হলো।")
            else:
                st.warning("দয়া করে বিষয়ের নাম লিখুন!")

    # ----------------- ট্যাব ৩: গভীর বিশ্লেষণ -----------------
    with tab3:
        st.subheader("🔍 যেকোনো বিষয়ের গভীর ও তাত্ত্বিক বিশ্লেষণ")
        topic_analysis = st.text_area("কোন বিষয়টি গভীরভাবে বিশ্লেষণ করতে চান?", placeholder="যেমন: বাংলাদেশের অর্থনীতি বা কৃত্রিম বুদ্ধিমত্তার প্রভাব...", key="analysis_input")
        
        if st.button("বিশ্লেষণ শুরু করুন 🔍", key="btn_analysis"):
            if topic_analysis.strip() != "":
                with st.spinner("এআই গভীর বিশ্লেষণ তৈরি করছে... ⏳"):
                    try:
                        genai.configure(api_key=GEMINI_API_KEY)
                        model = genai.GenerativeModel('gemini-3.8-flash')
                        prompt = f"Provide a deep, comprehensive, and structured analytical breakdown of '{topic_analysis}' in fluent Bengali."
                        response = model.generate_content(prompt)
                        st.success("✅ গভীর বিশ্লেষণ:")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"ত্রুটি দেখা দিয়েছে: {e}")
            else:
                st.warning("দয়া করে কিছু একটা লিখুন!")

    # ----------------- ট্যাব ৪: সারসংক্ষেপ -----------------
    with tab4:
        st.subheader("📝 পাঠ্যবই বা বড় টপিকের মূল সারসংক্ষেপ (Summary)")
        topic_summary = st.text_area("কোন বড় প্রবন্ধ বা বিষয়ের সারসংক্ষেপ চাচ্ছেন?", placeholder="এখানে বড় কোনো প্যারাগ্রাফ বা বিষয়ের নাম দিন...", key="summary_input")
        
        if st.button("সারসংক্ষেপ তৈরি করুন 📝", key="btn_summary"):
            if topic_summary.strip() != "":
                with st.spinner("সারসংক্ষেপ তৈরি হচ্ছে... ⏳"):
                    try:
                        genai.configure(api_key=GEMINI_API_KEY)
                        model = genai.GenerativeModel('gemini-3.8-flash')
                        prompt = f"Summarize the following topic or text into concise, bullet-point key takeaways in fluent Bengali: '{topic_summary}'"
                        response = model.generate_content(prompt)
                        st.success("✅ মূল সারসংক্ষেপ (Key Takeaways):")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"ত্রুটি দেখা দিয়েছে: {e}")
            else:
                st.warning("দয়া করে কিছু একটা লিখুন!")

    # ----------------- ট্যাব ৫: ম্যাথ ও শর্টকাট অ্যানিমেশন -----------------
    with tab5:
        st.subheader("⚡ ম্যাথ শর্টকাট ও স্টেপ-বাই-স্টেপ লজিক")
        math_problem = st.text_input("কোন ম্যাথ বা শর্টকাট ট্রিক দেখতে চান?", placeholder="যেমন: ১১ দিয়ে গুণ করার শর্টকাট বা বীজগণিতের সূত্র...", key="math_input")
        
        if st.button("লজিক অ্যানিমেশন শুরু করুন 🎮", key="btn_math"):
            if math_problem.strip() != "":
                with st.spinner("ম্যাথ ম্যাজিক লজিক তৈরি হচ্ছে... ⏳"):
                    try:
                        genai.configure(api_key=GEMINI_API_KEY)
                        model = genai.GenerativeModel('gemini-3.8-flash')
                        prompt = f"Explain the math shortcut, tricks, and step-by-step logic for '{math_problem}' in a very simple and clear way in fluent Bengali."
                        response = model.generate_content(prompt)
                        
                        st.success("🎯 পর্দার পেছনের ম্যাজিক লজিক ও শর্টকাট:")
                        st.markdown(response.text)
                        st.balloons()
                    except Exception as e:
                        st.error(f"ত্রুটি দেখা দিয়েছে: {e}")
            else:
                st.warning("দয়া করে কোনো ম্যাথ বা শর্টকাটের নাম লিখুন!")

elif menu == "📞 যোগাযোগ":
    st.markdown("## 📞 যোগাযোগ করুন")
    st.markdown("""
    <div class="card">
        <h3>যোগাযোগের মাধ্যম</h3>
        <p><b>📧 ইমেইল:</b> delwarhosain08@gmail.com</p>
        <p><b>📱 মোবাইল:</b> 01563148910</p>
        <p><b>💬 WhatsApp:</b> <a href="https://wa.me/8801734165721" target="_blank">01734165721 (মেসেজ করতে ক্লিক করুন)</a></p>
        <p><b>📘 ফেসবুক পেজ:</b> <a href="https://www.facebook.com/share/1J55ZjGBqT/" target="_blank">আমাদের ফেসবুক পেজে ভিজিট করুন</a></p>
        <p><b>▶️ ইউটিউব চ্যানেল:</b> <a href="https://www.youtube.com/@teach.20accademy" target="_blank">আমাদের ইউটিউব চ্যানেল</a></p>
    </div>
    """, unsafe_allow_html=True)
