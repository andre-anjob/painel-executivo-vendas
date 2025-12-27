import streamlit as st
import pandas as pd
import plotly.express as px
import calendar

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
# CSS EXECUTIVO
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
</style>
""", unsafe_allow_html=True)

# ===============================
# CONFIG PLOTLY
# ===============================
PLOTLY_CONFIG = {
    "responsive": True,
    "displaylogo": False
}

# ===============================
# FUNÇÕES AUXILIARES
# ===============================
def calcular_variacao(atual, anterior):
    if anterior == 0:
        return 0
    return ((atual - anterior) / anterior) * 100

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

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
# TÍTULO
# ===============================
st.markdown("## 📊 Painel Executivo de Vendas")
st.markdown("Visão estratégica da performance comercial")

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
# KPIs GERAIS
# ===============================
st.markdown("## 📌 Visão Geral")

faturamento_total = df_f["valor_total"].sum()
qtd_vendas = len(df_f)
ticket_medio = faturamento_total / qtd_vendas if qtd_vendas else 0

col1, col2, col3 = st.columns(3)

col1.metric("💰 Faturamento", formatar_moeda(faturamento_total))
col2.metric("🧾 Volume de Vendas", f"{qtd_vendas:,}")
col3.metric("🎯 Ticket Médio", formatar_moeda(ticket_medio))

st.divider()

# ===============================
# PREVISÃO MENSAL
# ===============================
st.markdown("## 🔮 Previsão Mensal")

data_ref = df_f["data_venda"].max()
mes_ref = data_ref.month
ano_ref = data_ref.year

dias_no_mes = calendar.monthrange(ano_ref, mes_ref)[1]
dia_atual = data_ref.day

df_mes = df_f[
    (df_f["data_venda"].dt.month == mes_ref) &
    (df_f["data_venda"].dt.year == ano_ref)
]

faturamento_mes = df_mes["valor_total"].sum()

previsao_mes = (
    (faturamento_mes / dia_atual) * dias_no_mes
    if dia_atual > 0 else 0
)

saldo_mes = previsao_mes - faturamento_mes

colp1, colp2, colp3 = st.columns(3)

colp1.metric("📆 Previsão do Mês", formatar_moeda(previsao_mes))
colp2.metric("📊 Faturamento do Mês", formatar_moeda(faturamento_mes))
colp3.metric(
    "📉 Saldo para Atingir a Previsão",
    formatar_moeda(max(saldo_mes, 0))
)

if saldo_mes <= 0:
    st.success("✅ A previsão mensal já foi atingida ou superada.")
else:
    st.info("ℹ️ Ainda há faturamento necessário para atingir a previsão mensal.")

st.divider()

# ===============================
# PREVISÃO ANUAL (YTD)
# ===============================
st.markdown("## 📅 Previsão Anual (YTD)")

inicio_ano = pd.Timestamp(year=ano_ref, month=1, day=1)
fim_ano = pd.Timestamp(year=ano_ref, month=12, day=31)

df_ano = df[
    (df["data_venda"] >= inicio_ano) &
    (df["data_venda"] <= data_ref)
]

if canal != "Todos":
    df_ano = df_ano[df_ano["canal_venda"] == canal]

if vendedor != "Todos":
    df_ano = df_ano[df_ano["nome_vendedor"] == vendedor]

faturamento_ytd = df_ano["valor_total"].sum()

dias_corridos = (data_ref - inicio_ano).days + 1
dias_ano = 366 if calendar.isleap(ano_ref) else 365

previsao_anual = (
    (faturamento_ytd / dias_corridos) * dias_ano
    if dias_corridos > 0 else 0
)

saldo_anual = previsao_anual - faturamento_ytd

cola1, cola2, cola3 = st.columns(3)

cola1.metric("📅 Previsão Anual", formatar_moeda(previsao_anual))
cola2.metric("📊 Faturamento no Ano", formatar_moeda(faturamento_ytd))
cola3.metric(
    "📉 Saldo para Atingir a Previsão",
    formatar_moeda(max(saldo_anual, 0))
)

if saldo_anual <= 0:
    st.success("✅ A projeção anual já foi atingida ou superada.")
else:
    st.warning("⚠️ O faturamento anual está abaixo da projeção.")

st.divider()

# ===============================
# EVOLUÇÃO TEMPORAL
# ===============================
st.markdown("## 📈 Evolução dos Resultados")

df_time = (
    df_f
    .groupby(pd.Grouper(key="data_venda", freq="M"))
    .agg(faturamento=("valor_total", "sum"))
    .reset_index()
)

fig_time = px.line(df_time, x="data_venda", y="faturamento", markers=True)
fig_time.update_yaxes(tickprefix="R$ ", tickformat=",.2f")

st.plotly_chart(fig_time, config=PLOTLY_CONFIG, use_container_width=True)

# ===============================
# PERFORMANCE COMERCIAL
# ===============================
st.markdown("## 🏆 Performance Comercial")

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
        text=df_vend["faturamento"].apply(formatar_moeda)
    )

    fig_vend.update_xaxes(tickprefix="R$ ", tickformat=",.2f")
    st.plotly_chart(fig_vend, config=PLOTLY_CONFIG, use_container_width=True)

with col5:
    df_canal = (
        df_f.groupby("canal_venda", as_index=False)
        .agg(faturamento=("valor_total", "sum"))
    )

    fig_canal = px.pie(df_canal, names="canal_venda", values="faturamento")
    fig_canal.update_traces(textinfo="percent+label")

    st.plotly_chart(fig_canal, config=PLOTLY_CONFIG, use_container_width=True)

# ===============================
# TABELA DETALHADA
# ===============================
st.markdown("## 📋 Detalhamento das Vendas")

df_tabela = df_f.copy()
df_tabela["valor_total"] = df_tabela["valor_total"].apply(formatar_moeda)

st.dataframe(df_tabela, use_container_width=True)
