import telebot,os

API_TOKEN="api-token"
Firstname="First Name"
Lastname="Last Name"

bot = telebot.TeleBot(API_TOKEN)



def user_permit(func):
    def outburst(msg):
        if msg.from_user.first_name == Firstname and msg.from_user.last_name == Lastname :
            func(msg)
        else :
            bot.reply_to(msg,"You are abandoned")
    return outburst




@bot.message_handler(commands=['start','help'])
@user_permit
def welcome(msg):
    msgg='''
    /cwd --> Return Current directory
/back --> go to parent directory
/list_all --> List all files and directories
/list_dir --> List only directories
/list_files --> List File
/list_ext_<.ext> --> List all the files containing .ext extention
/goto_<directory> --> Go to a specific directory
/new_dir_<name> --> Create a new directory
/rename <old>#<new> --> Remane a file and folder
/rm_dir_<dir> --> Remove a directory if it is empty
/rm_file_<filename> --> Remove a file
/clean_<directory> --> Full Delete the directory
/get_<filename> --> Get a file from computer
/size_<filename> --> Get size
    '''
    bot.reply_to(msg,msgg)
    bot.reply_to(msg,"Easy Tools:\n /show_dirs,/show_files,/show_detail,/back,/cwd")

@bot.message_handler(commands='cwd')
@user_permit
def cur_dir(msg):
    curdir=os.path.abspath(os.curdir)
#    print msg
    bot.reply_to(msg,curdir)

@bot.message_handler(commands='back')
@user_permit
def backk(msg):
    os.chdir('..')
    curdir = os.path.abspath(os.curdir)
    bot.reply_to(msg,curdir)


@bot.message_handler(regexp='get_*')
@user_permit
def gett(msg):
    filee=str(msg.text[5:]).strip(' ')
    try :
        if os.path.exists(filee) and os.path.isfile(filee) :
            if int(os.path.getsize(filee)) <= 10*1024*1024 :
                f=open(filee,'rb')
                bot.send_document(msg.chat.id,f,msg.message_id)
                f.close()
            else :
                bot.reply_to(msg, "File size is too big: {} Size: {} bytes".format(filee,str(int(os.path.getsize(filee)))))
        else :
            bot.reply_to(msg, "Either does not exist or a folder " + filee)
    except os.error as err :
        bot.reply_to(msg,'OOps Something worng: '+str(err))
    except :
        bot.reply_to(msg, 'OOps Something worng:')

@bot.message_handler(regexp='goto_*')
@user_permit
def goto(msg):
    try:
        dirr=str(msg.text[6:]).strip(' ')
        if os.path.exists(dirr) and os.path.isdir(dirr):
            os.chdir(dirr)
            curdir = os.path.abspath(os.curdir)
            bot.reply_to(msg, curdir)
        else :
            bot.reply_to(msg, "Either does not exist or a file " + dirr)
    except os.error as err:
        bot.reply_to(msg, 'OOps Something worng: ' + str(err))
    except :
        bot.reply_to(msg, 'OOps Something worng:')


@bot.message_handler(regexp='list_*')
@user_permit
def listing(msg):
    try:
        type=str(msg.text[6:]).strip(' ').lower()
        rep=''
        if type =='all':
            rep='Listing Everything:\n'
            files=os.listdir(os.curdir)
            for f in files :
                if os.path.isdir(f):
                    rep +='D) '+ str(f) +'--> /goto_'+str(f)+" \n"
                elif os.path.isfile(f):
                    rep +='F) '+ str(f) + '--> /get_' + str(f) + " \n"
                else :
                    rep +='U) '+ str(f) + '--> Not a file or directory' + " \n"
           # print rep.decode(errors='ignore')
            bot.reply_to(msg,rep.decode(errors='ignore'))
        elif type == 'dir' :
            rep='Listing Directories:\n'
            files = os.listdir(os.curdir)
            for f in files:
                if os.path.isdir(f):
                    rep +='D) '+ str(f) +'--> /goto_'+str(f)+" \n"
            bot.reply_to(msg, rep.decode(errors='ignore'))
        elif type == 'files' :
            rep='Listing Files:\n'
            files = os.listdir(os.curdir)
            for f in files:
                if os.path.isfile(f):
                    rep +='F) '+ str(f) +'--> /get_'+str(f)+" \n"
            bot.reply_to(msg, rep.decode(errors='ignore'))
        elif type[:3] == 'ext':
            rep = 'Listing Extentions:\n'
            files = os.listdir(os.curdir)
            for f in files:
                if os.path.splitext(f)[1] == type[4:] :
                    rep +='F) '+ str(f) + '--> /get_' + str(f) + " \n"
            bot.reply_to(msg, rep.decode(errors='ignore'))
        else :
            bot.reply_to(msg,"/list_all , /list_files, /list_dir, /list_ext_<.ext>")
    except os.error as err:
        bot.reply_to(msg,'Something Wrong '+str(err))
    except :
        type = str(msg.text[6:]).strip(' ').lower()
        rep = ''
        if type == 'all':
            rep = 'Listing Everything:\n'
            files = os.listdir(os.curdir)
            for f in files:
                if os.path.isdir(f):
                    rep += 'D) ' + str(f)  + " \n"
                elif os.path.isfile(f):
                    rep += 'F) ' + str(f)  + " \n"
                else:
                    rep += 'U) ' + str(f) + " \n"
           # print rep.decode(errors='ignore')
            bot.reply_to(msg, rep.decode(errors='ignore'))
        elif type == 'dir':
            rep = 'Listing Directories:\n'
            files = os.listdir(os.curdir)
            for f in files:
                if os.path.isdir(f):
                    rep += 'D) ' + str(f)  + " \n"
            bot.reply_to(msg, rep.decode(errors='ignore'))
        elif type == 'files':
            rep = 'Listing Files:\n'
            files = os.listdir(os.curdir)
            for f in files:
                if os.path.isfile(f):
                    rep += 'F) ' + str(f)  + " \n"
            bot.reply_to(msg, rep.decode(errors='ignore'))
        elif type[:3] == 'ext':
            rep = 'Listing Extentions:\n'
            files = os.listdir(os.curdir)
            for f in files:
                if os.path.splitext(f)[1] == type[4:]:
                    rep += 'F) ' + str(f)  + " \n"
            bot.reply_to(msg, rep.decode(errors='ignore'))
        else:
            bot.reply_to(msg, "/list_all , /list_files, /list_dir, /list_ext_<.ext>")

@bot.message_handler(regexp='new_dir_*')
@user_permit
def create_dir(msg):
    try :
        dirname=str(msg.text[9:])
        os.makedirs(dirname)
        bot.reply_to(msg,"Directory Created: "+dirname)
    except os.error as err:
        bot.reply_to(msg,'Something Wrong '+str(err))
    except :
        bot.reply_to(msg, 'Something Wrong Check the command')

@bot.message_handler(regexp='rename *')
@user_permit
def rename_dir(msg):
    try :
        old,new=str(msg.text[8:]).split('#')[:2]
        os.renames(old,new)
        bot.reply_to(msg,"Renamed From {} to {}:".format(old,new))
    except os.error as err:
        bot.reply_to(msg,'Something Wrong '+str(err))
    except :
        bot.reply_to(msg, 'Something Wrong Check the command')



@bot.message_handler(regexp='rm_dir_*')
@user_permit
def remove_directory(msg):
    try:
        dir_name=str(msg.text[8:])
        os.removedirs(dir_name)
        bot.reply_to(msg,"Directory Removed: "+dir_name)
    except os.error as err:
        bot.reply_to(msg,'Something Wrong '+str(err))
    except :
        bot.reply_to(msg, 'Something Wrong Check the command')

@bot.message_handler(regexp='rm_file_*')
@user_permit
def remove_file(msg):
    try:
        dir_namee=str(msg.text[9:])
        os.remove(dir_namee)
        bot.reply_to(msg,"File Removed: "+dir_namee)
    except os.error as err:
        bot.reply_to(msg,'Something Wrong '+str(err))
    except :
        bot.reply_to(msg, 'Something Wrong Check the command')

@bot.message_handler(regexp='clean_*')
@user_permit
def clean(msg):
    try:
        dir_namee=str(msg.text[7:])
        import shutil
        shutil.rmtree(dir_namee)
        bot.reply_to(msg,"Dir Cleaned: "+dir_namee)
    except os.error as err:
        bot.reply_to(msg,'Something Wrong '+str(err))
    except :
        bot.reply_to(msg, 'Something Wrong Check the command')


import urllib2,time
@bot.message_handler(content_types=['document','audio','video','voice','photo'])
@user_permit
def putt(msg):
    try:
        typee=msg.content_type
        global file_id
        global namee
        if typee == 'document':
            file_id=msg.document.file_id
            namee=msg.document.file_name
        elif typee== 'audio' :
            file_id=msg.audio.file_id
            namee=msg.audio.title
        elif typee== 'video' :
            file_id=msg.video.file_id
            namee='Video_Record_{0:0>2}{1:0>2}{2:0>2}{3:0>2}{4:0>2}{5:0>2}'.format(str(time.gmtime().tm_year),str(time.gmtime().tm_mon),str(time.gmtime().tm_mday),str(time.gmtime().tm_hour),str(time.gmtime().tm_min),str(time.gmtime().tm_sec))
        elif typee== 'voice' :
            file_id=msg.voice.file_id
            namee='Voice_Record_{0:0>2}{1:0>2}{2:0>2}{3:0>2}{4:0>2}{5:0>2}'.format(str(time.gmtime().tm_year),str(time.gmtime().tm_mon),str(time.gmtime().tm_mday),str(time.gmtime().tm_hour),str(time.gmtime().tm_min),str(time.gmtime().tm_sec))
        elif typee== 'photo' :
            file_id=msg.photo[len(msg.photo)-1].file_id
            namee=None
        else :
            file_id=msg.decument.file_id

        file_info=bot.get_file(file_id)
        fileee=urllib2.urlopen('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
        if namee==None :
            namee=file_info.file_path.split('/')[-1]
        elif typee != 'document' :
            extt=file_info.file_path.split('/')[-1].split('.')[-1]
            namee += '.'+extt
        else :
            pass

        if not os.path.exists(namee):
            g=open(namee,'wb')
            data = fileee.read()
            g.write(data)
            g.close()
            bot.reply_to(msg,"File Saved... "+namee)
        else :
            bot.reply_to(msg,'File already exist: '+namee)

    except os.error as err :
        bot.reply_to(msg, 'Something Wrong ' + str(err))
    except :
        bot.reply_to(msg, 'Something Wrong try to send again')





@bot.message_handler(regexp='size_*')
@user_permit
def get_detail(msg):
    filename=str(msg.text[6:]).strip(' ')
    try :
        sizee=os.path.getsize(filename)
        bot.reply_to(msg,"Size of {} is {} byte.".format(filename,str(sizee)))
    except os.error as err :
        bot.reply_to(msg,"Oops !! Something wrong "+str(err))
    except :
        bot.reply_to(msg, "Oops !! Something wrong ..")

@bot.message_handler(commands='show_dirs')
@user_permit
def goto_keyboard(msg):
    mrk=telebot.types.ReplyKeyboardMarkup()
    mrk.add('/back')
    listt=os.listdir('.')
    for i in listt :
        if os.path.isdir(i) :
            mrk.add('/goto_'+str(i).decode(errors='ignore'))
    bot.reply_to(msg,'Choose Where to go?',reply_markup=mrk)

@bot.message_handler(commands='show_files')
@user_permit
def get_keyboard(msg):
    mrkk=telebot.types.ReplyKeyboardMarkup()
    listt=os.listdir('.')
    mrkk.add('/back')
    for i in listt :
        if os.path.isfile(i) :
            mrkk.add('/get_'+str(i).decode(errors='ignore'))
    bot.reply_to(msg,'Choose What to get?',reply_markup=mrkk)

@bot.message_handler(commands='show_detail')
@user_permit
def size_keyboard(msg):
    mrkk=telebot.types.ReplyKeyboardMarkup()
    mrkk.add('/back')
    listt=os.listdir('.')
    for i in listt :
        if os.path.isfile(i) :
            mrkk.add('/size_'+str(i).decode(errors='ignore'))
    bot.reply_to(msg,'Choose file to get size?',reply_markup=mrkk)



@bot.message_handler(regexp='test *')
@user_permit
def test(msg):
    no=int(msg.text[6:])
    print(no)
    rep=''
    for i in range(1,no+1):
        rep += str(i)+'\n'
    bot.reply_to(msg,rep)

try :
    bot.polling()
except :
    bot.polling()
