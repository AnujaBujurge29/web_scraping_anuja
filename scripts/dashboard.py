import re
from collections import Counter
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

DB_PATH = "db/mlb_history.db"

# Connect to DB


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df_links = pd.read_sql("SELECT * FROM year_links", conn)
    df_details = pd.read_sql("SELECT * FROM year_details", conn)
    conn.close()
    return df_links, df_details


df_links, df_details = load_data()

st.title("MLB History Dashboard")

# Sidebar filters
years = sorted(df_links['Year'].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

# Filter details by year
details_year = df_details[df_details['Year'] == selected_year].copy()

st.header(f"Events in {selected_year}")
st.write(f"Number of event records: {len(details_year)}")

# Show raw text data
show_raw = st.checkbox("Show raw event details")
if show_raw:
    for i, detail in enumerate(details_year['Detail'].tolist()):
        st.write(f"{i+1}. {detail}")

# Visualization 1: Word frequency in details (simple text analysis)

all_text = " ".join(details_year['Detail'].tolist()).lower()
words = re.findall(r'\b\w{4,}\b', all_text)  # words >=4 chars
common_words = Counter(words).most_common(20)

words_df = pd.DataFrame(common_words, columns=["Word", "Count"])

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=words_df, x="Word", y="Count", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualization 2: Event length histogram
details_year['Length'] = details_year['Detail'].str.len()
fig2, ax2 = plt.subplots()
ax2.hist(details_year['Length'], bins=20, color='skyblue')
ax2.set_title(f"Distribution of Event Detail Lengths in {selected_year}")
ax2.set_xlabel("Character Count")
ax2.set_ylabel("Frequency")
st.pyplot(fig2)

# Visualization 3: Number of events over years (line chart)
events_per_year = df_details.groupby(
    'Year').size().reset_index(name='EventCount')

fig3, ax3 = plt.subplots()
sns.lineplot(data=events_per_year, x='Year', y='EventCount', ax=ax3)
ax3.set_title("Number of Event Records per Year")
st.pyplot(fig3)
