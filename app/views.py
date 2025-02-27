from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from .models import *
from .utils import ask

views_bp = Blueprint('views', __name__)



import random
@views_bp.route('/')
def home():
    # 봇 차단
    user_agent = request.headers.get("User-Agent", "").lower()
    if "python" in user_agent or "pandas" in user_agent or "requests" in user_agent:
        return jsonify({"error": "Bots are not allowed!"}), 403

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

    for word in today:
        for detail in word.details:
            detail.example = highlight(word.word, detail.example)

    return render_template('index.html', today=today)



@views_bp.route('/funcabulary')
def vocabulary():
    days = db.session.query(Day).count()
    num = [x for x in range(days)]
    return render_template('vocab.html', days=num)



@views_bp.route('/funcabulary/day<int:d_num>')
def day(d_num):
    # 봇 차단
    user_agent = request.headers.get("User-Agent", "").lower()
    if "python" in user_agent or "pandas" in user_agent or "requests" in user_agent:
        return jsonify({"error": "Bots are not allowed!"}), 403
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
from urllib.parse import unquote
@views_bp.route('tts_eng')
def tts_eng():
    word = request.args.get("word", "eng")
    day = Word.query.filter_by(word=word).first().day_id

    if not word:
        return jsonify({"Error": "No word provided!"}), 400

    path = os.path.join(os.getcwd(), "app", "static", "audio", f"day{day}", "eng")
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, f"{word}.mp3")

    if not os.path.exists(file_path):
        tts = gTTS(text=word, lang="en")
        tts.save(file_path)

    return jsonify({"eng_audio_url": f"/static/audio/day{day}/eng/{word}.mp3"})


@views_bp.route('tts_kor')
def tts_kor():
    meaning = request.args.get("meaning")
    if not meaning:
        return jsonify({"Error": "No meaning provided!"}), 400

    id = Detail.query.filter_by(meaning=meaning).first().word_id
    day = Word.query.filter_by(id=id).first().day_id

    meaning = unquote(meaning)  # 의미 디코딩

    # 의미에 해당하는 음성 파일을 생성
    path = os.path.join(os.getcwd(), "app", "static", "audio", f"day{day}", "kor")
    os.makedirs(path, exist_ok=True)

    file_paths = []
    file_path = os.path.join(path, f"{meaning}.mp3")

    # 파일이 존재하지 않으면 새로 생성
    if not os.path.exists(file_path):
        tts = gTTS(text=meaning, lang="ko")
        tts.save(file_path)

    file_paths.append(f"/static/audio/day{day}/kor/{meaning}.mp3")

    return jsonify({
        "kor_audio_urls": file_paths
    })




@views_bp.route('/funcabulary/myvocabulary', methods=['GET', 'POST'])
def my_vocab():
    # 봇 차단
    user_agent = request.headers.get("User-Agent", "").lower()
    if "python" in user_agent or "pandas" in user_agent or "requests" in user_agent:
        return jsonify({"error": "Bots are not allowed!"}), 403
    return render_template('my_vocab.html')



from collections import defaultdict
@views_bp.route('/search', methods=["GET"])
def search():
    # 봇 차단
    user_agent = request.headers.get("User-Agent", "").lower()
    if "python" in user_agent or "pandas" in user_agent or "requests" in user_agent:
        return jsonify({"error": "Bots are not allowed!"}), 403

    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search.html', query="", results=[])

    search_pattern = f"%{query}%"
    # search the word from 'words' table
    words_by_word = Word.query.filter(Word.word.ilike(search_pattern)).all()
    word_ids_by_word = {word.id for word in words_by_word}

    # search the meaning from 'details' table and bring its word_id
    details_by_meaning = Detail.query.filter(Detail.meaning.ilike(search_pattern)).all()
    word_ids_by_meaning = {detail.word_id for detail in details_by_meaning}

    # search the derivative from 'derivatives' table and bring its word_id
    derivatives_by_word = Derivative.query.filter(Derivative.word.ilike(search_pattern)).all()
    word_ids_by_derivative = {derivative.word_id for derivative in derivatives_by_word}

    # search the pos from 'pos' table by its word_id
    pos_by_name = POS.query.filter(POS.pos.ilike(search_pattern)).all()
    pos_ids = {pos.id for pos in pos_by_name}

    # bring word_id from 'details' & 'derivatives' tables by pos_id
    word_ids_by_pos_detail = {detail.word_id for detail in Detail.query.filter(Detail.pos_id.in_(pos_ids)).all()}
    word_ids_by_pos_derivative = {derivative.word_id for derivative in Derivative.query.filter(Derivative.pos_id.in_(pos_ids)).all()}

    # combine all word_id
    all_word_ids = word_ids_by_word | word_ids_by_meaning | word_ids_by_derivative | word_ids_by_pos_detail | word_ids_by_pos_derivative

    if not all_word_ids:
        return render_template('search.html', query=query, results=[])

    # search 'words', 'details', 'derivatives' searched word_id
    words = Word.query.filter(Word.id.in_(all_word_ids)).all()
    details = Detail.query.filter(Detail.word_id.in_(all_word_ids)).all()
    derivatives = Derivative.query.filter(Derivative.word_id.in_(all_word_ids)).all()

    # group the results
    grouped_results = defaultdict(list)

    for word in words:
        grouped_details = [d for d in details if d.word_id == word.id]
        grouped_derivatives = [d for d in derivatives if d.word_id == word.id]

        grouped_results[word.day_id].append({
            "word": word.word,
            "derivatives": grouped_derivatives,
            "details": grouped_details,
        })
    results = [{"day": day, "words": words} for day, words in sorted(grouped_results.items())]
    return render_template('search.html', query=query, results=results)



@views_bp.route('/api/chat', methods=['POST'])
def chat():
    user_inp = request.json.get("Message", "").strip()

    ai = ask(user_inp)

    return jsonify({"response": ai})