import streamlit as st
from sklearn.linear_model import LinearRegression
import feedparser
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

sleep_data_X = np.array([
    [50, 3, 20], [60, 5, 25], [70, 7, 30], [80, 10, 35],
    [55, 2, 28], [65, 6, 22], [75, 8, 38]
])
sleep_data_y = np.array([1.6, 2.45, 3.3, 4.35, 1.9, 2.6, 4.0])
sleep_model = LinearRegression()
sleep_model.fit(sleep_data_X, sleep_data_y)

water_data_X = np.array([
    [50, 1, 20], [60, 3, 25], [70, 5, 30], [80, 7, 35],
    [90, 9, 40], [65, 5, 20], [75, 5, 35]
])
water_data_y = np.array([1.2, 1.8, 2.5, 3.2, 4.0, 2.0, 3.0])
water_model = LinearRegression()
water_model.fit(water_data_X, water_data_y)

steps_data_X = np.array([
    [20, 50, 1.60], [25, 60, 1.70], [30, 70, 1.75], [35, 80, 1.80],
    [40, 90, 1.85], [28, 65, 1.68], [33, 75, 1.78]
])
steps_data_y = np.array([8000, 8500, 9000, 10000, 11000, 8700, 9500])
steps_model = LinearRegression()
steps_model.fit(steps_data_X, steps_data_y)

health_data_X = np.array([
    [50, 1, 20], [60, 3, 25], [70, 5, 30], [80, 7, 35],
    [90, 9, 40], [65, 5, 20], [75, 5, 35]
])
health_data_y = np.array([1.2, 1.8, 2.5, 3.2, 4.0, 2.0, 3.0])
health_model = LinearRegression()
health_model.fit(health_data_X, health_data_y)


np.random.seed(42)
size = np.random.randint(30, 200, 100)
rooms = np.random.randint(1, 6, 100)
price = size * 15 + rooms * 20 + np.random.randint(-50, 50, 100)
df = pd.DataFrame({"Diện tích (m2)": size, "Số phòng": rooms, "Giá (triệu VND)": price})
X_house = df[["Diện tích (m2)", "Số phòng"]]
y_house = df["Giá (triệu VND)"]
house_model = LinearRegression()
house_model.fit(X_house, y_house)

st.sidebar.title("Ứng dụng giải trí và sức khỏe")
st.sidebar.markdown("---")

menu_options = [
    "🎤 MV yêu thích",
    "💤 Dự đoán giờ ngủ",
    "📰 Đọc báo",
    "💲 Quy đổi tiền tệ",
    "💧Dự đoán số lượng nước nên uống mỗi ngày",
    "📊 Tính chỉ số BMI",
    "🩺 Kiểm tra nên gặp bác sĩ?",
    "🚶‍♂️ Dự đoán số bước mỗi ngày",
    "🧠 Kiểm tra chỉ số IQ",
    "💁‍♂️ Kiểm tra tính cách DISC",
    "👌 Nhân tướng học",
    "🏠 Dự đoán giá nhà"
]
selected_page = st.sidebar.radio("Chọn chức năng:", menu_options)

st.title(f"Ứng dụng giải trí và sức khỏe")

if selected_page == "🎤 MV yêu thích":
    st.header(f"🎵 MV yêu thích")
    st.sidebar.markdown("---")
    st.sidebar.title("🎶 Danh sách nghệ sĩ")
    selected_artist = st.sidebar.radio("Chọn nghệ sĩ:", list(videos.keys()))
    st.subheader(f"Các bài hát của {selected_artist}")
    for title, url in videos[selected_artist]:
        st.write(f"**{title}**")
        st.video(url)

elif selected_page == "💤 Dự đoán giờ ngủ":
    st.header("🔮 Dự đoán giờ ngủ mỗi đêm")
    age = st.number_input("Tuổi của bạn", min_value=5, max_value=100, value=25)
    activity = st.slider("Mức độ hoạt động thể chất (1 = ít, 10 = rất nhiều)", 1, 10, 5)
    screen_time = st.number_input("Thời gian dùng màn hình mỗi ngày (giờ)", min_value=0, max_value=24, value=6)
    if st.button("💤 Dự đoán ngay"):
        input_data = np.array([[age, activity, screen_time]])
        result = sleep_model.predict(input_data)[0]
        st.success(f"Bạn nên ngủ khoảng {result:.1f} giờ mỗi đêm")

elif selected_page == "📰 Đọc báo":
    st.header("📰 Tin tức mới nhất từ VnExpress")
    feed = feedparser.parse("https://vnexpress.net/rss/tin-moi-nhat.rss")
    if feed.entries:
        for entry in feed.entries[:5]:
            st.subheader(entry.title)
            st.write(f"_{entry.published}_")
            st.markdown(f"[Đọc thêm]({entry.link})")
            st.write("---")
    else:
        st.info("Không thể tải tin tức.")

elif selected_page == "💲 Quy đổi tiền tệ":
    st.header("💲 Quy đổi tiền tệ")
    currencies = ["VND", "USD", "EUR", "GBP", "JPY", "KRW", "CNY", "AUD", "CAD"]
    amount = st.number_input("Nhập số tiền cần quy đổi:", min_value=0.01, value=1.00)
    from_currency = st.selectbox("Từ tiền tệ:", currencies, index=1)
    to_currency = st.selectbox("Sang tiền tệ:", currencies, index=0)
    if st.button("🔄 Quy đổi"):
        st.warning("Vui lòng tích hợp API để dùng chức năng này.")

elif selected_page == "💧Dự đoán số lượng nước nên uống mỗi ngày":
    st.title("Dự đoán số lượng nước nên uống mỗi ngày")
    weight = st.number_input("Cân nặng (kg)", min_value=30, max_value=150, value=65)
    activity = st.slider("Mức độ hoạt động (1 = ít, 10 = rất nhiều)", 1, 10, 5)
    temp = st.number_input("Nhiệt độ môi trường °C", min_value=10, max_value=45, value=25)
    if st.button("Dự đoán lượng nước cần uống"):
        pred = water_model.predict([[weight, activity, temp]])[0]
        st.success(f"Bạn nên uống khoảng {pred:.2f} lít nước mỗi ngày")

elif selected_page == "📊 Tính chỉ số BMI":
    st.header("📊 Kiểm tra chỉ số BMI của bạn")
    can_nang = st.number_input("Nhập cân nặng (kg)", min_value=10.0, max_value=200.0, value=60.0)
    chieu_cao = st.number_input("Nhập chiều cao (m)", min_value=1.0, max_value=2.5, value=1.7)
    if st.button("🧮 Tính BMI"):
        bmi = can_nang / (chieu_cao ** 2)
        st.success(f"Chỉ số BMI của bạn là: {bmi:.2f}")

elif selected_page == "🩺 Kiểm tra nên gặp bác sĩ?":
    st.header("🩺 Kiểm tra: Có nên gặp bác sĩ không?")
    hr = st.number_input("Nhịp tim (bpm)", 40, 200, 70)
    age = st.number_input("Tuổi", 0, 120, 30)
    weight = st.number_input("Cân nặng (kg)", 10, 200, 65)
    if st.button("🔍 Kiểm tra sức khỏe"):
        score = health_model.predict([[hr, age, weight]])[0]
        st.success(f"Chỉ số rủi ro: {score:.2f}")

elif selected_page == "🚶‍♂️ Dự đoán số bước mỗi ngày":
    st.header("🚶‍♂️ Dự đoán số bước nên đi mỗi ngày")
    age = st.number_input("Tuổi", 5, 100, 25)
    weight = st.number_input("Cân nặng (kg)", 10, 200, 60)
    height = st.number_input("Chiều cao (m)", 1.0, 2.5, 1.70)
    if st.button("🏃 Dự đoán số bước"):
        steps = steps_model.predict([[age, weight, height]])[0]
        st.success(f"Bạn nên đi khoảng {int(steps):,} bước mỗi ngày")

elif selected_page == "🏠 Dự đoán giá nhà":
    st.header("🏠 Ứng dụng Dự đoán Giá Nhà")
    area = st.slider("Diện tích (m2):", 30, 300, 100)
    rooms = st.number_input("Số phòng:", 1, 10, 3)
    y_pred = house_model.predict([[area, rooms]])[0]
    st.subheader("📌 Kết quả dự đoán:")
    st.success(f"Ngôi nhà có giá khoảng **{y_pred:.1f} triệu VND**")
    st.subheader("📊 Biểu đồ dữ liệu và dự đoán")
    fig, ax = plt.subplots()
    ax.scatter(df["Diện tích (m2)"], df["Giá (triệu VND)"], label="Dữ liệu thật")
    ax.scatter(area, y_pred, color="red", s=100, label="Ngôi nhà của bạn")
    ax.set_xlabel("Diện tích (m2)")
    ax.set_ylabel("Giá (triệu VND)")
    ax.legend()
    st.pyplot(fig)
