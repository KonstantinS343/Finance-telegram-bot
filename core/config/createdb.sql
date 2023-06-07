create table category(
    main_idtf varchar(255) primary key,
    name varchar(255)
);

create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category_key integer,
    foreign key(category_key) references category(main_idtf)
);

create table budget(
    id integer primary key,
    balance real
);

insert into category (main_idtf, name) 
values 
    ("food" ,"еда"),
    ("entertainments", "развлечения"),
    ("rent", "аренда"),
    ("home", "дом"),
    ("transport", "транспорт"),
    ("gifts", "подарки"),
    ("health", "здоровье"),
    ("other", "другое");