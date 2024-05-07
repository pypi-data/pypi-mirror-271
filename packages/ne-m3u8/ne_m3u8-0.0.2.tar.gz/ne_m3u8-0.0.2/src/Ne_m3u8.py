import os
import requests
import m3u8
import threading
from DownloadKit import DownloadKit
from m3u8 import M3U8, Segment
from urllib.parse import urljoin
import decrypto, ffmpeg


class Neko_m3u8:
    def __init__(self):
        self.all_ts_links = []
        self.kit = DownloadKit()
        self.thread_list = []

    def __web_get(self, url, **kwargs):
        if 'headers' not in kwargs:
            headers = {
                'accept': '*/*',
                'accept-language': 'zh-CN,zh;q=0.9',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'priority': 'u=1, i',
                'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            }
        else:
            headers = kwargs['headers']
        resp = requests.get(url, headers=headers)
        # print(kwargs)
        return resp

    def __get_m3u8_from_url_file(self, file_path: str, headers: dict = None) -> M3U8:
        # 打开并读取 m3u8 文件
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                m3u8_obj = m3u8.loads(f.read())
        else:
            m3u8_obj = m3u8.loads(self.__web_get(url=file_path, headers=headers).text)
        return m3u8_obj

    def parse_m3u8(self, file_path, headers: dict = None, base_url: str = None):
        m3u8_obj = self.__get_m3u8_from_url_file(file_path, headers)
        # 初始化一个列表来存储所有的 TS 链接
        ts_urls = []
        key, iv = self.get_m3u8_key_iv(m3u8_obj, base_url)
        # 检查是否存在 media playlists
        if m3u8_obj.playlists:
            for media_playlist in m3u8_obj.playlists:
                segments = media_playlist.segments
                for i, segment in enumerate(segments, start=1):
                    # 得到完整路径
                    full_url = urljoin(base_url, segment.uri)
                    ts_urls.append(full_url)
        else:
            # 如果没有 media playlists，则直接从主 playlist 获取 segments
            segments = m3u8_obj.segments
            for i, segment in enumerate(segments, start=1):
                # 得到完整路径
                full_url = urljoin(base_url, segment.uri)
                ts_urls.append(full_url)
        self.all_ts_links = ts_urls
        return ts_urls, key, iv

    def get_m3u8_key_iv(self, m3u8_obj: M3U8, base_url: str = None):
        try:
            key_url = urljoin(base_url, m3u8_obj.segments[0].key.uri)
            key_data = self.__web_get(url=key_url).text
            iv = m3u8_obj.segments[0].key.iv
            if iv.startswith('0x') or iv.startswith('0X'):
                iv = iv[2:]
                iv = str(int(iv, 16))
        except AttributeError:
            key_data = None
            iv = None
        return key_data, iv

    def decrypto_ts(self, file_path, key, iv):
        """
        :param file_path: ts 文件路径
        :param key:
        :param iv:
        :return:
        """
        if key and iv:
            with open(file_path, 'rb') as f:
                ts_data = f.read()
            encrypto_ts = decrypto.decrypt_ts_segment(encrypted_ts_data=ts_data,
                                                      key=key,
                                                      iv=iv)
            new_file = file_path.replace(os.path.basename(file_path), f'$${os.path.basename(file_path)}')
            with open(new_file, 'wb+') as ff:
                ff.write(encrypto_ts)
            os.remove(file_path)
            os.rename(new_file, file_path)

    def add_thread(self, file_path, headers: dict = None, base_url: str = None, save_dir: str = None,
                   file_name: str = None, suffix: str = 'ts', time_out: float = None, thread_num_limit: int = 32):
        ts_urls, key, iv = self.parse_m3u8(file_path, headers=headers, base_url=base_url)
        now_thread_num = 1
        ts_file_dir = os.path.join(save_dir, file_name)
        for index, ts_url in enumerate(ts_urls, start=1):
            self.kit.add(file_url=ts_url,
                         goal_path=ts_file_dir,
                         rename=str(index),
                         suffix=suffix,
                         timeout=time_out,
                         headers=headers)
            if now_thread_num % thread_num_limit == 0:
                self.kit.wait(show=True)
            now_thread_num += 1
        self.kit.wait()

        ts_files = os.listdir(ts_file_dir)
        for ts_file in ts_files:
            ts_path = os.path.join(ts_file_dir, ts_file)
            self.decrypto_ts(ts_path, key, iv)
        ffmpeg.merge_ts_files(ts_file_dir, os.path.join(save_dir, f'{file_name}.mp4'))

    def add(self, file_path, headers: dict = None, base_url: str = None, save_dir: str = None, file_name: str = None,
            suffix: str = 'ts', time_out: float = 15, thread_num_limit: int = 32):
        """多线程的方式下载m3u8自动解密并合并
        :param file_path: M3u8地址 网络地址或本地地址
        :param headers: 请求头
        :param base_url:
        :param save_dir: 保存路径
        :param file_name: 保存文件名称,无需后缀
        :param time_out: 超时时间
        :param suffix:
        :param thread_num_limit: 多线程下载ts线程数
        :return:
        """
        add_thread = threading.Thread(target=self.add_thread, args=(file_path, headers, base_url, save_dir, file_name,
                                                                    suffix, time_out, thread_num_limit))
        add_thread.start()
        self.thread_list.append(add_thread)

    def wait(self):
        for down_thread in self.thread_list:
            down_thread.join()


if __name__ == '__main__':
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://player.catw.moe',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://player.catw.moe/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    n_m = Neko_m3u8()
    m3u8_url = r'https://c.m3u8.anime.catw.cc/videos/65e3351fb75797bbd54d276e/6951cf/index.m3u8?counts=3&timestamp=1714983782000&key=8046217a56373b9b7c96a04696928c8a'
    base_url = 'https://c.m3u8.anime.catw.cc/videos/65e3351fb75797bbd54d276e/6951cf/'
    # with open(r'C:\Users\Administrator\Desktop\1.m3u8','r') as f:
    #     m3u8_url = f.read()
    output_dir = 'output_segments'
    output_mp4 = 'output.mp4'
    # n_m.parse_m3u8(m3u8_url, base_url=base_url)
    n_m.add(file_path=m3u8_url,
            save_dir=r'D:\pythoncode\代码\Ne_m3u8\新建文件夹',
            base_url=base_url,
            file_name='1',
            headers=headers)
