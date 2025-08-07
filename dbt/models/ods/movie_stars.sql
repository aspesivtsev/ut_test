{{
  config(
    materialized='table'
  )
}}

WITH raw_data AS (
    SELECT
      movie_id,
      jsonb_array_elements_text(stars) AS star_name
    FROM {{ ref('movies') }}
  )
  
    SELECT
      movie_id,
      {{ dbt_utils.generate_surrogate_key(['star_name']) }} AS star_id
    FROM raw_data
  
