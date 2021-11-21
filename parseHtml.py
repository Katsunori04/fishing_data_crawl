from bs4 import BeautifulSoup
import glob
import pandas as pd


def getHtmlDoc(html_file):
    # @param(str) : htmlのファイル名
    # @return(str) : html記述
    with open(html_file) as f:
        doc = f.read()
    return doc


def get_content(doc):
    # @pram(str) : html本文
    # @return(dict) : 解析結果
    soup = BeautifulSoup(doc, 'html.parser')
    fishing_post_doc = soup.select_one(
        ".fishingpost-box")  # fishingpostの１つ目を解析対象に
    soup = BeautifulSoup(str(fishing_post_doc), 'html.parser')

    titleArray = [title.get_text()
                  for title in soup.select("section div h1.title")]
    dateArray = [date.get_text().replace("UP!", "")
                 for date in soup.select("section div span.date")]
    descArray = [desc.get_text().replace("\n", "")
                 for desc in soup.select("section div.des.cl")]
    termArray = [term.get_text().split()[1:-1]
                 for term in soup.select("section div.terms")]

    return {"title": titleArray, "date": dateArray,
            "desc": descArray, "term": termArray}


def get_place4term(series):
    """
    @param(series):解析済みのpandasのtermカラム
    """
    try:
        return series[0].replace("の釣り情報", "")
    except:
        return ""


def get_fish4term(series):
    """
    @param(series):解析済みのpandasのtermカラム
    """
    try:
        return series[1].replace("釣り", "")
    except:
        return ""


def get_method4term(series):
    """
    @param(series):解析済みのpandasのtermカラム
    """
    try:
        return series[2].replace("釣果", "")
    except:
        return ""


# doc = getHtmlDoc("./html/100.html")
# doc_parse_result = get_content(doc)
# print([spot[0] for spot in doc_parse_result["term"]])
# print([spot[1] for spot in doc_parse_result["term"]])


df = pd.DataFrame()  # 結果格納用のDataFrame
for i, path in enumerate(glob.glob("./html/*.html")):
    doc = getHtmlDoc(path)
    result_df = pd.DataFrame(get_content(doc))
    print(i)  # カウント
    # print(result_dict)  # 結果確認
    df = pd.concat([df, result_df])
    # if i == 100:  # 検証用
    #     break

df.reset_index(inplace=True, drop=True)
df["spot"] = df["term"].apply(get_place4term)
df["fish"] = df["term"].apply(get_fish4term)
df["method"] = df["term"].apply(get_method4term)

df = df.drop(columns='term')
df = df.drop(columns='desc')
df = df.drop(columns='title')
df.to_csv("fishing_data.csv")
