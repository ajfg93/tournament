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
    c.execute("delete from scores; delete from matches;")
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    deleteMatches()
    conn = connect()
    c = conn.cursor()
    c.execute("delete from players")
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    num_of_players = 0
    conn = connect()
    c = conn.cursor()
    num_of_players =  c.execute("select count(*) from players")
    conn.close()
    if num_of_players:
        return num_of_players
    else:
        return 0


def registerPlayer(name):
    """Adds a player to the tournament database.
    
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    player_id = c.execute("insert into players (name) values (%s) returning id", (name,))
    print player_id
    print type(player_id)
    #initialized so I can use "update" in reportMatch
    # c.execute("insert into matches (id) values (%s)", (player_id,))
    # c.execute("insert into scores (id) values (%s)", (player_id,))

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
    player_lists = c.execute("select id, name, wins, round as matches from players, matches, scores where player.id = matches.id and matches.id = scores.id order by wins DESC")
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
    c.execute("update scores set win = win + 1 where id = %s", (winner,))
    c.execute("update matches set round = round + 1 where id = %s", (winner,))
    c.execute("update matches set round = rount + 1 where id = %s", (loser,))
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
    player_pairs = c.execute("select a.id as id1, a.name as name1, b.id as id2, b.name as name2 from player_pairs as a, player_pairs as b where a.wins = b.wins and a.round = b.round and a.id < b.id")
    conn.close()

    return player_pairs


