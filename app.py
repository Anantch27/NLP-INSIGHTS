import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- helper functions (kept inline for now) ---
def load_data(path="data/mydata.csv"):
    return pd.read_csv(path)

def simple_summary(df):
    return df.describe()

def plot_xy(df, x, y):
    fig, ax = plt.subplots()
    ax.plot(df[x], df[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    return fig

# ✅ correct: _file_ (double underscores)
PROJECT_ROOT = Path(__file__).parent
DATA_PATH = PROJECT_ROOT / "data" / "mydata.csv"

st.set_page_config(page_title="My Notebook → Streamlit App", page_icon="📊", layout="wide")
st.title("NLP INSIGHTS")

# Sidebar controls
st.sidebar.header("Controls")
data_source = st.sidebar.radio("Data source", ["Sample file", "Upload CSV"])

# Load data (robust to missing file)
@st.cache_data
def get_df(source_choice, data_path: Path):
    if source_choice == "Upload CSV":
        return None
    if data_path.exists():
        return load_data(str(data_path))
    return None  # fall back to uploader if file not found

df = get_df(data_source, DATA_PATH)

if data_source == "Upload CSV" or df is None:
    uploaded = st.file_uploader("Upload a CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)

if df is None:
    st.info("No data found. Upload a CSV or place one at ./data/mydata.csv")
    st.stop()

# Show data
st.subheader("Preview")
st.dataframe(df.head(50), use_container_width=True)

# Summary
st.subheader("Summary Stats")
summary = simple_summary(df)
st.dataframe(summary, use_container_width=True)
# Plot
st.subheader("Plot")
num_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
if len(num_cols) >= 2:
    x = st.selectbox("X axis", num_cols, index=0)
    y = st.selectbox("Y axis", num_cols, index=1)
    fig = plot_xy(df, x, y)
    st.pyplot(fig)
else:
    st.warning("Need at least two numeric columns to plot.")