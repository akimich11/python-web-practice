import requests


ACCESS_TOKEN = '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711'


def calc_age(uid):
    command_begin = 'https://api.vk.com/method/'
    user = requests.get(command_begin + 'users.get?user_ids=' + uid + '&fields=bdate&access_token=' +
                        ACCESS_TOKEN + '&v=5.71').json()['response'][0]
    user_id = str(user['id'])
    friends = requests.get(
        command_begin + 'friends.get?user_id=' + user_id + '&fields=bdate&access_token=' +
        ACCESS_TOKEN + '&v=5.71').json()
    byears = [int(friends['response']['items'][i]['bdate'].split('.')[2]) for i in range(friends['response']['count'])
              if ('bdate' in friends['response']['items'][i] and
                  len(friends['response']['items'][i]['bdate'].split('.')) == 3)]

    unique_years = set()
    frequencies = dict()
    for year in byears:
        length = len(unique_years)
        unique_years.add(2021 - year)
        if length == len(unique_years):
            frequencies[2021 - year] += 1
        else:
            frequencies[2021 - year] = 1

    tuples = []
    for year in frequencies:
        tuples.append((year, frequencies[year]))
    tuples.sort(key=lambda x: (-x[1], x[0]))
    return tuples