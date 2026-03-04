def format_match(match):

    teams = match.get("teams", [])

    score = match.get("score", [])

    status = match.get("status", "")

    summary = f"""
Match: {teams}

Status: {status}

Score: {score}
"""

    return summary