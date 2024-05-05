import pyttsx3

engine = pyttsx3.init()

def say(contents:str,echo=False):
    '''
    朗读字符串
    :param contents: 待朗读的字符串
    :param echo: 是否打印出字符串
    :return: 无
    '''
    engine.say(contents)
    if echo: print(contents)
    engine.runAndWait()

def str_to_mp3(contents:str,filename='pet.mp3',echo=True):
    '''
    字符串转 mp3 文件
    :param contents: 字符串
    :param filename: mp3文件名
    :return: 无
    '''
    engine.save_to_file(contents, filename)
    engine.runAndWait()
    result=f'{contents} is converted to mp3 file in {filename} !!'
    if echo: print(result)
    return  result

def txtfile_to_mp3(txtfile:str):
    '''
    文本文件转mp3
    :param txtfile:文本文件
    :return: 与文本文件同名的mp3 文件
    '''
    try:
        txt=open(txtfile,encoding='utf-8').read()
    except:
        txt=open(txtfile,encoding='gbk').read()

    filename=txtfile.split('.')[0]+'.mp3'
    return  str_to_mp3(txt,filename)

def split_mp3(mp3file,start_h=0,start_m=0,start_s=0,end_h=0,end_m=0,end_s=0):
    from pydub import AudioSegment
    sound=AudioSegment.from_mp3(mp3file)
    start_frame=(start_h*60*60+start_m*60+start_s)*1000
    end_frame=(end_h*60*60+end_m*60+end_s)*1000
    sound_clip = sound[start_frame:end_frame]
    sound_clip.export(mp3file.split('.')[0]+'_splited.mp3',format="mp3")
    return sound_clip

def concat_mp3file(file_list):
    from pydub import AudioSegment
    sounds=[AudioSegment.from_mp3(i) for i in file_list]
    from functools import reduce
    sound=reduce(lambda x,y: x+y, sounds)
    #sound=sum(sounds,[])
    sound.export('combined.mp3', format="mp3")

def overlay_mp3file(f1,f2):
    from pydub import AudioSegment
    sounds = [AudioSegment.from_mp3(i) for i in [f1,f2]]
    sound=sounds[0].overlay(sounds[1])
    sound.export('overlay.mp3', format="mp3")


if __name__ == '__main__':
    say('欢迎进入Python世界！！欢迎使用 Python Education Tools！ok.mp3')
    #file2mp3(('ejkg.txt'))
    #combine_mp3file(['d:/1.mp3','d:/2.mp3'])
    #overlay_mp3file('d:/1.mp3','d:/2.mp3')

