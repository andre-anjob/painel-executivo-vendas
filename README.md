# 📊 Painel Executivo de Vendas

Dashboard executivo desenvolvido em Python com foco em análise estratégica de vendas, permitindo uma visão clara da performance comercial por período, vendedores, canais e clientes.

🔗 **Dashboard online:**  
https://painel-executivo-vendas.streamlit.app

---

## 🎯 Objetivo do Projeto

Este projeto foi desenvolvido com o objetivo de demonstrar competências práticas em:

- Análise de dados aplicada ao negócio
- Construção de dashboards executivos
- Integração com banco de dados em nuvem
- Deploy de aplicações Python para ambiente produtivo

O dashboard permite apoiar a tomada de decisão por gestores comerciais e lideranças.

---

## 🧠 Visão Geral da Solução

A aplicação consome dados de um banco PostgreSQL hospedado no Supabase, processa as informações com Python e apresenta os indicadores em um dashboard interativo utilizando Streamlit.

O foco principal está em **clareza, objetividade e usabilidade executiva**.

---

## 📌 Principais Indicadores (KPIs)

- Faturamento total e mensal
- Evolução de vendas ao longo do tempo
- Top vendedores por faturamento
- Distribuição de vendas por canal
- Análise de clientes e produtos

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Streamlit** (visualização e interface)
- **Pandas** (manipulação de dados)
- **Plotly** (gráficos interativos)
- **PostgreSQL** (banco de dados relacional)
- **Supabase** (banco em nuvem)
- **SQLAlchemy** (conexão com banco)
- **Git & GitHub** (versionamento)
- **Streamlit Cloud** (deploy)

---

## 🏗️ Arquitetura do Projeto

```text
├── dash.py               # Aplicação principal (Streamlit)
├── db.py                 # Conexão com o banco de dados
├── queries.py            # Consultas SQL
├── requirements.txt      # Dependências do projeto
├── README.md             # Documentação
└── .gitignore            # Arquivos ignorados pelo Git
