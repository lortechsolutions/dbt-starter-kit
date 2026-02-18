{{ config(
    materialized='view',
    contract={'enforced': true},
    tags=['staging', 'example'],
) }}

with example_orders as (
  select
    1 as order_id,
    'example'::string as status,
    current_timestamp() as created_at
)

select *
from example_orders

