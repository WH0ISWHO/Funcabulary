from flask import Blueprint, render_template, redirect, request, url_for, jsonify

from .days import days
# from .models import Word

views_bp = Blueprint('views', __name__)


import random
@views_bp.route('/')
def home():
    today = []

    while len(today) < 3:
        num_4_day = random.randrange(1, len(days)) # idx of date(1 ~ 30)
        words = days[f'day{num_4_day}']

        num_4_word = random.randrange(1, len(words)) # idx of word (random word)
        today_word = words[num_4_word]

        if today_word not in today:
            today.append(today_word)

    return render_template('index.html', today=today)



@views_bp.route('/vocabulary')
def vocabulary():
    num = [x for x in range(30)]
    return render_template('vocab.html', days=num)



@views_bp.route('/addWord')
def add_word():
    return render_template('my_vocab.html')



@views_bp.route('/vocabulary/day<int:d_num>')
def day(d_num):
    # day에 맞는 영단어 가져오기
    words = days[f'day{d_num}']
    return render_template(f'days.html', words=words, d_num=d_num)



@views_bp.route('/vocabulary/myvocabulary', methods=['GET', 'POST'])
def my_vocab():
    return render_template('my_vocab.html')




# import requests
# @views_bp.route('/api/search', methods=['GET'])
# def search():
#     url = 'https://glosbe.com/gapi/translate?from=eng&dest=kor&format=json&pretty=true&phrase=text'
#     response = requests.get(url)

#     if response.status_code == 200:
#         data = response.json()
#         return jsonify(data)
#     else:
#         return jsonify({"error": "failed"})