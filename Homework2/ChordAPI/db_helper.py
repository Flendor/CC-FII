def get_single_chord_response(conn, chord_name):
    c = conn.cursor()
    statement = 'select c.* from chords c where lower(c.name) = lower(?)'
    c.execute(statement, (chord_name, ))
    results = c.fetchall()
    response_dict = {}
    if len(results) == 0:
        response_dict['response'] = 'Cannot find a chord with name: ' + chord_name
        return response_dict, 404
    for result in results:
        response_dict['chord_id'] = result[0]
        response_dict['name'] = result[1]
        response_dict['notes_in_chord'] = result[2]
        response_dict['index_finger_position'] = result[3]
        response_dict['middle_finger_position'] = result[4]
        response_dict['ring_finger_position'] = result[5]
        response_dict['pinkie_position'] = result[6]
        response_dict['thumb_position'] = result[7]
    return response_dict, 200


def make_chord_dict(result):
    chord_dict = dict()
    chord_dict['id'] = result[3]
    chord_dict['name'] = result[4]
    chord_dict['notes_in_chord'] = result[5]
    chord_dict['index_finger_position'] = result[6]
    chord_dict['middle_finger_position'] = result[7]
    chord_dict['ring_finger_position'] = result[8]
    chord_dict['pinkie_position'] = result[9]
    chord_dict['thumb_position'] = result[10]
    return chord_dict


def get_song_by_name(conn, song):
    c = conn.cursor()
    statement = 'select s.sid, s.name, s.artist, c.* from songs s join chords_songs cs on cs.sid = s.sid' \
                ' join chords c on c.cid = cs.cid where lower(s.name) = lower(?)'
    c.execute(statement, (song, ))
    results = c.fetchall()
    song_dict = dict()
    for result in results:
        if result[0] not in song_dict.keys():
            song_dict[result[0]] = {}
            song_dict[result[0]]['name'] = result[1]
            song_dict[result[0]]['artist'] = result[2]
            song_dict[result[0]]['chords'] = []
        chord_dictionary = make_chord_dict(result)
        song_dict[result[0]]['chords'].append(chord_dictionary)

    response_array = []
    for key, value in song_dict.items():
        response_dict = dict()
        response_dict['id'] = key
        response_dict['name'] = value['name']
        response_dict['artist'] = value['artist']
        response_dict['chords'] = value['chords']
        response_array.append(response_dict)
    return response_array, 200


def get_songs_by_artist(conn, artist):
    c = conn.cursor()
    statement = 'select s.sid, s.name, s.artist, c.* from songs s join chords_songs cs on cs.sid = s.sid' \
                ' join chords c on c.cid = cs.cid where lower(s.artist) = lower(?)'
    c.execute(statement, (artist,))
    results = c.fetchall()
    song_dict = dict()
    for result in results:
        if result[0] not in song_dict.keys():
            song_dict[result[0]] = {}
            song_dict[result[0]]['name'] = result[1]
            song_dict[result[0]]['artist'] = result[2]
            song_dict[result[0]]['chords'] = []
        chord_dictionary = make_chord_dict(result)
        song_dict[result[0]]['chords'].append(chord_dictionary)

    response_array = []
    for key, value in song_dict.items():
        response_dict = dict()
        response_dict['id'] = key
        response_dict['name'] = value['name']
        response_dict['artist'] = value['artist']
        response_dict['chords'] = value['chords']
        response_array.append(response_dict)
    return response_array, 200


def get_song_by_id(conn, sid):
    c = conn.cursor()
    statement = 'select s.sid, s.name, s.artist, c.* from songs s join chords_songs cs on cs.sid = s.sid' \
                ' join chords c on c.cid = cs.cid where s.sid = ?'
    c.execute(statement, (sid,))
    results = c.fetchall()
    response_dict = {}
    if len(results) == 0:
        response_dict['response'] = 'Cannot find a song with id: ' + str(sid)
        return response_dict, 404
    song_dict = dict()
    for result in results:
        if result[0] not in song_dict.keys():
            song_dict[result[0]] = {}
            song_dict[result[0]]['name'] = result[1]
            song_dict[result[0]]['artist'] = result[2]
            song_dict[result[0]]['chords'] = []
        chord_dictionary = make_chord_dict(result)
        song_dict[result[0]]['chords'].append(chord_dictionary)
    response_dict['song_id'] = sid
    response_dict['name'] = song_dict[sid]['name']
    response_dict['artist'] = song_dict[sid]['artist']
    response_dict['chords'] = song_dict[sid]['chords']
    return response_dict, 200


def insert_chord_into_db(conn, body):
    c1 = conn.cursor()
    statement = 'select c.* from chords c where lower(c.name) = lower(?)'
    c1.execute(statement, (body['name'], ))
    result = c1.fetchall()
    if len(result) > 0:
        response_dict = {"Response": "Chord with this name already exists!"}
        return response_dict, 409

    c2 = conn.cursor()
    statement2 = 'insert into chords (name, notes, index_finger_position, middle_finger_position, ring_finger_position, pinkie_position, thumb_position) ' \
                 'values (?, ?, ?, ?, ?, ?, ?);'
    c2.execute(statement2, (body['name'], body['notes_in_chord'], body['index_finger_position'], body['middle_finger_position'],
                            body['ring_finger_position'], body['pinkie_position'], body['thumb_position']))
    conn.commit()
    response_dict = dict()
    response_dict['Response'] = 'localhost:9090/chord/' + body['name'].replace(' ', '')
    return response_dict, 201


def insert_song_into_db(conn, body):
    c1 = conn.cursor()
    statement = 'select s.* from songs s where lower(s.name) = lower(?) and lower(s.artist) = lower(?)'
    c1.execute(statement, (body['name'], body['artist']))
    result = c1.fetchall()
    if len(result) > 0:
        response_dict = {"Response": "Song with this name and artist already exists!"}
        return response_dict, 409

    c2 = conn.cursor()
    statement2 = 'insert into songs (name, artist) values (?, ?);'
    c2.execute(statement2, (body['name'], body['artist']))
    c3 = conn.cursor()
    statement3 = 'select s.sid from songs s where lower(s.name) = lower(?) and lower(s.artist) = lower(?)'
    c3.execute(statement3, (body['name'], body['artist']))
    id_result = c3.fetchall()
    c4 = conn.cursor()
    statement4 = 'insert into chords_songs (cid, sid) values (?, ?);'
    for chord in body['chords']:
        c5 = conn.cursor()
        statement5 = 'select c.cid from chords c where lower(c.name) = lower(?)'
        c5.execute(statement5, (chord, ))
        chord_id_result = c5.fetchall()
        if len(chord_id_result) == 0:
            response_dict = {'Response': 'Cannot find a chord with name: ' + chord}
            return response_dict, 404
        c4.execute(statement4, (chord_id_result[0][0], id_result[0][0]))
    conn.commit()
    response_dict = dict()
    response_dict['resource_link'] = 'localhost:9090/song/id/' + str(id_result[0][0])
    return response_dict, 201


def update_chord_in_db(conn, body, chord):
    c1 = conn.cursor()
    statement = 'select c.cid from chords c where lower(c.name) = lower(?)'
    c1.execute(statement, (chord,))
    result = c1.fetchall()
    if len(result) == 0:
        response_dict = {"Response": 'Cannot find a chord with name: ' + chord}
        return response_dict, 404

    c2 = conn.cursor()
    statement2 = 'update chords set name = ?, notes = ?, index_finger_position = ?, middle_finger_position = ?, ' \
                 'ring_finger_position = ?, pinkie_position = ?, thumb_position = ? where cid = ?'
    c2.execute(statement2,
               (body['name'], body['notes_in_chord'], body['index_finger_position'], body['middle_finger_position'],
                body['ring_finger_position'], body['pinkie_position'], body['thumb_position'], result[0][0]))
    conn.commit()
    response_dict = dict()
    response_dict['Response'] = 'localhost:9090/chord/' + body['name'].replace(' ', '')
    return response_dict, 200


def update_song_in_db(conn, body, sid):
    c1 = conn.cursor()
    statement = 'select s.* from songs s where s.sid = ?'
    c1.execute(statement, (sid, ))
    result = c1.fetchall()
    if len(result) == 0:
        response_dict = {"Response": "Cannot find song with id: " + str(sid)}
        return response_dict, 404

    c2 = conn.cursor()
    statement2 = 'update songs set name = ?, artist = ? where sid = ?;'
    c2.execute(statement2, (body['name'], body['artist'], sid, ))
    c3 = conn.cursor()
    statement3 = 'delete from chords_songs where sid = ?'
    c3.execute(statement3, (sid, ))
    c4 = conn.cursor()
    statement4 = 'insert into chords_songs (cid, sid) values (?, ?);'
    for chord in body['chords']:
        c5 = conn.cursor()
        statement5 = 'select c.cid from chords c where lower(c.name) = lower(?)'
        c5.execute(statement5, (chord,))
        chord_id_result = c5.fetchall()
        if len(chord_id_result) == 0:
            response_dict = {'Response': 'Cannot find a chord with name: ' + chord}
            return response_dict, 404
        c4.execute(statement4, (chord_id_result[0][0], sid))
    conn.commit()
    response_dict = dict()
    response_dict['resource_link'] = 'localhost:9090/song/id/' + str(sid)
    return response_dict, 200


def delete_chord_from_db(conn, chord):
    c1 = conn.cursor()
    statement = 'select c.* from chords c where lower(c.name) = lower(?)'
    c1.execute(statement, (chord, ))
    result = c1.fetchall()
    if len(result) == 0:
        response_dict = {"Response": "Cannot find chord with name: " + chord}
        return response_dict, 404

    c2 = conn.cursor()
    statement2 = 'delete from chords where lower(name) = lower(?)'
    c2.execute(statement2, (chord, ))
    conn.commit()
    response_dict = dict()
    response_dict['Response'] = chord + " was deleted successfully from the database!"
    return response_dict, 200


def delete_song_from_db(conn, sid):
    c1 = conn.cursor()
    statement = 'select s.name, s.artist from songs s where lower(s.sid) = lower(?)'
    c1.execute(statement, (sid,))
    result = c1.fetchall()
    if len(result) == 0:
        response_dict = {"Response": "Cannot find song with id: " + str(sid)}
        return response_dict, 404

    c2 = conn.cursor()
    statement2 = 'delete from songs where sid = ?'
    c2.execute(statement2, (sid,))
    conn.commit()
    response_dict = dict()
    response_dict['Response'] = result[0][0] + " by " + result[0][1] + " was deleted successfully from the database!"
    return response_dict, 200
