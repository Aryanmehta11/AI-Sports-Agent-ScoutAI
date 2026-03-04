import time

from sports_api import get_matches
from filters import is_important_match
from formatter import format_match
from analyst import analyze_match
from storyteller import extract_story
from create_generator import generate_content

seen_matches = set()

while True:

    matches = get_matches()

    for match in matches:

        match_id = match["id"]

        if match_id in seen_matches:
            continue

        if not is_important_match(match):
            continue

        summary = format_match(match)

        analysis = analyze_match(summary)

        story = extract_story(analysis)

        content = generate_content(story)

        print("\n===== MATCH ANALYSIS =====")
        print(summary)

        print("\n===== STORY =====")
        print(story)

        print("\n===== CONTENT =====")
        print(content)

        seen_matches.add(match_id)

    time.sleep(300)