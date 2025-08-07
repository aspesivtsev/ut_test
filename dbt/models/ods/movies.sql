
{{
  config(
    materialized='table'
 
  )
}}




SELECT
  {{ dbt_utils.generate_surrogate_key(['name', 'released_year']) }} AS movie_id,
  *
FROM {{ ref('movies_raw') }}
