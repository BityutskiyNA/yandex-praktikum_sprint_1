CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid NOT NULL,
    film_work_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person_film_work (id, person_id, film_work_id);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.genre_film_work (id, genre_id, film_work_id);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.person (id, full_name);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.genre (id, name);
CREATE UNIQUE INDEX IF NOT EXISTS film_work_person_idx ON content.film_work (id, title);

CREATE INDEX IF NOT EXISTS film_work_person_idx ON content.film_work (title);
CREATE INDEX IF NOT EXISTS film_work_person_idx ON content.person (full_name);
CREATE INDEX IF NOT EXISTS film_work_person_idx ON content.genre (name);

SET search_path TO content,public;