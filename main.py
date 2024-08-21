from pub_quiz_prep import PubQuizPrep

if __name__ == '__main__':
    quiz_prep = PubQuizPrep("gpt-4o", 0)
    quiz_prep.prepare_quiz(
        day="19",
        month="August",
        image_topic="Hollywood Schauspieler mit den meisten Oscars",
        image_num=9,
        music_theme="New York",
        music_num=30
    )