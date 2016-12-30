#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("update matches set round = 0; update scores set wins = 0;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    # deleteMatches()
    conn = connect()
    c = conn.cursor()
    c.execute("delete from scores; delete from matches;")
    c.execute("delete from players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    num_of_players = 0
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) from players")
    num_of_players = c.fetchone()
    conn.close()
    return num_of_players[0]



def registerPlayer(name):
    """Adds a player to the tournament database.
    
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into players (name) values (%s) returning id;", (name,))
    player_id = c.fetchone()[0]
    #initialized so I can use "update" in reportMatch
    c.execute("insert into matches (id) values (%s)", (player_id,))
    c.execute("insert into scores (id) values (%s)", (player_id,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select players.id, name , wins , round from players left join scores on players.id = scores.id left join matches on players.id = matches.id order by wins DESC")
    player_lists = c.fetchall()
    conn.close()

    return player_lists


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("update scores set wins = wins + 1 where id = %s", (winner,))
    c.execute("update matches set round = round + 1 where id = %s", (winner,))
    c.execute("update matches set round = round + 1 where id = %s", (loser,))
    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select id, name from player_pairs order by wins DESC;")
    player_pairs = c.fetchall()
    conn.close()

    #do the pair matches process
    length = len(player_pairs)
    n = 0
    re = []
    while n < length:
        minion = player_pairs[n] + player_pairs[n+1]
        n = n + 2
        re.append(minion)

    return re


