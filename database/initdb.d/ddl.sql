CREATE TABLE access_log (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    request_time timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP
);