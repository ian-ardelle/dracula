# CrossroadsVTM-Projects
The projects within this repository are used by Crossroads, the VtM Discord-based RP.
## Dracula
Dracula is a python-based bot which integrates with Discord, that pulls random integers from Random.org's generation engine via a JSON-RPC v2 request.
It utilizes several commands:

-$r2 [dicepool] [difficulty] [modifier]

-$re2 [dicepool] [difficulty] [modifier]

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
