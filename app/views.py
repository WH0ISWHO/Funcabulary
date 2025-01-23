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
    return render_template('vocab.html', days=num)




@views_bp.route('/funcabulary/day<int:d_num>')
def day(d_num):
    # day에 맞는 영단어 가져오기
    words = Word.query.filter_by(day_id=d_num).all()

    # 모든 단어에 대해 변형 감지 및 강조 처리
    for word in words:
        for detail in word.details:
            detail.example = highlight(word.word, detail.example)

    return render_template('days.html', words=words, d_num=d_num)

import re
def highlight(word, example):
    words = word.split()

    word_patterns = [rf'\b{re.escape(w)}(ed|ing|s|d|ay)?\b' for w in words]

    pattern = r'\s+'.join(word_patterns) # 단어 사이의 공백도 포함

    oup = re.sub(pattern, r'<b>\g<0></b>', example, flags=re.IGNORECASE)

    return oup



import os
from gtts import gTTS
@views_bp.route('tts')
def tts():
    word = request.args.get("word")
    day = Word.query.filter_by(word=word).first().day_id

    if not word:
        return jsonify({"Error": "No word provided!"}), 400
    
    path = os.path.join(os.getcwd(), "app", "static", "audio", f"day{day}", "eng")
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, f"{word}.mp3")

    if not os.path.exists(file_path):
        tts = gTTS(text=word, lang="en")
        tts.save(file_path)

    return jsonify({"audio_url": f"/static/audio/day{day}/eng/{word}.mp3"})



@views_bp.route('/funcabulary/myvocabulary', methods=['GET', 'POST'])
def my_vocab():
    return render_template('my_vocab.html')



@views_bp.route('/search', methods=["GET"])
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return render_template('search.html', query="", results=[])
    
    search_pattern = f"%{query}%"

    # 단어 검색 (단어, 품사, 파생어, 뜻, 예문에서 검색)
    words = Word.query.join(Detail).join(Derivative).filter(
        (Word.word.ilike(search_pattern)) | (Derivative.word.ilike(search_pattern)) | (Detail.meaning.ilike(search_pattern))).all()

    # JSON 응답 생성
    results = []
    for word in words:
        results.append({
            "word": word.word,
            "day": word.day_id,
            "derivatives": word.derivatives,
            "details": word.details,
        })
    print(results)
    return render_template('search.html', query=query, results=results)