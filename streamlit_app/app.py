import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="نظام التوظيف الذكي الأردني", layout="wide")

# تهيئة حالة الجلسة (Session State)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "has_history" not in st.session_state:
    st.session_state.has_history = False
if "history_data" not in st.session_state:
    st.session_state.history_data = []

# ----------------- 1. صفحة تسجيل الدخول / إنشاء الحساب -----------------
if not st.session_state.logged_in:
    st.title("🔐 تسجيل الدخول إلى نظام التوظيف الذكي")
    st.markdown("أدخل اسم المستخدم وكلمة المرور. إذا لم يكن الحساب موجوداً، سيتم إنشاؤه تلقائياً.")

    with st.form("login_form"):
        username = st.text_input("اسم المستخدم (Username)")
        password = st.text_input("كلمة المرور (Password)", type="password")
        submit_button = st.form_submit_button("دخول / إنشاء حساب")

        if submit_button:
            if username and password:
                # إرسال طلب POST إلى رابط 'user' في Django
                try:
                    res = requests.post(
                        "http://127.0.0.1:8000/user/", 
                        data={"username": username, "password": password}
                    )
                    
                    if res.status_code == 200:
                        res_data = res.json()
                        st.session_state.logged_in = True
                        st.session_state.user_id = res_data.get("user_id")
                        
                        # التحقق من وجود سجل بحث سابق
                        if res_data.get("status") == "history_found":
                            st.session_state.has_history = True
                            st.session_state.history_data = res_data.get("results")
                        else:
                            st.session_state.has_history = False
                            
                        st.rerun()
                    else:
                        st.error(f"خطأ في البيانات: {res.json().get('error', res.text)}")
                except Exception as e:
                    st.error(f"انات تعذر الاتصال بالسيرفر: {str(e)}")
            else:
                st.warning("الرجاء إدخال اسم المستخدم وكلمة المرور.")

# ----------------- 2. الواجهة بعد تسجيل الدخول -----------------
else:
    st.sidebar.success(f"مرحباً بك! (User ID: {st.session_state.user_id})")
    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.has_history = False
        st.session_state.history_data = []
        st.rerun()

    # الحالة أ: إذا وجد سجل بحث سابق
    if st.session_state.has_history and len(st.session_state.history_data) > 0:
        st.title("📋 جدول الوظائف التي تم البحث عنها مسبقاً")
        st.info("تم العثور على سجل بحث سابق لحسابك:")
        
        df_history = pd.DataFrame(st.session_state.history_data)
        st.dataframe(
            df_history,
            column_config={
                "link": st.column_config.LinkColumn("رابط الوظيفة"),
                "score": st.column_config.ProgressColumn("نسبة التوافق", format="%d%%", min_value=0, max_value=100),
            },
            hide_index=True,
            use_container_width=True
        )
        
        if st.button("🔍 إجراء بحث جديد عن وظيفة"):
            st.session_state.has_history = False
            st.rerun()

    # الحالة ب: إذا لم يوجد سجل بحث (أو اختار المستخدم بحثاً جديداً)
    else:
        st.title("📄 صفحة إدخال البيانات للبحث عن مطابقة")
        
        with st.form("job_search_form"):
            job_title = st.text_input("المسمى الوظيفي المطلوب")
            location = st.text_input("الموقع", "Irbid")
            description = st.text_area("وصف الوظيفة (Job Description)")
            salary = st.number_input("الراتب المتوقع", min_value=0, value=500)
            uploaded_file = st.file_uploader("اختر ملف السيرة الذاتية (PDF)", type=["pdf"])
            
            search_submitted = st.form_submit_button("بدء التحليل والبحث")

            if search_submitted:
                if job_title and description and uploaded_file:
                    files = {
                        "resume_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")
                    }
                    data = {
                        "user": st.session_state.user_id,
                        "job_title": job_title,
                        "location": location,
                        "description": description,
                        "salary": salary
                    }
                    
                    with st.spinner("جاري تحليل السيرة الذاتية ومطابقة الوظائف عبر الذكاء الاصطناعي..."):
                        try:
                            response = requests.post("http://127.0.0.1:8000/details/", data=data, files=files)
                            
                            if response.status_code in [200, 201]:
                                st.success("تم التخزين وتشغيل التحليل بنجاح!")
                                data_result = response.json()
                                
                                if isinstance(data_result, list) and len(data_result) > 0:
                                    df = pd.DataFrame(data_result)
                                    st.subheader("📋 نتائج مطابقة الوظائف المقترحة:")
                                    st.dataframe(
                                        df,
                                        column_config={
                                            "link": st.column_config.LinkColumn("رابط الوظيفة"),
                                            "score": st.column_config.ProgressColumn("نسبة التوافق", format="%d%%", min_value=0, max_value=100),
                                        },
                                        hide_index=True,
                                        use_container_width=True
                                    )
                                else:
                                    st.info("تمت العملية ولكن لم يتم إرجاع نتائج مطابقة.")
                            else:
                                st.error(f"حدث خطأ من السيرفر: {response.text}")
                        except Exception as e:
                            st.error(f"تعذر الاتصال بالسيرفر: {str(e)}")
                else:
                    st.warning("الرجاء تعبئة جميع الحقول الإجبارية ورفع ملف السيرة الذاتية.")