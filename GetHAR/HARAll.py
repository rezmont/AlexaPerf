import json
import socket
import subprocess
import shlex
import multiprocessing as mp
from time import sleep


def run_with_timeout(timeout, func, args):
    """
    :rtype: object
    """
    # receive_end, send_end = mp.Pipe(duplex=False)
    # p = mp.Process(target=func, args=args, kwargs=dict(send_end=send_end))
    p = mp.Process(target=func, args=args)
    p.daemon = True
    p.start()
    # send_end.close()  # child must be the only one with it opened
    p.join(timeout)
    if p.is_alive():
        ####  debug('%s timeout', args)
        p.terminate()


def har_url(q, page_url):
    cmd = 'curl -L -w %{{url_effective}} -o /dev/null -s "{0}"'.format(page_url)
    # print cmd
    try:
        proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE)
        out, err = proc.communicate()
        out = out.strip()
        effective_url = page_url
        if (len(out)) and (err is None):
            effective_url = out.strip()
            print '{} --> {}'.format(page_url, effective_url)
        if err is not None:
            json_obj = {'url': page_url, 'OK': 0}
            q.put(json_obj)
            return

        with open('./data_har/{0}.har'.format(page_url), 'wb') as fo:
            cmd = "phantomjs ./phantomjs/netsniff_withtimeoute.js {0}".format(effective_url)
            print cmd
            err_code = subprocess.call(shlex.split(cmd), stdout=fo)
            if err_code == 1:
                json_obj = {'url': page_url, 'OK': 0}
                q.put(json_obj)
            return
    except:
        json_obj = {'url': page_url, 'OK': 0}
        q.put(json_obj)


def listener(q):
    """listens for messages on the q, writes to file. """
    f2 = open('./alexa_har_err.txt', 'wb')
    while 1:
        m = q.get()
        if m['OK'] == -1:
            break
        if m['OK'] == 0:
            f2.write(m['url'] + '\n')
            f2.flush()

    f2.close()


def main():
    # fo = open('./data_har/{0}.har'.format('x'), 'wb')
    # fo.write('x')
    # fo.close()

    manager = mp.Manager()
    q = manager.Queue()
    pool = mp.Pool(mp.cpu_count())
    # pool = mp.Pool(1)
    watcher = pool.apply_async(listener, (q,))
    # alexa_file = '/home/motamedi/Dropbox/workspace/web_perf/top-500.csv'
    alexa_file = '../top-500-redo.csv'
    br = open(alexa_file, 'rb')
    cnt = 0
    for l in br:
        page_url = l.strip()
        # prc = mp.Process(target=har_url, args=(q, page_url,))
        # prc.start()

        prc = mp.Process(target=run_with_timeout, args=(5, har_url, (q, page_url,)))
        prc.start()
        cnt += 1
        sleep(1)
        # if cnt == 10:
        #     break

    sleep(10)
    q.put(dict(OK=-1))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
