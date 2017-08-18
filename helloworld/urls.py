
from django.conf.urls import url
 
from . import view
from seesaw import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^$', view.hello),
    url(r'^index/$', views.index),
    url(r'^checkPassWord/$',views.checkPassWord),
    url(r'^deleteAll/$',views.deleteAll),
    url(r'^createCourse/$',views.createCourse),
    url(r'^getCourse/$',views.getCourse),
    url(r'^getCourseID/$',views.getCourseID),
    url(r'uploadImg/$',views.uploadImg),
    url(r'getImg/$',views.getImg), 
    url(r'checkStudentPassword/$',views.checkStudentPassword),
    url(r'checkCourseCode/$',views.checkCourseCode),
    url(r'createStudentAccount/$',views.createStudentAccount),
    url(r'getTakes/$',views.getTakes),
    url(r'getImgOwner/$',views.getImgOwner),
    url(r'uploadStImg/$',views.uploadStImg),
    url(r'getCourseGroup/$',views.getCourseGroup),
    url(r'getGroupMemberName/$',views.getGroupMemberName),
    url(r'getUnGroupMemberName/$',views.getUnGroupMemberName), 
    url(r'getUnGroupMemberEmail/$',views.getUnGroupMemberEmail), 
    url(r'uploadSelectedEmail/$',views.uploadSelectedEmail),   
    url(r'getGroupMemberEmail/$',views.getGroupMemberEmail), 
    url(r'getSectionNum/$',views.getSectionNum), 
    url(r'getCourseMsg/$',views.getCourseMsg),
    url(r'uploadSection/$',views.uploadSection),
    url(r'getSections/$',views.getSections),
    url(r'uploadSection/$',views.uploadSection), 
    url(r'getGroupNum/$',views.getGroupNum),
    url(r'uploadHomework/$',views.uploadHomework), 
    url(r'getGroupID/$',views.getGroupID),
    url(r'getHomeworkByGroup/$',views.getHomeworkByGroup),
    url(r'getStudentName/$',views.getStudentName),
    url(r'getImgCreateTime/$',views.getImgCreateTime),
    url(r'getItemContent/$',views.getItemContent),
    url(r'setHomeworkStar/$',views.setHomeworkStar),
    url(r'getStarNum/$',views.getStarNum),
    url(r'getRankNum/$',views.getRankNum),
    url(r'createTake/$',views.createTake),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
