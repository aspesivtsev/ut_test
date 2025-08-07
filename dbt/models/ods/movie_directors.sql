{{
  config(
    materialized='table'
  )
}}

WITH raw_data AS (
    SELECT
      movie_id,
      jsonb_array_elements_text(directors) AS director_name
    FROM {{ ref('movies') }}
  )

SELECT
  movie_id,
  {{ dbt_utils.generate_surrogate_key(['director_name']) }} AS director_id
FROM raw_data
