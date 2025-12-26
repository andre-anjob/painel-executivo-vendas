FATURAMENTO_MENSAL = """
SELECT
    DATE_TRUNC('month', data_venda) AS mes,
    SUM(valor_total) AS faturamento,
    COUNT(*) AS qtd_vendas,
    AVG(valor_total) AS ticket_medio
FROM vendas
WHERE status_venda = 'Concluída'
GROUP BY 1
ORDER BY 1;
"""

TOP_VENDEDORES = """
SELECT
    vnd.nome_vendedor,
    SUM(v.valor_total) AS faturamento
FROM vendas v
JOIN vendedores vnd ON vnd.id_vendedor = v.id_vendedor
WHERE v.status_venda = 'Concluída'
GROUP BY vnd.nome_vendedor
ORDER BY faturamento DESC
LIMIT 5;
"""

CANAL_VENDA = """
SELECT
    canal_venda,
    SUM(valor_total) AS faturamento
FROM vendas
WHERE status_venda = 'Concluída'
GROUP BY canal_venda;
"""

BASE_VENDAS = """
SELECT
    v.data_venda,
    v.valor_total,
    v.status_venda,
    vnd.nome_vendedor,
    v.canal_venda
FROM vendas v
JOIN vendedores vnd ON vnd.id_vendedor = v.id_vendedor
WHERE v.status_venda = 'Concluída';

"""

