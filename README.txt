Simple REST - API to create, modify and grade quizzes of 20 questions
    (there's a parameter to switch it to any size inside the app.py file, the request type must turn into post)

Each question has 2 - 4 possible options (this size is randomly choose), only one is correct!

ENDPOINTS ( SERVER:PORT ):

    [GET] /quiz                     Create a new Quiz instance with a unique code

    [GET] /quiz/<quiz_code>         Return the instance of a Quiz with the selected code

    [PUT] /quiz/<quiz_code>/update  Update the <quiz_code> instance with the data passed as json and returns the updated instance,
                                    MODIFIES:
                                        QUIZ: name, description, max_score
                                        QUESTION: text, updates max_score per question according to the new quiz max_score
                                        OPTIONS:text, and set the correct one

    [PUT] /quiz/<quiz_code>/answer  Update the <quiz_code> instance with the data passed as json and returns the updated instance,
                                    MODIFIES:
                                        OPTIONS: Set if an option was selected by the user

    [GET] /quiz/<quiz_code>/grade   Grade the <quiz_code> instance according to the options selected,if no option was selected it sets the score to 0.0


Best Practices:
    - Files respect PEP 8
    - No method is longer than 35 lines
    - Respect naming conventions
    - Lines aren't longer than 100 chars

Patterns:
    - Singleton using meta-classes in db_controller, consult, update, insert, delete files
    - db_controller acts as a DAO to access Quiz operations

Improvements:
    - Generate random text instead of C-"id"
    - Fill the requirements.txt file
    - Use virtualenv for the app
    - Integrate to docker
    - Add security by username and password.

Software:
    - Python 2.7.9
    - Flask 0.11.1
    - SqlAlchemy 1.0.14
    - Persistence: sql_lite just for simplicity of deployment


Coded using Pycharm 2017.2.2

RUN: python run.py
