{{
  config(
    materialized='table'
  )
}}

WITH source AS (
  SELECT jsonb_array_elements_text(stars) AS star_name
  FROM {{ ref('movies_raw') }}
)

SELECT DISTINCT
  {{ dbt_utils.generate_surrogate_key(['star_name']) }} AS star_id,
  star_name
FROM source
