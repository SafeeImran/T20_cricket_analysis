import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
st.set_page_config(page_title="Asia Cup Cricket Analytics", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv("asiacup_cleaned.csv")

df = load_data()

st.title("🏏 Asia Cup Cricket Analytics Dashboard")

# Sidebar Filters

st.sidebar.header("🔎 Filter Matches")
year_list = sorted(df["year"].dropna().unique())
team_list = sorted(df["team"].dropna().unique())
opponent_list = sorted(df["opponent"].dropna().unique())

selected_year = st.sidebar.multiselect("Select Year(s):", year_list, default=year_list)
selected_team = st.sidebar.multiselect("Select Team(s):", team_list, default=team_list)
selected_opponent = st.sidebar.multiselect("Select Opponent(s):", opponent_list, default=opponent_list)

df_filtered = df[
    (df["year"].isin(selected_year)) &
    (df["team"].isin(selected_team)) &
    (df["opponent"].isin(selected_opponent))
]

# Add CSV Download Button
st.sidebar.markdown("---")
st.sidebar.subheader("💾 Download Data")

# Convert to CSV (string buffer)
csv_filtered = df_filtered.to_csv(index=False).encode("utf-8")
csv_full = df.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="⬇️ Download Filtered Data (CSV)",
    data=csv_filtered,
    file_name="asiacup_cleaned.csv",
    mime="text/csv"
)

st.sidebar.download_button(
    label="⬇️ Download Full Data (CSV)",
    data=csv_full,
    file_name="asiacup.csv",
    mime="text/csv"
)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["🏠 Overview", "🏏 Batting Analysis", "🎯 Bowling Analysis", "📊 Trends & Correlations", "📍 Venue & Toss", ""]
)

# Tab 1: Overview

with tab1:
    st.subheader("🏆 Tournament Overview")

    # --- KPIs ---
    total_matches = len(df_filtered)
    total_wins = df_filtered["win_binary"].sum()
    win_rate = round((total_wins / total_matches) * 100, 2) if total_matches > 0 else 0
    toss_win_rate = round(
        (df_filtered[df_filtered["toss"] == df_filtered["result"]].shape[0] / total_matches) * 100, 2
    ) if total_matches > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Total Matches", total_matches)
    col2.metric("✅ Win %", f"{win_rate}%")
    col3.metric("🎲 Toss → Win %", f"{toss_win_rate}%")

    st.markdown("---")

    # --- Team Performance (Stacked Bar with animation) ---
    st.subheader("📌 Team Performance Across Years")
    fig_team = px.bar(
        df_filtered, x="team", color="result",
        animation_frame="year", barmode="stack",
        title="Wins vs Losses by Team"
    )
    st.plotly_chart(fig_team, use_container_width=True)

    # --- Toss Impact (Sunburst Chart) ---
    st.subheader("📌 Toss Impact on Match Results")
    df_toss = df_filtered.dropna(subset=["toss", "selection", "result"])
    if not df_toss.empty:
        fig_toss = px.sunburst(
            df_toss, path=["toss", "selection", "result"],
            title="Toss → Decision → Match Result Breakdown"
        )
        st.plotly_chart(fig_toss, use_container_width=True)
    else:
        st.info("No toss data available for the selected filters.")




# Tab 2: Batting Analysis
 
with tab2:
   

    st.subheader("📌 Batting Margin vs Match Result")
    fig4 = px.scatter(df_filtered, x="batting_margin", y="run_scored",
                      color="result", hover_data=["team","opponent","year"],
                      title="Batting Margin vs Runs Scored")
    st.plotly_chart(fig4, use_container_width=True)


# Tab 3: Bowling Analysis

with tab3:
    st.subheader("📌 Bowling Effectiveness vs Match Result")
    fig5 = px.scatter(df_filtered, x="bowling_effectiveness", y="wicket_taken",
                      color="result", hover_data=["team","opponent","year"],
                      title="Bowling Effectiveness vs Wickets Taken")
    st.plotly_chart(fig5, use_container_width=True)


# Tab 4: Trends & Correlations

with tab4:
    st.subheader("📌 Feature Relationships (Scatter Matrix)")
    fig7 = px.scatter_matrix(df_filtered,
                             dimensions=["run_scored","wicket_lost","fours","sixes",
                                         "wicket_taken","avg_bat_strike_rate"],
                             color="result", title="Scatter Matrix of Match Features")
    st.plotly_chart(fig7, use_container_width=True)

    st.subheader("📌 Team Win Rate Over Time")
    win_rate = df_filtered.groupby(["year","team"])["win_binary"].mean().reset_index()
    fig7 = px.line(win_rate, x="year", y="win_binary", color="team",
                   markers=True, title="Team Win Rate Over Time")
    st.plotly_chart(fig7, use_container_width=True)


# Tab 5: Venue & Toss

with tab5:
    st.subheader("📌 Venue Advantage")
    fig8 = px.histogram(df_filtered, x="ground", color="result", barmode="group",
                        animation_frame="year", title="Match Results by Venue")
    st.plotly_chart(fig8, use_container_width=True)

    st.subheader("📌 Toss Decision Split (Bat vs Field)")
    fig9 = px.pie(df_filtered, names="selection", title="Bat vs Field Choice after Toss")
    st.plotly_chart(fig9, use_container_width=True)


# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center;">
        <p>👨‍💻 Developed by <b>Safee Imran</b></p>
        <p>🔗 <a href="https://github.com/SafeeImran" target="_blank">GitHub Profile</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
