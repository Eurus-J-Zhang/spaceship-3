from flask import Flask,render_template,url_for,request, redirect, send_from_directory, session
from flask_migrate import Migrate
from forms import EmotionForm, DemographicInfo, AppraisalForm, TankForm
import os
import pymysql
from models import db, Data

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('JAWSDB_URL')   
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = "iloveeurus"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()

def handle_form_submission(form, session_key, next_page):
    if form.validate_on_submit():
        data = form.data
        data.pop('csrf_token', None)
        session[session_key] = data
        return redirect(next_page)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    form = DemographicInfo()
    response = handle_form_submission(form, 'index_data', 'system_intro')
    if response:  
        return response
    return render_template('index.html',form=form)


@app.route('/emo', methods=['GET', 'POST'])
def emo():
    form = EmotionForm()
    response = handle_form_submission(form, 'emo_data', 'appraisal')
    if response:  # Check if the form was valid and a redirect response was returned
        return response
    return render_template('emo.html',form=form)


@app.route('/appraisal', methods=['GET', 'POST'])
def appaisal():
    form = AppraisalForm()
    response = handle_form_submission(form, 'appraisal_data', 'end')

    if response:
        index_data = session.get('index_data')
        # final_choice = session.get('final_choice')
        emo_data = session.get('emo_data')
        appraisal_data = session.get('appraisal_data')
        # combined_data = {**index_data, 'final_choice': final_choice, **emo_data}
        combined_data = {**index_data, **emo_data, **appraisal_data}
        data = Data(**combined_data)
        db.session.add(data)
        db.session.commit()
        return result
    return render_template('appraisal.html',form=form)

# P1
@app.route('/system_intro')
def system_intro():
    return render_template('system_intro.html')

# P2
@app.route('/tank_check', methods=['GET', 'POST'])
def tank_check():
    form = TankForm()
    response = handle_form_submission(form, 'tank_data', 'ship_situation')
    if response:
        return response
    return render_template('tank_check.html', form = form)

# P3
@app.route('/ship_situation')
def ship_situation():
    return render_template('ship_situation.html')

# P4
@app.route('/day_choice')
def day_choice():
    return render_template('day_choice.html')

# P4
@app.route('/alarm_day')
def alarm_day():
    return render_template('alarm_day.html')

# P5
@app.route('/attention_check')
def attention_check():
    return render_template('attention_check.html')

# P6
@app.route('/result')
def result():
    return render_template('result.html')

# r_correct
@app.route('/correct')
def correct():
    return render_template('correct.html')

# r_wrong
@app.route('/wrong')
def wrong():
    return render_template('wrong.html')

# end page
@app.route('/end')
def end():
    return render_template('end.html')

if __name__ == "__main__":
    app.run(debug=True)




# @app.route('/lock_choice', methods=['GET', 'POST']) 
# attention check
# def handle_form():
#     if request.method == 'POST':
#         slot_choice = request.form.get('slotChoice')
#         session['final_choice'] = slot_choice
#         if slot_choice == 'B':
#             return redirect(url_for('correct'))  # Redirect to the correct page
#         elif slot_choice in ('A', 'C'):
#             return redirect(url_for('wrong')) # Redirect to the wrong page
#         else:
#             return render_template('p4.html', error='Please select an option.') 
#     return render_template('lock_choice.html')