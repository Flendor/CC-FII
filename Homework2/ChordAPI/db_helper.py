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

