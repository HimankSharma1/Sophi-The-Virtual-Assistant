from pytube import YouTube
import os
def GetVideo(resolution, formet):
    link=YouTube("https://www.youtube.com/watch?v=Bt6TmXqRCb4")

    if formet=='mp4':
        DownloadFile=link.streams.filter(resolution=resolution).first().download(output_path="D:\sophia data", filename_prefix=resolution)
    
    elif formet=="mp3":
        DownloadFile=link.streams.filter(only_audio=True).first().download(output_path="D:\sophia data")
        base = os.path.splitext(DownloadFile)
        newfile=f"{base[0]}.mp3"
        os.path.realpath(DownloadFile)
        os.rename(DownloadFile, newfile)
        
        
GetVideo('360p', 'mp3')  
