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
