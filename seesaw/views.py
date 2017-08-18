from django.shortcuts import render
from django.shortcuts import HttpResponse
from seesaw import  models
from dss.Serializer import serializer
import json
import os
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from django.core import serializers

access_key = '93L43E91oA1cbC9k40ZK2eSeOCqxxjJz1SsL4NGv'
secret_key = '2nALux7vEJkrcuH0ZOWUhW2bI6vIvvtqpysS71aH'

#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'seesaw-image'


def index(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        usremail = request.POST.get("email", None)
        usrpassword = request.POST.get("password", None)
        #temp = {"user": username,"email": email,"password": password}
        #user_list.append(temp)
        models.teacher.objects.create(name=username,email=usremail,password=usrpassword)
    user_list = models.teacher.objects.all() 
    return render(request, "index.html",{"data":user_list})

def checkPassWord(request):
    if request.method == "GET":
        usremail = request.GET['email']
        usrpassword = request.GET['password']
    #print(usremail,usrpassword)
    model = models.teacher.objects.get(email=usremail,password=usrpassword)
    name = model.name
    return HttpResponse(name)
def deleteAll(request):
    models.teacher.objects.all().delete()
    return HttpResponse("deleteall")

def createCourse(request):
    if request.method == "POST":
        usremail = request.POST.get("email",None)
        getCourseName = request.POST.get("courseName",None)
        getGrade = request.POST.get("grade",None)
        getTime = request.POST.get("time",None)
        getGroup = request.POST.get("group_num",None)
        getcourse = models.course.objects.create(name=getCourseName,grade=getGrade,time=getTime,group_num=getGroup)
        getteacher = models.teacher.objects.get(email = usremail)
        newTeaches = models.teaches.objects.create(teacher=getteacher,course=getcourse) 
    for i in range(int(getGroup)):
        newGroup = models.group.objects.create(course=getcourse)
    course_list = models.course.objects.all()
    teaches_name = models.teaches.objects.filter(teacher=getteacher)
    jsoncourse = serializer(getcourse,output_type='json')
    return HttpResponse(jsoncourse)

def getCourse(request):
    teaches_course_name = ""
    course_name = ""
    if request.method == "GET":
        usremail = request.GET["email"]
        getteacher = models.teacher.objects.get(email=usremail)
    teaches_list = models.teaches.objects.filter(teacher=getteacher)
    for var in teaches_list:
        course_name += var.course.name + "  " + var.course.grade + ","
    teaches_course_name = course_name
    return HttpResponse(teaches_course_name)

def getCourseID(request):
    teaches_course_id = ""
    course_id = ""
    if request.method == "GET":
        usremail = request.GET["email"]
        getteacher = models.teacher.objects.get(email=usremail)
    teaches_list = models.teaches.objects.filter(teacher=getteacher)
    for var in teaches_list:
        course_id += str(var.course.id) + " "
    teaches_course_id = course_id
    return HttpResponse(teaches_course_id)
    

def uploadImg(request):
    if request.method == 'POST':
        usremail = request.POST.get("email",None)
        usrcourseid = request.POST.get("courseid",None)
        getimg = request.POST.get('img_path',None)
        getcreatetime = request.POST.get('create_time',None)
        getcontent = request.POST.get("content",None)
#    getteacher = models.teacher.objects.get(email=usremail)
    getcourse = models.course.objects.get(id=usrcourseid)
    getteaches = models.teaches.objects.get(course=getcourse)
    newimg = models.T_Img_Item.objects.create(teaches=getteaches,img_path=getimg,create_time=getcreatetime,content=getcontent)
    
    return HttpResponse(newimg.img_path)

def uploadStImg(request):
    if request.method == 'POST':
        usremail = request.POST.get("email",None)
        usrcourseid = request.POST.get("courseid",None)
        getimg  = request.POST.get("img_path",None)
        getcreatetime = request.POST.get("create_time",None)
        getcontent = request.POST.get("content",None)
    getstudent = models.student.objects.get(email=usremail)
    getcourse = models.course.objects.get(id=usrcourseid)
    newitem = models.S_Img_Item.objects.create(student=getstudent,course=getcourse,img_path=getimg,create_time=getcreatetime,content=getcontent)

    return HttpResponse(newitem.img_path)



def getImg(request):
    imgsfile = []
    if request.method == 'GET':
        usrcourseid = request.GET["courseid"]
    getcourse = models.course.objects.get(id=usrcourseid)
    getteaches = models.teaches.objects.get(course=getcourse)
    getimgs = models.T_Img_Item.objects.filter(teaches=getteaches)
    getstimgs = models.S_Img_Item.objects.filter(course=getcourse)
    imgs = serializer(getimgs, output_type='json')
    for var in getimgs:
        imgsfile.append(var.img_path)
    for var in getstimgs:
        imgsfile.append(var.img_path)
    jsonimgsfiles = serializer(imgsfile,output_type='json')
    return HttpResponse(jsonimgsfiles)


def getItemContent(request):
    imgsfile = []
    if request.method == 'GET':
        usrcourseid = request.GET["courseid"]
    getcourse = models.course.objects.get(id=usrcourseid)
    getteaches = models.teaches.objects.get(course=getcourse)
    getimgs = models.T_Img_Item.objects.filter(teaches=getteaches)
    getstimgs = models.S_Img_Item.objects.filter(course=getcourse)
    imgs = serializer(getimgs, output_type='json')
    for var in getimgs:
        imgsfile.append(var.content)
    for var in getstimgs:
        imgsfile.append(var.content)
    jsonimgsfiles = serializer(imgsfile,output_type='json')
    return HttpResponse(jsonimgsfiles)

def getImgCreateTime(request):
    imgsfile = []
    if request.method == 'GET':
        usrcourseid = request.GET["courseid"]
    getcourse = models.course.objects.get(id=usrcourseid)
    getteaches = models.teaches.objects.get(course=getcourse)
    getimgs = models.T_Img_Item.objects.filter(teaches=getteaches)
    getstimgs = models.S_Img_Item.objects.filter(course=getcourse)
    imgs = serializer(getimgs, output_type='json')
    for var in getimgs:
        imgsfile.append(var.create_time)
    for var in getstimgs:
        imgsfile.append(var.create_time)
    jsonimgsfiles = serializer(imgsfile,output_type='json')
    return HttpResponse(jsonimgsfiles)


def getImgOwner(request):
    imgsfile = []
    if request.method == 'GET':
#        usremail = request.GET["email"]
        usrcourseid = request.GET["courseid"]
#    getteacher = models.Teacher.objects.get(email=usremail)
    getcourse = models.course.objects.get(id=usrcourseid)
    getteaches = models.teaches.objects.get(course=getcourse)
    getimgs = models.T_Img_Item.objects.filter(teaches=getteaches)
    getstimgs = models.S_Img_Item.objects.filter(course=getcourse)
    imgs = serializer(getimgs,datetime_format='string', output_type='json')
    for var in getimgs:
        imgsfile.append(var.teaches.teacher.name)
    for var in getstimgs:
        imgsfile.append(var.student.name)
    jsonimgsfiles = serializer(imgsfile,output_type='json')
    return HttpResponse(jsonimgsfiles)
def createStudentAccount(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        usremail = request.POST.get("email", None)
        usrpassword = request.POST.get("password", None)
        usrcode = request.POST.get("code", None)
    newstudent = models.student.objects.create(name=username,email=usremail,password=usrpassword)
    getcourse = models.course.objects.get(id=usrcode)
    newtakes = models.takes.objects.create(student=newstudent,course=getcourse)
    newungroupmember = models.un_group_member.objects.create(student=newstudent,course=getcourse)
    return HttpResponse(newstudent.name)

def checkStudentPassword(request):
    if request.method == "GET":
        usremail = request.GET['email']
        usrpassword = request.GET['password']
    #print(usremail,usrpassword)
    model = models.student.objects.get(email=usremail,password=usrpassword)
    name = model.name
    return HttpResponse(name)

def checkCourseCode(request):
    if request.method == 'GET':
        coursecode = request.GET['code']
    coursemodel = models.course.objects.get(id=coursecode)
    name = coursemodel.name
    return HttpResponse(name)

def getTakes(request):
    if request.method == 'GET':
        getemail = request.GET['email']
    getstudent = models.student.objects.get(email=getemail)
    #getcourse = models.Course.objects.get(id=getcourseid)
    gettakes = models.takes.objects.filter(student=getstudent)
    structtakes = []
   
    for var in gettakes:
        temptake = {}
        temptake['course_id'] = var.course_id
        temptake['course_name'] = var.course.name + "  " + var.course.grade
        print(temptake)
        structtakes.append(temptake)
    jsontakes = serializer(structtakes,output_type='json') 
    return HttpResponse(jsontakes)

def getCourseGroup(request):
    if request.method == 'GET':
        getcourseid = request.GET['courseid']
    getcourse = models.course.objects.get(id=getcourseid)
    getgroups = models.group.objects.filter(course=getcourse)
    groupstruct  = []
    for var in getgroups:
        tempgroup = {}
        tempgroup['pk'] = var.id
        gethomeworks = models.homework.objects.filter(group=var)
        homeworknum = len(gethomeworks)
        tempgroup['work_num'] = homeworknum
        groupstruct.append(tempgroup)
    jsongroup = serializer(groupstruct,output_type='json')
    return HttpResponse(jsongroup)

def getGroupMemberName(request):
    if request.method == 'GET':
        getgroupid = request.GET['groupid']
    getgroup = models.group.objects.get(id=getgroupid)
    getgroupmember = models.group_member.objects.filter(group=getgroup)

    getgroupnames = []
    for var in getgroupmember:
        getgroupnames.append(var.student)
    jsonnames = serializer(getgroupnames,output_type='json')
    return HttpResponse(serializers.serialize('json', getgroupnames), content_type="application/json")
def getGroupMemberEmail(request):
    if request.method == 'GET':
        getgroupid = request.GET['groupid']
    getgroup = models.group.objects.get(id=getgroupid)
    getgroupmember = models.group_member.objects.filter(group=getgroup)
    getgroupemails = []
    for var in getgroupmember:
        getgroupemails.append(var.student.email)
    jsonemails = serializer(getgroupemails,output_type='json')
    return HttpResponse(jsonemails)
def getUnGroupMemberName(request):
    if request.method == 'GET':
        getcourseid = request.GET['courseid']
    getcourse = models.course.objects.get(id=getcourseid)
    getungroup = models.un_group_member.objects.filter(course=getcourse)
    getungroupname = []
    for var in getungroup:
        getungroupname.append(var.student.name)
    jsonname = serializer(getungroupname,output_type='json')
    return HttpResponse(jsonname)

def getUnGroupMemberEmail(request):
    if request.method == 'GET':
        getcourseid = request.GET['courseid']
    getcourse = models.course.objects.get(id=getcourseid)
    getungroup = models.un_group_member.objects.filter(course=getcourse)
    getungroupemail = []
    for var in getungroup:
        getungroupemail.append(var.student.email)
    jsonemail = serializer(getungroupemail,output_type='json')
    return HttpResponse(jsonemail)

def uploadSelectedEmail(request):
    if request.method == 'POST':
        getemails = request.POST.get("emails",None)
        getgroupid = request.POST.get("groupid",None)
    emaillist = getemails.split(',')
    for var in emaillist:
        getstudent = models.student.objects.get(email=var)
        getgroup = models.group.objects.get(id=getgroupid)
        newmember = models.group_member.objects.create(group=getgroup,student=getstudent)
        models.un_group_member.objects.get(student=getstudent).delete()
    return HttpResponse("DONE")
def getSectionNum(request):
    if request.method == 'GET':
        getcourseid = request.GET["courseid"]
    getcourse = models.course.objects.get(id=getcourseid)
    getsections = models.section.objects.filter(course=getcourse)
    weekTime = getcourse.time
    num=0
    for var in getsections:
        num+=1
    return HttpResponse(num)


def getCourseMsg(request):
    if request.method == 'GET':
        getcourseid = request.GET["courseid"]
    getcourse = models.course.objects.get(id=getcourseid)
    jsoncourse = serializer(getcourse,output_type='json')
    desired_format = '%Y-%m-%d-%H-%M'
    strdate = getcourse.create_time.strftime(desired_format)
    getweektime = getcourse.time
    strdate += ","
    strdate += getweektime 
    return HttpResponse(strdate)

def uploadSection(request):
    if request.method == 'GET':
        getcourseid = request.GET["courseid"]
        getcontent = request.GET["content"]
        gethomeworkddl = request.GET["enddate"]
        getcreatetime = request.GET["startDate"]
    getcourse = models.course.objects.get(id=getcourseid)
    newsection = models.section.objects.create(course=getcourse,content=getcontent,homework_ddl=gethomeworkddl,create_time=getcreatetime)
    jsonsection = serializer(newsection,output_type='json')
    return HttpResponse(jsonsection)

def getSections(request):
    if request.method == 'GET':
        getcourseid = request.GET["courseid"]
    getcourse = models.course.objects.get(id=getcourseid)
    sections = models.section.objects.filter(course=getcourse)
    jsonsections = serializer(sections,output_type='json')
    return HttpResponse(jsonsections)

def getGroupNum(request):
    if request.method == 'GET':
        getcourseid = request.GET["courseid"]
    getcourse = models.course.objects.get(id=getcourseid)
    getgroupnum = getcourse.group_num
    return HttpResponse(getgroupnum)

def uploadHomework(request):
    if request.method == 'GET':
        getemail = request.GET["email"]
        getsectionid = request.GET["sectionid"]
        getcontent = request.GET["content"]
        getimgpath = request.GET["imgpath"]
        getgroupid = request.GET["groupid"]
        getcreatetime = request.GET["create_time"]
    getuser = models.student.objects.get(email=getemail)
    getsection = models.section.objects.get(id=getsectionid)
    getgroup = models.group.objects.get(id=getgroupid)
    newhomework = models.homework.objects.create(student=getuser,section=getsection,content=getcontent,img_path=getimgpath,group=getgroup,create_time=getcreatetime)
    jsonhomework = serializer(newhomework,output_type='json')
    return HttpResponse(jsonhomework)

def getGroupID(request):
    if request.method == 'GET':
        getemail = request.GET["email"]
    getstudent = models.student.objects.get(email=getemail)
    getgroupmember = models.group_member.objects.get(student=getstudent)
    return HttpResponse(getgroupmember.group.id)

def getHomeworkByGroup(request):
    if request.method == 'GET':
        getgroupid = request.GET["groupid"]
        getsectionid = request.GET["sectionid"]
    getgroup = models.group.objects.get(id=getgroupid)
    getsection = models.section.objects.get(id=getsectionid)
    gethomeworks = models.homework.objects.filter(group=getgroup,section=getsection)
    jsonhomework = serializer(gethomeworks,output_type='json')
    return HttpResponse(jsonhomework)

def getStudentName(request):
    if request.method == 'GET':
        getgroupid = request.GET["groupid"]
        getsectionid = request.GET["sectionid"]
    getgroup = models.group.objects.get(id=getgroupid)
    getsection = models.section.objects.get(id=getsectionid)
    gethomeworks = models.homework.objects.filter(group=getgroup,section=getsection)
    names = []
    for var in gethomeworks:
        getstudent = models.student.objects.get(email=var.student_id)
        names.append(getstudent.name)
    
    jsonnames = serializer(names,output_type='json')
    return HttpResponse(jsonnames)

def setHomeworkStar(request):
    if request.method == 'GET':
        gethomeworkid = request.GET["homeworkid"]
        getstar = request.GET["star"]
    gethomework = models.homework.objects.get(id=gethomeworkid)
    gethomework.get_star = int(getstar)
    gethomework.save()
    jsonhomework = serializer(gethomework,output_type='json')
    return HttpResponse(jsonhomework)

def getStarNum(request):
    if request.method == 'GET':
        getemail = request.GET["email"]
    getstudent = models.student.objects.get(email=getemail)
    gethomeworks = models.homework.objects.filter(student=getstudent)
    starnum = 0
    for var in gethomeworks:
        starnum += var.get_star
    return HttpResponse(starnum)

def getRankNum(request):
    if request.method == 'GET':
        getgroupid = request.GET["groupid"]
    getgroup = models.group.objects.get(id=getgroupid)
    get_homeworks = models.homework.objects.filter(group=getgroup)
    _starNum = 0
    for var in get_homeworks:
        _starNum += var.get_star
    rank = 1
    getcourse = getgroup.course
    getgroups = models.group.objects.filter(course=getcourse)
    for var in getgroups:
        get_temp_homeworks = models.homework.objects.filter(group=var)
        temp_star_num = 0
        for work in get_temp_homeworks:
            temp_star_num += work.get_star
        if temp_star_num > _starNum:
            rank += 1
    return HttpResponse(rank)

def createTake(request):
    if request.method == 'GET':
        getcourseid = request.GET["courseid"]
        getemail = request.GET["email"]
    getcourse = models.course.objects.get(id=getcourseid)
    getstudent = models.student.objects.get(email=getemail)
    newtake = models.takes.objects.create(course=getcourse,student=getstudent)
    jsontake = serializer(newtake,output_type='json')
    return HttpResponse(jsontake)
