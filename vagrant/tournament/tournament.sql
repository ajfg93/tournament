-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
drop database if exists tournament;
create database tournament;
\c tournament;

create table players (
	id serial PRIMARY KEY,
	name varchar(50) NOT NULL
);

create table matches (
	id serial PRIMARY KEY,
	winner smallint references players(id),
	loser smallint references players(id)
);

create view win_c as 
	select players.id, name, count(winner) as win_sum from 
	players left join matches 
	on players.id = winner
	group by players.id
	order by win_sum DESC;

create view lose_c as 
	select players.id, name, count(loser) as lose_sum from 
	players left join matches 
	on players.id = loser
	group by players.id
	order by lose_sum DESC;

create view match_c as
	select win_c.id, win_c.name, win_sum, (win_sum + lose_sum) as match
	from win_c, lose_c
	where win_c.id = lose_c.id
	order by match DESC, win_sum DESC;