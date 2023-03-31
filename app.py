from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_survey_page():
    """Displays Survey title and instructions, makes a POST request to "/star-survey" on form submission """
    return render_template("home_survey_page.html",
                           title=survey.title,
                           instructions=survey.instructions)


@app.route('/start-survey', methods=['POST'])
def set_session_data():
    """
        The start page form redirects to this POST route which sets a session key ("responses") equal to an empty list. This list will be used to store data and will be cleared every time the user retakes the survey from the start page. Finnally redirect to the first question. 
    """
    session["responses"] = []
    return redirect('/questions/0')


@app.route('/questions/<int:num>')
def questions(num):
    """Renders the form for the proper question in order, identifies the answer data from the session key, responses.
            Redirect user to thank you page IF all the questions have been answered and
            redirects user to the correct question if the user has not answered previous questions but attempts to skip
            to future questions.    
    """
    responses = session["responses"]

    if len(responses) == len(survey.questions):
        return redirect("/thank_you")

    if num != len(responses):
        flash("You haven't answered this questions yet!")
        return redirect(f'/questions/{len(responses)}')
    else:
        return render_template('questions.html',
                               question=survey.questions[num].question,
                               answers=survey.questions[num].choices)


@app.route('/answers', methods=["POST"])
def answers():
    """
    Handles post request from each question form and adds the question data to the session key value, responses. Then checks to see if there is 
    another question after the current one. If so redirect to that page. If not redirect to the thank you page.    

    """
    answer = request.form.get("choice")
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    if len(responses) != len(survey.questions):
        return redirect(f'/questions/{len(responses)}')

    else:
        return redirect("/thank_you")


@app.route('/thank_you')
def completed_survey():
    """Page shown once the user has answered all questions"""
    return render_template("completed.html")
