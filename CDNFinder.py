import dns
import dns.message
import dns.query

CDN_PROVIDER = [
    [".afxcdn.net", "afxcdn.net"],
    [".akadns.net", "Akamai"],
    [".akamai.net", "Akamai"],
    [".akamaiedge.net", "Akamai"],
    [".akamaitechnologies.com", "Akamai"],
    [".anankecdn.com.br", "Ananke"],
    [".att-dsa.net", "AT&T"],
    [".ay1.b.yahoo.com", "Yahoo"],
    [".azioncdn.net", "Azion"],
    [".bluehatnetwork.com", "Blue Hat Network"],
    [".c3cache.net", "ChinaCache"],
    [".c3cdn.net", "ChinaCache"],
    [".cachefly.net", "Cachefly"],
    [".cap-mii.net", "Mirror Image"],
    [".ccgslb.com", "ChinaCache"],
    [".ccgslb.net", "ChinaCache"],
    [".cdn.bitgravity.com", "Bitgravity"],
    [".cdn.telefonica.com", "Telefonica"],
    [".cdn77.net", "CDN77"],
    [".cdngc.net", "CDNetworks"],
    [".chinacache.net", "ChinaCache"],
    [".clients.turbobytes.com", "Turbobytes"],
    [".cloudflare.com", "Cloudflare"],
    [".cloudfront.net", "Amazon Cloudfront"],
    [".cotcdn.net", "Cotendo"],
    [".edgecastcdn.net", "EdgeCast"],
    [".fastly.net", "Fastly"],
    [".footprint.net", "Level3"],
    [".gccdn.cn", "CDNetworks"],
    [".gccdn.net", "CDNetworks"],
    [".google.", "Google"],
    [".googleusercontent.com", "Google"],
    [".gslb.taobao.com", "Taobao"],
    [".gslb.tbcache.com", "Alimama"],
    [".hwcdn.net", "Highwinds"],
    [".instacontent.net", "Mirror Image"],
    [".internapcdn.net", "Internap"],
    [".kxcdn.com", "KeyCDN"],
    [".l.doubleclick.net", "Google"],
    [".llnwd.net", "Limelight"],
    [".lswcdn.net", "LeaseWeb CDN"],
    [".lxdns.com", "ChinaNetCenter"],
    [".mirror-image.net", "Mirror Image"],
    [".netdna-cdn.com", "MaxCDN"],
    [".netdna-ssl.com", "MaxCDN"],
    [".netdna.com", "MaxCDN"],
    [".panthercdn.com", "Panther"],
    [".rncdn1.com", "Reflected Networks"],
    [".simplecdn.net", "Simple CDN"],
    [".swiftcdn1.com", "SwiftCDN"],
    [".systemcdn.net", "EdgeCast"],
    [".vo.msecnd.net", "Windows Azure"],
    [".voxcdn.net", "Voxel"],
    [".yimg.", "Yahoo"],
    ["bo.lt", "BO.LT"],
    ["cdn.optimizely.com", "Akamai"],
    ["edgecastcdn.net", "EdgeCast"],
    ["google-analytics.com", "Google"],
    ["googlesyndication.", "Google"],
    ["hwcdn.net", "Highwinds"],
    ["youtube.", "Google"],
]


def finder(host):
    result = None
    for cdn in CDN_PROVIDER:
        if cdn[0] in host:
            return cdn[1]
    return None


def findcdnfromhost(host, dnsip="8.8.8.8"):
    """

    :param host:
    :param dnsip:
    :return:
    """
    newhost = host
    try:
        q = dns.message.make_query(host, "A")
        r = dns.query.udp(q, dnsip)
        # print r.answer
        for ans in r.answer:
            if "CNAME" in ans.to_text():
                newhost = ans.to_text().split("CNAME ")[1][:-1]
                result = finder(newhost)
                if result is not None:
                    return result
    except:
        pass
    return finder(newhost)


if __name__ == "__main__":
    import sys

    print findcdnfromhost("https://static01.nyt.com/")
    print findcdnfromhost('a1.nyt.com')
    print findcdnfromhost('static01.nyt.com')

