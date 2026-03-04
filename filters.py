IMPORTANT_TEAMS = [
    "India",
    "Australia",
    "England",
    "Pakistan",
    "New Zealand",
    "South Africa"
]

KEYWORDS = [
    "ipl",
    "world cup",
    "t20",
    "odi",
    "test"
]

def is_important_match(match):

    name = match.get("name", "").lower()

    for team in IMPORTANT_TEAMS:
        if team.lower() in name:
            return True

    for keyword in KEYWORDS:
        if keyword in name:
            return True

    return False