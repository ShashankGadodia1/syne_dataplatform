{% snapshot snapshot__distribution_centers %}

{{
    config(
      target_schema='syne_dataplatform_snapshot',
      unique_key='id',
      strategy='check',
      check_cols=['name', 'latitude', 'longitude'],
	  invalidate_hard_deletes=True
    )
}}

SELECT * FROM {{ source('thelook_ecommerce', 'distribution_centers') }}

{% endsnapshot %}