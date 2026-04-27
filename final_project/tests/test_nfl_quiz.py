# Scott Hershberger
# CS417
# Pytest tests for nfl_quiz.py
 
import pytest
from unittest.mock import patch, MagicMock
from queue import Queue
from nfl_quiz import questions, answer_check_grade, review_answers, get_team_data
 
 
# Fake team data used across all tests — no real API calls needed
@pytest.fixture
def fake_teams():
    return [
        {
            "name": "New England Patriots",
            "city": "Foxborough",
            "coach": "Bill Belichick",
            "owner": "Robert Kraft",
            "stadium": "Gillette Stadium",
            "established": "1960"
        }
    ]
 
# Mock the API response so get_team_data() never hits the real API
@pytest.fixture
def mock_api(fake_teams):
    mock_response = MagicMock()
    mock_response.json.return_value = {"response": fake_teams}
    with patch("requests.get", return_value=mock_response):
        yield
 
 
# Test 1: answer_check_grade correctly scores all correct answers
def test_all_correct_answers():
    answers_queue: Queue[tuple[str, str]] = Queue()
    answers_queue.put(("Foxborough", "Foxborough"))
    answers_queue.put(("Bill Belichick", "Bill Belichick"))
    answers_queue.put(("Robert Kraft", "Robert Kraft"))
    answers_queue.put(("Gillette Stadium", "Gillette Stadium"))
    answers_queue.put(("1960", "1960"))
 
    num_correct, grade_perc, _ = answer_check_grade(answers_queue)
 
    assert num_correct == 5
    assert grade_perc == 100.0
 
 
# Test 2: answer_check_grade correctly scores all wrong answers
def test_all_wrong_answers():
    answers_queue: Queue[tuple[str, str]] = Queue()
    answers_queue.put(("Foxborough", "Buffalo"))
    answers_queue.put(("Bill Belichick", "wrong coach"))
    answers_queue.put(("Robert Kraft", "wrong owner"))
    answers_queue.put(("Gillette Stadium", "wrong stadium"))
    answers_queue.put(("1960", "9999"))
 
    num_correct, grade_perc, _ = answer_check_grade(answers_queue)
 
    assert num_correct == 0
    assert grade_perc == 0.0
 
 
# Test 3: questions() returns an empty queue if the team name is not found
def test_team_not_found(fake_teams):
    with patch("builtins.input", side_effect=["Faketeam XYZ"]):
        result = questions(fake_teams)
 
    assert result.empty()
 
 
# Test 4: get_team_data() returns a list from the mocked API response
def test_get_team_data_returns_list(mock_api):
    result = get_team_data()
 
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "New England Patriots"
 
 
# Test 5: questions() matches different valid variations of a team name
@pytest.mark.parametrize("user_input", [
    "Patriots",
    "patriots",
    "PATRIOTS",
    "New England",
    "new england patriots",
])
def test_team_name_variations(user_input, fake_teams):
    with patch("builtins.input", side_effect=[user_input, "Foxborough", "Bill Belichick", "Robert Kraft", "Gillette Stadium", "1960"]):
        result = questions(fake_teams)
 
    assert not result.empty()