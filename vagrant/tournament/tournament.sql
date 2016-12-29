-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
create table players (
	id serial PRIMARY KEY,
	name varchar(50) NOT NULL,
	dateCreated timestamp DEFAULT current_timestamp
);

create table matches (
	id serial references players(id),
	round smallint NOT NULL DEFAULT 0,
	PRIMARY KEY (id)
);

create table scores (
	id serial references matches(id),
	wins smallint NOT NULL DEFAULT 0,
	PRIMARY KEY (id)
);

create view player_pairs as 
	select players.id, name, wins, round 
	from players, matches, scores
	where players.id = matches.id and 
	matches.id = scores.id;


