#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name = "tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname = {}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("database connection failed")

def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute("truncate matches")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    # deleteMatches()
    db, cursor = connect()
    cursor.execute("truncate players cascade")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
    cursor.execute("select count(*) from players")
    num_of_players = cursor.fetchone()
    db.close()
    return num_of_players[0]



def registerPlayer(name):
    """Adds a player to the tournament database.
    
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db, cursor = connect()

    query = "insert into players (name) values (%s);"
    parameter = (name,)
    cursor.execute(query, parameter)

    db.commit()
    db.close()


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
    db, cursor = connect()

    cursor.execute("select * from match_c")
    player_lists = cursor.fetchall()
    db.close()

    return player_lists


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()

    query = "insert into matches (winner,loser) values (%s,%s)"
    parameter = (winner, loser)
    cursor.execute(query, parameter)
    db.commit()
    db.close()
 
 
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
    player_pairs = playerStandings()

    #do the pair matches process
    length = len(player_pairs)
    n = 0
    re = []
    while n < length:
        minion = (player_pairs[n][0], player_pairs[n][1], player_pairs[n+1][0], player_pairs[n+1][1])
        n = n + 2
        re.append(minion)

    return re


