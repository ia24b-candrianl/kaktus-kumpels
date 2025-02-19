drop table if exists warenkorb, website, ventilator, customer, bestellung_credit, bestellung_rechnung, warenkorb_product, warenkorb cascade;

create table if not exists customer (
customer_id serial,
customer_firstname varchar(20),
customer_lastname varchar(20),
customer_email varchar(30),
customer_password varchar(20),
primary key (customer_id)
);


insert into customer (customer_firstname, customer_lastname, customer_email, customer_password)
values ('David','Roth', 'Dan.keller@gmail.com', '1234');

select * from customer;

delete from customer;


create table if not exists ventilator (
ventilator_id serial,
name varchar(20),
price integer,
performance integer,
description varchar(250),
primary key (ventilator_id)
);

select * from ventilator;


create table if not exists bestellung_credit (
bestellung_id serial,
customer_id integer,
card_number varchar(20),
safety_code varchar(5),
first_name varchar(20),
last_name varchar(20),
expiration date,
foreign key (customer_id) references customer (customer_id),
primary key (bestellung_id)
);

insert into bestellung_credit (customer_id, card_number, safety_code, first_name, last_name, expiration)
values ((SELECT customer_id FROM customer WHERE customer_firstname = 'Nicolai'),
'123456789123456', '234', 'Nicolai', 'Halbheer', '2008-01-18'); 

select * from bestellung_credit;


create table if not exists bestellung_rechnung (
bestellung_rechnung_id serial,
customer_id integer,
adress varchar(30),
last_name varchar(20),
first_name varchar(20),
email varchar(30),
foreign key (customer_id) references customer (customer_id),
primary key (bestellung_rechnung_id)
);

select * from bestellung_rechnung;

create table if not exists warenkorb (
warenkorb_id serial,
customer_id integer,
amount integer,
foreign key (customer_id) references customer (customer_id),
primary key (warenkorb_id)
);


select * from warenkorb;


create table if not exists warenkorb_produkt(
warenkorb_id integer,
ventilator_id integer,
menge integer,
primary key (warenkorb_id, ventilator_id),
foreign key (warenkorb_id) references warenkorb (warenkorb_id),
foreign key (ventilator_id) references ventilator (ventilator_id)

);

create table if not exists website (
website_id serial,
website_name varchar(20),
website_url varchar(100),
primary key (website_id)

);

select * from website;



