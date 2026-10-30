import json
import requests
import pandas as pd
from sklearn.linear_model import LogisticRegression

# ==========================================
# 1. إعدادات الربط مع المزودين والمواقع (APIs)
# ==========================================
# استبدل هذه القيم بمفاتيح الحسابات الخاصة بك (API Keys)
FOOTBALL_API_URL = "https://api-sports.io"
FOOTBALL_API_KEY = "YOUR_API_FOOTBALL_KEY_HERE" # مفتاح API-Football

ONESIGNAL_URL = "https://onesignal.com"
ONESIGNAL_APP_ID = "YOUR_ONESIGNAL_APP_ID"         # مفتاح OneSignal App ID
ONESIGNAL_REST_KEY = "YOUR_ONESIGNAL_REST_KEY"     # مفتاح OneSignal API Key

# ==========================================
# 2. سحب البيانات الرياضية الإحصائية
# ==========================================
def fetch_match_data(fixture_id):
    """
    سحب بيانات المباراة من API-Football (أو محاكاة إحصائيات Opta/Sportradar)
    """
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': FOOTBALL_API_KEY
    }
    query = {"id": fixture_id}
    
    # في الواقع سنقوم بطلب الـ API، هنا نضع بيانات تجريبية (Mock Data) كبديل في حال عدم وجود مفتاح
    try:
        # تفكيك التعليق بالأسفل لتفعيل سحب البيانات الحقيقي:
        # response = requests.get(FOOTBALL_API_URL, headers=headers, params=query).json()
        
        # بيانات إحصائية افتراضية للمباراة القادمة (أداء آخر 5 مباريات، نسبة الاستحواذ، غيابات)
        mock_data = {
            "home_team": "Real Madrid",
            "away_team": "Barcelona",
            "home_form": 0.80,      # كفاءة الفريق صاحب الأرض (80%)
            "away_form": 0.75,      # كفاءة الفريق الضيف (75%)
            "home_injuries": 1,     # عدد الإصابات المؤثرة لدى الأرض
            "away_injuries": 3,     # عدد الإصابات المؤثرة لدى الضيف
            "home_h2h_win_rate": 0.60 # نسبة الفوز في المواجهات المباشرة التاريخية (Opta Data)
        }
        return mock_data
    except Exception as e:
        print(f"حدث خطأ أثناء سحب البيانات: {e}")
        return None

# ==========================================
# 3. محرك الذكاء الاصطناعي للتوقعات (AI Engine)
# ==========================================
def train_prediction_model():
    """
    تدريب نموذج ذكاء اصطناعي مبسط بناءً على بيانات تاريخية (مثل الموفرة من Sportradar)
    """
    # بيانات تاريخية تجريبية للتدريب: [نموذج الأرض, نموذج الضيف, إصابات الأرض, إصابات الضيف, نسبة المواجهات التاريخية]
    X_train = [
        [0.85, 0.60, 0, 2, 0.70], # فوز صاحب الأرض (1)
        [0.50, 0.80, 2, 0, 0.40], # فوز الضيف أو تعادل (0)
        [0.90, 0.50, 1, 3, 0.65], # فوز صاحب الأرض (1)
        [0.40, 0.70, 3, 1, 0.30]  # فوز الضيف أو تعادل (0)
    ]
    # النتيجة: 1 تعني فوز صاحب الأرض، 0 تعني تعادل أو خسارة
    y_train = [1, 0, 1, 0]
    
    # استخدام خوارزمية الانحدار اللوجستي للتوقع
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def predict_match_outcome(model, match_data):
    """
    حساب التوقع ونسبة الدقة للمباراة الحالية
    """
    # تجهيز بيانات المباراة المدخلة للخوارزمية
    current_match_features = [[
        match_data["home_form"],
        match_data["away_form"],
        match_data["home_injuries"],
        match_data["away_injuries"],
        match_data["home_h2h_win_rate"]
    ]]
    
    # حساب الاحتمالات المئوية
    probabilities = model.predict_proba(current_match_features)[0]
    home_win_probability = probabilities[1] * 100 # نسبة فوز صاحب الأرض
    
    return round(home_win_probability, 2)

# ==========================================
# 4. إرسال الإشعارات التلقائية بالمنصة (OneSignal)
# ==========================================
def send_push_notification(match_name, prediction_percentage):
    """
    إرسال إشعار فوري للمستخدمين بالتوقع الجديد ونسبة دقته عبر OneSignal
    """
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Basic {ONESIGNAL_REST_KEY}"
    }
    
    payload = {
        "app_id": ONESHIGNAL_APP_ID,
        "included_segments": ["All Users"], # إرسال لجميع المشتركين
        "headings": {"en": "🔥 توقع ذكي جديد!"},
        "contents": {
            "en": f"توقع مباراة {match_name}: نسبة فوز صاحب الأرض هي {prediction_percentage}% بناءً على تحليل الذكاء الاصطناعي."
        }
    }
    
    # تفعيل الإرسال الحقيقي عند إضافة المفاتيح الصحيحة
    # response = requests.post(ONESIGNAL_URL, headers=headers, data=json.dumps(payload))
    # return response.status_code
    print(f"\n[OneSignal Notification Sent]: توقع مباراة {match_name} جاهز بنسبة {prediction_percentage}%")

# ==========================================
# 5. تشغيل المنومة البرمجية بالكامل
# ==========================================
if __name__ == "__main__":
    print("⏳ جاري تشغيل النظام وربط المواقع الرياضية والذكاء الاصطناعي...")
    
    # الخطوة 1: سحب البيانات (محاكاة الربط مع API-Football و Opta)
    match_data = fetch_match_data(fixture_id=12345)
    
    if match_data:
        match_name = f"{match_data['home_team']} VS {match_data['away_team']}"
        print(f"📊 تم سحب إحصائيات مباراة: {match_name}")
        
        # الخطوة 2: تدريب نموذج التوقع (محاكاة الاستفادة من أرشيف Sportradar)
        ai_model = train_prediction_model()
        
        # الخطوة 3: استخراج التوقع النهائي
        prediction_score = predict_match_outcome(ai_model, match_data)
        print(f"🤖 حسابات الذكاء الاصطناعي انتهت. نسبة فوز {match_data['home_team']} هي: {prediction_score}%")
        
        # الخطوة 4: دفع التوقع للمستخدمين عبر نظام الإشعارات (OneSignal)
        send_push_notification(match_name, prediction_score)
        
        print("\n✅ تمت العملية بنجاح! الموقع جاهز لعرض البيانات الآن.")
