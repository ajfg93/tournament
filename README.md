#Project code introduction

#tables
I create 3 tables with reference keys and 1 views.

```
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

```
##main functions
- `registerPlayer` 
	- insert data in players table and return id.
	- use the id to initialize rows in table matches and scores. (round and wins have **0** as default value).
	- 
- `deleteMatches`
	- only set column round and wins to **0**. Do not delete the rows.
	
- `deletePlayers`
	- delete all rows from tables, including players.

- `swissPairings`
	- `select id, name from player_pairs order by wins DESC`. 
	- ```
		 #do the pair matches process
    length = len(player_pairs)
    n = 0
    re = []
    while n < length:
        minion = player_pairs[n] + player_pairs[n+1]
        n = n + 2
        re.append(minion)
	return re
	  ```
	- accroding to the rules of Swiss Match, before the match is finished, I can simply pair each two of the rows after descending querying.
		- check the **tournament_analysis.xlsx** to verify my assumption
