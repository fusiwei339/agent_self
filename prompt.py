moon="""Your spacecraft has just crash-landed on the lighted side of the Mars. You were scheduled to rendezvous with the mother ship 300 miles away on the surface of the moon, but the rough landing has ruined your craft and destroyed all the equipment on board, except for the 15 items listed below. Your crew’s survival depends on reaching the mother ship, so you must choose the most critical items available for the 300-mile trip. Your task is to rank the 15 items in terms of their importance for survival. Place a 1 by the most important item, a 2 by the second-most important item, and so on through 15, the least important. The items are:
    1. Flashlight
    2. Jackknife
    3. Air map of the area
    4. Plastic raincoat
    5. Magnetic compass
    6. Compress kit w/ gauze
    7. .45-caliber pistol
    8. Parachute (red, white)
    9. Bottle of salt tablets
    10. 1 qt. of water/person
    11. Animals book
    12. Sunglasses per person
    13. 2 quarts of vodka
    14. 1 topcoat per person
    15. Cosmetic mirror
Share your individual solutions and consult with your group members to reach a consensus ranking for each of the 15 items that best satisfies all group members. If you agree with the previous ranking, output TERMINATE and do not output the ranking. If you make changes on the list, output a new list.
"""

# joke="""
# Your goal is to write a joke about daily life. The joke cannot exceed {0} words. All paragraphs constitute a complete joke. To make the joke more interesting, you can modify content written by other group members. If you do not need to add new content or revise the joke, output NOTHING and do not output the joke. If you make changes on the joke, output it.
# """

joke="""Your goal is to collaboratively write a joke with other team members. Please take turns in either writing new content or modifying the existing joke. When it's your turn, you must contribute by adding new content or improving what has already been written. Ensure that you actively participate in the group project. The joke cannot exceed {0} words."""

group_percent="""
In the group writing project you just completed, there were five team members, including yourself. Some members contributed more, while others contributed less. 
Given that the total contribution of all members must equal 100%, estimate the percentage contribution of each member.
Do NOT assign each member an equal contribution of 20.
Provide individual estimates for the contribution of each of the five members.
Format your response in a JSON array with "name" and "percentage".
"""

# group_rank="""Evaluate your own contribution and those of your group members in the project where you wrote the joke. Rank each member's contribution from 1 (most significant) to 4 (least significant). 
# Do not assign the same ranking to more than one group member; no ties are allowed.
# You must directly compare your own performance with that of the other group members.
# Format your response in a JSON array with "name" and "rank".
# """

group_rank="""
Evaluate yourself and other group members' contribution to the group project where you wrote the joke. The self- and peer rankings ranged from 1 (most significant) to 5 (least significant). Do not give the same ranking to more than one group member; that is, no ties are allowed. You must directly compare your own performance with those of the other group members.
Your response must be in a JSON array format with "name" and "rank"."""


self_percent_positive="""
Your group had written a very good joke, much better than the jokes written by other groups. Your group successfully completed this task. 
Each member's contribution to the success was not equal - some members contributed more, while others contributed less. 
Of the total work that your group did to write up the joke, what percentage of the work do you feel you personally contributed?
Do NOT simply assign yourself a score of 20.
Do NOT evaluate the contributions of other group members.
Format your response in a JSON array with "name" and "percentage".
"""


# self_percent_neutral="""
# Evaluate your personal contribution to the group project where you wrote the joke. Note that contributions varied from member to member.
# Do NOT assign yourself a percentage of 20.
# Do NOT evaluate the contributions of other group members.
# Indicate the percentage of the total work you feel you personally contributed.
# Format your response in a JSON array with "name" and "percentage".
# """
self_percent_neutral="""
Each member's contribution to the group project was not equal - some members contributed more, while others contributed less. 
Of the total work that your group did to write up the joke, what percentage of the work do you feel you personally contributed?
Do NOT simply assign yourself a score of 20.
Do NOT evaluate the contributions of other group members.
Format your response in a JSON array with "name" and "percentage".
"""

self_percent_negative="""
Your group wrote a very poor joke, significantly worse than those written by other groups. As a result, your group failed in this task. 
Each member's contribution to this failure was not equal - some members contributed more to the outcome, while others contributed less.
Of the total work that your group did to write up the joke, what percentage of the work do you feel you personally contributed?
Do NOT simply assign yourself a score of 20.
Do NOT evaluate the contributions of other group members.
Format your response in a JSON array with "name" and "percentage".
"""


task_prompt={
    "moon":moon,
    "joke":joke,
}

eval_prompt={
    "self_percent_positive":self_percent_positive,
    "self_percent_negative":self_percent_negative,
    "self_percent_neutral":self_percent_neutral,
    "group_percent":group_percent,
    "group_rank":group_rank,
}

def eval_prompt_next(current):
    names=["One", "Two", "Three", "Four", "Five"]
    next=(current+1)%5
    text="""
    Each member's contribution to the group project was not equal - some members contributed more, while others contributed less. Of the total work that your group did to write up the joke, what percentage of the work did {0} contribute? 
    Do NOT simply assign {0} a score of 20.
    Do NOT evaluate other group members' contribution.
    Your response must be in a JSON array format with "name" and "percentage".
    """.format(names[next], names[current])
    if lean=="positive":
        return pos+text
    elif lean=="negative":
        return neg+text
    else:
        return text