import json
import CDNFinder as cdnfinder
from haralyzer import HarPage, HarParser
from urlparse import urlparse
import os


def list_all_hars():
    har_folder = './GetHAR/data_har_cleaned'
    result_list = []
    for (path, dirs, files) in os.walk(har_folder):
        for top_site in files:
            fn = os.path.join(path, top_site)
            result_list.append(fn)
    return result_list


def list_err_hars():
    har_folder = './GetHAR/data_har_cleaned'
    result_list = []
    with open('./data/err', 'rb') as br:
        for el in br:
            fn = el.strip()
            result_list.append(os.path.join(har_folder, fn))
    return result_list


def main(har_list):
    bw = open('./data/top_site_cdn.jsons', 'wb')
    err = []
    for fn in har_list:
        print fn
        top_site = os.path.basename(fn)
        try:
            with open(fn, 'r') as fp:
                har_parser = HarParser(json.loads(fp.read()))

            har_page = har_parser.pages[0]

            content_from_cdn_size = {}
            content_from_cdn_count = {}
            for entry in har_page.entries:
                # print entry
                object_url = entry['request']['url']
                parsed_uri = urlparse(object_url)
                # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                domain = '{uri.netloc}'.format(uri=parsed_uri)
                cdn = cdnfinder.findcdnfromhost(domain)
                # print cdn, domain

                if cdn is not None:
                    dl_from_cdn_size = content_from_cdn_size[cdn] if cdn in content_from_cdn_size else 0
                    dl_from_cdn_count = content_from_cdn_count[cdn] if cdn in content_from_cdn_count else 0
                    body_size = entry['response']['bodySize']
                    content_from_cdn_size[cdn] = body_size + dl_from_cdn_size
                    content_from_cdn_count[cdn] = 1 + dl_from_cdn_count

            # site_name = top_site.replace('.har', '')
            site_name = top_site.replace('.har', '')
            final_json = {'url': site_name, 'object_size': content_from_cdn_size, 'object_count': content_from_cdn_count}
            bw.write('%s\n' % json.dumps(final_json))
        except:
            err.append(top_site)
            print '!!! ', top_site
    bw.close()

    with open('./data/err', 'wb') as err_bw:
        for el in err:
            err_bw.write('{}\n'.format(el))


def har_cleaner():
    har_folder = './GetHAR/data_har'
    har_folder_out = './GetHAR/data_har_cleaned'
    empty = []
    for (path, dirs, files) in os.walk(har_folder):
        for top_site in files:
            with open(os.path.join(har_folder_out, top_site), 'wb') as har_bw:
                har_br = open(os.path.join(har_folder, top_site), 'rb')
                is_started = False
                for l in har_br:
                    if not is_started and l.startswith('{'):
                        is_started = True
                    if is_started:
                        har_bw.write(l)
                har_br.close()
                if not is_started:
                    empty.append(top_site.replace('.har', ''))
    with open('top-500-redo.csv', 'wb') as bw:
        for el in empty:
            bw.write('{}\n'.format(el))


if __name__ == '__main__':
    lst = list_all_hars()
    main(lst)
    # har_cleaner()
