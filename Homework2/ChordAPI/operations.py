def get_chord_name_from_url(url):
    url_chord = url.split('/')[-1]
    chord = url_chord[0] + ' ' + url_chord[1:]
    return chord


def get_name_from_url(url):
    name = url.split('/')[-1]
    all_names = name.split('%20')
    final_name = ''
    for index, name in enumerate(all_names):
        if index != 0:
            final_name += ' '
        final_name += name
    return final_name


def get_sid_from_url(url):
    url_sid = url.split('/')[-1]
    sid = int(url_sid)
    return sid


def is_chord_body_valid(body):
    print(body)
    if "notes_in_chord" not in body.keys() or "name" not in body.keys() or "index_finger_position" not in body.keys() \
            or "middle_finger_position" not in body.keys() or "ring_finger_position" not in body.keys() \
            or "pinkie_position" not in body.keys() or "thumb_position" not in body.keys():
        return False
    return True


def is_song_body_valid(body):
    if "name" not in body.keys() or "artist" not in body.keys() or "chords" not in body.keys():
        return False
    if not isinstance(body['chords'], list):
        return False
    chords = list(filter(lambda x: isinstance(x, str), body['chords']))
    if len(chords) != len(body['chords']):
        return False
    return True
