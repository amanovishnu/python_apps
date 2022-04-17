create table log_table (
    id integer primary key auto_increment,
    entry_date date not null
);

create table food (
    id integer primary key auto_increment,
    name text not null,
    protein integer not null,
    carbohydrates integer not null,
    fat integer not null,
    calories integer not null,
);

create table food_date (
    food_id integer not null,
    log_date_id integer not null,
    primary key(food_id, log_date_id)
);