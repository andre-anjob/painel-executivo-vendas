import pandas as pd
from db import get_engine
import queries

def run_query(sql):
    engine = get_engine()
    return pd.read_sql(sql, engine)

def main():
    df_faturamento = run_query(queries.FATURAMENTO_MENSAL)
    df_top_vendedores = run_query(queries.TOP_VENDEDORES)
    df_canal = run_query(queries.CANAL_VENDA)

    print("Faturamento mensal:")
    print(df_faturamento.head())

    print("\nTop vendedores:")
    print(df_top_vendedores)

    print("\nCanal de venda:")
    print(df_canal)

if __name__ == "__main__":
    main()
