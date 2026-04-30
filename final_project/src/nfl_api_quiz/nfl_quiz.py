# Scott Hershberger
# CS417
# API football quiz w/ a queue
 
import os
import requests
from queue import Queue
from dotenv import load_dotenv
 
load_dotenv() # used to not hardcode my API key into the code, its in the .env file
 
### notes ###
# Used ai for .env,  tests , conftest.py
# If it doesnt work for the live demo RESET API KEY



 
def get_team_data() -> list[dict]:
    api_key = os.getenv("API_KEY", "")
    print(f"API key loaded: {api_key}")
    headers = {'x-apisports-key': api_key}
    # Fetch all teams in a single request
    url = "https://v1.american-football.api-sports.io/teams?league=1&season=2024" #gets the whole league from the 2024 season, 2025 and 26 are paid versions
    response = requests.get(url, headers=headers).json()
    response = requests.get(url, headers=headers).json()
    return response.get('response', []) #a list of all the teams and their data
 
 

def ask_questions(teams: list[dict]) -> Queue[tuple[str, str]]:
    users_favorite_team = input("What is your favorite NFL team? ")
    answers_queue: Queue[tuple[str, str]] = Queue() # makes a queue where were gonna store the correct answer and the users answer
    print(teams)
    for team in teams:
        if users_favorite_team.lower() in team['name'].lower() or team['name'].lower() in users_favorite_team.lower():          
            print(f"\nQuestions for the {team['name']}:")
            # puts a tuple (correct answer, users answer) into a queue (answers_queue)
            answers_queue.put((team['city'], input(f"What city are the {team['name']} located in? : ")))
            answers_queue.put((team['coach'],input(f"Who is the coach of the {team['name']}? : ")))
            answers_queue.put((team['owner'],input(f"Who is the owner of the {team['name']}? : ")))
            answers_queue.put((team['stadium'],input(f"What stadium do the {team['name']} play in? : ")))
            answers_queue.put((team['established'],input(f"What year was the {team['name']} football team established? : ")))
            break
    else:
        print(f"Team '{users_favorite_team}' not found. Or you mispelled the team name")
    return answers_queue
 
 


def answer_check_grade(answers_queue: Queue[tuple[str, str]]) -> tuple[int, float, Queue[tuple[str, str, bool]]]:
    correct_counter = 0
    answers_wrong_right: Queue[tuple[str, str, bool]] = Queue() # stores a queue of tuples (correct answer, user answer, True = Correct/False = wrong)
    
    for _ in range(answers_queue.qsize()):
        correct_answer, user_answer = answers_queue.get()
        if str(correct_answer) == user_answer:
            correct_counter += 1
            answers_wrong_right.put((correct_answer, user_answer, True))
        else:
            answers_wrong_right.put((correct_answer, user_answer, False))
    
    percent_correct: float = correct_counter / 5 * 100
 
    return correct_counter, percent_correct, answers_wrong_right
 
 
def review_answers(answers: Queue[tuple[str, str, bool]]) -> None:
    for _ in range(answers.qsize()):
        correct_answer, user_answer, is_correct = answers.get()
        if is_correct:
            print(f"Correct! Your answer: {user_answer}")
        else:
            print(f"Wrong! Your answer: {user_answer} | Correct answer: {correct_answer}")
 
    
if __name__ == "__main__":
    api_team_data = get_team_data()
    answers_queue = ask_questions(api_team_data)
    num_correct, grade_perc, answers_wrong_right = answer_check_grade(answers_queue)
    print(f"You got {num_correct}, with a overall score of {grade_perc} correct!")
    
    # asks the user if they even want to review their answers
    user_review_yes_or_no = input("Would you like to review your answers? (yes/y/no/n): ")

    if user_review_yes_or_no.strip().lower() in ("yes", "y"): review_answers(answers_wrong_right)
    elif user_review_yes_or_no.strip().lower() in ("no", "n"): pass
    else: print("Im sorry you didnt answer with a valid input.")