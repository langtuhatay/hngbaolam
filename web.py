import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    b1 = st.button("Bài hát của Đen Vâu")
with col2:
    b2 = st.button("Bài hát của Hà Anh Tuấn")
with col3:
    b3 = st.button("Bài hát của Sơn Tùng M-TP")

videos = {
    "Đen Vâu": [
        ("Bữa ăn cho em", "https://www.youtube.com/watch?v=ukHK1GVyr0I"),
        ("Mang tiền về cho mẹ", "https://www.youtube.com/watch?v=UVbv-PJXm14"),
        ("Trời hôm nay nhiều mây cực!", "https://www.youtube.com/watch?v=MBaF0l-PcRY"),
        ("Hai triệu năm", "https://www.youtube.com/watch?v=LSMDNL4n0kM")
    ],
    "Hà Anh Tuấn": [
        ("Tuyết rơi mùa hè", "https://www.youtube.com/watch?v=pTh3KCD7Euc"),
        ("Nước ngoài", "https://www.youtube.com/watch?v=pU3O9Lnp-Z0"),
        ("Tháng tư là lời nói dối của em", "https://www.youtube.com/watch?v=UCXao7aTDQM"),
        ("Xuân thì", "https://www.youtube.com/watch?v=3s1r_g_jXNs")
    ],
    "Sơn Tùng M-TP": [
        ("Lạc trôi", "https://www.youtube.com/watch?v=Llw9Q6akRo4"),
        ("Chúng ta không thuộc về nhau", "https://www.youtube.com/watch?v=qGRU3sRbaYw"),
        ("Muộn rồi mà sao còn", "https://www.youtube.com/watch?v=xypzmu5mMPY"),
        ("Hãy trao cho anh", "https://www.youtube.com/watch?v=knW7-x7Y7RE")
    ]
}

def show_videos(singer_name):
    with st.expander(f"{singer_name} 🎵"):
        st.title("MV YÊU THÍCH")
        for title, url in videos[singer_name]:
            st.write(title)
            st.video(url)

if b1:
    show_videos("Đen Vâu")
if b2:
    show_videos("Hà Anh Tuấn")
if b3:
    show_videos("Sơn Tùng M-TP")
