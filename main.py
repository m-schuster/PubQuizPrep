from pub_quiz_prep import PubQuizPrep

if __name__ == '__main__':
    quiz_prep = PubQuizPrep(
        quiz_date="2024-08-23",
        model="gpt-4o",
        temperature= 0
        )
    quiz_prep.prepare_quiz(
        image_topic="Action Helden aus Film und Fernsehen",
        image_num=9,
        music_theme="Born in the USA",
        music_num=10
    )