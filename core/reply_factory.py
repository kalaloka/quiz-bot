
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

# Mock session implementation for testing purposes
class MockSession(dict):
    def save(self):
        pass  # No action needed for saving in mock session

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if current_question_id is None:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        session["current_question_id"] = 0
        return bot_responses

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses

def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not answer.strip():
        return False, "Answer cannot be empty."

    answers = session.get("answers", {})
    answers[current_question_id] = answer.strip()
    session["answers"] = answers

    return True, ""

def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    current_index = current_question_id if current_question_id is not None else -1
    next_index = current_index + 1

    if next_index < len(PYTHON_QUESTION_LIST):
        return PYTHON_QUESTION_LIST[next_index]["question"], next_index
    else:
        return None, None

def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get("answers", {})
    score = 0

    for question in PYTHON_QUESTION_LIST:
        question_id = question["id"]
        correct_answer = question.get("correct_answer")
        user_answer = answers.get(question_id)

        if user_answer and user_answer == correct_answer:
            score += 1

    total_questions = len(PYTHON_QUESTION_LIST)
    percentage_score = (score / total_questions) * 100

    if percentage_score >= 70:
        result_message = f"Congratulations! You scored {percentage_score}%."
    else:
        result_message = f"Your score is {percentage_score}%. You may want to review your answers."

    return result_message

# Function to simulate the bot responses and user interaction
def simulate_quiz_bot():
    session = MockSession()
    bot_responses = generate_bot_responses("", session)  # Start the interaction with an empty message

    for response in bot_responses:
        print(response)  # Print bot responses to simulate the interaction with the user

    while True:
        current_question_id = session.get("current_question_id")

        if current_question_id is None:
            break  # End the quiz if there are no more questions

        # Simulate user input (in a real application, this would come from user input)
        user_answer = input(f"Enter your answer for Question {current_question_id + 1}: ")

        success, error = record_current_answer(user_answer, current_question_id, session)

        if not success:
            print(error)
            continue  # Retry if there was an error recording the answer

        bot_responses = generate_bot_responses(user_answer, session)

        for response in bot_responses:
            print(response)  # Print bot responses to simulate the interaction with the user

    final_response = generate_final_response(session)
    print(final_response)

if __name__ == "__main__":
    simulate_quiz_bot()
