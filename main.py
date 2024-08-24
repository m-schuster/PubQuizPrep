from pub_quiz_prep import PubQuizPrep

if __name__ == '__main__':
    quiz_prep = PubQuizPrep(
        quiz_date="2024-08-26",
        model="gpt-4o",
        temperature= 0
        )
    quiz_prep.prepare_quiz(
        image_topic="Olympiastadien von oben",
        image_num=27,
        music_theme="Sport und Sportler",
        music_num=40
    )