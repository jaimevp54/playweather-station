-- Schema for to-do application examples.

-- Projects are high-level activities made up of tasks
create table readings (
    sensor  text,
    value text,
    reading_date  date,
    is_delivered boolean NOT NULL DEFAULT FALSE ,
    PRIMARY KEY (sensor, reading_date)
);

create table gps (
    latitude  real,
    longitude real,
    altitude real,
    reading_date  date,
    is_delivered boolean NOT NULL DEFAULT FALSE ,
    PRIMARY KEY (reading_date)
);
