# Dracula: The Python-Based Character and Data Tracker for Discord TTRPGs
Dracula is a python-based bot which integrates with Discord. Initially, its intended function was merely that of a dice bot - simplifying calcualtions when it came to oWoD dice rolls. It expanded into a tracker for some of the more upkeep-intensive and difficult to track stats as well, specifically for a "living server"-styled game. It has since been expanded to support multiple rulesets and track additional information, including character experience and provide notifications, along with the ability to be used in multiple games at once.

## Commands
There are several commands Dracula offers, both in an administrative capacity, and for players and participants in the game itself. A basic three-tiered role structure is implemented for determining which commands a given member may use:

- Storyteller: The Storyteller role is a full-access role. It's effectively an administrative role - all commands are usable by Storytellers.
- Narrator: The Narrator role is closer to that of a moderator. Its purpose is to be able to retrieve data more than write it, and allows for some additional permissions without compromising the privacy of character data. It's akin to read-only access.
- Player / None: All other members of a given server are given limited access to commands, and some commands behave differently as well. Where Storytellers and Narrators have access to view others' character data with commands, Players are limited to their own character data.

Plans are in place to expand this three-tier structure to a more robust permissions list.

# Storyteller-only Commands
- $bp_wp_pop: Populates the stat-tracking database with default character stats for all who have the Player tag.
- $add_player [member_id]: Adds an entry to the stat-tracking database for a member with the given member_id.
- $set_bp [member_id] [value]: Sets the Blood Points of the specified member to a new value.


Both of these have the same default values: Dicepool = 1, Difficulty = 6, Modifier = 0. $r generates [dicepool] random integers, and
compares the results to that of the difficulty. After generating the successes, it takes the modifier and adds it to the success count
and prints the results / total successes as a Discord message, highlighting the user who initiated the command. $re is identical, but
it takes into account "exploding dice", and may query Random.org multiple times as a result. 

Additionally, it allows for generating random integers with Python3's own random.py library. This improves performance, and saves API calls. To use this system instead, try the following two commands:

-$r [dicepool] [difficulty] [modifier]

-$re [dicepool] [difficulty] [modifier]

=============================================

-$time

Takes no parameters but provides a date and timestamp for the IC universe of Crossroads, accounting for time compression and nighttime dilation.
