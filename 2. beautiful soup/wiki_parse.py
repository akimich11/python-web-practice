import bs4
import unittest


def count_letters(header):
    letters = 0
    for h in header:
        if h.get_text()[0] in ['E', 'C', 'T']:
            letters += 1
    return letters


def next_tag(tag):
    for next_sib in tag.next_siblings:
        if isinstance(next_sib, bs4.element.Tag):
            return next_sib


def count_imgs(body):
    all_imgs = body.find_all('img')
    imgs = 0
    for img in all_imgs:
        if img.get('width') is not None and int(img.get('width')) >= 200:
            imgs += 1
    return imgs


def count_headers(body):
    headers = 0
    for header in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        headers += count_letters(body.find_all(header))
    return headers


def count_links(body):
    all_links = body.find_all('a')
    chain_len = int(len(all_links) != 0)
    links_len = chain_len
    i = 0
    while i < len(all_links):
        while i != len(all_links) - 1 and next_tag(all_links[i]) == all_links[i + 1]:
            chain_len += 1
            i += 1
        links_len = max(links_len, chain_len)
        chain_len = 1
        i += 1
    return links_len


def count_lists(body):
    ols = body.find_all('ol')
    uls = body.find_all('ul')
    lists = 0
    for ol in ols:
        parents = [tag.name for tag in ol.parents]
        if 'li' not in parents:
            lists += 1

    for ul in uls:
        parents = [tag.name for tag in ul.parents]
        if 'li' not in parents:
            lists += 1
    return lists


def parse(path_to_file):
    soup = bs4.BeautifulSoup(open(path_to_file, 'r', encoding='utf-8'), 'lxml')
    body = soup.find(id="bodyContent")
    imgs = count_imgs(body)
    headers = count_headers(body)
    links_len = count_links(body)
    lists = count_lists(body)

    return [imgs, headers, links_len, lists]


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()
