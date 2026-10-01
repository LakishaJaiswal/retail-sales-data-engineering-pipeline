-- 1. Total Revenue
SELECT
    SUM(revenue) AS total_revenue
FROM fact_sales;


-- 2. Total Orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM fact_sales;


-- 3. Total Quantity Sold
SELECT
    SUM(quantity) AS total_quantity
FROM fact_sales;


-- 4. Average Order Value
SELECT
    ROUND(
        SUM(revenue) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value
FROM fact_sales;


-- 5. Revenue by Month
SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.revenue) AS monthly_revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- 6. Revenue by Region
SELECT
    c.region,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.region
ORDER BY revenue DESC;


-- 7. Revenue by Product Category
SELECT
    p.category,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY revenue DESC;


-- 8. Top Products
SELECT
    p.product_id,
    p.category,
    SUM(f.quantity) AS units_sold,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_id,
    p.category
ORDER BY revenue DESC
LIMIT 5;


-- 9. Customer Revenue
SELECT
    c.customer_id,
    c.region,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY
    c.customer_id,
    c.region
ORDER BY revenue DESC;


-- 10. Monthly Category Performance
SELECT
    d.month_name,
    p.category,
    SUM(f.revenue) AS revenue
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    d.month,
    d.month_name,
    p.category
ORDER BY
    d.month,
    revenue DESC;
