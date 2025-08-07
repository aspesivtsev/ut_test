{{
  config(
    materialized='table'
  )
}}

WITH source AS (
  SELECT jsonb_array_elements_text(directors) AS director_name
  FROM {{ ref('movies_raw') }}
)

SELECT DISTINCT
  {{ dbt_utils.generate_surrogate_key(['director_name']) }} AS director_id,
  director_name
FROM source

