from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from .models import *

views_bp = Blueprint('views', __name__)


import random
@views_bp.route('/')
def home():
    today = []

    num_days = db.session.query(Day).count()

    while len(today) < 3:
        num_4_day = random.randrange(1, num_days) # idx of date(1 ~ 30)
        words = Word.query.filter_by(day_id = num_4_day).all()

        if not words:
            continue

        random_word = random.choice(words)

        # prevent duplication
        if random_word not in today:
            today.append(random_word)

    return render_template('index.html', today=today)



@views_bp.route('/funcabulary')
def vocabulary():
    days = db.session.query(Day).count()
    num = [x for x in range(days)]
    print(num)
    return render_template('vocab.html', days=num)



@views_bp.route('/funcabulary/day<int:d_num>')
def day(d_num):
    day = Day.query.filter_by(id=d_num).first()

    if not day:
        return "<h1>Day not found!</h1>", 404
    
    print(d_num)

    # day에 맞는 영단어 가져오기
    words = Word.query.filter_by(day_id = d_num).all()
    return render_template(f'days.html', words=words, d_num=d_num)



@views_bp.route('/funcabulary/myvocabulary', methods=['GET', 'POST'])
def my_vocab():
    return render_template('my_vocab.html')