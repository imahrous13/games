# quiz_brain.py
class QuizBrain:
    def __init__(self, q_list):
        self.question_number = 0
        self.score = 0
        self.question_list = q_list

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        current_question = self.question_list[self.question_number]  # <-- no -1
        self.question_number += 1
        user_answer = input(
            f"Q.{self.question_number}: {current_question.text} (True/False): "
        ).strip()

        self.check_answer(user_answer, current_question.answer)

    def check_answer(self, user_answer, correct_answer):
        # normalize a few common inputs
        norm = {
            "t": "true",
            "true": "true",
            "y": "true",
            "f": "false",
            "false": "false",
            "n": "false",
        }
        ua = norm.get(user_answer.lower(), user_answer.lower())
        ca = correct_answer.lower()

        if ua == ca:
            print("You got it right!")
            self.score += 1
        else:
            print("That's wrong.")
        print(f"The correct answer was: {correct_answer}")
        print(f"Your current score is {self.score}/{self.question_number}\n")
