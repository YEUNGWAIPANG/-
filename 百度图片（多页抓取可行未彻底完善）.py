import re
import os
import requests
from time import sleep
from tqdm import tqdm
from fake_useragent import UserAgent

headers={
        "User-Agent":UserAgent().random,
        "Referer":"https://image.baidu.com"
        }

def getHTML(kw,i):
    url='https://image.baidu.com/search/acjson'
    params={
            'tn':'resultjson_com' ,
            'ipn':'rj' ,
            'ct':'201326592',
            'is':' ' ,
            'fp':'result',
            'queryWord':kw,
            'cl':'2' ,
            'lm':'-1' ,
            'ie':'utf-8' ,
            'oe':'utf-8' ,
            'adpicid':' ' ,
            'st':' ' ,
            'z':' ' ,
            'ic':' ' ,
            'hd':' ' ,
            'latest':' ' ,
            'copyright':' ' ,
            'word':kw ,
            's':' ' ,
            'se':' ' ,
            'tab':' ' ,
            'width':' ' ,
            'height':' ' ,
            'face':' ' ,
            'istype':' ' ,
            'qc':' ' ,
            'nc':' 1' ,
            'fr':' ' ,
            'expermode':' ' ,
            'force':' ' ,
            'cg':'girl' ,
            'pn': i  ,
            'rn':'30' ,
            'gsm':'3c' ,
            '1599561776995':' ',
    }
    r=requests.get(url,headers=headers,params=params)
    r.raise_for_status()
    r.encoding=r.apparent_encoding
    urls=re.findall('"thumbURL":"(.*?)"',r.text)
    # for i in urls:
    #     print(i)
    return urls,r.text

def download(urls,num,kw):
    if not os.path.exists('./%s'%(kw)):
        dir=os.mkdir('./%s'%(kw))
    for pic in tqdm(urls):
        try:
            i=requests.get(pic,headers=headers)
            path=os.path.abspath(kw)+"\\"+"%s"%kw+str(num)+".jpg"
            f=open(path,"wb")
            f.write(i.content)
            f.close()
            num+=1
        except:
            continue
    return num

def main():
    kw=input('图片关键字:')
    rtext=getHTML(kw,0)[1]
    zongshu=re.findall('"displayNum":(.*?)"',rtext)[0]
    print('找到关键字为"%s"的图片共%s张\n'%(kw,zongshu.replace(",","")))
    total=int(input('需要下载的总数:'))
    print("\n开始下载\n")
    num=1
    i=0
    while num<total:   
        urls=getHTML(kw,i)[0]
        num=download(urls,num,kw)#括号里的num为上一次的num,等号左边的num为从下载函数中给图片编号完成后返回的num
        i+=30
        sleep(5)
    print('\n下载完毕')

main()
