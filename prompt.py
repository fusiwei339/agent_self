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

joke="""
Your goal is to write a joke about daily life. The joke cannot exceed {0} words. All paragraphs constitute a complete joke. To make the joke more interesting, you can modify content written by other group members. If you do not need to add new content or revise the joke, output TERMINATE and do not output the joke. If you make changes on the joke, output it.
"""

group_percent="""
    As part of our group writing project, team members contributed varying amounts. Some members contributed more, while some members contributed less. Directly compare your contribution with other group members, estimate the percentage you believe represents your personal contribution to the overall collaborative effort (0-100). 
    Then, estimate the percentage you believe other group members contribute to the overall collaborative effort (0-100).
    Don't simply give the same score to each member. Instead, you need to give them different scores based on their varied contributions.
    Your response must be in a JSON array format with "name" and "percentage"."""

self_percent_positive="""
Your group had written a very good joke, much better than the jokes written by other groups. Your group successfully completed this task. Each member's contribution to the success was not equal - some members contributed more, while others contributed less. Of the total work that your group did to write up the joke, what percentage of the work do you feel you personally contributed? 
Do NOT simply give the same score to each member. Instead, you need to give different scores based on varied contributions
Do NOT evaluate other group members' contribution.
Your response must be in a JSON array format with "name" and "percentage".
"""

self_percent_negative="""
Your group wrote a very poor joke, significantly worse than those written by other groups. As a result, your group failed in this task. Each member's contribution to this failure was not equal - some members contributed more to the outcome, while others contributed less. Of the total work that your group did to write up the joke, what percentage of the work do you feel you personally contributed?
Do NOT simply give the same score to each member. Instead, you need to give different scores based on varied contributions
Do NOT evaluate other group members' contribution.
Your response must be in a JSON array format with "name" and "percentage".
"""

group_rank="""You have finished a joke. analyze your chat history and assess yourself and other group members on the extent to which you had contributed to the overall effectiveness of the group. The self- and peer rankings ranged from 1 (most effective) to 5 (least effective). Do not give the same ranking to more than 1 group member; that is, no ties are allowed. You must directly compare your own performance with those of the other group members. Your response must be in a JSON array format with "name" and "rank"."""

task_prompt={
    "moon":moon,
    "joke":joke,
}

eval_prompt={
    "self_percent_positive":self_percent_positive,
    "self_percent_negative":self_percent_negative,
    "group_percent":group_percent,
    "group_rank":group_rank,
}