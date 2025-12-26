import streamlit as st
import pandas as pd
import plotly.express as px

from db import get_engine
import queries

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="Painel Executivo de Vendas",
    page_icon="📊",
    layout="wide"
)

# ===============================
# CSS EXECUTIVO (VISUAL)
# ===============================
st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-weight: 600;
    }

    .kpi-card {
        background-color: #f9fafb;
        border-radius: 12px;
        padding: 20px;
        border-left: 6px solid #2563eb;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
    }

    .kpi-title {
        font-size: 14px;
        color: #6b7280;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: bold;
        color: #111827;
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# TÍTULO
# ===============================
st.markdown("## 📊 Painel Executivo de Vendas")
st.markdown("Visão estratégica da performance comercial")

# ===============================
# CONFIG PLOTLY
# ===============================
PLOTLY_CONFIG = {
    "responsive": True,
    "displaylogo": False
}

# ===============================
# CARREGAMENTO DOS DADOS
# ===============================
@st.cache_data(ttl=600)
def load_base():
    engine = get_engine()
    return pd.read_sql(queries.BASE_VENDAS, engine)

df = load_base()
df["data_venda"] = pd.to_datetime(df["data_venda"])

# ===============================
# SIDEBAR - FILTROS
# ===============================
st.sidebar.markdown("## 🎛️ Filtros")

data_min = df["data_venda"].min()
data_max = df["data_venda"].max()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

canal = st.sidebar.selectbox(
    "Canal de Venda",
    ["Todos"] + sorted(df["canal_venda"].unique())
)

vendedor = st.sidebar.selectbox(
    "Vendedor",
    ["Todos"] + sorted(df["nome_vendedor"].unique())
)

# ===============================
# APLICAÇÃO DOS FILTROS
# ===============================
df_f = df.copy()

if len(periodo) == 2:
    df_f = df_f[
        (df_f["data_venda"] >= pd.to_datetime(periodo[0])) &
        (df_f["data_venda"] <= pd.to_datetime(periodo[1]))
    ]

if canal != "Todos":
    df_f = df_f[df_f["canal_venda"] == canal]

if vendedor != "Todos":
    df_f = df_f[df_f["nome_vendedor"] == vendedor]

# ===============================
# KPIs EXECUTIVOS
# ===============================
faturamento = df_f["valor_total"].sum()
qtd_vendas = len(df_f)
ticket_medio = faturamento / qtd_vendas if qtd_vendas else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Faturamento Total</div>
        <div class="kpi-value">R$ {faturamento:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Total de Vendas</div>
        <div class="kpi-value">{qtd_vendas:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">Ticket Médio</div>
        <div class="kpi-value">R$ {ticket_medio:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ===============================
# FATURAMENTO AO LONGO DO TEMPO
# ===============================
df_time = (
    df_f
    .groupby(pd.Grouper(key="data_venda", freq="M"))
    .agg(faturamento=("valor_total", "sum"))
    .reset_index()
)

fig_time = px.line(
    df_time,
    x="data_venda",
    y="faturamento",
    title="Evolução do Faturamento",
    markers=True
)

st.plotly_chart(fig_time, config=PLOTLY_CONFIG, use_container_width=True)

# ===============================
# GRÁFICOS LATERAIS
# ===============================
col4, col5 = st.columns(2)

with col4:
    df_vend = (
        df_f.groupby("nome_vendedor", as_index=False)
        .agg(faturamento=("valor_total", "sum"))
        .sort_values("faturamento", ascending=False)
        .head(10)
    )

    fig_vend = px.bar(
        df_vend,
        x="faturamento",
        y="nome_vendedor",
        orientation="h",
        title="Top Vendedores"
    )

    st.plotly_chart(fig_vend, config=PLOTLY_CONFIG, use_container_width=True)

with col5:
    df_canal = (
        df_f.groupby("canal_venda", as_index=False)
        .agg(faturamento=("valor_total", "sum"))
    )

    fig_canal = px.pie(
        df_canal,
        names="canal_venda",
        values="faturamento",
        title="Distribuição por Canal"
    )

    st.plotly_chart(fig_canal, config=PLOTLY_CONFIG, use_container_width=True)

# ===============================
# TABELA FINAL
# ===============================
st.markdown("## 📋 Detalhamento das Vendas")
st.dataframe(df_f, use_container_width=True)
