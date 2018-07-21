# python实现音乐下载，API采用QQMusic

import requests
import json

headers = {
    'Host': 'c.y.qq.com',
    'Referer': 'http://c.y.qq.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
                  'Safari/537.36 '
}

def qq_post(mid):
    # mid:歌曲id
    post_url = 'http://www.douqq.com/qqmusic/qqapi.php'
    data = {
        'mid': mid
    }
    rest = requests.post(post_url, data=data)
    get_json = json.loads(rest.text)
    return eval(get_json)

def download_file(src, file_path):
    r = requests.get(src, stream=True)
    f = open(file_path, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
    return file_path

def choice_download(dic):
    print('1. m4a视频')
    print('2. mp3普通品质')
    print('3. mp3高品质')
    print('4. ape高品无损')
    print('5. flac无损音频')
    select = int(input('请输入你要下载的音乐的音质: '))
    src = ''
    # 歌曲的后缀即音质
    postfix = ''
    if select == 1:
        src = dic['m4a']
        postfix = '.m4a'
    elif select == 2:
        src = dic['mp3_l']
        postfix = '.mp3'
    elif select == 3:
        src = dic['mp3_h']
        postfix = '.mp3'
    elif select == 4:
        src = dic['ape']
        postfix = '.ape'
    elif select == 5:
        src = dic['flac']
        postfix = '.flac'
    return postfix, src.replace('\/\/', '//').replace('\/', '/')

def find_songs(word):
    get_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&w=' + word
    rest1 = requests.get(get_url, headers=headers)
    get_json = json.loads(rest1.text.strip('callback()[]'))
    jsons = get_json['data']['song']['list']
    songmid = []
    media_mid = []
    song_singer = []
    i = 1
    for song in jsons:
        print(i, ':' + song['songname'], '----', song['singer'][0]['name'])
        songmid.append(song['songmid'])
        media_mid.append(song['media_mid'])
        song_singer.append(song['singer'][0]['name'])
        i = i + 1
    select = int(input('请输入你的选择: ')) - 1
    return songmid[select], song_singer[select]

if __name__ == '__main__':
    songname = input('请输入要查找的歌曲: ')
    song_mid, singer = find_songs(songname)
    dic = qq_post(song_mid)
    postfix, url = choice_download(dic)
    save_path = "F:\\Musics\\"
    download_file(url, save_path + songname + ' - ' + singer + postfix)
    print('已下载成功!')

