import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
import matplotlib as mpl

# 🔤 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
mpl.rcParams['axes.unicode_minus'] = False

# 🔄 예시 데이터 불러오기
# 실제 사용 시 df = pd.read_sql(...) 또는 csv 읽기
df = pd.read_csv("bestsellers.csv")  # 예시. 너의 데이터에 맞게 수정!

# 리뷰 전처리
df['리뷰개수'] = df['리뷰개수'].astype(str).str.extract(r'(\d+)')
df['리뷰개수'] = pd.to_numeric(df['리뷰개수'], errors='coerce')
df['리뷰점수'] = pd.to_numeric(df['리뷰점수'], errors='coerce')

df_filtered = df[df['리뷰점수'] > 0]
top5_reviews = df.sort_values(by='리뷰개수', ascending=False).head(5)

# 📊 Streamlit 시작
st.set_page_config(page_title="베스트셀러 시각화", layout="wide")
st.title("📚 교보문고 베스트셀러 대시보드")

# 1. 책별 리뷰 점수
st.header("1. 책별 리뷰 점수 (0점 제외)")
fig1, ax1 = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_filtered, y='제목', x='리뷰점수', orient='h', ax=ax1)
ax1.set_title('책별 리뷰점수 (0 제외)', fontproperties=font_prop)
ax1.set_xlabel('점수')
ax1.set_ylabel('')
st.pyplot(fig1)

# 2. 출판사별 베스트셀러 수
st.header("2. 출판사별 베스트셀러 수")
fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.countplot(data=df, y='출판사', order=df['출판사'].value_counts().index, ax=ax2)
ax2.set_title('출판사별 베스트셀러 수', fontproperties=font_prop)
ax2.set_xlabel('빈도수', fontproperties=font_prop)
max_val = df['출판사'].value_counts().max()
ax2.set_xticks(range(0, max_val+2, 1))
st.pyplot(fig2)

# 3. 리뷰 수 상위 5개
st.header("3. 리뷰 수 Top 5 책")
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(data=top5_reviews, y='제목', x='리뷰개수', hue='제목', palette='Set2', legend=False, ax=ax3)
ax3.set_title('리뷰 수 Top 5 책', fontproperties=font_prop)
ax3.set_xlabel('')
ax3.set_ylabel('')
st.pyplot(fig3)