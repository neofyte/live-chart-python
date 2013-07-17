drop table if exists A___2SPL;
create table A___2SPL (
    id integer primary key autoincrement,
    datetime text unique,
    height real
);
drop table if exists A___2NPL;
create table A___2NPL (
    id integer primary key autoincrement,
    datetime text unique,
    height real
);