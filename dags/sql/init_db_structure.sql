--Создаем схему SRC в БД, если ее не существует
CREATE SCHEMA IF NOT EXISTS dwh_src;
CREATE SCHEMA IF NOT EXISTS dwh_ods;

CREATE TABLE IF NOT EXISTS dwh_src.movies_raw_json (
    id SERIAL NOT NULL PRIMARY KEY,
    data JSONB,
    loaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--переехали в dbt
-- -- Таблица фильмов
-- CREATE TABLE movies (
--     movie_id INT PRIMARY KEY,
--     name VARCHAR(255),
--     release_year INTEGER
-- );



-- CREATE TABLE movie_directors (
--     movie_id INTEGER REFERENCES movies(movie_id),
--     star_id INTEGER REFERENCES people(star_id),
--     PRIMARY KEY (movie_id, star_id)
-- );

-- CREATE TABLE movie_stars (
--     movie_id INTEGER REFERENCES movies(movie_id),
--     star_id INTEGER REFERENCES people(star_id),
--     PRIMARY KEY (movie_id, star_id)
-- );