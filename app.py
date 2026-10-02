import streamlit as st

st.set_page_config(
    page_title="আদর্শ প্রাইভেট কেয়ার",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ব্রাউজার টাইটেল এবং আইকন পুরোপুরি সেট করার জন্য অতিরিক্ত এইচটিএমএল ট্যাগ
st.markdown("""
    <script>
        document.title = "আদর্শ প্রাইভেট কেয়ার";
    </script>
""", unsafe_allow_html=True)
# ============================================================
# আদর্শ প্রাইভেট কেয়ার
# Professional Coaching Management System
# Complete Cohesively Fixed Code
# ============================================================

import streamlit as st
from pathlib import Path
from datetime import datetime
from html import escape

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

# ============================================================
# PROJECT PATH
# ============================================================

from pathlib import Path

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


# ============================================================
# SUPABASE CONFIGURATION
# ============================================================

DEFAULT_SUPABASE_URL = "https://esjxmccsgttshrlwtljl.supabase.co"
DEFAULT_SUPABASE_KEY = "sb_publishable_Vq8VcCEfjROHeE7PNsT3kw_Nx0aNvvq"


def get_supabase_config():
    """
    Supabase configuration safely loads from Streamlit secrets
    first and falls back to the current project configuration.
    """
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
    """
    Creates the Supabase client.
    """
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


def show_success(message):
    st.success(f"✅ {message}")


def show_error(message):
    st.error(f"❌ {message}")


def show_warning(message):
    st.warning(f"⚠️ {message}")


def show_info(message):
    st.info(f"ℹ️ {message}")


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


def update_row(table_name, match_column, match_value, data):
    if not database_available():
        return False, [], "Supabase connection নেই।"

    try:
        response = supabase.table(table_name).update(data).eq(match_column, match_value).execute()
        return True, response.data or [], None
    except Exception as error:
        return False, [], str(error)


def delete_row(table_name, match_column, match_value):
    if not database_available():
        return False, "Supabase connection নেই।"

    try:
        supabase.table(table_name).delete().eq(match_column, match_value).execute()
        return True, None
    except Exception as error:
        return False, str(error)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #eef2ff 0%, #fdf2f8 45%, #ecfeff 100%);
    }
    .main {
        padding-top: 1rem;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #312e81 0%, #4f46e5 50%, #7c3aed 100%);
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    h1, h2 {
        font-weight: 800 !important;
    }
    h3 {
        font-weight: 700 !important;
    }
    .hero {
        background: linear-gradient(135deg, #4f46e5, #7c3aed, #db2777);
        padding: 42px 25px;
        border-radius: 28px;
        color: white;
        box-shadow: 0 15px 40px rgba(79,70,229,0.30);
        margin-bottom: 25px;
        text-align: center;
    }
    .hero-title {
        color: white;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        color: #f5f3ff;
        font-size: 20px;
        margin: 8px 0;
    }
    .hero-description {
        color: #ede9fe;
        font-size: 15px;
        margin-top: 15px;
    }
    .card {
        background: rgba(255, 255, 255, 0.97);
        padding: 25px;
        border-radius: 22px;
        box-shadow: 0 8px 28px rgba(0,0,0,0.08);
        border: 1px solid rgba(99,102,241,0.12);
        margin-bottom: 20px;
    }
    .feature {
        background: white;
        padding: 25px;
        min-height: 190px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 7px 25px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }
    .feature-icon {
        font-size: 45px;
        margin-bottom: 10px;
    }
    .contact-card {
        background: linear-gradient(135deg, #ffffff, #f5f3ff);
        padding: 22px;
        min-height: 150px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 7px 22px rgba(0,0,0,0.07);
    }
    .contact-icon {
        font-size: 35px;
    }
    .social-button {
        display: block;
        text-align: center;
        padding: 14px;
        margin: 8px 0;
        border-radius: 12px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
        color: white !important;
        text-decoration: none;
        font-weight: 700;
    }
    .social-button:hover {
        opacity: 0.88;
    }
    .notice {
        background: white;
        border-left: 6px solid #4f46e5;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.06);
    }
    .info-box {
        background: linear-gradient(135deg, #eef2ff, #f5f3ff);
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #ddd6fe;
        margin-bottom: 20px;
    }
    .stat-card {
        background: white;
        padding: 22px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 7px 25px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }
    .stat-number {
        font-size: 32px;
        font-weight: 800;
        color: #4f46e5;
    }
    .stat-label {
        color: #6b7280;
        font-size: 14px;
    }
    .footer {
        text-align: center;
        padding: 35px 20px;
        color: #6b7280;
        font-size: 14px;
        margin-top: 30px;
    }
    @media (max-width: 768px) {
        .hero-title { font-size: 30px; }
        .hero-subtitle { font-size: 16px; }
        .feature { min-height: auto; }
    }
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
            "📊 ফলাফল",
            "💰 ফি ও পেমেন্ট",
            "📚 স্টাডি ম্যাটেরিয়াল",
            "ℹ️️ আমাদের সম্পর্কে",
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
# MAIN PAGE ROUTING & SECTIONS
# ============================================================

if "শিক্ষক" in menu:
    st.markdown("## 👨‍🏫 শিক্ষক পরিচিতি")
    
    # গিটহাবে আপলোড করা আপনার ছবি দেখানোর কোড
    if Path("111111.jpg").exists():
        st.image("111111.jpg", width=220, caption="আদর্শ প্রাইভেট কেয়ার")
    else:
        st.warning("ছবির ফাইলটি খুঁজে পাওয়া যায়নি।")
        
    st.markdown("---")
    st.markdown("**শিক্ষকের নাম:** Delwar Hosain")
    st.markdown("**শিক্ষাগত যোগ্যতা:** MBA")
    st.markdown("**প্রতিষ্ঠানের নাম:** আদর্শ প্রাইভেট কেয়ার")

elif "আমাদের সম্পর্কে" in menu:
    st.markdown("## ℹ️ আমাদের সম্পর্কে")
    st.markdown("""
    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h3>আদর্শ প্রাইভেট কেয়ার</h3>
        <p>গুণগত শিক্ষা এবং একটি উজ্জ্বল ভবিষ্যৎ গঠনে আমরা বদ্ধপরিকর। আমাদের এখানে তৃতীয় থেকে দশম শ্রেণি পর্যন্ত গণিত, ইংরেজি ও ব্যবসায় শিক্ষা বিষয়ে অত্যন্ত যত্নসহকারে পাঠদান করা হয়।</p>
        <p><b>আমাদের লক্ষ্য:</b> প্রতিটি শিক্ষার্থীর মেধার পূর্ণ বিকাশ ঘটানো, প্রতিটি ছাত্র ছাত্রী বেসিক তৈরি করা আমাদের লক্ষ এবং পড়াশোনায় তাদের আত্মবিশ্বাস ফিরিয়ে আনা।</p>
    </div>
    """, unsafe_allow_html=True)

elif "যোগাযোগ" in menu:
    st.markdown("## 📞 যোগাযোগ করুন")
    st.markdown("""
    <div style="background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
        <h3>যোগাযোগের মাধ্যম</h3>
        <p><b>📧 ইমেইল:</b> delwarhosain08@gmail.com</p>
        <p><b>📱 মোবাইল:</b> 01563148910</p>
        <p><b>💬 WhatsApp:</b> <a href="https://wa.me/8801734165721" target="_blank">01734165721 (মেসেজ করতে ক্লিক করুন)</a></p>
        <p><b>📘 ফেসবুক পেজ:</b> <a href="https://www.facebook.com/share/1J55ZjGBqT/" target="_blank">আমাদের ফেসবুক পেজে ভিজিট করুন</a></p>
        <p><b>▶️ ইউটিউব চ্যানেল:</b> <a href="https://www.youtube.com/@teach.20accademy" target="_blank">আমাদের ইউটিউব চ্যানেল</a></p>
    </div>
    """, unsafe_allow_html=True)

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
# HOME PAGE
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

    st.markdown(
        """
        <div class="info-box">
            <h3>🌟 আমাদের শিক্ষা প্ল্যাটফর্মে স্বাগতম</h3>
            <p>আদর্শ প্রাইভেট কেয়ারে শিক্ষার্থীদের মানসম্মত শিক্ষা নিশ্চিত করতে আমরা প্রতিশ্রুতিবদ্ধ।</p>
        </div>
        """,
        unsafe_allow_html=True
    )

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

# 📢 নোটিশ সেকশন হ্যান্ডলিং উদাহরণ (যাতে নোটিশ পেজটি ঠিকভাবে কাজ করে)
elif menu == "📢 নোটিশ":
    st.markdown("## 📢 প্রাতিষ্ঠানিক নোটিশ বোর্ড")
    
    # নোটিশ দেখানোর অংশ
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

    # Custom CSS for Modern Chat UI
    st.markdown("""
        <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            margin-bottom: 10px;
        }
        .chat-bubble-sent {
            background: linear-gradient(135deg, #0084ff 0%, #00c6ff 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin: 4px 0 4px 25%;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            word-wrap: break-word;
        }
        .chat-bubble-received {
            background: #f0f2f5;
            color: #1c1e21;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 4px 25% 4px 0;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            word-wrap: break-word;
        }
        .chat-meta-sent {
            font-size: 10px;
            color: rgba(255, 255, 255, 0.8);
            text-align: right;
            margin-top: 4px;
        }
        .chat-meta-received {
            font-size: 10px;
            color: #65676b;
            text-align: left;
            margin-top: 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    # =====================================================
    # USER INFORMATION & RECIPIENT SELECTION
    # =====================================================
    
    col1, col2 = st.columns(2)
    with col1:
        sender_name = st.text_input(
            "👤 আপনার নাম",
            placeholder="যেমন: আব্দুল্লাহ",
            key="chat_sender_name"
        )
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
            recipient_name = st.text_input(
                "শিক্ষকের নাম",
                placeholder="যেমন: করিম স্যার",
                key="chat_teacher_name"
            ).strip()
        else:
            recipient_role = "student"
            recipient_name = st.text_input(
                "বন্ধুর নাম",
                placeholder="যেমন: রাকিব",
                key="chat_friend_name"
            ).strip()

    sender_clean = sender_name.strip()
    recipient_clean = recipient_name.strip()

    # =====================================================
    # CONVERSATION ID
    # =====================================================
    if sender_clean and recipient_clean:
        users = sorted([
            sender_clean.lower().replace(" ", ""),
            recipient_clean.lower().replace(" ", "")
        ])
        conversation_id = f"chat_{users[0]}_{users[1]}"
    else:
        conversation_id = None

    st.markdown("---")

    # =====================================================
    # CHAT HISTORY & DISPLAY
    # =====================================================
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

        # Container for chat messages view
        chat_box = st.container()
        with chat_box:
            if messages:
                for m in messages:
                    message_sender = str(m.get("sender_name") or m.get("student_name") or "অজানা")
                    message_text = str(m.get("message") or "")
                    message_time = str(m.get("created_at") or "")[:16].replace("T", " ")

                    if message_sender.strip().lower() == sender_clean.lower():
                        # Sent Message
                        st.markdown(f"""
                            <div class="chat-container">
                                <div class="chat-bubble-sent">
                                    <div style="font-size: 15px;">{message_text}</div>
                                    <div class="chat-meta-sent">আপনি • {message_time}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Received Message
                        icon = "👨‍🏫" if m.get("sender_role") == "teacher" else "👨‍🎓"
                        st.markdown(f"""
                            <div class="chat-container">
                                <div class="chat-bubble-received">
                                    <div style="font-size: 12px; font-weight: bold; color: #444; margin-bottom: 2px;">{icon} {message_sender}</div>
                                    <div style="font-size: 15px;">{message_text}</div>
                                    <div class="chat-meta-received">{message_time}</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.markdown("<p style='text-align: center; color: gray;'>এখনো কোনো বার্তা আদান-প্রদান হয়নি। প্রথম বার্তাটি পাঠিয়ে শুরু করুন!</p>", unsafe_allow_html=True)

    # =====================================================
    # MESSAGE INPUT SECTION
    # =====================================================
    st.markdown("---")
    
    with st.form(key="chat_form", clear_on_submit=True):
        msg = st.text_area(
            "✍️ নতুন বার্তা লিখুন",
            placeholder="আপনার বার্তা এখানে টাইপ করুন...",
            height=80,
            key="chat_message_input"
        )
        
        col_btn1, col_btn2 = st.columns([6, 1])
        with col_btn1:
            submit_btn = st.form_submit_button("📤 বার্তা পাঠান", use_container_width=True)

        if submit_btn:
            if not sender_clean:
                st.warning("⚠️ অনুগ্রহ করে আপনার নাম লিখুন।")
            elif not recipient_clean:
                st.warning("⚠️ যার কাছে পাঠাবেন তার নাম লিখুন।")
            elif not msg.strip():
                st.warning("⚠️ মেসেজ খালি রাখা যাবে না।")
            elif not conversation_id:
                st.error("❌ চ্যাট আইডি তৈরি করা যায়নি।")
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
                        st.error(f"❌ পাঠাতে সমস্যা হয়েছে: {err}")
                except Exception as e:
                    st.error(f"❌ সমস্যা হয়েছে: {e}")

# ============================================================
# ক্লাসসমূহ পেজ (এখানে যুক্ত করুন)
# ============================================================
elif menu == "📚 ক্লাসসমূহ":
    st.markdown("## 📚 আমাদের ক্লাসসমূহ ও সিলেবাস")
    st.markdown("আদর্শ প্রাইভেট কেয়ারে ৬ষ্ঠ থেকে ১০ম শ্রেণি এবং এসএসসি পর্যন্ত প্রতিটি বিষয়ের জন্য অভিজ্ঞ শিক্ষক দ্বারা পাঠদান করা হয়।")
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
                st.markdown(
                    f"""
                    <div style="background: white; padding: 15px; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e0e7ff;">
                        <h4 style="color: #4f46e5; margin-bottom: 5px;">📖 {safe_text(subj)}</h4>
                        <p style="font-size: 13px; color: #6b7280;">নিয়মিত ক্লাস ও পরীক্ষা</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("---")
        st.info(f"💡 আপনি যদি **{selected_class_name}** এর রুটিন বা ভর্তি সংক্রান্ত কোনো তথ্য জানতে চান, তবে যোগাযোগ পেজে যোগাযোগ করুন।")

import streamlit as st

# ============================================================
# শিক্ষার্থী পেজ (সম্পূর্ণ কোড)
# ============================================================
if menu == "👨‍🎓 শিক্ষার্থী":
    st.markdown("## 👨‍🎓 শিক্ষার্থী ব্যবস্থাপনা পোর্টাল")
    st.markdown("নতুন শিক্ষার্থী ভর্তি করান এবং ডাটাবেস থেকে সকল শিক্ষার্থীর তালিকা দেখুন।")
    st.markdown("---")

    # ট্যাব তৈরি করা (নতুন ভর্তি এবং তালিকা দেখার জন্য)
    tab1, tab2 = st.tabs(["➕ নতুন শিক্ষার্থী ভর্তি", "📋 শিক্ষার্থীর তালিকা"])

    with tab1:
        st.markdown("### নতুন শিক্ষার্থী নিবন্ধনের ফর্ম")
        with st.form("student_registration_form"):
            col1, col2 = st.columns(2)
            with col1:
                student_name = st.text_input("শিক্ষার্থীর নাম *")
                student_phone = st.text_input("মোবাইল নম্বর")
                guardian_name = st.text_input("অভিভাবকের নাম")
            with col2:
                student_class = st.selectbox("শ্রেণি নির্বাচন করুন *", list(CLASS_DATA.keys()))
                roll_no = st.text_input("রোল নম্বর / আইডি")
                address = st.text_input("ঠিকানা")

            submit_student = st.form_submit_button("শিক্ষার্থী সংরক্ষণ করুন")

            if submit_student:
                if student_name:
                    data = {
                        "name": student_name,
                        "class": student_class,
                        "phone": student_phone,
                        "guardian": guardian_name,
                        "roll": roll_no,
                        "address": address
                    }
                    success, _, err = insert_row("students", data)
                    if success:
                        st.success(f"সফলভাবে **{student_name}**-এর তথ্য সংরক্ষণ করা হয়েছে!")
                    else:
                        st.error(f"তথ্য সংরক্ষণ করতে সমস্যা হয়েছে: {err}")
                else:
                    st.warning("দয়া করে অন্তত শিক্ষার্থীর নাম প্রদান করুন।")

    with tab2:
        st.markdown("### নিবন্ধিত শিক্ষার্থীদের তালিকা")
        students = fetch_table("students", order_column="created_at", descending=True, limit=100)
        
        if students:
            for idx, st_info in enumerate(students, 1):
                with st.container():
                    st.markdown(
                        f"""
                        <div style="background: white; padding: 15px; border-radius: 12px; margin-bottom: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.05); border-left: 5px solid #4f46e5;">
                            <b>#{idx} | নাম:</b> {safe_text(st_info.get('name'))} &nbsp;&nbsp;|&nbsp;&nbsp;
                            <b>শ্রেণি:</b> {safe_text(st_info.get('class'))} &nbsp;&nbsp;|&nbsp;&nbsp;
                            <b>রোল:</b> {safe_text(st_info.get('roll'))} <br>
                            <small style="color: #6b7280;">মোবাইল: {safe_text(st_info.get('phone'))} | অভিভাবক: {safe_text(st_info.get('guardian'))} | ঠিকানা: {safe_text(st_info.get('address'))}</small>
                        </div>
                         """,
                        unsafe_allow_html=True
                    )
        else:
            st.info(
                "ডাটাবেসে এই মুহূর্তে কোনো শিক্ষার্থীর তথ্য জমা নেই। "
                "অনুগ্রহ করে নতুন শিক্ষার্থী ভর্তি করান।"
            )

if menu == "💰 ফি ও পেমেন্ট":

    st.markdown("## 💰 ফি ও পেমেন্ট")
    st.caption(
        "শিক্ষার্থীর মাসিক বেতন, payment history এবং "
        "মাসিক fee document ব্যবস্থাপনা"
    )

    # =====================================================
    # ADMIN / HOST CHECK
    # =====================================================

    user_role = str(st.session_state.get("user_role", "guest")).strip().lower()
    admin_mode = bool(st.session_state.get("admin_mode", False))

    is_host = admin_mode or user_role in [
        "admin",
        "host",
        "administrator",
        "owner",
    ]

    # =====================================================
    # FEE STRUCTURE & MONTHS
    # =====================================================

    FEE_STRUCTURE = {
        "৩য় শ্রেণি": 1500,
        "৪র্থ শ্রেণি": 1500,
        "৫ম শ্রেণি": 1500,
        "৬ষ্ঠ শ্রেণি": 2000,
        "৭ম শ্রেণি": 2000,
        "৮ম শ্রেণি": 2500,
        "৯ম শ্রেণি": 3500,
    }

    MONTHS = [
        "জানুয়ারি",
        "ফেব্রুয়ারি",
        "মার্চ",
        "এপ্রিল",
        "মে",
        "জুন",
        "জুলাই",
        "আগস্ট",
        "সেপ্টেম্বর",
        "অক্টোবর",
        "নভেম্বর",
        "ডিসেম্বর",
    ]

    CURRENT_YEAR = datetime.now().year

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3 = st.tabs(
        ["💳 বেতন গ্রহণ", "📊 বেতন রিপোর্ট", "📁 মাসিক ডকুমেন্ট"]
    )

    # =====================================================
    # TAB 1 — বেতন গ্রহণ
    # =====================================================

    with tab1:

        st.markdown("### 💳 শিক্ষার্থীর বেতন গ্রহণ")

        col1, col2 = st.columns(2)

        with col1:
            student_name = st.text_input(
                "👨‍🎓 শিক্ষার্থীর নাম",
                placeholder="শিক্ষার্থীর পূর্ণ নাম",
                key="fee_student_name",
            )

            class_name = st.selectbox(
                "📚 শ্রেণি", list(FEE_STRUCTURE.keys()), key="fee_class_name"
            )

        with col2:
            fee_month = st.selectbox(
                "📅 কোন মাসের বেতন?", MONTHS, key="fee_month"
            )

            fee_year = st.number_input(
                "📆 বছর",
                min_value=2020,
                max_value=2100,
                value=CURRENT_YEAR,
                step=1,
                key="fee_year",
            )

        amount = FEE_STRUCTURE.get(class_name, 0)

        st.info(
            f"💰 {class_name} এর নির্ধারিত মাসিক বেতন: **৳ {amount:,.0f}**"
        )

        col3, col4 = st.columns(2)

        with col3:
            payment_method = st.selectbox(
                "💳 পেমেন্টের মাধ্যম",
                [
                    "নগদ",
                    "বিকাশ",
                    "নগদ (Nagad)",
                    "রকেট",
                    "ব্যাংক",
                    "অন্যান্য",
                ],
                key="fee_payment_method",
            )

        with col4:
            transaction_id = st.text_input(
                "🔢 Transaction ID (যদি থাকে)",
                placeholder="যেমন: TX123456",
                key="fee_transaction_id",
            )

        note = st.text_area(
            "📝 মন্তব্য",
            placeholder="প্রয়োজনে অতিরিক্ত তথ্য লিখুন...",
            key="fee_note",
        )

        if st.button(
            "✅ বেতন জমা করুন", use_container_width=True, key="save_fee_payment"
        ):

            if not student_name.strip():
                st.warning("⚠️ শিক্ষার্থীর নাম লিখুন।")
            else:
                try:
                    existing = (
                        supabase.table("student_fees")
                        .select("id")
                        .eq("student_name", student_name.strip())
                        .eq("class_name", class_name)
                        .eq("fee_month", fee_month)
                        .eq("fee_year", int(fee_year))
                        .execute()
                    )

                    if existing.data:
                        st.warning(
                            f"⚠️ {student_name.strip()} এর {fee_month} {int(fee_year)} এর payment আগে থেকেই আছে।"
                        )
                    else:
                        payment_data = {
                            "student_name": student_name.strip(),
                            "class_name": class_name,
                            "fee_month": fee_month,
                            "fee_year": int(fee_year),
                            "amount": amount,
                            "payment_status": "Paid",
                            "payment_date": datetime.now().isoformat(),
                            "payment_method": payment_method,
                            "transaction_id": transaction_id.strip(),
                            "note": note.strip(),
                        }

                        success, data, err = insert_row(
                            "student_fees", payment_data
                        )

                        if success:
                            st.success(
                                f"✅ {student_name.strip()} এর {fee_month} মাসের বেতন সফলভাবে জমা হয়েছে।"
                            )
                            st.rerun()
                        else:
                            st.error(f"❌ বেতন সংরক্ষণে সমস্যা: {err}")

                except Exception as e:
                    st.error(f"❌ বেতন যাচাই করতে সমস্যা: {e}")

    # =====================================================
    # TAB 2 — বেতন রিপোর্ট
    # =====================================================

    with tab2:

        st.markdown("### 📊 বেতন রিপোর্ট")

        col1, col2, col3 = st.columns(3)

        with col1:
            report_year = st.number_input(
                "📆 বছর",
                min_value=2020,
                max_value=2100,
                value=CURRENT_YEAR,
                step=1,
                key="report_year",
            )

        with col2:
            report_month = st.selectbox(
                "📅 মাস", ["সব মাস"] + MONTHS, key="report_month"
            )

        with col3:
            report_class = st.selectbox(
                "📚 শ্রেণি",
                ["সব শ্রেণি"] + list(FEE_STRUCTURE.keys()),
                key="report_class",
            )

        try:
            query = (
                supabase.table("student_fees")
                .select("*")
                .eq("fee_year", int(report_year))
            )

            if report_month != "সব মাস":
                query = query.eq("fee_month", report_month)

            if report_class != "সব শ্রেণি":
                query = query.eq("class_name", report_class)

            result = query.order("student_name", desc=False).execute()
            fee_records = result.data or []

        except Exception as e:
            fee_records = []
            st.error(f"❌ রিপোর্ট লোড করতে সমস্যা: {e}")

        if fee_records:
            total_amount = sum(float(r.get("amount") or 0) for r in fee_records)
            total_students = len(fee_records)

            c1, c2 = st.columns(2)
            with c1:
                st.metric("👨‍🎓 মোট Payment", total_students)
            with c2:
                st.metric("💰 মোট আদায়", f"৳ {total_amount:,.0f}")

            st.markdown("---")

            for record in fee_records:
                st.markdown(
                    f"""
                    **👨‍🎓 {record.get('student_name', '')}**
                    
                    📚 শ্রেণি: {record.get('class_name', '')}
                    
                    📅 মাস: {record.get('fee_month', '')} {record.get('fee_year', '')}
                    
                    💰 পরিমাণ: ৳ {float(record.get('amount') or 0):,.0f}
                    
                    💳 মাধ্যম: {record.get('payment_method', '')}
                    
                    🕒 তারিখ: {record.get('payment_date', '')}
                    
                    ---
                    """
                )
        else:
            st.info("📭 এই নির্বাচনের জন্য কোনো payment record পাওয়া যায়নি।")

    # =====================================================
    # TAB 3 — মাসিক ডকুমেন্ট
    # =====================================================

    with tab3:

        st.markdown("### 📁 মাসিক বেতন ডকুমেন্ট")

        if not is_host:
            st.info(
                "🔒 মাসিক বেতন ডকুমেন্ট সংরক্ষণ ও ব্যবস্থাপনা শুধুমাত্র Host/Admin-এর জন্য।"
            )
        else:
            st.success("👑 Admin/Host Mode চালু আছে।")
            st.markdown(
                "আপনি এখানে প্রতি মাসের বেতন সংক্রান্ত PDF, Excel, ছবি বা অন্যান্য document সংরক্ষণ করতে পারবেন।"
            )

            document_title = st.text_input(
                "📄 Document-এর নাম",
                placeholder="যেমন: সেপ্টেম্বর ২০২৬ বেতন হিসাব",
            )

            col1, col2 = st.columns(2)

            with col1:
                document_month = st.selectbox(
                    "📅 মাস", MONTHS, key="document_month"
                )

            with col2:
                document_year = st.number_input(
                    "📆 বছর",
                    min_value=2020,
                    max_value=2100,
                    value=CURRENT_YEAR,
                    step=1,
                    key="document_year",
                )

            uploaded_file = st.file_uploader(
                "📎 বেতন সংক্রান্ত Document আপলোড করুন",
                type=["pdf", "jpg", "jpeg", "png", "xlsx", "xls", "csv", "docx"],
                key="fee_document_upload",
            )

            if st.button(
                "📤 Document সংরক্ষণ করুন",
                use_container_width=True,
                key="save_fee_document",
            ):

                if not document_title.strip():
                    st.warning("⚠️ Document-এর নাম দিন।")
                elif uploaded_file is None:
                    st.warning("⚠️ একটি document নির্বাচন করুন।")
                else:
                    try:
                        file_bytes = uploaded_file.getvalue()
                        file_name = uploaded_file.name
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                        storage_path = f"{int(document_year)}/{document_month}/{timestamp}_{file_name}"

                        supabase.storage.from_("fee-documents").upload(
                            storage_path,
                            file_bytes,
                            {"content-type": uploaded_file.type},
                        )

                        document_data = {
                            "document_title": document_title.strip(),
                            "fee_month": document_month,
                            "fee_year": int(document_year),
                            "file_name": file_name,
                            "file_path": storage_path,
                            "uploaded_by": st.session_state.get(
                                "user_name", "Admin"
                            ),
                        }

                        success, data, err = insert_row(
                            "fee_documents", document_data
                        )

                        if success:
                            st.success(
                                "✅ মাসিক বেতন document সফলভাবে সংরক্ষণ করা হয়েছে।"
                            )
                            st.rerun()
                        else:
                            st.error(
                                f"❌ Document record সংরক্ষণে সমস্যা: {err}"
                            )

                    except Exception as e:
                        st.error(f"❌ Document upload করতে সমস্যা: {e}")

            st.markdown("---")
            st.markdown("### 📚 সংরক্ষিত মাসিক Document")

            try:
                documents = (
                    supabase.table("fee_documents")
                    .select("*")
                    .order("created_at", desc=True)
                    .execute()
                ).data or []
            except Exception as e:
                documents = []
                st.error(f"❌ Document list লোড করতে সমস্যা: {e}")

            if documents:
                for doc in documents:
                    st.markdown(
                        f"""
                        <div style="
                            padding:15px;
                            border-radius:12px;
                            border:1px solid #ddd;
                            margin-bottom:12px;
                            background:#ffffff;
                        ">
                        <b>📄 {safe_text(doc.get('document_title'))}</b>
                        <br><br>
                        📅 মাস: {safe_text(doc.get('fee_month'))} - {safe_text(doc.get('fee_year'))}
                        <br>
                        📎 ফাইল: {safe_text(doc.get('file_name'))}
                        <br>
                        👤 সংরক্ষণ করেছেন: {safe_text(doc.get('uploaded_by'))}
                        <br>
                        🕒 সময়: {safe_text(doc.get('created_at'))}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
 # =========================================================
# 💰 ফি ও পেমেন্ট
# =========================================================

elif menu == "💰 ফি ও পেমেন্ট":

    st.markdown("## 💰 ফি ও পেমেন্ট")

    st.caption(
        "শিক্ষার্থীর মাসিক বেতন, payment history এবং "
        "মাসিক fee document ব্যবস্থাপনা"
    )

    # =====================================================
    # এখানে আপনার Fee & Payment-এর আগের সব code থাকবে
    # =====================================================

    # উদাহরণ: আপনার document section-এর শেষ অংশ
    if documents:

        for doc in documents:

            st.markdown(
                f"""
                <div style="
                    padding:15px;
                    border-radius:12px;
                    border:1px solid #ddd;
                    margin-bottom:12px;
                    background:#ffffff;
                ">

                <b>📄
                {safe_text(doc.get('document_title'))}
                </b>

                <br><br>

                📅 মাস:
                {safe_text(doc.get('fee_month'))}
                -
                {safe_text(doc.get('fee_year'))}

                <br>

                📎 ফাইল:
                {safe_text(doc.get('file_name'))}

                <br>

                👤 সংরক্ষণ করেছেন:
                {safe_text(doc.get('uploaded_by'))}

                <br>

                🕒 সময়:
                {safe_text(doc.get('created_at'))}

                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.info(
            "📭 এখনো কোনো মাসিক document সংরক্ষণ করা হয়নি।"
        )

# =========================================================
# 📚 স্টাডি ম্যাটেরিয়াল
# =========================================================

elif menu == "📚 স্টাডি ম্যাটেরিয়াল":

    st.markdown("## 📚 স্টাডি ম্যাটেরিয়াল")

    st.caption(
        "শিক্ষার্থীদের জন্য শিক্ষণীয় নোট, সূত্র, ছবি ও PDF"
    )

    # -----------------------------------------------------
    # 👑 ADMIN / HOST ACCESS
    # -----------------------------------------------------

    user_role = str(
        st.session_state.get(
            "user_role",
            "admin"
        )
    ).strip().lower()

    admin_mode = bool(
        st.session_state.get(
            "admin_mode",
            True
        )
    )

    # এই অ্যাপের Admin/Host হিসেবে
    # Study Material যোগ করার অনুমতি
    is_host = True

    # -----------------------------------------------------
    # TABS
    # -----------------------------------------------------

    view_tab, add_tab = st.tabs(
        [
            "📖 ম্যাটেরিয়াল দেখুন",
            "➕ নতুন ম্যাটেরিয়াল যোগ করুন"
        ]
    )

    # =====================================================
    # 📖 VIEW
    # =====================================================

    with view_tab:

        st.markdown(
            "### 📖 শিক্ষণীয় ম্যাটেরিয়াল"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            selected_class = st.selectbox(
                "📚 শ্রেণি",
                [
                    "সব শ্রেণি",
                    "৩য় শ্রেণি",
                    "৪র্থ শ্রেণি",
                    "৫ম শ্রেণি",
                    "৬ষ্ঠ শ্রেণি",
                    "৭ম শ্রেণি",
                    "৮ম শ্রেণি",
                    "৯ম শ্রেণি"
                ],
                key="study_view_class"
            )

        with col2:

            selected_subject = st.selectbox(
                "📘 বিষয়",
                [
                    "সব বিষয়",
                    "গণিত",
                    "ইংরেজি",
                    "বাংলা",
                    "বিজ্ঞান",
                    "ICT",
                    "অন্যান্য"
                ],
                key="study_view_subject"
            )

        with col3:

            search_text = st.text_input(
                "🔍 খুঁজুন",
                placeholder="যেমন: বর্গের সূত্র",
                key="study_search"
            )

        # -------------------------------------------------
        # LOAD DATA
        # -------------------------------------------------
        try:

            query = (
                supabase
                .table("study_materials")
                .select("*")
                .order(
                    "created_at",
                    desc=True
                )
            )

            if selected_class != "সব শ্রেণি":

                query = query.eq(
                    "class_name",
                    selected_class
                )

            if selected_subject != "সব বিষয়":

                query = query.eq(
                    "subject",
                    selected_subject
                )

            result = query.execute()

            materials = result.data or []

        except Exception as e:

            materials = []

            st.error(
                f"❌ Study Material লোড করতে সমস্যা হয়েছে: {e}"
            )


        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        if search_text.strip():

            keyword = (
                search_text
                .strip()
                .lower()
            )

            materials = [
                item
                for item in materials
                if (
                    keyword in str(
                        item.get(
                            "title",
                            ""
                        )
                    ).lower()
                    or
                    keyword in str(
                        item.get(
                            "content",
                            ""
                        )
                    ).lower()
                    or
                    keyword in str(
                        item.get(
                            "description",
                            ""
                        )
                    ).lower()
                )
            ]


        # -------------------------------------------------
        # SHOW MATERIAL
        # -------------------------------------------------

        if materials:

            st.success(
                f"📚 মোট {len(materials)}টি "
                "Study Material পাওয়া গেছে।"
            )

            for material in materials:

                st.markdown("---")

                st.markdown(
                    f"## 📖 {safe_text(material.get('title'))}"
                )

                c1, c2, c3 = st.columns(3)

                with c1:

                    st.caption(
                        "📚 শ্রেণি: "
                        + safe_text(
                            material.get(
                                "class_name"
                            )
                        )
                    )

                with c2:

                    st.caption(
                        "📘 বিষয়: "
                        + safe_text(
                            material.get(
                                "subject"
                            )
                        )
                    )

                with c3:

                    st.caption(
                        "📑 ধরন: "
                        + safe_text(
                            material.get(
                                "material_type"
                            )
                        )
                    )


                description = material.get(
                    "description"
                )

                if description:

                    st.info(
                        safe_text(
                            description
                        )
                    )


                image_url = material.get(
                    "image_url"
                )

                if image_url:

                    st.image(
                        image_url,
                        use_container_width=True
                    )


                content = material.get(
                    "content"
                )

                if content:

                    st.markdown(
                        "### 📝 নোট / সূত্র"
                    )

                    st.markdown(
                        content
                    )


                file_url = material.get(
                    "file_url"
                )

                file_name = material.get(
                    "file_name"
                )

                if file_url:

                    st.caption(
                        "📎 "
                        + safe_text(
                            file_name
                        )
                    )

                    st.link_button(
                        "📥 ফাইল দেখুন / Download",
                        file_url,
                        use_container_width=True
                    )

        else:

            st.info(
                "📭 এখনো কোনো Study Material পাওয়া যায়নি।"
            )


    # =====================================================
    # ➕ ADD MATERIAL
    # =====================================================

    with add_tab:

        if not is_host:

            st.warning(
                "🔒 নতুন Study Material যোগ করার "
                "অনুমতি শুধুমাত্র Admin/Host-এর আছে।"
            )

        else:

            st.success(
                "👑 Admin / Host Mode চালু আছে।"
            )

            st.markdown(
                "### ➕ নতুন Study Material যোগ করুন"
            )

            material_title = st.text_input(
                "📖 Material-এর শিরোনাম",
                placeholder="যেমন: বীজগণিতের গুরুত্বপূর্ণ সূত্র",
                key="study_material_title"
            )

            col1, col2 = st.columns(2)

            with col1:

                material_class = st.selectbox(
                    "📚 শ্রেণি",
                    [
                        "৩য় শ্রেণি",
                        "৪র্থ শ্রেণি",
                        "৫ম শ্রেণি",
                        "৬ষ্ঠ শ্রেণি",
                        "৭ম শ্রেণি",
                        "৮ম শ্রেণি",
                        "৯ম শ্রেণি"
                    ],
                    key="study_material_class"
                )

            with col2:

                material_subject = st.selectbox(
                    "📘 বিষয়",
                    [
                        "গণিত",
                        "ইংরেজি",
                        "বাংলা",
                        "বিজ্ঞান",
                        "ICT",
                        "অন্যান্য"
                    ],
                    key="study_material_subject"
                )

            material_type = st.selectbox(
                "📑 ধরন",
                [
                    "সূত্র",
                    "নোট",
                    "অধ্যায়",
                    "প্রশ্ন ও উত্তর",
                    "ছবি",
                    "PDF",
                    "অন্যান্য"
                ],
                key="study_material_type"
            )

            description = st.text_area(
                "📝 সংক্ষিপ্ত বিবরণ",
                key="study_material_description"
            )

            material_content = st.text_area(
                "✍️ মূল লেখা / সূত্র",
                height=400,
                placeholder=(
                    "যেমন:\n\n"
                    "1. (a+b)² = (a-b)² + 4ab\n"
                    "2. (a-b)² = (a+b)² - 4ab\n"
                    "3. a²+b² = (a+b)² - 2ab"
                ),
                key="study_material_content"
            )

            uploaded_image = st.file_uploader(
                "🖼️ শিক্ষণীয় ছবি নির্বাচন করুন",
                type=[
                    "png",
                    "jpg",
                    "jpeg",
                    "webp"
                ],
                key="study_material_image"
            )

            uploaded_file = st.file_uploader(
                "📎 PDF / Document নির্বাচন করুন",
                type=[
                    "pdf",
                    "xlsx",
                    "xls",
                    "docx",
                    "csv"
                ],
                key="study_material_file"
            )


            # -------------------------------------------------
            # SAVE
            # -------------------------------------------------

            if st.button(
                "💾 Study Material সংরক্ষণ করুন",
                use_container_width=True,
                key="save_study_material"
            ):

                if not material_title.strip():

                    st.warning(
                        "⚠️ Material-এর শিরোনাম লিখুন।"
                    )

                elif (
                    not material_content.strip()
                    and uploaded_image is None
                    and uploaded_file is None
                ):

                    st.warning(
                        "⚠️ লেখা, ছবি অথবা PDF/Document "
                        "অন্তত একটি যোগ করুন।"
                    )

                else:

                    try:

                        image_url = None
                        file_url = None
                        file_name = None


                        # =================================
                        # IMAGE
                        # =================================

                        if uploaded_image is not None:

                            image_bytes = (
                                uploaded_image.getvalue()
                            )

                            image_path = (
                                "images/"
                                + datetime.now().strftime(
                                    "%Y%m%d_%H%M%S"
                                )
                                + "_"
                                + uploaded_image.name
                            )

                            supabase.storage.from_(
                                "study-materials"
                            ).upload(
                                image_path,
                                image_bytes,
                                {
                                    "content-type":
                                        uploaded_image.type
                                }
                            )

                            image_url = (
                                supabase.storage
                                .from_(
                                    "study-materials"
                                )
                                .get_public_url(
                                    image_path
                                )
                            )


                        # =================================
                        # FILE
                        # =================================

                        if uploaded_file is not None:

                            file_bytes = (
                                uploaded_file.getvalue()
                            )

                            file_name = (
                                uploaded_file.name
                            )

                            file_path = (
                                "files/"
                                + datetime.now().strftime(
                                    "%Y%m%d_%H%M%S"
                                )
                                + "_"
                                + file_name
                            )

                            supabase.storage.from_(
                                "study-materials"
                            ).upload(
                                file_path,
                                file_bytes,
                                {
                                    "content-type":
                                        uploaded_file.type
                                }
                            )

                            file_url = (
                                supabase.storage
                                .from_(
                                    "study-materials"
                                )
                                .get_public_url(
                                    file_path
                                )
                            )


                        # =================================
                        # DATABASE
                        # =================================

                        material_data = {

                            "title":
                                material_title.strip(),

                            "class_name":
                                material_class,

                            "subject":
                                material_subject,

                            "material_type":
                                material_type,

                            "description":
                                description.strip(),

                            "content":
                                material_content.strip(),

                            "image_url":
                                image_url,

                            "file_url":
                                file_url,

                            "file_name":
                                file_name,

                            "uploaded_by":
                                st.session_state.get(
                                    "user_name",
                                    "Admin"
                                )
                        }


                        success, data, err = insert_row(
                            "study_materials",
                            material_data
                        )


                        if success:

                            st.success(
                                "✅ Study Material "
                                "সফলভাবে সংরক্ষণ করা হয়েছে!"
                            )

                            st.rerun()

                        else:

                            st.error(
                                f"❌ Material সংরক্ষণে সমস্যা: {err}"
                            )


                    except Exception as e:

                        st.error(
                            f"❌ Study Material যোগ করতে সমস্যা: {e}"
                        )

    # =====================================================
    # CHAT HISTORY
    # =====================================================

    if "ai_chat_history" not in st.session_state:

        st.session_state.ai_chat_history = []

    # =====================================================
    # PREVIOUS CHAT
    # =====================================================

    if st.session_state.ai_chat_history:

        st.markdown("### 💬 আগের কথোপকথন")

        for chat in st.session_state.ai_chat_history:

            if chat["role"] == "user":

                with st.chat_message("user"):

                    st.markdown(
                        chat["content"]
                    )

            elif chat["role"] == "assistant":

                with st.chat_message("assistant"):

                    st.markdown(
                        chat["content"]
                    )

    # =====================================================
    # USER QUESTION
    # =====================================================

    user_question = st.chat_input(
        "আপনার প্রশ্ন লিখুন... যেমন: (a+b)² এর সূত্র বুঝিয়ে দাও"
    )

    # =====================================================
    # AI RESPONSE
    # =====================================================

    if user_question:

        # -------------------------------------------------
        # User message দেখানো
        # -------------------------------------------------

        with st.chat_message("user"):

            st.markdown(
                user_question
            )

        # History-তে User message সংরক্ষণ
        st.session_state.ai_chat_history.append(
            {
                "role": "user",
                "content": user_question
            }
        )

# =====================================================
# CHAT CONTROL
# =====================================================

if "ai_chat_history" in st.session_state and st.session_state.ai_chat_history:

    st.markdown("---")

    if st.button(
        "🗑️ কথোপকথন মুছে ফেলুন",
        key="clear_ai_chat"
    ):

        st.session_state.ai_chat_history = []
st.markdown("""
    <style>
    /* অ্যাপের মূল ব্যাকগ্রাউন্ড এবং লেখার কালার ঠিক করার জন্য */
    .stApp {
        background-color: #0e1117; /* একটি সুন্দর গাঢ় (Dark) ব্যাকগ্রাউন্ড */
        color: #ffffff; /* লেখাগুলো সাদা করার জন্য */
    }
    
    /* ইনপুট বক্স বা লেখার ঘরের রঙ স্পষ্ট করার জন্য */
    input, textarea, select {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)
        st.rerun()
