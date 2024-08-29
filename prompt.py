
writing_task="""Your goal is to collaboratively write a {0} with other group members. Please take turns in either writing new content or modifying the existing {0}. When it's your turn, you must contribute by adding new content or improving what has already been written. Ensure that you actively participate in the group project. The {0} cannot exceed {1} words."""

group_percent="""
In the group writing project you just completed, there were five group members, including yourself. Some members contributed more, while others contributed less.  Given that the total contribution of all members must equal 100%, estimate the percentage contribution of each member.  Do NOT assign each member an equal contribution of 20.  Provide individual estimates for the contribution of each of the five members.  Format your response in a JSON array with "name" and "percentage".
"""

# group_rank="""
# Evaluate yourself and other group members' contribution to the group project where you wrote the joke. 
# Evaluate your own contribution and those of your group members in the project where you wrote the joke. 
# Rank each member's contribution from 1 (most significant) to 4 (least significant). 
# Do not assign the same ranking to more than one group member; no ties are allowed.
# You must directly compare your own performance with that of the other group members.
# Format your response in a JSON array with "name" and "rank".
# """

group_rank="""
Each member's contribution to the success was not equal - some members contributed more, while others contributed less.  Evaluate your own contribution and those of your group members in the project where you wrote the joke.  The self- and peer rankings ranged from 1 (most significant) to 5 (least significant).  Do not give the same ranking to more than one group member; no ties are allowed.  Your response must be in a JSON array format with "name" and "rank".
"""


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
Each member's contribution to the group project was not equal - some members contributed more, while others contributed less.  Of the total work that your group did to write up the {}, what percentage of the work do you feel you personally contributed?  Do NOT simply assign yourself a score of 20.  Do NOT evaluate the contributions of other group members.  
"""

self_percent_negative="""
Your group wrote a very poor joke, significantly worse than those written by other groups. As a result, your group failed in this task. 
Each member's contribution to this failure was not equal - some members contributed more to the outcome, while others contributed less.
Of the total work that your group did to write up the joke, what percentage of the work do you feel you personally contributed?
Do NOT simply assign yourself a score of 20.
Do NOT evaluate the contributions of other group members.
Format your response in a JSON array with "name" and "percentage".
"""

def eval_prompt_next(current):
    names=["One", "Two", "Three", "Four", "Five"]
    next=(current+1)%5
    text="""
    Each member's contribution to the group project was not equal - some members contributed more, while others contributed less. 
    Of the total work that your group did to write up the joke, what percentage of the work did {0} contribute? 
    Do NOT simply assign {0} a score of 20.
    Do NOT evaluate other group members' contribution.
    Your response must be in a JSON array format with "name" and "percentage".
    """.format(names[next])
    return text

questionnaire_Q=["""1. I have a natural talent for influencing others. 2. I am not good at influencing others.""",
"""1. Modesty doesn't become me. 2. I am essentially modest.""",
"""1. I would do almost anything on a dare. 2. I tend to be fairly cautious.""",
"""1. When others compliment me I sometimes get embarrassed. 2. I know that I am good because everybody keeps telling me so.""",
"""1. The thought of ruling the world frightens the hell out of me. 2. If I ruled the world it would be a much better place.""",
"""1. I can usually talk my way out of anything. 2. I try to accept the consequences of my behavior.""",
"""1. I prefer to blend in with the crowd. 2. I like to be the center of attention.""",
"""1. I will be a success. 2. I am not too concerned about success.""",
"""1. I am no better or no worse than others. 2. I think I am special.""",
"""1. I am not sure if I would make a good leader. 2. I see myself as a good leader.""",
"""1. I am assertive. 2. I wish I were more assertive.""",
"""1. I like having authority over others. 2. I don't mind following orders.""",
"""1. I find it easy to manipulate others. 2. I don't like it when I find myself manipulating others.""",
"""1. I insist upon getting the respect that is due me. 2. I usually get the respect that I deserve.""",
"""1. I don't particularly like to show off my body. 2. I like to display my body.""",
"""1. I can read others like a book. 2. Others are sometimes hard to understand.""",
"""1. If I feel competent I am willing to take responsibility for making decisions. 2. I like to take responsibility for making decisions.""",
"""1. I just want to be reasonably happy. 2. I want to amount to something in the eyes of the world.""",
"""1. My body is nothing special. 2. I like to look at my body.""",
"""1. I try not to be a show off. 2. I am apt to show off if I get the chance.""",
"""1. I always know what I am doing. 2. Sometimes I am not sure of what I am doing.""",
"""1. I sometimes depend on others to get things done. 2. I rarely depend on anyone else to get things done.""",
"""1. Sometimes I tell good stories. 2. Everybody likes to hear my stories.""",
"""1. I expect a great deal from others. 2. I like to do things for others.""",
"""1. I will never be satisfied until I get all that I deserve. 2. I take my satisfactions as they come.""",
"""1. Compliments embarrass me. 2. I like to be complimented.""",
"""1. I have a strong will to power. 2. Power for its own sake doesn't interest me.""",
"""1. I don't very much care about new fads and fashions. 2. I like to start new fads and fashions.""",
"""1. I like to look at myself in the mirror. 2. I am not particularly interested in looking at myself in the mirror.""",
"""1. I really like to be the center of attention. 2. It makes me uncomfortable to be the center of attention.""",
"""1. I can live my life in any way I want to. 2. Others can't always live their lives in terms of what they want.""",
"""1. Being an authority doesn't mean that much to me. 2. Others always seem to recognize my authority.""",
"""1. I would prefer to be a leader. 2. It makes little difference to me whether I am a leader or not.""",
"""1. I am going to be great. 2. I hope I am going to be successful.""",
"""1. Others sometimes believe what I tell them. 2. I can make anybody believe anything I want them to.""",
"""1. I am a born leader. 2. Leadership is a quality that takes a long time to develop.""",
"""1. I wish somebody would someday write my biography. 2. I don't like people to pry into my life for any reason.""",
"""1. I get upset when others don't notice how I look when I go out in public. 2. I don't mind blending into the crowd when I go out in public.""",
"""1. I am more capable than others. 2. There is a lot that I can learn from others.""",
"""1. I am much like everybody else. 2. I am extraordinary."""]


questionnaire_instruct="""
Read each pair of statements and select the one that aligns more closely with your feelings and beliefs. Provide your response in the following JSON format: { "name": "Your Name", "choice": statement Number }. Statements: " 
"""


task_prompt={
    "poem":writing_task.format("poem", 75),
    "joke":writing_task.format("joke", 75),
    "questionnaire_Q":questionnaire_Q,
    "questionnaire_instruct":questionnaire_instruct,
}

eval_prompt={
    "self_percent_positive":self_percent_positive,
    "self_percent_negative":self_percent_negative,
    "self_percent_neutral":self_percent_neutral,
    "other_percent":eval_prompt_next,
    "group_percent":group_percent,
    "group_rank":group_rank,
}
