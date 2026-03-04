context_prompt = """
Extract sports context from the question.

Return JSON:

sport
teams
competition
intent
"""

analysis_prompt = """
You are a professional sports analyst.

Match data:
{data}

Question:
{question}

Explain:

1 match summary
2 why the team lost
3 turning point
4 key player
"""

content_prompt = """
You are a YouTube sports strategist.

Using this analysis:

{analysis}

Generate:

3 viral hooks
3 YouTube titles
Shorts script

Script format:

HOOK
FACT
TWIST
ENGAGEMENT
"""