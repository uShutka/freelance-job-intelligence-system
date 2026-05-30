import plotly.express as px
import streamlit as st

from freelance_job_intelligence_system.alerts.telegram import build_job_alert
from freelance_job_intelligence_system.analytics.market_metrics import (
    level_distribution,
    market_summary,
    rate_by_skill,
    skill_trends,
    source_summary,
)
from freelance_job_intelligence_system.pipeline import run_pipeline

st.set_page_config(page_title="Job Market Intelligence", layout="wide")

jobs = run_pipeline()
summary = market_summary(jobs)

st.title("Freelance & Remote Job Market Intelligence System")

top = st.columns(5)
top[0].metric("Jobs collected", summary["total_jobs"])
top[1].metric("Avg score", f"{summary['average_score']:.0f}/100")
top[2].metric("Avg rate", f"${summary['average_hourly_rate']:.0f}/h")
top[3].metric("Remote share", f"{summary['remote_share']:.0%}")
top[4].metric("Top score", f"{summary['top_job_score']}/100")

left, right = st.columns([1.2, 1])
with left:
    st.subheader("Top matching jobs")
    st.dataframe(jobs[["title", "source", "score", "hourly_rate", "level", "skills"]].head(10), use_container_width=True)
with right:
    st.subheader("Skill demand")
    st.plotly_chart(px.bar(skill_trends(jobs).head(10), x="skill", y="jobs"), use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Source quality")
    st.dataframe(source_summary(jobs), use_container_width=True)
with col_b:
    st.subheader("Rates by skill")
    st.dataframe(rate_by_skill(jobs), use_container_width=True)

st.subheader("Level distribution")
st.plotly_chart(px.bar(level_distribution(jobs), x="level", y="jobs", color="level"), use_container_width=True)

st.subheader("Telegram alert preview")
st.code(build_job_alert(jobs.iloc[0]))
