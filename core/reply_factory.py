from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
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
        return PYTHON_QUESTION_LIST[next_index], next_index
    else:
        return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    # Dummy implementation; in real case, you would calculate based on session['answers']
    return "Thank you for completing the questionnaire! Your responses have been recorded."

