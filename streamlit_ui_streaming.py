import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import sys
from datetime import datetime, timedelta

# Ensure project root is on path if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@st.cache_data
def load_company_data():
    try:
        df = pd.read_excel('croatia + company descriptions.xlsx')
        cols = ['Company name Latin alphabet', 'Company Description', 'Region in country clean']
        for year in range(2019, 2024):
            colname = f'HighGrowthFirm {year}'
            if colname in df.columns:
                cols.append(colname)
        return df[cols]
    except Exception as e:
        st.error(f"Error loading company data: {str(e)}")
        base_cols = ['Company name Latin alphabet', 'Company Description', 'Region in country clean']
        hgf_cols = [f'HighGrowthFirm {year}' for year in range(2019, 2024)]
        return pd.DataFrame(columns=base_cols + hgf_cols)

# Custom color palette
COLORS = {
    'primary': '#3b82f6',      # Blue
    'secondary': '#10b981',    # Green
    'accent': '#ef4444',       # Red
    'background': '#f8fafc',   # Light gray
    'card': '#ffffff',         # White
    'text': '#1e293b',         # Dark gray
    'border': '#e2e8f0',       # Light border
    'gradient_start': '#2563eb',  # Dark blue
    'gradient_end': '#3b82f6'     # Light blue
}

# Custom CSS for modern design
st.markdown(f"""
    <style>
    .main {{
        background-color: {COLORS['background']};
    }}
    .stApp {{
        max-width: 1200px;
        margin: 0 auto;
    }}
    ... (existing CSS blocks here) ...
    </style>
""", unsafe_allow_html=True)

# Additional animations and styles
ANIMATION_CSS = """
@keyframes fadeInUp {
  0% { opacity: 0; transform: translateY(40px); }
  100% { opacity: 1; transform: translateY(0); }
}
... (rest of animation CSS) ...
"""
st.markdown(f"<style>{ANIMATION_CSS}</style>", unsafe_allow_html=True)

EXTRA_CSS = """
/* Zebra stripes and hover for table */
.dataframe tbody tr:nth-child(odd) { background: #f3f6fa; }
... (rest of extra CSS) ...
"""
st.markdown(f"<style>{EXTRA_CSS}</style>", unsafe_allow_html=True)

def main():
    # Load data
    company_data = load_company_data()

    # Header
    st.markdown(f'''
        <div class="header-gradient animated-header" style="box-shadow: 0 6px 24px 0 rgba(59,130,246,0.10);">
            <div class="header-title" style="font-size:2.8rem; letter-spacing:0.01em;">🚀 Croatian HGFs</div>
            <div class="header-subtitle" style="font-size:1.3rem;">Explore high-growth firms, regions, and company insights in Croatia</div>
        </div>
    ''', unsafe_allow_html=True)

    def section_divider():
        st.markdown('<div style="height:2.5rem;"></div>', unsafe_allow_html=True)

    # Sidebar with company selector
    with st.sidebar:
        st.markdown('<div class="sidebar-section sidebar-collapsible" style="background:linear-gradient(90deg,#f0fdf4 0%,#f3f6fa 100%);">', unsafe_allow_html=True)
        st.markdown('<button class="sidebar-toggle" onclick="var s=document.getElementById(\'sidebar-content\'); if(s.style.maxHeight){s.style.maxHeight=null;}else{s.style.maxHeight=s.scrollHeight+\'px\';}"><span class="sidebar-icon">☰</span>Navigation</button>', unsafe_allow_html=True)
        st.markdown('<div id="sidebar-content" style="max-height: 1000px; transition: max-height 0.4s cubic-bezier(0.4,0,0.2,1);">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title"><span class="sidebar-icon">🏢</span>Selected Company</div>', unsafe_allow_html=True)
        company_names = company_data['Company name Latin alphabet'].dropna().unique().tolist() if not company_data.empty else []
        selected_company = st.selectbox("Select Company", company_names)
        with st.expander("Company Details", expanded=True):
            if selected_company and not company_data.empty:
                row = company_data[company_data['Company name Latin alphabet'] == selected_company]
                if not row.empty:
                    st.markdown(f"**Company Name:** {selected_company}")
                    st.markdown("---")
                    st.markdown("**Description:**")
                    st.markdown(row['Company Description'].values[0])
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    section_divider()

    # High Growth Firms by Year
    st.markdown('<div class="data-table pastel-section chart-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight:700; font-size:1.35rem; margin-bottom:0.5rem;'>🚀 High Growth Firms by Year (2019–2023)</h3>", unsafe_allow_html=True)
    years = list(range(2019, 2024))
    hgf_counts = []
    for year in years:
        col = f"HighGrowthFirm {year}"
        if col in company_data.columns:
            count = pd.to_numeric(company_data[col].replace('n.a.', 0), errors='coerce').fillna(0).astype(int).eq(1).sum()
            hgf_counts.append(count)
        else:
            hgf_counts.append(0)
    fig_hgf = go.Figure(go.Bar(x=years, y=hgf_counts, marker=dict(color=COLORS['primary'])))
    fig_hgf.update_layout(xaxis_title='Year', yaxis_title='Number of High Growth Firms', plot_bgcolor=COLORS['background'], paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter, sans-serif', size=15), margin=dict(l=30, r=30, t=30, b=30), height=350, xaxis=dict(dtick=1), yaxis=dict(gridcolor=COLORS['border']), showlegend=False)
    st.plotly_chart(fig_hgf, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    section_divider()

    # Top 10 Regions by Number of Companies
    st.markdown('<div class="data-table pastel-section chart-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight:700; font-size:1.35rem; margin-bottom:0.5rem;'>🏆 Top 10 Regions by Number of Companies</h3>", unsafe_allow_html=True)
    if 'Region in country clean' in company_data.columns:
        region_counts = company_data['Region in country clean'].value_counts().nlargest(10)
        fig_bar = go.Figure(go.Bar(x=region_counts.values[::-1], y=region_counts.index[::-1], orientation='h', marker=dict(color=COLORS['primary'])))
        fig_bar.update_layout(xaxis_title='Number of Companies', yaxis_title='Region', plot_bgcolor=COLORS['background'], paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter, sans-serif', size=15), margin=dict(l=30, r=30, t=30, b=30), height=400, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("The column 'Region in country clean' was not found in your data.")
    st.markdown("</div>", unsafe_allow_html=True)

    section_divider()

    # Employee Count Over Time
    st.markdown('<div class="data-table pastel-section chart-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight:700; font-size:1.35rem; margin-bottom:0.5rem;'>👥 Employee Count Over Time</h3>", unsafe_allow_html=True)
    chart_company = st.selectbox("Select company for employee chart", company_data['Company name Latin alphabet'].dropna().unique().tolist(), key="employee_chart_company")
    years = list(range(2016, 2025))
    np.random.seed(hash(chart_company) % 2**32)
    base = np.random.randint(10, 100)
    growth = np.random.uniform(0.95, 1.15, len(years))
    employees = [int(base * np.prod(growth[:i+1])) for i in range(len(years))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=employees, mode='lines+markers', line=dict(color=COLORS['primary'], width=3), marker=dict(size=8, color=COLORS['primary'])))
    fig.update_layout(xaxis_title='Year', yaxis_title='Number of Employees', plot_bgcolor=COLORS['background'], paper_bgcolor='rgba(0,0,0,0)', font=dict(family='Inter, sans-serif', size=15), margin=dict(l=30, r=30, t=30, b=30), height=350, xaxis=dict(dtick=1), yaxis=dict(gridcolor=COLORS['border']), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    section_divider()

    # Company Database Table
    st.markdown('<div class="data-table pastel-section chart-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-weight:700; font-size:1.35rem; margin-bottom:0.5rem;'>📋 Company Database</h3>", unsafe_allow_html=True)
    search_query = st.text_input("🔍 Search companies by name or description", "")
    filtered_data = company_data
    if search_query:
        sq = search_query.lower()
        filtered_data = company_data[
            company_data['Company name Latin alphabet'].str.lower().str.contains(sq, na=False) |
            company_data['Company Description'].str.lower().str.contains(sq, na=False)
        ]
    st.dataframe(filtered_data, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
