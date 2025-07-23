import streamlit as st
from sklearn.linear_model import LinearRegression
import feedparser
import requests
import numpy as np

try:
    EXCHANGE_RATE_API_KEY = st.secrets["EXCHANGE_RATE_API_KEY"]
except KeyError:
    st.error("Lỗi: Không tìm thấy API Key. Vui lòng cấu hình API Key trong file .streamlit/secrets.toml (khi chạy cục bộ) hoặc trong Streamlit Cloud Secrets.")
    st.stop()

st.sidebar.title("🎶 Danh sách nghệ sĩ")
selected_artist = st.sidebar.radio("Chọn nghệ sĩ:", ["Đen Vâu", "Hà Anh Tuấn", "Sơn Tùng M-TP"])

videos = {
    "Đen Vâu": [
        ("Bữa ăn cho em", "https://www.youtube.com/embed/P-Y3o67z_0Q"),
        ("Mang tiền về cho mẹ", "https://www.youtube.com/embed/V-B-xWq28_0"),
        ("Trời hôm nay nhiều mây cực!", "https://www.youtube.com/embed/bL7X_u98rP4"),
        ("Hai triệu năm", "https://www.youtube.com/embed/sQZ_G5C8cI0")
    ],
    "Hà Anh Tuấn": [
        ("Tuyết rơi mùa hè", "https://www.youtube.com/embed/t8k3n383wR8"),
        ("Nước ngoài", "https://www.youtube.com/embed/bL7X_u98rP4"),
        ("Tháng tư là lời nói dối của em", "https://www.youtube.com/embed/U9sQv0y_19c"),
        ("Xuân thì", "https://www.youtube.com/embed/bL7X_u98rP4")
    ],
    "Sơn Tùng M-TP": [
        ("Lạc trôi", "https://www.youtube.com/embed/L1_gYfM_t8I"),
        ("Chúng ta không thuộc về nhau", "https://www.youtube.com/embed/fn7k5C1z20k"),
        ("Muộn rồi mà sao còn", "https://www.youtube.com/embed/FwF9yF5wA10"),
        ("Hãy trao cho anh", "https://www.youtube.com/embed/D3a47XnLq8o")
    ]
}

st.title("🎧 Ứng dụng giải trí và sức khỏe")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🎤 MV yêu thích",
    "💤 Dự đoán giờ ngủ",
    "📰 Đọc báo",
    "💲 Quy đổi tiền tệ",
    "💧Dự đoán số lượng nước nên uống mỗi ngày",
    "📊 Tính chỉ số BMI",
    "🩺 Kiểm tra nên gặp bác sĩ?",
    "🚶‍♂️ Dự đoán số bước mỗi ngày",
    "🧠 Kiểm tra chỉ số IQ",
    "💁‍♂️ Kiểm tra tính cách DISC"
])
with tab1:
    st.header(f"Các bài hát của {selected_artist} 🎵")
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)

with tab2:
    st.header("🔮 Dự đoán giờ ngủ mỗi đêm")
    x = [
    [50, 3, 20],
    [60, 5, 25],
    [70, 7, 30],
    [80, 10, 35],
    [55, 2, 28],
    [65, 6, 22],
    [75, 8, 38]
]
    y = [1.6, 2.45, 3.3, 4.35, 1.9, 2.6, 4.0]
    model = LinearRegression()
    model.fit(x, y)
    st.write("Nhập thông tin cá nhân:")
    age = st.number_input("Tuổi của bạn", min_value=5, max_value=100, value=25)
    activity = st.slider("Mức độ hoạt động thể chất (1 = ít, 10 = rất nhiều)", 1, 10, 5)
    screen_time = st.number_input("Thời gian dùng màn hình mỗi ngày (giờ)", min_value=0, max_value=24, value=6)
    if st.button("💤 Dự đoán ngay"):
        input_data = [[age, activity, screen_time]]
        result = model.predict(input_data)[0]
        st.success(f"Bạn nên ngủ khoảng {result:.1f} giờ mỗi đêm")
        if result < 6.5:
            st.warning("😴 Có thể bạn cần nghỉ ngơi nhiều hơn để cải thiện sức khỏe.")
        elif result > 9:
            st.info("😅 Có thể bạn đang vận động nhiều – ngủ bù hợp lý nhé.")
        else:
            st.success("✅ Lượng ngủ lý tưởng! Hãy giữ thói quen tốt nhé.")

with tab3:
    st.header("📰 Tin tức mới nhất từ VnExpress")
    feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
    if feed.entries:
        for entry in feed.entries[:5]:
            st.subheader(entry.title)
            st.write(f"_{entry.published}_")
            st.markdown(f"[Đọc thêm]({entry.link})")
            st.write("---")
    else:
        st.info("Không thể tải tin tức. Vui lòng kiểm tra kết nối mạng hoặc nguồn RSS.")

with tab4:
    st.header("💲 Quy đổi tiền tệ")
    currencies = ["VND", "USD", "EUR", "GBP", "JPY", "KRW", "CNY", "AUD", "CAD"]
    amount = st.number_input("Nhập số tiền cần quy đổi:", min_value=0.01, value=1.00)
    from_currency = st.selectbox("Từ tiền tệ:", currencies, index=1)
    to_currency = st.selectbox("Sang tiền tệ:", currencies, index=0)
    if st.button("🔄 Quy đổi"):
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/{from_currency}"
        try:
            response = requests.get(url)
            data = response.json()
            if data["result"] == "success":
                rate = data["conversion_rates"].get(to_currency)
                if rate:
                    converted = amount * rate
                    st.success(f"{amount} {from_currency} = {converted:.2f} {to_currency}")
                    st.info(f"Tỷ giá: 1 {from_currency} = {rate:.5f} {to_currency}")
                else:
                    st.warning("Không tìm thấy tỷ giá.")
            else:
                st.error("Lỗi khi lấy dữ liệu tỷ giá.")
        except:
            st.error("Không thể kết nối đến API.")

with tab5:
    st.title("Dự đoán số lượng nước nên uống mỗi ngày")
    x = [
    [50, 1, 20],
    [60, 3, 25],
    [70, 5, 30],
    [80, 7, 35],
    [90, 9, 40],
    [65, 5, 20],
    [75, 5, 35]
]
    y = [1.2, 1.8, 2.5, 3.2, 4.0, 2.0, 3.0]
    model = LinearRegression()
    model.fit(x, y)
    st.write("Nhập thông tin của bạn")
    weight = st.number_input("Cân nặng (kg)", min_value=30, max_value=150, value=65)
    activity = st.slider("Mức độ hoạt động (1 = ít, 10 = rất nhiều)", 1, 10, 5)
    temp = st.number_input("Nhiệt độ môi trường °C", min_value=10, max_value=45, value=25)
    if st.button("Dự đoán lượng nước cần uống"):
        pred = model.predict([[weight, activity, temp]])[0]
        st.success(f"Bạn nên uống khoảng {pred:.2f} lít nước mỗi ngày")

with tab6:
    st.header("📊 Kiểm tra chỉ số BMI của bạn")

    can_nang = st.number_input("Nhập cân nặng của bạn (kg)", min_value=10.0, max_value=200.0, value=60.0, step=0.1)
    chieu_cao = st.number_input("Nhập chiều cao của bạn (m)", min_value=1.0, max_value=2.5, value=1.7, step=0.01)

    if st.button("🧮 Tính BMI"):
        bmi = can_nang / (chieu_cao ** 2)
        st.success(f"Chỉ số BMI của bạn là: {bmi:.2f}")

        if bmi < 18.5:
            st.warning("Bạn đang thiếu cân, nên ăn uống đầy đủ và dinh dưỡng hơn.")
        elif 18.5 <= bmi < 25:
            st.info("Bạn có cân nặng bình thường. Hãy tiếp tục duy trì lối sống lành mạnh.")
        elif 25 <= bmi < 30:
            st.warning("Bạn đang thừa cân. Nên cân đối chế độ ăn và tập thể dục.")
        else:
            st.error("Bạn đang béo phì. Nên gặp chuyên gia dinh dưỡng hoặc bác sĩ để được tư vấn.")

with tab7:
    st.header("🩺 Kiểm tra: Có nên gặp bác sĩ không?")
    x = [
    [50, 1, 20],
    [60, 3, 25],
    [70, 5, 30],
    [80, 7, 35],
    [90, 9, 40],
    [65, 5, 20],
    [75, 5, 35]
]
    y = [1.2, 1.8, 2.5, 3.2, 4.0, 2.0, 3.0]
    model = LinearRegression()
    model.fit(x, y)
    hr = st.number_input("Nhịp tim (bpm)", 40, 200, 70)
    age = st.number_input("Tuổi", 0, 120, 30)
    weight = st.number_input("Cân nặng (kg)", 10, 200, 65)
    if st.button("🔍 Kiểm tra sức khỏe"):
        score = model.predict([[hr, age, weight]])[0]
        st.success(f"Chỉ số rủi ro: {score:.2f}")

with tab8:
    st.header("🚶‍♂️ Dự đoán số bước nên đi mỗi ngày")
    x = [
    [20, 50, 1.60],
    [25, 60, 1.70],
    [30, 70, 1.75],
    [35, 80, 1.80],
    [40, 90, 1.85],
    [28, 65, 1.68],
    [33, 75, 1.78]
]
    y = [8000, 8500, 9000, 10000, 11000, 8700, 9500]
    model = LinearRegression()
    model.fit(x, y)
    age = st.number_input("Tuổi", 5, 100, 25)
    weight = st.number_input("Cân nặng (kg)", 10, 200, 60)
    height = st.number_input("Chiều cao (m)", 1.0, 2.5, 1.70)
    if st.button("🏃 Dự đoán số bước"):
        steps = model.predict([[age, weight, height]])[0]
        st.success(f"Bạn nên đi khoảng {int(steps):,} bước mỗi ngày")
with tab9:
    st.header("🧠 Kiểm tra chỉ số IQ theo độ tuổi")

    def get_iq_range(age):
        if 5 <= age <= 7:
            return 85, 115
        elif 8 <= age <= 12:
            return 90, 115
        elif 13 <= age <= 17:
            return 90, 115
        elif age >= 18:
            return 85, 115
        else:
            return None, None

    age = st.number_input("Nhập tuổi của bạn:", min_value=1, max_value=100, value=18)
    iq = st.number_input("Nhập chỉ số IQ của bạn:", min_value=40, max_value=200, value=100)

    if st.button("Kiểm tra IQ"):
        min_iq, max_iq = get_iq_range(age)

        if min_iq is None:
            st.error("Tuổi không hợp lệ để đánh giá.")
        elif iq < min_iq:
            st.error("Chỉ số IQ của bạn dưới mức trung bình.")
        elif iq > max_iq:
            st.warning("Chỉ số IQ của bạn trên mức trung bình.")
        else:
            st.success("Chỉ số IQ của bạn nằm trong mức trung bình.")
with tab10:
    st.header("Kiểm tra tính cách DISC")
    st.markdown("Chọn một mô tả đúng nhất và một mô tả ít đúng nhất trong từng nhóm:")

    groups = [
        {
            "D": "Tôi quyết đoán và thích kiểm soát",
            "I": "Tôi thích thân thiện và nói chuyện dễ dàng",
            "S": "Tôi kiên nhẫn và đáng tin cậy",
            "C": "Tôi chính xác và có hệ thống"
        },
        {
            "D": "Tôi thích thử thách và hành động nhanh",
            "I": "Tôi tràn đầy năng lượng và lạc quan",
            "S": "Tôi ổn định và hỗ trợ người khác",
            "C": "Tôi làm việc theo quy tắc rõ ràng"
        },
        {
            "D": "Tôi thích kiểm soát kết quả",
            "I": "Tôi thích được công nhận",
            "S": "Tôi ưu tiên sự hài hòa",
            "C": "Tôi chú ý đến việc chi tiết và phân tích"
        }
    ]

    scores = {"D": 0, "I": 0, "S": 0, "C": 0}

    for idx, group in enumerate(groups):
        st.markdown(f"### Nhóm {idx + 1}")
        options = list(group.values())
        keys = list(group.keys())

        most = st.radio("✅ Mô tả đúng nhất với bạn", options, key=f"most_{idx}")
        least = st.radio("❌ Mô tả ít đúng nhất với bạn", options, key=f"least_{idx}")

        for key, val in group.items():
            if val == most:
                scores[key] += 1
            if val == least:
                scores[key] -= 1

    if st.button("🔍 Xem kết quả DISC"):
        st.subheader("🧠 Kết quả của bạn")
        max_type = max(scores, key=scores.get)

        for style, score in scores.items():
            st.write(f"{style}: {score} điểm")

        st.markdown(f"**Tính cách nổi bật nhất của bạn là: {max_type}**")

        descriptions = {
            "D": "Quyết đoán, định hướng kết quả và thích kiểm soát",
            "I": "Giao tiếp tốt, tràn đầy năng lượng và truyền cảm hứng",
            "S": "Kiên nhẫn, đáng tin cậy và hỗ trợ người khác",
            "C": "Chính xác, tuân thủ quy trình và thích phân tích logic"
        }

        st.info(descriptions[max_type])
        st.caption("Đây chỉ là bài tham khảo về chỉ số DISC")
