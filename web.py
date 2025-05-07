import streamlit as st

# Sidebar
st.sidebar.image('https://yt3.googleusercontent.com/p2GLClmkc7oAlrfDey6e5hE4JUKu_KbEy7l3tS2tMeGMlHYL8qnl_s7ta2AOVyQhV8GkrkvN=s900-c-k-c0x00ffffff-no-rj', caption='Bùi Trường Linh')
st.sidebar.title("Thông tin ca sĩ")
st.sidebar.markdown("""
- **Tên đầy đủ**: Bùi Trường Linh  
- **Ngày sinh**: 2000  
- **Quê quán**: Việt Nam  
- **Phong cách**: Indie, Ballad  
- **Nổi bật**: 'Từng Ngày Như Mãi Mãi', 'Chuyện đôi ta'
""")

# Main Page
st.title("🎶 Bùi Trường Linh ")

st.header("🎵 Bài hát yêu thích")
st.subheader("Từng Ngày Như Mãi Mãi")
audio_file = open('Từng Ngày Như Mãi Mãi buitruonglinh_4.mp3', 'rb') 
st.audio(audio_file, format='audio/mp3')

st.header("🎬 MV yêu thích")
st.subheader("Chuyện đôi ta")
st.video('https://www.youtube.com/watch?v=69ZDBWoj5YM')  
