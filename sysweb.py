import time,psutil
from flask import Flask,redirect,send_file


HOST='localhost'
PORT=2000
DEBUG=False

app = Flask(__name__)



def sec2time(timee):
    return "{} days {} hours {} minutes {} seconds".format(str(int(timee / (24 * 3600))), str(int((timee / 3600) % 24)),str(int((timee / 60) % 60)), str(int(timee % 60)))
@app.route('/')
@app.route('/help/')
def help():
    a=['/help/','/sys/','/network/','/proc/','/recent_proc/','/time/','/add/2.0/3.0/','/top_mem/','/top_cpu/','/path/']
    b=''
    for i in a :
        b+='<a href="{0}">{0}</a><br>'.format(str(i))
    return (b)

@app.route('/time/',)
def timee():
    return (time.ctime())

@app.route('/add/<float:a>/<float:b>/')
def add(a,b):
    return (str(a+b))

@app.route('/proc/')
def processes():
    a=''
    a += "<b><u><i>Showing list of {} process: </i></u></b><br>".format(str(len(psutil.pids())))
    for i in psutil.pids():
        try:
            p = psutil.Process(i)
            a+='<b><a href="/proc/{0}/">{0}</a></b> --> {1} --><i> {2}</i> --> <b><i><a href="/kill/{0}/">KILL {1}</b></i></a><br>'.format(str(i), str(p.name()), str(p.cmdline()))
        except:
            a+="Not available --> " + str(i)+"<br>"
    return a

@app.route('/proc/<int:pid>/')
def det_proc(pid):
    a=''
    p=psutil.Process(pid)
    a+="<b><i>PID</i></b>--> "+str(pid)+'<br>'
    a+="<b>Command Line</b>--> "+str(p.cmdline())+'<br>'
    a += "<b>Process Name</b>--> " + str(p.name())+'<br>'
    #a += "<b>cpu num</b>--> " + str(p.cpu_num())+'<br>'
    a += "<b>Start time</b>--> " + str(time.ctime(p.create_time()))+'<br>'
    a += "<b>Running For</b>--> " + sec2time(time.time()-p.create_time()) + '<br>'
    a += "<b>Exe file</b>--> " + str(p.exe())+'<br>'
    a += "<b>User</b>--> " + str(p.username())+'<br>'
    a += "<b>Status</b>--> " + str(p.status())+'<br>'
    a += "<b>Connections</b>--> " + str(p.connections())+'<br>'
    a += "<b>Memory Percent</b>--> " + str(p.memory_percent()) + '<br>'
    a += "<b>CPU Percent</b>--> " + str(p.cpu_percent()) + '<br>'
    a += "<b>CWD</b>--> " + str(p.cwd())+'<br>'
    a += '<b><a href="/kill/'+str(pid)+'/">KILL IT</b><br>'
#    a += "<b>Terminal</b>--> " + str(p.terminal())+'<br>'
    return (a)

@app.route('/kill/<int:piid>/')
def killit(piid):
    pp=psutil.Process(piid)
    pp.kill()
    return (redirect('/proc/'))

@app.route('/network/')
def network():
    a=''
    for key in psutil.net_if_addrs().keys():
        a+='<b><i><a href="/network/'+str(key)+'/">'+key+":</a></b></i><br>"
        for i in range(len(psutil.net_if_addrs()[key])):
            sett=psutil.net_if_addrs()[key][i]
            a+="<i><u>{0}</u><br>Family: {1}<br>Address: {2}<br>Netmask: {3}<br>Broadcast: {4}<br>PTP: {5}<br></i><br>".format(str(i),str(sett[0]),str(sett[1]),str(sett[2]),str(sett[3]),str(sett[4]))
        a+="<u>Statistics of "+key+":</u><br>"
        a+=str(psutil.net_io_counters(pernic=True)[key])+'<br>'
        a+="<br>"
    return (a)

@app.route('/network/<path:key>/')
def net_key(key):
    a=""
    a += "<b><i>" + key + ":</b></i><br>"
    for i in range(len(psutil.net_if_addrs()[key])):
        sett = psutil.net_if_addrs()[key][i]
        a += "<i><u>{0}</u><br>Family: {1}<br>Address: {2}<br>Netmask: {3}<br>Broadcast: {4}<br>PTP: {5}<br></i><br>".format(
            str(i), str(sett[0]), str(sett[1]), str(sett[2]), str(sett[3]), str(sett[4]))
    a += "<u>Statistics of " + key + ":</u><br>"
    a += str(psutil.net_io_counters(pernic=True)[key]) + '<br>'
    a += "<br>"
    return (a)

@app.route('/top_mem/')
def topm():
    return (redirect('/top_mem/5'))
@app.route('/top_mem/<int:noo>/')
def top_mem(noo):
    pids=psutil.pids()
    topp=[]
    for pid in pids:
        try :
            p=psutil.Process(pid)
            topp.append({'pid':pid,'name':p.name(),'mem':p.memory_percent(),'command':p.cmdline(),'cpu':p.cpu_percent()})
        except :
            pass
    topp.sort(key=lambda i:i['mem'],reverse=True)
    a=''
    numm=0
    if len(topp) > noo :
        numm=noo
    else :
        numm=len(topp)
    a += "<b><u><i>Showing list of Top {} process with highest Memory percent:</i></u></b><br><br>".format(str(numm))
    for i in range(numm):
        m=topp[i]
        a += '<b><a href="/proc/{0}/">{0}</a></b> --> {1} --><b>{3}</b>--><i> {2}</i> --> <b><i><a href="/kill/{0}/">KILL {1}</b></i></a><br>'.format(str(m['pid']),str(m['name']),str(m['command']),str(m['mem']))
    return (a)

@app.route('/top_cpu/')
def topc():
    return (redirect('/top_cpu/5'))

@app.route('/top_cpu/<int:noo>/')
def top_cpu(noo):
    pids=psutil.pids()
    topp=[]
    for pid in pids:
        try :
            p=psutil.Process(pid)
            topp.append({'pid':pid,'name':p.name(),'mem':p.memory_percent(),'command':p.cmdline(),'cpu':p.cpu_percent()})
        except :
            pass
    topp.sort(key=lambda i:i['cpu'],reverse=True)
    a=''
    numm = 0
    if len(topp) > noo:
        numm = noo
    else:
        numm = len(topp)
    a+="<b><u><i>Showing list of Top {} process with highest cpu percent:</i></u></b><br><br>".format(str(numm))
    for i in range(numm):
        m=topp[i]
        a += '<b><a href="/proc/{0}/">{0}</a></b> --> {1} --><b>{3}</b>--><i> {2}</i> --> <b><i><a href="/kill/{0}/">KILL {1}</b></i></a><br>'.format(str(m['pid']),str(m['name']),str(m['command']),str(m['cpu']))
    return (a)

from socket import gethostname
from collections import OrderedDict
import platform

@app.route('/sys/')
def sysinfo():
    dik=OrderedDict()
    dik['Host Name'] = gethostname()
    dik['Last Boot']=time.ctime(psutil.boot_time())
    dik['Time Now']=time.ctime(time.time())
    up= time.time() - psutil.boot_time()
    dik['Uptime']="{} days {} hours {} minutes {} seconds<br>".format(str(int(up/(24*3600))),str(int((up/3600)%24)),str(int((up/60)%60)),str(int(up%60)))
    dik['OS']=platform.uname()[0]
    dik['Release']=platform.uname()[2]
    dik['Version'] = platform.uname()[3]
    dik['Machine Type'] = platform.uname()[4]
    dik['Processor Info'] = platform.uname()[5]
    dik['Linux Disrtibution if it is Linux']=platform.dist()

    a=''
    a+='<h1><b><u><i>System Informations:</h1></b></u></i><br><br>'
    for key in dik.keys():
        a+="<b><i> {0} </b></i>--> {1}<br>".format(str(key),str(dik[key]))
    return a


@app.route('/recent_proc/')
def recent_proc_m():
    return (redirect('/recent_proc/5'))

@app.route('/recent_proc/<int:noo>/')
def recent_proc(noo):
    pids=psutil.pids()
    topp=[]
    time_now=time.time()
    upfor=0
    for pid in pids:
        try :
            p=psutil.Process(pid)
            upfor=time_now - p.create_time()
            topp.append({'pid':pid,'name':p.name(),'command':p.cmdline(),'upfor':upfor})
        except :
            pass
    topp.sort(key=lambda i:i['upfor'],reverse=False)
    a=''
    numm = 0
    if len(topp) > noo:
        numm = noo
    else:
        numm = len(topp)
    a+="<b><u><i>Showing list of Recent {} process :</i></u></b><br><br>".format(str(numm))
    for i in range(numm):
        m=topp[i]
        a += '<b><a href="/proc/{0}/">{0}</a></b> --> {1} --><b>{3}</b>--><i> {2}</i> --> <b><i><a href="/kill/{0}/">KILL {1}</b></i></a><br>'.format(str(m['pid']),str(m['name']),str(m['command']),str(sec2time(m['upfor'])))
    return (a)

import os

@app.route('/path/')
def patt():
    return (redirect("/path/"+os.path.abspath(os.path.curdir)))

@app.route('/path/<path:lis>')
def pathh(lis):
    way=lis.replace('/',os.path.sep)
    if os.path.isfile(way)== True:
        return send_file(way,as_attachment=True)
        #f=open(way,'rb')
        #msg=f.read()
        #f.close()
    else:
        a=''
        a+='<i><b><u>Listing Directory: {}</i></b></u><br><br>'.format(str(way))
        type = ''
        try:
            ll=os.listdir(way)
            ll.append('..')
            for i in ll :
                ma=os.path.abspath(os.path.join(way,i))
                if os.path.isdir(ma) == True:
                    type = 'Directory'
                else :
                    type = 'File'
                try:
                    a+='{} --> <b><a href="/path/{}">{}</a><b> --> Size: {} -->Creation: {} --> Last access: {}<br>'.format(str(type),str(ma),str(i),str(os.path.getsize(ma)),str(time.ctime(os.path.getctime(ma))),str(time.ctime(os.path.getatime(ma))))
                except :
                    print ma+" Cant be shoWn in webpage...."
                    pass
        except :
            a+="<b>Not available {}</b>".format(str(way))
    return (a)


@app.errorhandler(404)
def notfound(e):
    return "<h1>Not a valid url... Please double check it!!!</h1>"

@app.errorhandler(500)
def notfound(e):
    return "<h1>OOPS!!! You can't check this or Not available !!!!Please double check the url or nevigate again!! </h1>"


if __name__ == '__main__':
   app.run(host=HOST,port=PORT,debug=DEBUG)
