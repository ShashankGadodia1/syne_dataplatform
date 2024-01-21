def model(dbt, session):

    dbt.config(materialized="table" #,packages = ["numpy==1.23.1", "pyspark"]
               )
    #products=dbt.ref('stg_ecommerce__products')
    order_items=dbt.ref('stg_ecommerce__order_items')

    '''final_df = (
       products
       .join(order_items, products.product_id == order_items.product_id, 'inner')
       .select(order_items.order_item_id.alias('order_item_id'),
               order_items.order_id.alias('order_id'),
               order_items.user_id.alias('user_id'),
               order_items.product_id.alias('product_id'),
               order_items.item_sale_price.alias('item_sale_price'),
               products.product_department.alias('product_department'),
               products.product_cost.alias('product_cost'),
               products.product_retail_price.alias('product_retail_price')
       )
   )'''
    df = order_items.to_pandas_on_spark()

    return df

    #return final_df