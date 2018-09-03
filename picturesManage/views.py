from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from PIL import Image
from picturesManage.models import Pictures
import time,os
from django.core.paginator import Paginator
from _datetime import datetime
# Create your views here.

def index(request):
    '''
    首页
    :return:
    '''
    return render(request,"index.html")

def pictureslist(request,pageNum,pageTotal):
    '''
    图片列表
    :param request:
    :return:
    '''
    pics = Pictures.objects.all()
    if pageNum == "" or pageNum is None:
        pageNum = "1"
    if pageTotal == '' or pageTotal is None:
        pageTotal = "10"
    pageList = Paginator(pics, int(pageTotal))
    currentPlist = pageList.page(int(pageNum))
    pageRange = pageList.page_range
    context = {"currentPlist":currentPlist,"pageRange":pageRange,"pageNum":pageNum}

    return render(request,"pictures.html",context)

def addpicture(request):
    '''
    添加页面
    :param request:
    :return:
    '''
    return render(request,"add.html")

def submitpicture(request):
    '''
    提交添加
    :param request:
    :return:
    '''
    context = savePic(request,None)
    return render(request,'result.html',context)

def editpicture(request):
    '''
    编辑页面
    :param request:
    :return:
    '''
    #删除原来的图片
    pid = request.POST["pid"]
    picture = Pictures.objects.get(id=pid)
    pUrl = picture.p_url
    thumb = picture.thumb_p_url

    context = savePic(request,pid)
    resultValue = context.get("resultValue")
    if resultValue == 1:
        if os.path.exists("./static/" + pUrl):
            os.remove("./static/" + pUrl)
        if os.path.exists("./static/" + thumb):
            os.remove("./static/" + thumb)
    return render(request,"result.html",context)

def editshow(request,pid):
    '''
    编辑页面
    :param request:
    :return:
    '''
    return render(request,"edit.html",{"pid":pid})

def editajax(request,pid):
    '''
    编辑页面ajax请求数据
    :param request:
    :return:
    '''
    pic = Pictures.objects.get(id=pid)
    print(pic)
    list = []
    list.append({"id":pic.id,"title":pic.title,"p_url":pic.p_url,"thumb_p_url":pic.thumb_p_url,"addtime":pic.addtime})
    return JsonResponse({"data":list})

def detelpicture(request,pid):
    '''
    删除图片
    :param request:
    :return:
    '''
    try:
        pic = Pictures.objects.get(id=pid)
        p_url = pic.p_url
        thumb_p_url = pic.thumb_p_url
        pic.delete()

        if os.path.exists("./static/" + p_url):
            os.remove("./static/" + p_url)
        if os.path.exists("./static/" + thumb_p_url):
            os.remove("./static/" + thumb_p_url)
        context = {"resultValue":1}
    except Exception as err:
        print(err)
        context = {"resultValue": 0}
    return render(request,"result.html",context)


def savePic(request,pid):
    '''
    保存图片及信息
    :param request:
    :param pid:
    :return:
    '''

    # 获取并保存图片
    try:
        picture = request.FILES.get("picture", None)
        if picture is None:
            return render(request, "result.html", {'resultValue': 0})
        fileName = str(time.time()) + "." + picture.name.split(".").pop()
        destination = open("./static/pics/" + fileName, "wb")
        for chunk in picture.chunks():
            destination.write(chunk)
        destination.close()
        p_url = "pics/" + fileName

        # 生成并保存缩略图
        im = Image.open("./static/pics/" + fileName)
        im.thumbnail((75, 75))
        thumb_p_url = "pics/s_" + fileName
        im.save("./static/" + thumb_p_url, None)

        # 保存图片及缩略图
        title = request.POST["title"]
        pic = Pictures()
        # 编辑
        if pid is not None:
            pic = Pictures.objects.get(id=pid)
            pic.addtime = datetime.now()
        pic.title = title
        pic.p_url = p_url
        pic.thumb_p_url = thumb_p_url

        pic.save()
        context = {"resultValue": 1}
    except Exception as err:
        print(err)
        context = {"resultValue": 0}
    return context