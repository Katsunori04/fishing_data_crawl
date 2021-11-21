import urllib.request
import sys
import time
from retry import retry


@retry(tries=5, delay=5)
def pageDownload(url, filename):
    urllib.request.urlretrieve(url, filename)


if __name__ == "__main__":
    dir_name = "html/"
    base_url = "https://fishing.ne.jp/fishingpost/area/osaka"
    base_url2 = "https://fishing.ne.jp/fishingpost/area/osaka/page"

    for i in range(2191):
        filename = str(i) + ".html"
        i = i + 1
        print("download : {}".format(str(i)))
        if i == 1:
            target_url = base_url
        else:
            target_url = base_url2 + "/" + str(i)

        pageDownload(target_url, dir_name + filename)

        time.sleep(1)
