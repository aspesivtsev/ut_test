-- models/movies_raw.sql

{{
  config(
    materialized='table'
 
  )
}}


SELECT 
    
    data->>'name' AS name,
    (data->>'oscar')::int AS oscar,
    (data->>'released_year')::int AS released_year,
    data->>'poster' AS poster,
    data->>'rating' AS rating,
    data->>'duration' AS duration,
    data->>'genre' AS genres,
    data->>'summary' AS summary,
    (data->'directors')::JSONB AS directors,
    (data->'stars')::JSONB AS stars

FROM dwh_src.movies_raw_json

