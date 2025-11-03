{{ config(materialized='table', tags=['staging']) }}

with source as (
    -- In a real project, reference external/raw data here
    select 1 as customer_id, 'Alice' as name, '2024-01-01'::date as signup_date
    union all
    select 2, 'Bob', '2024-02-10'::date
),
final as (
    select
        customer_id,
        name,
        signup_date
    from source
)
select * from final

