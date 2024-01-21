with source1 as (
    select * from {{ ref('fct_orders') }}
)
, source2 as (
    select * from {{ (ref('stg_ecommerce__products')) }}
)
SELECT fc.order_item_id
, p.product_id
, p.product_name
, p.product_category
, {{ percent_profit('fc.item_sale_price', 'fc.cost') }} AS percent_profit --defined macros
FROM source1 fc
inner join source2 p on fc.product_id = p.product_id
