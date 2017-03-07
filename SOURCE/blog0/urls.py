"""blog0 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from polls import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    url(r'^test/', views.index),
	url(r'^adminadmin/', admin.site.urls),
	url(r'^login/', views.login),
	url(r'^logout/$',views.logout),
    url(r'^main/$', views.main),
    url(r'^student/$', views.main),
    url(r'^student/(?P<fsc>[a-zA-Z0-9]+)$', views.studentfsc,name='fsc'),
    url(r'^instructor/$', views.main),
    url(r'^instructor/(?P<fsc>[a-zA-Z0-9]+)$', views.instructorfsc,name='fsc'),
    url(r'^admin/$', views.main),
    url(r'^admin/(?P<fsc>[a-zA-Z0-9]+)$', views.adminfsc,name='fsc'),
    url(r'^API/stu/selcourses/$',views.get_all_sel_courses_json),
    url(r'^API/stu/delcourse/(?P<sec_id>[a-zA-Z0-9]+)$', views.my_custom_sql_stu_delete_courses,name='sec_id'),
    url(r'^API/stu/addcourse/(?P<sec_id>[a-zA-Z0-9]+)$', views.my_custom_sql_stu_add_courses,name='sec_id'),
    url(r'^API/ins/delcoursestu/(?P<sec_id_stu_id>(.*)+)$', views.my_custom_sql_ins_delete_courses_stu,name='sec_id_stu_id'),
    url(r'^API/ins/addcoursestu/(?P<sec_id_stu_id>(.*)+)$', views.my_custom_sql_ins_add_courses_stu,name='sec_id_stu_id'),
    url(r'^API/ins/upgradecoursestu/(?P<sec_id_stu_id>(.*)+)$', views.my_custom_sql_ins_upgrade_courses_stu,name='sec_id_stu_id'),
    url(r'^API/ins/delcourse/(?P<title_sid_semester_year>(.*)+)$',views.my_custom_sql_ins_delete_course,name='title_sid_semester_year'),
    url(r'^API/ins/addcourse/(?P<cid_sid_semester_year>(.*)+)$',views.my_custom_sql_ins_add_course,name='cid_sid_semester_year'),
    url(r'^API/admin/delcourse/(?P<course_id>(.*)+)$',views.my_custom_sql_admin_delete_course,name='course_id'),
    url(r'^API/admin/addcourse/(?P<id_title_deptname_credits>(.*)+)$',views.my_custom_sql_admin_add_course,name='id_title_deptname_credits'),
    url(r'^API/admin/upgradecourse/(?P<id_title_deptname_credits>(.*)+)$',views.my_custom_sql_admin_upgrade_course,name='id_title_deptname_credits'),
    url(r'^API/admin/delsection/(?P<title_sid_semester_year>(.*)+)$',views.my_custom_sql_admin_delete_section,name='title_sid_semester_year'),
    url(r'^API/admin/addsection/(?P<cid_sid_semester_year_building_room_times_week_weeks>(.*)+)$',views.my_custom_sql_admin_add_section,name='cid_sid_semester_year_building_room_times_week_weeks'),
    url(r'^API/admin/upgradestu/(?P<id_name_dept_credits>(.*)+)$',views.my_custom_sql_admin_upgrade_stu,name='id_name_dept_credits'),
    url(r'^API/admin/upgradeins/(?P<id_name_dept_salary>(.*)+)$',views.my_custom_sql_admin_upgrade_ins,name='id_name_dept_salary'),
    url(r'^API/auth/register/stu/(?P<id_name_dept_credits>(.*)+)$', views.register_stu_login_user,name='id_name_dept_credits'),
    url(r'^API/auth/unregister/stu/(?P<id_>(.*)+)$', views.ungister_stu_login_user,name='id_'),
    url(r'^API/auth/register/ins/(?P<id_name_dept_salary>(.*)+)$', views.register_ins_login_user,name='id_name_dept_salary'),
    url(r'^API/auth/unregister/ins/(?P<id_>(.*)+)$', views.ungister_ins_login_user,name='id_'),
    url(r'^$', views.login),
]
