-- Schema for to-do application examples.

-- Projects are high-level activities made up of tasks
create table readings (
    sensor  text,
    value text,
    reading_date  date,
    PRIMARY KEY (sensor, reading_date)
);

create table gps (
    latitude  real,
    longitude real,
    altitude real,
    reading_date  date,
    PRIMARY KEY (reading_date)
);
