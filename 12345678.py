# =================================================================================
# اسم الملف: MASTER_GRADUATION_GATE_SYSTEM_ULTRA_VERSION_2026.py
# الإصدار: 256.0.0 (النسخة المستقرة - معالجة أخطاء النطاق والمتغيرات الشاملة)
# المبرمج: المساعد الذكي (لصالح الخريج المهندس عبد الله بندر الزهراني)
# التوافق الكامل: Python 3.10, 3.11, 3.12, 3.13 & Streamlit Core 2026
# الكلية: كلية علوم الحاسب والمعلومات - قسم هندسة البرمجيات وتطوير النظم
# الحجم الهيكلي: نظام برميلي ممتد ومعالج للمزامنة وحفظ الحالات الديناميكية
# =================================================================================

import streamlit as st
import numpy as np
import pandas as pd
import time
import json
import os
import base64
import math
import random
import hashlib
from datetime import datetime, timedelta
from io import BytesIO
import requests
import hashlib
def send_telegram_notification(message):
    """دالة مطورة لإرسال التنبيهات الفورية لهاتف المشرف عبر التليجرام مرة واحدة فقط"""
    # تهيئة ذاكرة منع التكرار في الجلسة إن لم تكن موجودة
    if "sent_telegram_hashes" not in st.session_state:
        st.session_state["sent_telegram_hashes"] = set()
        
    # تم وضع التوكن والـ ID الخاصين بك كقيم افتراضية ثابتة
    token = st.session_state.get("tg_bot_token", "7146882882:AAGxRQpq6gK-JP_-VIuYnYkU8P_plXa1zlg")
    chat_id = st.session_state.get("tg_chat_id", "1374850835")
    
    if not token or not chat_id:
        return False
        
    # توليد بصمة فريدة (Hash) لنص الرسالة لمنع تكرارها عند الـ Rerun
    message_hash = hashlib.md5(message.encode('utf-8')).hexdigest()
    
    # إذا كانت الرسالة أُرسلت من قبل في هذه الجلسة، اخرج فوراً دون إرسال مجدد
    if message_hash in st.session_state["sent_telegram_hashes"]:
        return True 
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": f"🔔 *[نظام TITAN - حفل التخرج 2026]*\n\n{message}",
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=4)
        if response.status_code == 200:
            # حفظ بصمة الرسالة بنجاح لمنع تكرارها
            st.session_state["sent_telegram_hashes"].add(message_hash)
            return True
        return False
    except Exception:
        return False
try:
    from streamlit_qrcode_scanner import qrcode_scanner
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False

# محاولة استيراد مكتبة توليد الـ QR Code
try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

# محاولة استيراد مكتبة الماسح الذكي للجوال
try:
    from streamlit_qrcode_scanner import qrcode_scanner
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False


# =================================================================================
# التهيئة العليا لصفحة الموقع (Enterprise Page Configuration)
# =================================================================================
def initialize_ultra_page_framework_configuration():
    st.set_page_config(
        page_title="نظام تتبع الحضور والملاحظات الميدانية الموحد - حفل التخرج 2026",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

initialize_ultra_page_framework_configuration()


# =================================================================================
# محرك الأنماط وتصميم واجهة المستخدم الفاخرة (Cyberpunk Dark Mode CSS UI Engine)
# =================================================================================
def inject_monumental_cyberpunk_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght=300;400;600;700;900&family=Tajawal:wght=300;400;500;700;900&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Cairo', 'Tajawal', sans-serif;
            direction: rtl;
            text-align: right;
        }

        .stApp {
            background: linear-gradient(135deg, #060814 0%, #0b1120 50%, #171138 100%) !important;
            background-attachment: fixed !important;
        }

        .glass-card {
            background: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 22px;
            padding: 26px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            box-shadow: 0 15px 45px rgba(0, 0, 0, 0.6);
            margin-bottom: 22px;
            width: 100%;
            box-sizing: border-box;
        }

        .note-card-critical {
            background: linear-gradient(90deg, rgba(220, 38, 38, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%);
            border-right: 5px solid #ef4444;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        
        .note-card-warning {
            background: linear-gradient(90deg, rgba(245, 158, 11, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%);
            border-right: 5px solid #f59e0b;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        .note-card-success {
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(15, 23, 42, 0.8) 100%);
            border-right: 5px solid #10b981;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 10px;
        }

        p, span, label, .stMarkdown {
            color: #f3f4f6 !important;
            font-weight: 500;
        }

        .stButton>button {
            width: 100% !important;
            border-radius: 14px !important;
            padding: 12px 24px !important;
            background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            transition: all 0.3s ease-in-out;
            border: none !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.4);
        }

        input, select, textarea {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            border-radius: 12px !important;
            background-color: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }

        .camera-floating-overlay-success {
            background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
            border: 2px solid #10b981;
            border-radius: 14px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
            margin-bottom: 15px;
        }

        .camera-floating-overlay-danger {
            background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
            border: 2px solid #ef4444;
            border-radius: 14px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3);
            margin-bottom: 15px;
        }

        .camera-floating-overlay-warning {
            background: linear-gradient(135deg, #78350f 0%, #92400e 100%);
            border: 2px solid #f59e0b;
            border-radius: 14px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(245, 158, 11, 0.3);
            margin-bottom: 15px;
        }

        .graduation-luxury-card {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            border: 2px solid #fbbf24;
            box-shadow: 0 20px 45px rgba(0,0,0,0.7);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

inject_monumental_cyberpunk_styles()


# =================================================================================
# قاعدة البيانات المركزية المشتركة في الذاكرة (Enterprise In-Memory Database Core)
# =================================================================================
@st.cache_resource
def get_monumental_server_shared_database_instance():
    initial_student_dictionary_store = {}
    for student_index in range(1, 601):
        formatted_code_key = f"{student_index:04d}"
        initial_student_dictionary_store[formatted_code_key] = {
            "status": "غائب",
            "notes": [],
            "medical_logs": [],
            "current_location": "خارج القاعة",
            "ticket_assigned": "الأصلية",
            "risk_score": 0.0,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    return {
        "student_db": initial_student_dictionary_store,
        "used_codes": {},  
        "logs": [],
        "it_tickets": [], 
        "staff_session_scans": 0,
        "system_status": "نشط وجاهز"
    }

GLOBAL_SERVER_CORE_DATA = get_monumental_server_shared_database_instance()


# =================================================================================
# محرك إدارة الجلسات والمتغيرات المحلية ومنع تصفير التبويبات عند التحديث
# =================================================================================
def initialize_monumental_browser_session_states():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "last_staff_outcome" not in st.session_state:
        st.session_state.last_staff_outcome = None
    if "last_admin_outcome" not in st.session_state:
        st.session_state.last_admin_outcome = None
    if "last_processed_code" not in st.session_state:
        st.session_state.last_processed_code = ""
    if "ai_start_time" not in st.session_state:
        st.session_state.ai_start_time = datetime.now() - timedelta(minutes=15)
    
    # حفظ التبويبات النشطة حتى لا تضيع عند عمل الـ Rerun للموظف والادمن
    if "staff_current_tab" not in st.session_state:
        st.session_state.staff_current_tab = 0
    if "admin_current_tab" not in st.session_state:
        st.session_state.admin_current_tab = 0

initialize_monumental_browser_session_states()


# =================================================================================
# الثوابت الأمنية الحاكمة وصلاحيات الوصول العليا (Security Guard System)
# =================================================================================
SYSTEM_CAPACITY_LIMIT = 600
ADMIN_ACCESS_SECRET = "adcdiw3Here@"  
STAFF_ACCESS_SECRET = "1234567"       


# =================================================================================
# محرك الذكاء الاصطناعي التنبؤي وتحليل سرعة البوابات (Predictive Flow Analytics Engine)
# =================================================================================
def calculate_monumental_ai_predictions():
    current_total_scanned = len(GLOBAL_SERVER_CORE_DATA["used_codes"])
    
    if current_total_scanned == 0:
        simulated_rate_per_min = 2.0
        estimated_minutes_to_fill = SYSTEM_CAPACITY_LIMIT / simulated_rate_per_min
        congestion_level = "🟢 منخفض (حركة انسيابية ممتازة)"
        predicted_completion_time = (datetime.now() + timedelta(minutes=estimated_minutes_to_fill)).strftime("%H:%M")
    else:
        elapsed_time_delta = datetime.now() - st.session_state.ai_start_time
        elapsed_minutes = max(elapsed_time_delta.total_seconds() / 60.0, 1.0)
        
        simulated_rate_per_min = current_total_scanned / elapsed_minutes
        remaining_students_count = SYSTEM_CAPACITY_LIMIT - current_total_scanned
        
        if simulated_rate_per_min > 0:
            estimated_minutes_to_fill = remaining_students_count / simulated_rate_per_min
        else:
            estimated_minutes_to_fill = 60.0
            
        predicted_completion_time = (datetime.now() + timedelta(minutes=estimated_minutes_to_fill)).strftime("%H:%M")
        
        if simulated_rate_per_min > 10.0:
            congestion_level = "🚨 ذروة تكدس (تطلب تدخل فوري لتوزيع المسارات)"
        elif simulated_rate_per_min > 5.0:
            congestion_level = "🟡 ضغط متوسط (حركة نشطة متسارعة)"
        else:
            congestion_level = "🟢 منخفض (حركة انسيابية)"
            
    return {
        "flow_rate": round(simulated_rate_per_min, 1),
        "minutes_remaining": int(estimated_minutes_to_fill),
        "predicted_time": predicted_completion_time,
        "congestion": congestion_level
    }


# =================================================================================
# معالجة المعاملات وحالات الدخول والتكرار المانعة للتجمد الميداني
# =================================================================================
def add_log_transaction_extended(student_id_code, status_tag, narrative_details, staff_user="ميداني"):
    current_time_stamp_str = datetime.now().strftime("%H:%M:%S")
    GLOBAL_SERVER_CORE_DATA["logs"].insert(0, {
        "التوقيت": current_time_stamp_str,
        "رقم هوية الطالب": student_id_code,
        "الحالة الفنية": status_tag,
        "التفاصيل والبيان": narrative_details,
        "بواسطة": staff_user
    })
    # 🤖 إرسال إشعارات فورية لتليجرام المشرف في الحالات الحرجة فقط لمنع الإزعاج
    if status_tag in ["عارض طبي", "خارج النطاق", "رفض دخول مكرر", "عطل فني"]:
        telegram_msg = f"⚠️ *تنبيه حرج من البوابات الميدانية*\n• *نوع الإجراء:* {status_tag}\n• *المعرف:* {student_id_code}\n• *التفاصيل:* {narrative_details}\n• *بواسطة:* {staff_user} (الساعة {current_time_stamp_str})"
        send_telegram_notification(telegram_msg)

def process_and_verify_scanned_code_extended(raw_input_payload, user_context="staff"):
    if not raw_input_payload:
        return "blank_payload", "يرجى إدخال كود أو رقم هوية صحيح للتأكد."
        
    normalized_code_string = str(raw_input_payload).strip().zfill(4)
    st.session_state.last_processed_code = normalized_code_string
    
    if normalized_code_string not in GLOBAL_SERVER_CORE_DATA["student_db"]:
        add_log_transaction_extended(normalized_code_string, "خارج النطاق", "رقم هوية غير معتمد بالكشوفات الرسمية", user_context)
        return "invalid_entry", f"⚠️ غير معتمد: رقم الهوية ({normalized_code_string}) غير مدرج بالكشوفات!"
        
    student_record = GLOBAL_SERVER_CORE_DATA["student_db"][normalized_code_string]
    
    # معالجة ذكية لحالة العودة من الخروج المؤقت دون إطلاق إنذار التكرار
    if student_record["current_location"] == "خروج مؤقت":
        student_record["current_location"] = "داخل القاعة"
        student_record["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_log_transaction_extended(normalized_code_string, "إعادة دخول", "تمت عودة الطالب إلى القاعة وإلغاء فوت الملاحظة المؤقتة", user_context)
        return "success_entry", f"🔄 أهلاً بعودتك! تم تسجيل إعادة دخول الطالب رقم ({normalized_code_string}) بنجاح."

    if normalized_code_string in GLOBAL_SERVER_CORE_DATA["used_codes"]:
        recorded_prior_timestamp = GLOBAL_SERVER_CORE_DATA["used_codes"][normalized_code_string]
        add_log_transaction_extended(normalized_code_string, "رفض دخول مكرر", f"محاولة عبور مكررة تابعة لتوقيت: {recorded_prior_timestamp}", user_context)
        return "duplicate_entry", f"🚨 تذكرة مكررة مسبقاً! عبر البوابات الساعة {recorded_prior_timestamp}."
        
    exact_processing_time = datetime.now().strftime("%H:%M:%S")
    GLOBAL_SERVER_CORE_DATA["used_codes"][normalized_code_string] = exact_processing_time
    student_record["status"] = "حاضر"
    student_record["current_location"] = "داخل القاعة"
    student_record["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    GLOBAL_SERVER_CORE_DATA["staff_session_scans"] += 1
    
    add_log_transaction_extended(normalized_code_string, "مصرح بالدخول", "تم تأكيد صلاحية الكارت وإثبات الحضور بنجاح وصفرية المخاطر", user_context)
    return "success_entry", f"🟢 مصرح بالدخول! تم تسجيل حضور رقم الهوية ({normalized_code_string}) بنجاح."


def generate_monumental_qr_image(student_code_id):
    if QRCODE_AVAILABLE:
        qr_object_instance = qrcode.QRCode(version=1, box_size=10, border=2)
        qr_object_instance.add_data(student_code_id)
        qr_object_instance.make(fit=True)
        img_buffer_holder = qr_object_instance.make_image(fill_color="#1e1b4b", back_color="#ffffff")
        bytes_io_stream = BytesIO()
        img_buffer_holder.save(bytes_io_stream, format="PNG")
        return base64.b64encode(bytes_io_stream.getvalue()).decode()
    else:
        dummy_svg_avatar = f"""<svg width="150" height="150"><rect width="150" height="150" fill="#ffffff"/><text x="75" y="80" fill="#000" text-anchor="middle">{student_code_id}</text></svg>"""
        return base64.b64encode(dummy_svg_avatar.encode()).decode()


# =================================================================================
# نظام محاكاة البيانات وحقن الكشوفات الوهمية للمناقشة
# =================================================================================
def execute_bulk_ai_simulation_data(attended_count, notes_count):
    all_keys = list(GLOBAL_SERVER_CORE_DATA["student_db"].keys())
    random.shuffle(all_keys)
    
    # 1. محاكاة الحضور
    attended_keys = all_keys[:attended_count]
    for k in attended_keys:
        if k not in GLOBAL_SERVER_CORE_DATA["used_codes"]:
            exact_time = (datetime.now() - timedelta(minutes=random.randint(1, 45))).strftime("%H:%M:%S")
            GLOBAL_SERVER_CORE_DATA["used_codes"][k] = exact_time
            GLOBAL_SERVER_CORE_DATA["student_db"][k]["status"] = "حاضر"
            GLOBAL_SERVER_CORE_DATA["student_db"][k]["current_location"] = "داخل القاعة"
            
    # 2. محاكاة الملاحظات الميدانية
    notes_keys = all_keys[attended_count:attended_count+notes_count]
    note_types_pool = ["خروج مؤقت للضرورة", "حالة خاصة / VIP", "مشكلة تذكرية / كارت تالف", "ملاحظة عامة"]
    note_texts_pool = ["خرج لإحضار عائلته من المواقف", "طالب متفوق - تكريم خاص من العميد", "الكارت تالف وتم إدخاله يدوياً", "مرافق مع ذوي الاحتياجات الخاصة"]
    
    for k in notes_keys:
        if k not in GLOBAL_SERVER_CORE_DATA["used_codes"]:
            GLOBAL_SERVER_CORE_DATA["used_codes"][k] = datetime.now().strftime("%H:%M:%S")
        
        GLOBAL_SERVER_CORE_DATA["student_db"][k]["status"] = "حاضر"
        n_type = random.choice(note_types_pool)
        n_text = random.choice(note_texts_pool)
        
        if n_type == "خروج مؤقت للضرورة":
            GLOBAL_SERVER_CORE_DATA["student_db"][k]["current_location"] = "خروج مؤقت"
            n_text = "خرج مؤقتاً لدورات المياه / المرفقات"
            
        compiled_note = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": n_type,
            "text": n_text
        }
        GLOBAL_SERVER_CORE_DATA["student_db"][k]["notes"].append(compiled_note)


# =================================================================================
# بوابة التوثيق الأمني الرقمي الموحد (Unified Secure Gate Access)
# =================================================================================
if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align: center; max-width: 550px; margin: 0 auto; background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px); padding: 35px; border-radius: 24px; border: 1px solid rgba(99, 102, 241, 0.25); box-shadow: 0 25px 55px rgba(0, 0, 0, 0.7);'>
            <div style='font-size: 60px; margin-bottom: 12px;'>🎓</div>
            <h1 style='font-size: 24px; margin-bottom: 4px; font-weight: 900; color: #ffffff;'>منصة التحقق الرقمية الفيدرالية الموحدة</h1>
            <p style='color: #38bdf8 !important; font-size: 14px; font-weight: 600; margin-bottom: 20px;'>نظام إدارة الحفل وإثبات الملاحظات الميدانية المزامنة (2026)</p>
            <p style='color: #9ca3af !important; font-size: 12px;'>تطوير وتصميم الطالب: عبد الله بندر الزهراني</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("<div style='max-width:550px; margin:0 auto; padding-top: 20px;'>", unsafe_allow_html=True)
    entered_secure_secret = st.text_input("مفتاح المرور المعتمد للدخول بالمنصة الفيدرالية:", type="password", placeholder="أدخل رمز الموظف (1234567) أو المشرف المسؤول...")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🔐 تسجيل الدخول والتوثيق الأمني الفوري", use_container_width=True):
        if entered_secure_secret == ADMIN_ACCESS_SECRET:
            st.session_state.authenticated = True
            st.session_state.user_role = "admin"
            st.toast("🎉 تم التوثيق كـ مشرف عام للنظام بنجاح باهر!", icon="🚀")
            time.sleep(0.1)
            st.rerun()
        elif entered_secure_secret == STAFF_ACCESS_SECRET:
            st.session_state.authenticated = True
            st.session_state.user_role = "staff"
            st.toast("🎯 تم التوثيق كـ موظف مسح ميداني بنجاح مستقر!", icon="⚡")
            time.sleep(0.1)
            st.rerun()
        else:
            st.markdown('<div class="camera-floating-overlay-danger"><h4 style="margin:0; color:#fff;">❌ خطأ أمني: رمز المرور المدخل غير صحيح! يرجى إعادة التأكد.</h4></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =================================================================================
# واجهة الموظف الميداني المتقدمة الشاملة (Staff Operations & Field Notes Hub)
# =================================================================================
if st.session_state.user_role == "staff":
    st.markdown(
        """
        <div class='glass-card' style='background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(23, 23, 67, 0.95) 100%); text-align: center; padding: 18px; border-color: #6366f1;'>
            <h2 style='margin:0; font-size: 22px; color: #ffffff;'>🎯 بوابة العمليات والملاحظات الرقمية للموظف الميداني</h2>
            <p style='margin:4px 0 0 0; color:#38bdf8 !important; font-size:13px;'>سيرفر مركزي متزامن - رصد تحركات الطلاب، حالات الخروج المؤقت، والبلاغات الميدانية</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # شريط مؤشرات الأداء اللحظي
    staff_col1, staff_col2, staff_col3, staff_col4 = st.columns(4)
    with staff_col1:
        st.metric("✅ إجمالي الطلاب الحاضرين", f"{len(GLOBAL_SERVER_CORE_DATA['used_codes'])} / 600")
    with staff_col2:
        current_temp_out = sum(1 for s in GLOBAL_SERVER_CORE_DATA["student_db"].values() if s["current_location"] == "خروج مؤقت")
        st.metric("🚶‍♂️ خروج مؤقت حالياً", f"{current_temp_out} خريجين")
    with staff_col3:
        st.metric("📸 مسحاتك في الجلسة الحالية", f"{GLOBAL_SERVER_CORE_DATA['staff_session_scans']} كارت")
    with staff_col4:
        st.metric("🛠️ بلاغات النظام التقنية", f"{len(GLOBAL_SERVER_CORE_DATA['it_tickets'])} بلاغ")

    st.markdown("<br>", unsafe_allow_html=True)
    
    staff_sub_tabs = st.tabs([
        "📷 ماسح الكاميرا والتحقق السريع", 
        "📝 نظام إدارة الملاحظات وتتبع الطلاب", 
        "🔍 مستعلم الهويات والتحكم الميداني",
        "🏥 الحالات الطبية والطارئة بالقاعة",
        "⚙️ بلاغات الأعطال التقنية للبوابة"
    ])
    
    # --- النظام الفرعي 1: الكاميرا وماسح الأكواد اليدوي التلقائي المانع للتكرار ---
 # --- النظام الفرعي 1: الكاميرا وماسح الأكواد اليدوي التلقائي المانع للتكرار ---
# --- النظام الفرعي 1: الكاميرا وماسح الأكواد المطور والتلقائي المانع للتكرار ---
    with staff_sub_tabs[0]:
        st.markdown("### 📷 وحدة التدقيق البصري وماسح الكروت الحي المطور")
        
        # عرض نتيجة المسح الأخيرة بشكل بارز في الأعلى
        if st.session_state.last_staff_outcome:
            status_res, text_res = st.session_state.last_staff_outcome
            if status_res == "success_entry":
                st.markdown(f'<div class="camera-floating-overlay-success"><h4>🟢 مصرح بالدخول وثبت الحضور</h4><p>{text_res}</p></div>', unsafe_allow_html=True)
            elif status_res == "duplicate_entry":
                st.markdown(f'<div class="camera-floating-overlay-danger"><h4>🚨 تنبيه: محاولة عبور تذكرة مكررة!</h4><p>{text_res}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="camera-floating-overlay-warning"><h4>⚠️ تنبيه إداري مؤقت</h4><p>{text_res}</p></div>', unsafe_allow_html=True)
                
        # تقسيم الواجهة لعرض المسح الذكي بجانب التعليمات الميدانية
        cam_col1, cam_col2 = st.columns([2, 1])
        
        with cam_col1:
            st.markdown("#### 🎥 عدسة مسح الـ QR الذكية")
            lens_active = st.toggle("⚙️ تفعيل البث المباشر للكاميرا وقراءة الكروت فوراً", value=True, key="lens_active_toggle")
            
            if lens_active:
                if SCANNER_AVAILABLE:
                    try:
                        # تشغيل الماسح بشكل مستمر ومباشر
                        scanned_payload = qrcode_scanner(key='ultra_gate_live_scanner_2026')
                        
                        if scanned_payload:
                            # تنظيف المدخلات وتحويلها لتنسيق 4 خانات
                            cleaned_code = str(scanned_payload).strip().zfill(4)
                            
                            # شرط هام لمنع حلقة التكرار اللانهائية لنفس الكود المفحوص
                            if cleaned_code != st.session_state.last_processed_code:
                                r_key, r_msg = process_and_verify_scanned_code_extended(cleaned_code, "staff")
                                st.session_state.last_staff_outcome = (r_key, r_msg)
                                st.toast(f"تمت معالجة الكود: {cleaned_code}", icon="⚡")
                                time.sleep(0.4) # مهلة بسيطة لاستقرار المعالجة
                                st.rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء تشغيل الكاميرا: {str(e)}")
                else:
                    st.warning("⚠️ مكتبة `streamlit_qrcode_scanner` غير مثبتة في البيئة الحالية. سيتم الاعتماد على المسح السريع أدناه.")

        with cam_col2:
            st.markdown("#### 💡 تعليمات العبور الذكي")
            st.info("""
            * **التلقائية:** ضع كود الـ QR أمام الكاميرا، وسيقوم النظام باعتماده فوراً دون الحاجة لضغط أي زر.
            * **تصفير الحالة:** الإشعار بالأعلى يتغير تلقائياً مع كل خريج جديد يعبر البوابة.
            * **الخروج المؤقت:** إذا كان الطالب مسجلاً (خروج مؤقت)، سيتعرف النظام عليه ويعيده كـ (حاضر) تلقائياً.
            """)

        st.markdown("---")
        st.markdown("#### ⌨️ المسح الليزري السريع / الإدخال اليدوي المباشر")
        st.caption("ملاحظة: هذا الحقل مبرمج ليعمل تلقائياً فوراً عند استخدام مسدس المسح (Barcode Scanner) دون الحاجة للنقر على زر إرسال.")
        
        # حقل ذكي خارج الـ Form ليعمل بمجرد إدخال القيمة (مفيد جداً لمسدسات القراءة الليزرية)
        typed_code = st.text_input(
            "وجه قارئ الليزر هنا أو اكتب الرقم يدوياً (ثم اضغط Enter):", 
            placeholder="مثال: 0045", 
            key="instant_manual_scan_field"
        )
        
        if typed_code:
            cleaned_typed = typed_code.strip().zfill(4)
            r_key, r_msg = process_and_verify_scanned_code_extended(cleaned_typed, "staff")
            st.session_state.last_staff_outcome = (r_key, r_msg)
            # تفريغ الحقل فوراً للاستعداد للقراءة التالية
            st.rerun()
    # --- النظام الفرعي 2: نظام إدارة الملاحظات وتتبع الطلاب ---
    with staff_sub_tabs[1]:
        st.markdown("### 📝 وحدة إثبات وتتبع الملاحظات الميدانية الفورية")
        
        note_layout_col1, note_layout_col2 = st.columns([1, 2])
        with note_layout_col1:
            st.markdown("#### 🛠️ تدوين ملاحظة جديدة على خريج")
            target_id = st.number_input("رقم الطالب المستهدف (1-600):", min_value=1, max_value=600, step=1, value=1, key="note_tgt")
            formatted_tgt = f"{target_id:04d}"
            
            note_classification = st.selectbox(
                "تصنيف الإجراء الميداني الفوري:",
                ["خروج مؤقت للضرورة", "حالة خاصة / VIP", "مشكلة تذكرية / كارت تالف", "ملاحظة عامة"],
                key="note_class_select"
            )
            note_narrative = st.text_area("تفاصيل وتبرير الحالة الميدانية:", placeholder="اكتب هنا التفاصيل...", key="note_narrative_input")
            
            if st.button("💾 تثبيت الملاحظة وتحديث حالة الموقع", use_container_width=True, key="save_note_btn"):
                if note_narrative:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    new_note = {
                        "time": current_time,
                        "type": note_classification,
                        "text": note_narrative
                    }
                    GLOBAL_SERVER_CORE_DATA["student_db"][formatted_tgt]["notes"].append(new_note)
                    
                    if note_classification == "خروج مؤقت للضرورة":
                        GLOBAL_SERVER_CORE_DATA["student_db"][formatted_tgt]["current_location"] = "خروج مؤقت"
                        add_log_transaction_extended(formatted_tgt, "خروج مؤقت", f"تم تسجيل خروج مؤقت: {note_narrative}", "ميداني")
                    else:
                        add_log_transaction_extended(formatted_tgt, "ملاحظة ميدانية", f"[{note_classification}] - {note_narrative}", "ميداني")
                        
                    st.toast(f"🎉 تم ربط الملاحظة بنجاح بالطالب {formatted_tgt}", icon="📝")
                    time.sleep(0.1)
                    st.rerun()
                else:
                    st.error("⚠️ يرجى تدوين النص لتبرير الملاحظة.")
                    
        with note_layout_col2:
            st.markdown("#### 📋 قائمة الملاحظات والتحركات النشطة حالياً بالقاعة")
            active_notes_list = []
            for s_id, s_info in GLOBAL_SERVER_CORE_DATA["student_db"].items():
                if s_info["notes"] or s_info["current_location"] == "خروج مؤقت":
                    last_note_text = s_info["notes"][-1]["text"] if s_info["notes"] else "لا توجد ملاحظات نصية مقيدة"
                    last_note_type = s_info["notes"][-1]["type"] if s_info["notes"] else "طبيعي"
                    active_notes_list.append({
                        "رقم الطالب": s_id,
                        "حالة الحضور": s_info["status"],
                        "الموقع الحالي": s_info["current_location"],
                        "نوع الإجراء": last_note_type,
                        "بيان تفصيل الملاحظة": last_note_text,
                        "تحديث": s_info["last_update"]
                    })
                    
            if active_notes_list:
                st.dataframe(pd.DataFrame(active_notes_list), use_container_width=True, hide_index=True)
            else:
                st.markdown("<div style='text-align:center; padding:30px; color:#9ca3af;'>لا توجد ملاحظات استثنائية نشطة حالياً.</div>", unsafe_allow_html=True)

    # --- النظام الفرعي 3: مستعلم الهويات السريع والتحكم الفردي ---
    with staff_sub_tabs[2]:
        st.markdown("### 🔍 وحدة الفحص الشامل والتحكم الفردي الفوري")
        search_id = st.text_input("أدخل رقم كود التذكرة للفحص الفوري وعرض الأرشيف الميداني:", placeholder="مثال: 0012", key="staff_search_view_input")
        
        if search_id:
            fmt_search = search_id.strip().zfill(4)
            if fmt_search in GLOBAL_SERVER_CORE_DATA["student_db"]:
                std_rec = GLOBAL_SERVER_CORE_DATA["student_db"][fmt_search]
                
                st.markdown(f"<div class='glass-card' style='border-right: 4px solid #38bdf8;'>", unsafe_allow_html=True)
                sc_1, sc_2, sc_3 = st.columns(3)
                with sc_1:
                    st.markdown(f"🆔 **معرف التذكرة:** `{fmt_search}`")
                    st.markdown(f"📊 **حالة الحضور:** `{std_rec['status']}`")
                with sc_2:
                    st.markdown(f"📍 **الموقع اللوجستي:** `{std_rec['current_location']}`")
                    st.markdown(f"📅 **آخر حركة بالنظام:** `{std_rec['last_update']}`")
                with sc_3:
                    if std_rec["current_location"] == "خروج مؤقت":
                        if st.button("🟢 تأكيد العودة يدويًا الآن", key=f"btn_ret_{fmt_search}"):
                            std_rec["current_location"] = "داخل القاعة"
                            std_rec["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            add_log_transaction_extended(fmt_search, "إعادة دخول", "تم إثبات العودة يدويًا من لوحة التحكم السريع", "ميداني")
                            st.toast("تمت إعادة الطالب لوضع الحضور داخل القاعة بنجاح!", icon="✅")
                            time.sleep(0.1)
                            st.rerun()
                    elif std_rec["status"] == "حاضر" and std_rec["current_location"] == "داخل القاعة":
                        if st.button("🚨 تسجيل خروج طارئ / مؤقت فوري", key=f"btn_out_{fmt_search}"):
                            std_rec["current_location"] = "خروج مؤقت"
                            std_rec["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            add_log_transaction_extended(fmt_search, "خروج مؤقت", "تسجيل خروج مؤقت يدوي من لوحة التحكم السريع", "ميداني")
                            st.toast("تم تسجيل خروج الطالب مؤقتاً بنجاح!", icon="🚶‍♂️")
                            time.sleep(0.1)
                            st.rerun()
                            
                st.markdown("---")
                st.markdown("#### 📜 سجل الملاحظات التاريخي المتراكم:")
                if std_rec["notes"]:
                    for n in std_rec["notes"]:
                        st.markdown(f"• `[{n['time']}]` **({n['type']})**: {n['text']}")
                else:
                    st.caption("لا توجد ملاحظات تاريخية مقيدة على هذا الرقم حتى الآن.")
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.error("❌ المعرف غير مدرج في كشوفات الـ 600 طالب الرسمية!")

    # --- النظام الفرعي 4: نظام التدقيق الطبي والإسعافات الأولية بالقاعة ---
    with staff_sub_tabs[3]:
        st.markdown("### 🏥 وحدة تسجيل البلاغات الحيوية والطبية الطارئة")
        
        med_col1, med_col2 = st.columns([1, 2])
        with med_col1:
            med_id = st.number_input("رقم الطالب المصاب بعارض صحي:", min_value=1, max_value=600, value=1, key="med_id_input")
            fmt_med_id = f"{med_id:04d}"
            med_severity = st.selectbox("درجة خطورة الحالة الحالية:", ["🔴 حرجة جداً (طلب إسعاف فوري)", "🟡 متوسطة (دوار / إرهاق)", "🟢 بسيطة (تم التعامل معها)"])
            med_desc = st.text_area("تفاصيل العارض الطبي والوضع الحالي:", placeholder="مثال: هبوط في الضغط...")
            
            if st.button("🚑 إرسال بلاغ طبي عاجل لغرفة المشرفين", use_container_width=True):
                if med_desc:
                    med_entry = {
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "severity": med_severity,
                        "desc": med_desc
                    }
                    GLOBAL_SERVER_CORE_DATA["student_db"][fmt_med_id]["medical_logs"].append(med_entry)
                    add_log_transaction_extended(fmt_med_id, "عارض طبي", f"[{med_severity}] - {med_desc}", "ميداني")
                    st.success("🚨 تم ترحيل البلاغ الطبي بنجاح لغرفة المراقبة العليا.")
                    time.sleep(0.1)
                    st.rerun()
        with med_col2:
            st.markdown("#### 📋 سجل الحالات الطبية المرصودة بالقاعة")
            med_records = []
            for s_id, s_info in GLOBAL_SERVER_CORE_DATA["student_db"].items():
                if s_info["medical_logs"]:
                    for m in s_info["medical_logs"]:
                        med_records.append({
                            "رقم الخريج": s_id,
                            "التوقيت": m["time"],
                            "مستوى الخطورة": m["severity"],
                            "تفاصيل البيان الطبي": m["desc"]
                        })

            if med_records:
                st.dataframe(pd.DataFrame(med_records), use_container_width=True, hide_index=True)
            else:
                st.caption("👍 لا توجد بلاغات طبية طارئة مسجلة حتى اللحظة.")


    # --- النظام الفرعي 5: نظام بلاغات الأعطال التقنية للبوابات ---
    with staff_sub_tabs[4]:
        st.markdown("### ⚙️ وحدة الدعم الفني وبلاغات البوابات الميدانية")
        
        with st.form(key="it_ticket_form", clear_on_submit=True):
            gate_num = st.selectbox("بوابة العطل الحالية:", ["البوابة الرئيسية الأولى", "بوابة الخريجين الثانية", "ممر كبار الشخصيات VIP"])
            issue_type = st.selectbox("نوع المشكلة التقنية:", ["فقدان الاتصال بالسيرفر المركزي", "كاميرا المسح لا تستجيب", "بطء شديد في تحميل واجهة الاستعلام", "أخرى"])
            issue_desc = st.text_area("وصف مفصل للعطل الفني:")
            submit_ticket = st.form_submit_button("📡 إرسال بلاغ الدعم الفني الفوري للشبكة")
            
            if submit_ticket and issue_desc:
                ticket_payload = {
                    "gate": gate_num,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "type": issue_type,
                    "desc": issue_desc,
                    "status": "قيد المراجعة الفنية"
                }
                GLOBAL_SERVER_CORE_DATA["it_tickets"].append(ticket_payload)
                send_telegram_notification(f"🛠️ *بلاغ عطل تقني جديد*\n• *الموقع:* {gate_num}\n• *نوع المشكلة:* {issue_type}\n• *الوصف:* {issue_desc}")

                st.toast("⚡ تم رفع التذكرة لقسم هندسة البرمجيات والشبكات بالموقع", icon="🛠️")
                time.sleep(0.1)
                st.rerun()

    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("🚪 تسجيل الخروج الآمن وإنهاء الجلسة الميدانية للموظف"):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.last_staff_outcome = None
        st.session_state.last_processed_code = ""
        st.rerun()
    st.stop()


# =================================================================================
# لوحة التحكم الإدارية والمراقبة العليا للمشرف العام (Admin Operations Dashboard)
# =================================================================================
if st.session_state.user_role == "admin":
    with st.sidebar:
        st.markdown("""<div style='text-align: center;'><h2>👑 لوحة الإشراف العليا</h2><p style='color:#38bdf8 !important; font-size:13px;'>مراقبة البوابات والملاحظات الميدانية</p></div>""", unsafe_allow_html=True)
        st.success("👤 المشرف المسؤول: عبد الله بندر الزهراني")
        st.info("📅 عام التخرج والإنتاج الهيكلي: 2026")
        st.divider()
        
        st.markdown("### 🤖 وحدة محاكاة الكشوفات (للجنة المناقشة)")
        if st.button("🧪 محاكاة حضور 350 طالب + 15 ملاحظة"):
            execute_bulk_ai_simulation_data(350, 15)
            st.toast("🎉 تم توليد بيانات الحضور والملاحظات بنجاح!", icon="📊")
            time.sleep(0.1)
            st.rerun()
            
        if st.button("🧪 محاكاة حضور 580 طالب + 40 ملاحظة"):
            execute_bulk_ai_simulation_data(580, 40)
            st.toast("🔥 تم ملء القاعة بالكامل وحقن الملاحظات الميدانية!", icon="⚡")
            time.sleep(0.1)
            st.rerun()
        
        st.divider()
        if st.button("📡 تحديث ومزامنة حركة السيرفر"):
            st.toast("🔄 تم تحديث وقراءة مصفوفات الملاحظات الميدانية بنجاح!", icon="⚡")
            time.sleep(0.1)
            st.rerun()
        
        if st.button("🗑️ تصفير الداتابيز وإعادة تهيئة النظام"):
            GLOBAL_SERVER_CORE_DATA["used_codes"] = {}
            GLOBAL_SERVER_CORE_DATA["logs"] = []
            GLOBAL_SERVER_CORE_DATA["it_tickets"] = []
            GLOBAL_SERVER_CORE_DATA["staff_session_scans"] = 0
            st.session_state.last_staff_outcome = None
            st.session_state.last_admin_outcome = None
            st.session_state.last_processed_code = ""
            for code_key in GLOBAL_SERVER_CORE_DATA["student_db"]:
                GLOBAL_SERVER_CORE_DATA["student_db"][code_key]["status"] = "غائب"
                GLOBAL_SERVER_CORE_DATA["student_db"][code_key]["notes"] = []
                GLOBAL_SERVER_CORE_DATA["student_db"][code_key]["medical_logs"] = []
                GLOBAL_SERVER_CORE_DATA["student_db"][code_key]["current_location"] = "خ خارج القاعة"
            st.toast("🗑️ تم تصفير قاعدة البيانات وحذف الملاحظات بالكامل!", icon="💥")
            time.sleep(0.1)
            st.rerun()
            
        if st.button("🚪 تسجيل خروج المشرف الآمن"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.last_admin_outcome = None
            st.session_state.last_processed_code = ""
            st.rerun()

    # متن لوحة التحكم والتحليلات الخاصة بالمشرف العام
    admin_tabs_container = st.tabs([
        "🔍 منفذ التدقيق والمراقبة الحية", 
        "📁 كشوفات ومحرر الطلاب والملاحظات", 
        "📈 التحليلات البيانية ومعدل التدفق", 
        "🗂️ منشئ ومولد كروت التخرج المعتمدة",
        "🛠️ مركز بلاغات الأعطال التقنية",
        "📑 السجل الرقابي العام وتصدير التقارير"
    ])

    # --- تبويب المشرف 1: منفذ الاستعلام المباشر ---
    with admin_tabs_container[0]:
        st.markdown("### ⌨️ وحدة الاستعلام وإصدار التصاريح العليا للمشرف")
        
        if st.session_state.last_admin_outcome:
            adm_key, adm_msg = st.session_state.last_admin_outcome
            if adm_key == "success_entry":
                st.markdown(f'<div class="note-card-success"><h4>✅ إشعار التدقيق والقبول الإداري:</h4><p>{adm_msg}</p></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="note-card-critical"><h4>❌ إشعار المنع والتكرار الأمني:</h4><p>{adm_msg}</p></div>', unsafe_allow_html=True)
                
        with st.form(key="admin_verify_form", clear_on_submit=True):
            admin_input = st.text_input("أدخل رقم هوية الطالب للفحص المباشر:", placeholder="مثال: 1 أو 0001", key="admin_search_raw_input")
            submit_admin_btn = st.form_submit_button(label="🚀 فحص يدوي وإثبات حضور لحظي بالسيرفر")
            
            if submit_admin_btn and admin_input:
                res_key, res_msg = process_and_verify_scanned_code_extended(admin_input, "admin")
                st.session_state.last_admin_outcome = (res_key, res_msg)
                st.rerun()

    # --- تبويب المشرف 2: كشوفات ومحرر الطلاب والملاحظات الميدانية المزامنة ---
    with admin_tabs_container[1]:
        st.markdown("### 📁 دليل كشوفات الـ 600 طالب والملاحظات الميدانية الموحدة")
        
        admin_search_query = st.text_input("صندوق البحث السريع المتقدم في الكشوفات والملاحظات الحية:", placeholder="اكتب رقم التذكرة، الحالة للفرز التلقائي...", key="admin_table_filter_input")
        
        master_build_dict = {}
        for c_key, c_val in GLOBAL_SERVER_CORE_DATA["student_db"].items():
            last_note_txt = c_val["notes"][-1]["text"] if c_val["notes"] else "لا توجد ملاحظات ميدانية"
            master_build_dict[c_key] = {
                "حالة الحضور الفورية": c_val.get("status"),
                "الموقع الحالي بالقاعة": c_val.get("current_location"),
                "توقيت العبور البوابي": GLOBAL_SERVER_CORE_DATA["used_codes"].get(c_key, "— لم يعبر البوابات بعد"),
                "آخر ملاحظة ميدانية للموظف": last_note_txt
            }
            
        admin_df = pd.DataFrame.from_dict(master_build_dict, orient='index').reset_index()
        admin_df.columns = ['رقم الطالب', 'حالة الحضور الفورية', 'الموقع الحالي بالقاعة', 'توقيت العبور البوابي', 'آخر ملاحظة ميدانية للموظف']
        
        if admin_search_query:
            filtered_df = admin_df[admin_df.apply(lambda row: admin_search_query in row.values.astype(str), axis=1)]
        else:
            filtered_df = admin_df
            
        st.data_editor(filtered_df, use_container_width=True, disabled=["رقم الطالب", "توقيت العبور البوابي", "آخر ملاحظة ميدانية للموظف"], key="admin_master_editor_v255")

    # --- تبويب المشرف 3: التحليلات البيانية المتقدمة ومعدلات الامتلاء والتدفق البوابي ---
    with admin_tabs_container[2]:
        st.markdown("### 📈 المؤشرات الإحصائية ومعدل التدفق الذكي")
        
        tot_max = SYSTEM_CAPACITY_LIMIT
        curr_att = len(GLOBAL_SERVER_CORE_DATA["used_codes"])
        rem_abs = tot_max - curr_att
        fill_ratio = (curr_att / tot_max) * 100
        
        # تصحيح المشكلة: حساب المتغير محلياً هنا لضمان عمل الرسوم البيانية للأدمن بشكل مستقل
        admin_temp_out_count = sum(1 for s in GLOBAL_SERVER_CORE_DATA["student_db"].values() if s["current_location"] == "خروج مؤقت")
        
        ai_metrics = calculate_monumental_ai_predictions()
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("👥 الطلاب الحاضرين بالقاعة", f"{curr_att} طالب")
        with col_b:
            st.metric("⏳ الطلاب الغائبين / بالخارج", f"{rem_abs} طالب")
        with col_c:
            st.metric("📈 نسبة الامتلاء الكلية المقعدية", f"{fill_ratio:.1f}%")
            
        st.markdown("<br><div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("#### 🤖 التقرير التنبؤي لمحرك الذكاء الاصطناعي المركزي:")
        st.markdown(f"• معدل مسح ومعالجة الكروت الحالي: `{ai_metrics['flow_rate']}` كارت في الدقيقة.")
        st.markdown(f"• حالة الاختناق والتكدس المرصودة: **{ai_metrics['congestion']}**")
        st.markdown(f"• الوقت المتوقع لامتلاء المقاعد واكتمال الدخول: الساعة `{ai_metrics['predicted_time']}`")
        st.markdown("</div>", unsafe_allow_html=True)
        
# البديل المدمج والمستقر لـ Plotly باستخدام مكتبة Altair المدعومة تلقائياً في Streamlit
        st.markdown("#### 📊 مخطط بياني حي لنسب الحضور والغياب والملاحظات")
        
        # تجهيز البيانات في شكل DataFrame مناسب للرسم
        chart_data = pd.DataFrame({
            'الحالة الحركية للطلاب': ['حاضر داخل القاعة', 'غائب / خارج البوابات', 'خروج مؤقت'],
            'عدد الطلاب': [curr_att - admin_temp_out_count, rem_abs, admin_temp_out_count]
        })
        
        try:
            import altair as alt
            # بناء مخطط شريطي (Bar Chart) احترافي يتناسق مع ألوان الواجهة
            luxury_chart = alt.Chart(chart_data).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
                x=alt.X('الحالة الحركية للطلاب:N', sort=None, axis=alt.Axis(labelAngle=0, title=None)),
                y=alt.Y('عدد الطلاب:Q', title='إجمالي العدد'),
                color=alt.Color('الحالة الحركية للطلاب:N', scale=alt.Scale(
                    domain=['حاضر داخل القاعة', 'غائب / خارج البوابات', 'خروج مؤقت'],
                    range=['#10b981', '#374151', '#f59e0b'] # الأخضر، الرمادي الداكن، والبرتقالي
                ), legend=None)
            ).properties(
                height=300
            ).configure_view(
                strokeWidth=0
            ).configure_axis(
                grid=False
            )
            
            st.altair_chart(luxury_chart, use_container_width=True)
            
        except Exception:
            # حل احتياطي فوري فائق البساطة في حال عدم توفر Altair لأي سبب
            st.bar_chart(data=chart_data, x='الحالة الحركية للطلاب', y='عدد الطلاب', use_container_width=True)
    # --- تبويب المشرف 4: منشئ ومولد كروت التخرج الرسمية المعتمدة ---
    with admin_tabs_container[3]:
        st.markdown("### 🗂️ إصدار وتوليد بطاقات العبور والـ QR الرسمية")
        
        sel_student = st.number_input("اختر معرف الخريج لتوليد كارت دعوته الخاص (1-600):", min_value=1, max_value=600, value=1, step=1, key="sel_std_card")
        fmt_sel = f"{sel_student:04d}"
        
        encoded_qr = generate_monumental_qr_image(fmt_sel)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style='max-width: 400px; margin: 0 auto;'>
                <div class='graduation-luxury-card'>
                    <div style='font-size: 11px; color: #fbbf24; font-weight: 900; letter-spacing: 2px;'>بطاقة دعوة رسمية معتمدة للحفل</div>
                    <h2 style='margin: 10px 0 4px 0; font-size: 20px; color: #ffffff;'>حفل تخرج خريجي عام 2026</h2>
                    <hr style='border: 1px solid rgba(255,255,255,0.15); margin: 8px 0;'>
                    <div style='font-size: 18px; font-weight: bold; color: #ffffff; margin-bottom: 4px;'>🎓 طالب رقم هوية: {fmt_sel}</div>
                    <div style='font-size: 13px; color: #e5e7eb; margin-bottom: 15px;'>الموقع الحالي برصد البوابات: <b style='color:#38bdf8;'>{GLOBAL_SERVER_CORE_DATA['student_db'][fmt_sel]['current_location']}</b></div>
                    <div style='background: #ffffff; padding: 14px; display: inline-block; border-radius: 12px;'>
                        <img src='data:image/png;base64,{encoded_qr}' width='150' height='150' style='display: block;' />
                    </div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # --- تبويب المشرف 5: مركز بلاغات الدعم الفني لمراقبة بوابات الموظفين الميدانيين ---
    with admin_tabs_container[4]:
        st.markdown("### 🛠️ مركز التحكم وبلاغات الأعطال التقنية لبوابات الموظفين")
        
        if GLOBAL_SERVER_CORE_DATA["it_tickets"]:
            for idx, ticket in enumerate(GLOBAL_SERVER_CORE_DATA["it_tickets"]):
                st.markdown(f"<div class='note-card-warning'>", unsafe_allow_html=True)
                st.markdown(f"📍 **البوابة المتأثرة:** `{ticket['gate']}` | ⏱️ **التوقيت:** `{ticket['time']}`")
                st.markdown(f"⚠️ **نوع العطل التقني المنبثق:** `{ticket['type']}`")
                st.markdown(f"📝 **وصف المشكلة الميدانية:** {ticket['desc']}")
                st.markdown(f"⚙️ **الحالة الفنية الإدارية الحالية:** `[{ticket['status']}]`")
                
                if ticket["status"] == "قيد المراجعة الفنية":
                    if st.button(f"✅ تم الإصلاح وإغلاق التذكرة الفنية #{idx+1}", key=f"fix_tkt_{idx}"):
                        ticket["status"] = "تم الحل والإصلاح الميداني"
                        st.toast("تم إرسال إشعار إصلاح العطل لجهاز الموظف", icon="🔧")
                        time.sleep(0.1)
                        st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.success("👍 ممتاز! كافة قراءات البوابات وشاشات الموظفين الميدانيين تعمل بكفاءة وبدون أعطال تقنية.")

    # --- تبويب المشرف 6: السجل الرقابي العام الموحد وتصدير التقارير النهائية الشاملة للمناقشة ---
    with admin_tabs_container[5]:
        st.markdown("### 📑 السجل الرقابي الفيدرالي الشامل وعمليات المسح والملاحظات")
        
        if GLOBAL_SERVER_CORE_DATA["logs"]:
            logs_df = pd.DataFrame(GLOBAL_SERVER_CORE_DATA["logs"])
            st.dataframe(logs_df, use_container_width=True, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            csv_bytes = logs_df.to_csv(index=False).encode('utf-8-sig')
            
            st.download_button(
                label="📥 تحميل التقرير الختامي الشامل للحضور والملاحظات والعمليات (Excel CSV)",
                data=csv_bytes,
                file_name=f"graduation_full_enterprise_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("السجلات نظيفة ومستعدة لاستقبال قراءات وملاحظات موظفي البوابات الميدانية.")


# =================================================================================
# فحص سلامة مصفوفات الـ 600 طالب (Self-Testing Integrity Bounds)
# =================================================================================
def verify_monumental_system_integrity_bounds():
    try:
        current_size = len(GLOBAL_SERVER_CORE_DATA["student_db"])
        if current_size != SYSTEM_CAPACITY_LIMIT:
            for i in range(1, 601):
                key = f"{i:04d}"
                if key not in GLOBAL_SERVER_CORE_DATA["student_db"]:
                    GLOBAL_SERVER_CORE_DATA["student_db"][key] = {
                        "status": "غائب",
                        "notes": [],
                        "medical_logs": [],
                        "current_location": "خارج القاعة",
                        "ticket_assigned": "الأصلية",
                        "risk_score": 0.0,
                        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
    except Exception as integrity_error:
        pass

verify_monumental_system_integrity_bounds()


# =================================================================================
# تذييل الصفحة البرمجي والتوثيقي لحقوق عام 2026 (Monumental Footer Framework)
# =================================================================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

st.markdown(
    """
    <div style='text-align: center; padding: 12px;'>
        <p style='color: #6b7280 !important; font-size: 12px; margin: 0;'>🔒 نظام بوابات الحفل المانع للتجميد والمزامن لحظياً بين الحسابات مع لوحة الملاحظات والبلاغات الطبية والتقنية الموسعة - إصدار الإنتاج الفاخر لعام 2026</p>
        <p style='color: #6b7280 !important; font-size: 11px; margin: 4px 0 0 0;'>مشروع التخرج المعتمد للأخ الخريج المهندس: <b>عبد الله بندر الزهراني</b> - كلية علوم الحاسب والمعلومات</p>
    </div>
    """, 
    unsafe_allow_html=True
)