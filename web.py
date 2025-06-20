import streamlit as st
from sklearn.linear_model import LinearRegression
import feedparser
import requests

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

tab1, tab2, tab3, tab4 = st.tabs(["🎤 MV yêu thích", "💤 Dự đoán giờ ngủ", "📰 Đọc báo", "💲 Quy đổi tiền tệ"])

with tab1:
    st.header(f"Các bài hát của {selected_artist} 🎵")
    for title, url in videos[selected_artist]:
        st.subheader(title)
        st.video(url)

with tab2:
    st.header("🔮 Dự đoán giờ ngủ mỗi đêm")

    x = [
        [10, 1, 8],
        [20, 5, 6],
        [25, 8, 3],
        [30, 6, 5],
        [35, 2, 9],
        [40, 4, 3]
    ]
    y = [10, 8, 6, 7, 9.5, 9]

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
                exchange_rates = data["conversion_rates"]
                
                if to_currency in exchange_rates:
                    rate = exchange_rates[to_currency]
                    converted_amount = amount * rate
                    st.success(f"{amount:,.2f} {from_currency} = **{converted_amount:,.2f} {to_currency}**")
                    st.info(f"Tỷ giá hiện tại: 1 {from_currency} = {rate:,.5f} {to_currency}")
                else:
                    st.warning("Không tìm thấy tỷ giá cho đồng tiền đích. Vui lòng thử lại.")
            elif data["result"] == "error":
                st.error(f"Lỗi từ API: {data.get('error-type', 'Không xác định')}. Vui lòng kiểm tra API Key và đồng tiền cơ sở.")
            else:
                st.error("Lỗi không xác định khi lấy dữ liệu tỷ giá.")

        except requests.exceptions.ConnectionError:
            st.error("Không thể kết nối đến máy chủ API. Vui lòng kiểm tra kết nối internet của bạn.")
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")
