"""Fixed Unit 8 submission fixtures and their provenance.

LABEL_SAMPLES copies the six exact Unit 7 samples saved in README.md. The
full human_original is the verified original draft. plain_human overlaps that
draft, formal_human is the Gettysburg Address, and mixed_edit is AI-edited.

GENERATED_SAMPLES was written by Codex for Unit 8. Its plain and formal
examples are synthetic style probes and do not count as the learner's writing
for criteria 1 or 2.
"""

LABEL_SAMPLES = {
    "ai_original": (
        "Effective communication plays an important role in the success of any "
        "organization. By establishing clear goals and encouraging open dialogue, teams "
        "can work together to achieve shared objectives. A structured approach helps "
        "individuals understand their responsibilities and contribute to a positive "
        "working environment. Regular feedback provides opportunities for continuous "
        "improvement and supports the development of valuable skills. In addition, "
        "consistent communication helps build trust and strengthens relationships among "
        "team members. Ultimately, organizations that prioritize these practices are "
        "better positioned to adapt to changing circumstances and achieve long-term "
        "success."
    ),
    "human_original": (
        "According to `detector.py`, ai writers tend to write in a straightforward , "
        "linear style , where the next word or token is likely predictable or to follow "
        "the words coming before, while humans do the opposite. Human writers could "
        "write \"AI-like\" by writing in a plain and structured way. Having structure and "
        "straightforwardness is correlated with sounding like an AI. P.S., I can see "
        "how this would hurt people who trained or studied to make their writer cleaner "
        "and well structured."
    ),
    "mixed_edit": (
        "According to detector.py, AI-generated text tends to follow predictable "
        "patterns, where the next word or token is likely given the words before it. "
        "Human writing can be less predictable, but humans do not always write that "
        "way. Human writers can write in an AI-looking way by using plain, structured "
        "language. The signal cannot tell whether that predictability came from a "
        "person or an AI. I can see how this could hurt people who trained or studied "
        "to make their writing clearer and well structured."
    ),
    "formal_human": (
        "Fourscore and seven years ago our fathers brought forth on this continent a "
        "new nation, conceived in liberty and dedicated to the proposition that all men "
        "are created equal. Now we are engaged in a great civil war, testing whether "
        "that nation or any nation so conceived and so dedicated can long endure. We "
        "are met on a great battlefield of that war. We have come to dedicate a portion "
        "of that field as a final resting-place for those who here gave their lives "
        "that that nation might live. It is altogether fitting and proper that we "
        "should do this. But in a larger sense, we cannot dedicate, we cannot "
        "consecrate, we cannot hallow this ground."
    ),
    "ai_light_edit": (
        "Effective communication matters in the success of any organization. By "
        "establishing clear goals and encouraging open dialogue, teams can work "
        "together to achieve shared objectives. A structured approach helps individuals "
        "understand their responsibilities and contribute to a positive working "
        "environment. Regular feedback provides opportunities for continuous "
        "improvement and supports the development of valuable skills. In addition, "
        "consistent communication helps build trust and strengthens relationships among "
        "team members. In the end, organizations that prioritize these practices are "
        "better positioned to adapt to changing circumstances and achieve lasting "
        "success."
    ),
    "plain_human": (
        "Human writers could write \"AI-like\" by writing in a plain and structured way. "
        "Having structure and straightforwardness is correlated with sounding like an "
        "AI. P.S., I can see how this would hurt people who trained or studied to make "
        "their writer cleaner and well structured."
    ),
}

GENERATED_SAMPLES = {
    "plain_bike": (
        "The chain came off halfway up the hill. I turned the bike over on a patch of "
        "grass, then tucked the chain back onto the little ring. My hands smelled like "
        "pennies all the way home. I had a napkin in my pocket, but it just stuck to "
        "the grease."
    ),
    "plain_rain": (
        "I left the washing out because the sky over the shed looked clear. By the time "
        "I heard rain against the window, one sleeve was already dripping into the "
        "mint. I brought the shirts inside and draped them over the backs of the "
        "kitchen chairs."
    ),
    "plain_library": (
        "The small branch library has a drawer full of pencils by the door. On Tuesday "
        "the drawer jammed, so the librarian put a handful in an old teacup. I borrowed "
        "one to copy a recipe and gave it back before I left."
    ),
    "plain_soup": (
        "I put too much lemon in the soup and spent ten minutes trying to get it right "
        "again. In the end I added a potato and ate it with toast. The next day the "
        "soup tasted fine cold, straight from the mug."
    ),
    "formal_archive": (
        "The cataloguing protocol assigns a stable identifier to each acquisition "
        "before the condition report is entered. When an item changes location, staff "
        "append the new location and date to the custody record. This policy allows a "
        "later reviewer to reconstruct the movement of an item from the original "
        "accession to its current shelf."
    ),
    "formal_water": (
        "The survey distinguished intermittent surface flow from standing water "
        "sustained by the shallow water table. Observations made after two days of rain "
        "were retained in the field record. These observations were analyzed separately "
        "because they reflected the effects of a discrete weather event."
    ),
    "formal_notice": (
        "Applications received after the published deadline will be considered in the "
        "next review period. An application is complete when the office has received "
        "the signed form and the two supporting documents. Applicants may request a "
        "written acknowledgment showing the date on which each document was received."
    ),
    "formal_transit": (
        "The revised timetable shifts the first weekday departure seven minutes "
        "earlier. The schedule change is intended to reduce transfer time at the "
        "northern terminal during the morning peak. Passenger counts from the first "
        "four weeks will be used to assess whether the adjustment improves the "
        "connection."
    ),
    "ai_planning": (
        "Good planning helps a group make steady progress on a shared task. When team "
        "members know their roles, they can focus on the work in front of them. A "
        "simple plan also makes it easier to review progress and decide what to do "
        "next. Teams can update the plan as new information comes in."
    ),
    "ai_workspace": (
        "A clean workspace can make daily tasks easier to manage. Put the things you "
        "use most often within reach and store the rest in clearly marked containers. "
        "Set aside a few minutes at the end of the day to return each item to its "
        "place. A regular routine keeps the space ready for the next task."
    ),
}

STYLE_PROBES = [text for name, text in GENERATED_SAMPLES.items() if name.startswith(("plain_", "formal_"))]

# The Unit 7 draft and the learner's numbered replies to the Unit 8 prompts.
# Keep the wording of each reply, including placeholders and typos.
AUTHOR_SAMPLES = {
    "unit7_draft": LABEL_SAMPLES["human_original"],
    "1_ubuntu_update": (
        "I was using a fresh distribution update for Ubuntu Linux. I noticed that one of "
        "the packages did not update, and I wanted to be able to use it as soon as possible. "
        "So I had an AI agent to find out a way to port it over and be able to use it."
    ),
    "2_cooking": (
        "Cooking typically goes way longer than I'd like it to. I always underestimate "
        "myself and the time it takes for me to cook. I should start planning out each steps "
        "and the projected time from start to finish."
    ),
    "3_consistency": (
        "I learnt that consistency is always better than intensity. I used to rely on bursts "
        "of hard effort and trying to believe that the reward or relaxation afterward would "
        "last forever. However, life isn't like that nor will it reward you with everlasting "
        "peace. Noticing how you feel and your energy levels also helps with being consistent "
        "at something and that leads to greater results."
    ),
    "4_productivity": (
        "I decided to read productivity quick tips and compare strategies instead of actually "
        "practicing or implementing them. I think I defaulted into doing the easier route "
        "because I thought it would give me similar benefits, but in reality, I was probably "
        "avoiding the necessary work."
    ),
    "5_team_note": (
        "Hey team, I noticed that xyz has been giving us the reoccuring issue of xyz. I think "
        "we should try to do xyz because xyz would reduce the issue xyz."
    ),
    "6_course_summary": (
        "In CodePath's AI Engineering course, I learned how to trace a model's output and "
        "workflow, from start to finish. We had assignments on creating a system that was "
        "optimized for observability and maintenance, and I think it helped me develop how to "
        "think as an engineer. I looked at the data, how the model retrieved it and what "
        "guidance it underwent, and how everything shaped the result."
    ),
    "7_upload_notice": (
        "Hello,\n"
        "I saw that <insert platform name> wasn't able to accept your upload and it says it "
        "failed/no-upload from here. Could you try to see if you have the right file type and "
        "if you get a confirmation message? Feel free to contact me or the course assistants "
        "if you need more help!"
    ),
}

# Fix the median comparison group before scoring. It includes both registers.
HUMAN_GROUP_NAMES = ("unit7_draft", "3_consistency", "5_team_note", "6_course_summary")
HUMAN_GROUP = [AUTHOR_SAMPLES[name] for name in HUMAN_GROUP_NAMES]
AI_GROUP = [
    LABEL_SAMPLES["ai_original"],
    LABEL_SAMPLES["ai_light_edit"],
    GENERATED_SAMPLES["ai_planning"],
    GENERATED_SAMPLES["ai_workspace"],
]
APPEAL_SAMPLES = [LABEL_SAMPLES[name] for name in ("human_original", "mixed_edit", "ai_original")]

BAD_INPUTS = [
    {"creator_id": "eval_bad_missing_text"},
    {"creator_id": "eval_bad_empty", "text": ""},
    {"creator_id": "eval_bad_spaces", "text": "   "},
    {"creator_id": "eval_bad_null", "text": None},
    {"creator_id": "eval_bad_number", "text": 42},
    {"creator_id": "eval_bad_text_list", "text": ["one", "two", "three"]},
    ["body", "is", "a list"],
    {"text": "This writing has no creator ID."},
    {"creator_id": 42, "text": "This writing has a numeric creator ID."},
    {"creator_id": "   ", "text": "This writing has a blank creator ID."},
    {"creator_id": "eval_bad_short", "text": "Two words"},
    {"creator_id": "eval_bad_long", "text": "word " * 2400 + "x"},
]

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        "texts": list(AUTHOR_SAMPLES.values()),
    },
    {
        "name": "synthetic plain and formal writing",
        "texts": STYLE_PROBES,
    },
    {
        "name": "four AI-generated pieces",
        "criterion": 2,
        "texts": AI_GROUP,
    },
    {
        "name": "four human-written pieces",
        "criterion": 2,
        "texts": HUMAN_GROUP,
    },
    {
        "name": "six label samples",
        "criterion": 3,
        "texts": list(LABEL_SAMPLES.values()),
    },
    # Criterion 4 uses APPEAL_SAMPLES followed by separate /appeal requests.
    {
        "name": "twelve invalid submission bodies",
        "criterion": 5,
        "bodies": BAD_INPUTS,
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            if not isinstance(bodies, list):
                problems.append(f"scenario {i}, bodies must be a list of request bodies")
                continue
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, (dict, list)):
                    problems.append(f"scenario {i}, body {j} must be a JSON object or array")
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
