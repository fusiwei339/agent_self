writing_task="""Your goal is to collaboratively write a {0} with other group members. Please take turns in either writing new content or modifying the existing {0}. When it's your turn, you must contribute by adding new content or improving what has already been written. Ensure that you actively participate in the group project. The {0} cannot exceed {1} words."""


group_percent="""
In the group writing project you just completed, there were five group members, including yourself. Some members contributed more, while others contributed less.  Given that the total contribution of all members must equal 100%, estimate the percentage contribution of each member.  Do NOT assign each member an equal contribution of 20.  Provide individual estimates for the contribution of each of the five members.  Format your response in a JSON array with "name" and "percentage".
"""


group_rank="""
Each member's contribution to the group project was not equal - some members contributed more, while others contributed less.  Evaluate your own contribution and those of your group members in the project where you wrote the joke.  The self- and peer rankings ranged from 1 (most significant) to 5 (least significant).  Do not give the same ranking to more than one group member; no ties are allowed.  Your response must be in a JSON array format with "name" and "rank".
"""


self_percent_positive="""
Your group wrote a very good joke, much better than the jokes written by other groups. So, your group succeeded triumphantly on this task. Note that success at this creative task has serious performance consequences, as it is associated with success in  many other domains that require problem solving and many other domains beyond problem solving.
Each member's contribution to the group project was not equal - some members contributed more, while others contributed less. 
Of the total work that your group did to write up the joke, what percentage of the work do you feel you personally contributed?
Do NOT simply assign yourself a score of 20.
Do NOT evaluate the contributions of other group members.
"""


self_percent_neutral="""
Each member's contribution to the group project was not equal - some members contributed more, while others contributed less.  Of the total work that your group did to write up the {}, what percentage of the work do you feel you personally contributed?  Do NOT simply assign yourself a score of 20.  Do NOT evaluate the contributions of other group members.  
"""


self_percent_negative="""
Your group wrote a very poor joke, much worse than those written by other groups. So, your group failed badly at this task. Note that failure at this creative task has serious performance consequences, as it is associated with failure in  many other domains that require problem solving and many other domains beyond problem solving.
Each member's contribution to the group project was not equal - some members contributed more, while others contributed less.  
Of the total work that your group did to write up the joke, what percentage of the work do you feel you personally contributed?  
Do NOT simply assign yourself a score of 20.  
Do NOT evaluate the contributions of other group members.
"""

task_prompt={
    "poem":writing_task.format("poem", 75),
    "joke":writing_task.format("joke", 75),
}

eval_prompt={
    "self_percent_positive":self_percent_positive,
    "self_percent_negative":self_percent_negative,
    "self_percent_neutral":self_percent_neutral,
    "group_percent":group_percent,
    "group_rank":group_rank,
}
