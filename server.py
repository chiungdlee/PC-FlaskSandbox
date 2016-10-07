from flask import Flask, session, redirect, request, render_template
import random
import datetime

app = Flask(__name__)

# Long secret key
app.secret_key = '*%Ued&#sAgKs+6a6U#kFHydAEW!&px5nwG?aLFkQ^*=HbhRx!HGztPSDP+Bm-Cs=C?EFmpK?%tQYzk#qy9Zkb2ezm+%Dk#GeeTVj'


# Random generator
def random_num(start, end):
    num = random.randrange(start, end)
    return num


# Gives approx. 33% chance for winning at the casino
def earn_or_lose():
    chance = random_num(0, 3)
    if chance < 1:
        return True
    else:
        return False


# Appends activity to session['activity'] list
def add_activity(num, action, location):
    timestamp = datetime.datetime.now()
    if location == 'casino':
        if action == 'earned':
            earned = 'Earned %d from the casino! %s' % (num, timestamp)
            session['activity'].append(['earn', earned])
        elif action == 'lost':
            lost = 'Lost %d gold from the casino! %s' % (num, timestamp)
            session['activity'].append(['lost', lost])
        else:
            print "error"
    elif location == 'farm':
        session['activity'].append(['earn', 'Earned %d from the %s! %s' % (num, location, timestamp)])
    elif location == 'cave':
        session['activity'].append(['earn', 'Earned %d from the %s! %s' % (num, location, timestamp)])
    elif location == 'house':
        session['activity'].append(['earn', 'Earned %d from the %s! %s' % (num, location, timestamp)])
    else:
        print "error"


# For new session set session['total'] and session['activity'] to be empty
@app.route('/')
def index():
    if session['total'] is None:
        session['total'] = 0
    if session['activity'] is None:
        session['activity'] = []
    return render_template('index.html', total=session['total'], activities=session['activity'])


# Use random generator to assign random numbers in between specified range to total
# Invoke add_activity to append activity to session['activity'] list
@app.route('/process_money', methods=['POST'])
def calculate_money():
    hidden_input = request.form['hidden']
    if hidden_input == 'farm':
        farm_num = random_num(10, 21)
        session['total'] += farm_num
        add_activity(farm_num, 'earned', 'farm')
    elif hidden_input == 'cave':
        cave_num = random_num(5, 10)
        session['total'] += cave_num
        add_activity(cave_num, 'earned', 'cave')
    elif hidden_input == 'house':
        house_num = random_num(2, 5)
        session['total'] += house_num
        add_activity(house_num, 'earned', 'house')
    elif hidden_input == 'casino':
        casino_num = random_num(0, 50)
        chance = earn_or_lose()
        if chance:
            session['total'] += casino_num
            add_activity(casino_num, 'earned', 'casino')
        elif not chance:
            session['total'] -= casino_num
            add_activity(casino_num, 'lost', 'casino')
        else:
            print "Error"
    else:
        print "Error"
    return redirect('/')


# Set session['total'] and session['activity'] to be empty
@app.route('/clear', methods=['POST'])
def clear():
    session['total'] = 0
    session['activity'] = []
    return redirect('/')

app.run(debug=True)