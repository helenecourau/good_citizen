from .models import QuestionsAnswers


def answer_right_or_wrong(answer_user_id):
    '''For each question, looks if the user answer is right and
    calculate the number of good answer'''
    total_result = 0
    for answer in answer_user_id:
        result = None
        question_answer = QuestionsAnswers.objects.filter(question__id=answer["key"])
        right_answer = list(
            question_answer.filter(right_answer=True).values_list(
                "answer__pk", flat=True
            )
        )
        right_answer.sort()
        answer["value"].sort()
        if answer["value"] == right_answer:
            result = True
            total_result += 1
        else:
            result = False

    return total_result

def calulate_final_result(total_result, questions):
    '''Calculate if the user succeed or not'''
    if len(questions) > 0:
        if total_result >= len(questions) / 2:
            final_result = True
        else:
            final_result = False

        return final_result

def calulate_final_right_answer(right_answers):
    
    '''Dictionary of good answers with this format:
    {pk_question:[pk_good_anwser1, pk_good_anwser2]}
    used by front to append the green checkmarks before the good answers'''
    
    final_right_answer = {}
    for answer in right_answers:
        if answer.question.pk not in final_right_answer.keys():
            final_right_answer[answer.question.pk] = [answer.answer.pk]
        else:
            final_right_answer[answer.question.pk].append(answer.answer.pk)

    return final_right_answer