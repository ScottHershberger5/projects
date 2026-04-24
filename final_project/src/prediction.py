# Scott Hershberger
# CS417
# API football quiz w/ a queue


import requests
from queue import Queue

### notes ###
# 1. need to ask the user if they even want to check their answers
# 2. need to actually give the user a grade/score
# 3. check type hints for correctness / MYPY!!
# 4. 


def get_team_data():
    headers = {'x-apisports-key': 'fd6fbe35c28ce3526d4bb21d4d5246ba'}
    # Fetch all teams in a single request
    url = "https://v1.american-football.api-sports.io/teams?league=1&season=2024"
    response = requests.get(url, headers=headers).json()
    return response.get('response', []) #a list of all the teams and their data
    

#TYPE HINTS / ARGUMENTS
def questions(teams) -> Queue: #need to put arguments for the function , the queue, and the list of teams with data
    favorite_team = input("What is your favorite NFL team? ")
    answers_queue = Queue() # makes a queue where were gonna store the correct answer and the users answer
    for team in teams:
        if team['name'].lower() == favorite_team.lower():
            # print(f"\nTeam Data for {team['name']}:")
            # puts a tuple (correct answer, users answer) into a queue (answers_queue)
            answers_queue.put((team['city'], input(f"What city are the {team['name']} located in? : ")))
            answers_queue.put((team['coach'],input(f"Who is the coach of the {team['name']}? : ")))
            answers_queue.put((team['owner'],input(f"Who is the owner of the {team['name']}? : ")))
            answers_queue.put((team['stadium'],input(f"What stadium do the {team['name']} play in? : ")))
            answers_queue.put((team['established'],input(f"What year was the {team['name']} football team established? : ")))
            break
    else:
        print(f"Team '{favorite_team}' not found. Or you mispelled the team name")
    return answers_queue


# NOT FINISHED, NEED TO COMPARE ANSWERS
def answer_check(answers_queue: list[tuple[str,str]]) -> None: #TYPE HINTS
    for _ in range(answers_queue.qsize()):
        correct_a, user_a = answers_queue.get()
        print(f"This was your answer : {user_a}")
        print(f"This was the correct answer : {correct_a}")
    
if __name__ == "__main__":
    team_data = get_team_data()
    answers_queue = questions(team_data)
    #maybe ask the user here if they even want to check their answers
    answers = answer_check(answers_queue)
    