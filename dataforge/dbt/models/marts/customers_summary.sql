{{ config(materialized='table') }}

with customers as (
    select * from {{ ref('stg_customers') }}
),
metrics as (
    select count(*) as customer_count from customers
)
select
    current_date() as as_of_date,
    m.customer_count
from metrics m

