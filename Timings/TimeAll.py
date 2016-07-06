import json
import subprocess
import shlex
from random import randint
import multiprocessing as mp
from time import sleep
import socket


def is_ip(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False


def time_url(q, page_url):
    cmd = 'curl -L -w "@curl-format-pack.json" -o /dev/null -s "www.{0}"'.format(page_url)
    print cmd
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
    out, err = proc.communicate()
    out = out.strip()

    if (len(out)) and (err is None):
        json_obj = json.loads(out)
        json_obj['url'] = page_url
        json_obj['OK'] = 1
        q.put(json_obj)
    if err is not None:
        json_obj = {'url': page_url, 'OK': 0}
        q.put(json_obj)


def listener(q):
    """listens for messages on the q, writes to file. """
    f1 = open('./alexa_times.txt', 'wb')
    f2 = open('./alexa_err.txt', 'wb')
    while 1:
        m = q.get()
        if m['OK'] == -1:
            # f.write('killed')
            break
        if m['OK'] == 1:
            f1.write(json.dumps(m)+'\n')
            f1.flush()
        if m['OK'] == 0:
            f2.write(m['url']+'\n')
            f2.flush()

    f1.close()
    f2.close()


def main():
    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count() * 8)
    # pool = mp.Pool(256)
    watcher = pool.apply_async(listener, (q,))
    alexa_file = '../AlexaCrawler/top-500.csv'
    br = open(alexa_file, 'rb')
    cnt = 0
    for l in br:
        page_url = l.strip()
        prc = mp.Process(target=time_url, args=(q, page_url,))
        prc.start()
        cnt += 1
        # if cnt == 10:
        #     break

    sleep(120)
    q.put(dict(OK=-1))
    pool.close()


if __name__ == '__main__':
    main()
