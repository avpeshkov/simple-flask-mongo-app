import sys
from pprint import pprint

import flask
from flask import request, jsonify
from mongoengine import Q

from ...main import app
from ...models.song import Song


@app.route('/songs/', methods=['GET'])
def get_songs():
    query = Song.objects

    if message := flask.request.args.get("message") or '':
        query = query.filter(Q(artist__icontains=message) | Q(title__icontains=message))

    page_num = int(flask.request.args.get("page") or 1)
    songs = query.paginate(page=page_num, per_page=5)
    songs_len = query.count()

    if not songs:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify({'page': page_num,
                        'total_objects': songs_len,
                        'songs': [s.to_json() for s in songs.items]}), 200


@app.route('/songs/', methods=['POST'])
def update_song():
    song_id = request.form.get('song_id')
    rating = request.form.get('rating')

    song = Song.objects(pk=song_id).first()
    if not song:
        return jsonify({'error': 'data not found'}), 500
    else:
        song.update(rating=rating)
        song.reload()
    return jsonify(song.to_json()), 200


@app.route('/songs/average_difficulty/', methods=['GET'])
def get_average_difficulty():
    query = Song.objects
    if level := flask.request.args.get("level") or None:
        query = query(level=int(level))

    return jsonify({'total': query.count(), "average_difficulty": round(query.average('difficulty'), 2)}), 200


@app.route('/songs/average_rating/', methods=['GET', 'POST'])
def get_average_min_max_rating():
    query = Song.objects
    if request.method == 'POST':
        id_list = request.form.get('id_list', default='').split(',')
        if id_list:
            query = query.filter(pk__in=id_list)

    query.filter(rating__exists=True)
    if not query:
        return {'error': "Not song with rating"}, 500

    pipeline = [
        {"$group": {
            "_id": None,
            "max": {"$max": "$rating"},
            "min": {"$min": "$rating"},
            "avg": {"$avg": "$rating"}
        }}
    ]

    if data_list := list(query().aggregate(pipeline)):
        data = data_list.pop()

        return jsonify({'total': query.count(),
                        "average_rating": round(data['avg'], 2),
                        "min_rating": round(data['min'], 2),
                        "max_rating": round(data['max'], 2),
                        }), 200
    else:
        return {'error': "Fail to calculate data"}, 500
