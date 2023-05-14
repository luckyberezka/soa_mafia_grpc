# Default Server Address For Testing
HOST = "0.0.0.0"
PORT = "8080"

# Entry modes
CREATE_ROOM = "Create a new game session"
JOIN_ROOM = "Join the game session"
ENTRY_MODES_LIST = [CREATE_ROOM, JOIN_ROOM]

# Game statuses
PREPARING = 0
RUNNING = 1
INVALID = 2

# Time Of Day
DAY = "Day"
NIGHT = "Night"

# Notify Types
INFO = 0
JOIN = 1
KILL = 2
END = 3


# ACTIONS
VOTEKILL = "Execute a player"
GET_INFO = "Get info"
END_DAY = "End the day"
END_NIGHT = "End the night"
SUSPEND = "Suspend"
CHECK_ROLE = "Check role"
PUBLISH_DATA = "Publish new data the next day"
EXIT = "Exit"
FIRST_DAY_ACTIONS = [END_DAY]
DAY_ACTIONS = [VOTEKILL, GET_INFO, END_DAY]
NIGHT_MAFIA_ACTIONS = [VOTEKILL, GET_INFO, END_NIGHT]
NIGHT_OFFICER_ACTIONS = [CHECK_ROLE, GET_INFO, END_NIGHT]
SPIRIT_ACTIONS = [SUSPEND, EXIT]

# Roles
UNKNOWN_ROLE = "Unknown"
MAFIA_ROLE = "Mafia"
OFFICER_ROLE = "Officer"
CIVILIAN_ROLE = "Civilian"
SPIRIT_ROLE = "Spirit"
