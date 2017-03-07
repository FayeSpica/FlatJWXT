from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,StreamingHttpResponse
from django.db import connection

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from itertools import groupby
import traceback
import pymysql.cursors
#from decimal import *
from django.views.decorators.csrf import csrf_exempt
import urllib
import json  
import decimal  

from datetime import date, datetime  

def music_file_download(request):  
	# do something...  

	def file_iterator(file_name, chunk_size=512):  
		with open(file_name) as f:  
			while True:  
				c = f.read(chunk_size)  
				if c:  
					yield c  
				else:  
					break  

	the_file_name = "file_name.txt"  
	response = StreamingHttpResponse(file_iterator(the_file_name))  
	response['Content-Type'] = 'application/octet-stream'  
	response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)  
	return response  

class MyClass(object):  
	def __init__(self):  
		self.a=11  
		self.b=21  

def MYdefault(obj):  
	if isinstance(obj, datetime):  
		return obj.strftime('%Y-%m-%d %H:%M:%S')  
	elif isinstance(obj, date):  
		return obj.strftime('%Y-%m-%d')  
	elif isinstance(obj, MyClass):  
		return {'a':obj.a,'b':obj.b}  
	elif isinstance(obj, decimal.Decimal):  
		#print 'tttttttttttttttttttttttt'  
		return str(obj)  
	else:  
		return ''
#return ''  
#return str(obj)  
################################################################
#连接配置信息
config = {
		'host':'tonlyshy.cn',
		'port':3306,
		'user':'liaowm5',
		'password':'qq199721',
		'db':'lab6',
		'charset':'utf8mb4',
		'cursorclass':pymysql.cursors.DictCursor,
}

# Create your views here.
def index(request):
	return HttpResponse("Hello,廖维明")

def main(request):
	if request.user.is_authenticated():
		r=request.session.get('logged_role')
		print(r)
		if r=='学生':
			return render(request,'student.html')
		if r=='教师':
			return render(request,'instructor.html')
		if r=='教务员':
			return render(request,'admin.html')
		else:
			tips = "登录成功，未知跳转错误"
			return render(request,'login.html',{'tips':tips})
	else:
		return HttpResponseRedirect('/login/')

#############################################authentation########################################################
def login(request):
	try:
		if request.user.is_authenticated():
			return HttpResponseRedirect('/main/')
		else:
			username = request.POST.get('userid')#['userid']
			passwd = request.POST.get('passwd')#['passwd']
			user = authenticate(username=username, password=passwd)
			print(username)
			print(passwd)
			user_info = User.objects.get(username=username)
			if user_info.email=='student@tonlyshy.cn':
				print('学生')
				if user is not None:
					request.session['logged_user'] = get_usr_name(username,'student')
					request.session['logged_role'] = '学生'
					auth_login(request,user)
					return render(request,'student.html')
				#HttpResponse("存在用户"+User_list.Uname+"	密码="+User_list.Upassword)
				else:
					tips="用户名与密码不匹配"
					return render(request,'login.html',{'tips':tips})
			if user_info.email=='instructor@tonlyshy.cn':
				print('老师')
				if user is not None:
					request.session['logged_user'] = get_usr_name(username,'instructor')
					request.session['logged_role'] = '教师'
					auth_login(request,user)
					return render(request,'instructor.html')
				#HttpResponse("存在用户"+User_list.Uname+"	密码="+User_list.Upassword)
				else:
					tips="用户名与密码不匹配"
					return render(request,'login.html',{'tips':tips})
			if user_info.email=='admin@tonlyshy.cn':
				print('教务员')
				if user is not None:
					request.session['logged_user'] = 'admin'
					request.session['logged_role'] = '教务员'
					auth_login(request,user)
					return render(request,'admin.html')
				else:
					tips="用户名与密码不匹配"
					return render(request,'login.html',{'tips':tips})
			else:
				tip = "未知错误"
				return render(request,'login.html',{'tips':tip})
	except:
		tips="未知错误"
		#return HttpResponse(traceback.print_exc());
		return render(request,'login.html',{'tips':traceback.print_exc()})
	
def logout(request):
	try:
		auth_logout(request)
		tips="你已经登出"
		return render(request,'login.html',{'tips':tips})
	except:
		tips="未知错误"
		return render(request,'student.html',{'tips':tips})
def get_usr_name(usr_name_id,types):
	# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
        	# 执行sql语句，进行查询
			sql = 'SELECT name from %s'%types +' where ID = %s'
			cursor.execute(sql,usr_name_id)
			# 获取查询结果
			name = cursor.fetchall()
			print(name)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return name[0]['name']
@csrf_exempt
def register_stu_login_user(request,id_name_dept_credits):
	id_name_dept_credits_split=id_name_dept_credits.rsplit('/')
	id_=id_name_dept_credits_split[0]
	name_=id_name_dept_credits_split[1]
	dept_=id_name_dept_credits_split[2]
	credits_=id_name_dept_credits_split[3]

	print(id_+name_+dept_+credits_)
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		sql = 'SELECT * from student where ID = %s'
		cursor.execute(sql,id_)

		stu_info = cursor.fetchall()
		stu_login_info = User.objects.filter(username=id_);
		if stu_info and stu_login_info:
			return HttpResponse('错误：学生已经存在')
		else:
			User.objects.create_user(id_, email='student@tonlyshy.cn', password='abc123456')
			sql = 'INSERT into student values(%s,%s,%s,%s)'
			cursor.execute(sql,(id_,name_,dept_,credits_))
			connection.commit()
			connection.close()
			return HttpResponse('注册完成')
@csrf_exempt
def ungister_stu_login_user(request,id_):
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		sql = 'SELECT * from student where ID = %s'
		cursor.execute(sql,id_)

		stu_info = cursor.fetchall()
		stu_login_info = User.objects.filter(username=id_);
		if stu_info and stu_login_info:
			sql = 'DELETE from student where ID = %s'
			cursor.execute(sql,id_)
			connection.commit()
			connection.close()
			User.objects.filter(username=id_).delete()
			return HttpResponse('删除成功')
		else:
			return HttpResponse('错误：学生不存在')
@csrf_exempt
def register_ins_login_user(request,id_name_dept_salary):
	id_name_dept_salary_split=id_name_dept_salary.rsplit('/')
	id_=id_name_dept_salary_split[0]
	name_=id_name_dept_salary_split[1]
	dept_=id_name_dept_salary_split[2]
	salary_=id_name_dept_salary_split[3]

	print(id_+name_+dept_+salary_)
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		sql = 'SELECT * from instructor where ID = %s'
		cursor.execute(sql,id_)

		stu_info = cursor.fetchall()
		stu_login_info = User.objects.filter(username=id_);
		if stu_info and stu_login_info:
			return HttpResponse('错误：老师已经存在')
		else:
			User.objects.create_user(id_, email='instructor@tonlyshy.cn', password='abc123456')
			sql = 'INSERT into instructor values(%s,%s,%s,%s)'
			cursor.execute(sql,(id_,name_,dept_,salary_))
			connection.commit()
			connection.close()
			return HttpResponse('注册完成')
@csrf_exempt
def ungister_ins_login_user(request,id_):
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		sql = 'SELECT * from instructor where ID = %s'
		cursor.execute(sql,id_)

		stu_info = cursor.fetchall()
		stu_login_info = User.objects.filter(username=id_);
		if stu_info and stu_login_info:
			sql = 'DELETE from instructor where ID = %s'
			cursor.execute(sql,id_)
			connection.commit()
			connection.close()
			User.objects.filter(username=id_).delete()
			return HttpResponse('删除成功')
		else:
			return HttpResponse('错误：老师不存在')
#############################################student.html########################################################
def studentfsc(request,fsc):
	#函数(功能)选择
	func = {'info':my_custom_sql_stu_info,
			'grades':my_custom_sql_stu_grades,
			'courses':my_custom_sql_stu_courses,
			'secourses':my_custom_sql_stu_selected_courses
			}  
	if request.user.is_authenticated():
		return func.get(fsc)(request)
	else:
		return HttpResponseRedirect('/login/')
	
	###查询
def my_custom_sql_stu_info(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
        	# 执行sql语句，进行查询
			sql = 'SELECT * from student where ID = %s'
			cursor.execute(sql,request.user.username)
			# 获取查询结果
			stu_info = cursor.fetchall()
			print(stu_info)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return render(request,'student.html',{'stu_info': stu_info})
def my_custom_sql_stu_grades(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			#sql = 'SELECT title,credits,semester,year,grade FROM student natural join takes natural join course Where student.ID=%s'
			sql ='SELECT title,credits,a.semester,a.year,grade FROM student natural join takes as a , course natural join section as b Where student.ID=%s and a.course_id=b.course_id and a.sec_id=b.sec_id'
			cursor.execute(sql,request.user.username)
			# 获取查询结果
			stu_grades = cursor.fetchall()
			print(stu_grades)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return render(request,'student.html',{'stu_grades': stu_grades})
def my_custom_sql_stu_courses(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			stu_courses=[]
			sql = 'SELECT * FROM lab6.department order by dept_id'
			cursor.execute(sql)
			dept_list = cursor.fetchall()
			stu_courses.append(dept_list)
			#sql = 'SELECT sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM course natural join section natural join teaches natural join instructor natural join department'#student,course natural join section natural join teaches natural join instructor Where student.ID=%s and student.dept_name=course.dept_name'
			sql = 'select department.dept_id,sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM department ,instructor,course natural join section natural join teaches natural join instructor as tmp where department.dept_name=instructor.dept_name and instructor.ID=tmp.ID'
			cursor.execute(sql)
			# 获取查询结果
			stu_courses.append(cursor.fetchall())
			print(stu_courses)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return render(request,'student.html',{'stu_courses': stu_courses})
def my_custom_sql_stu_selected_courses(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			stu_selected_courses=[]
			sql = 'SELECT * FROM lab6.department order by dept_id'
			cursor.execute(sql)
			dept_list = cursor.fetchall()
			stu_selected_courses.append(dept_list)
			#sql = 'SELECT stu.sec_id,instructor.name,title,credits,t.semester,t.year,t.building,t.room_number,t.time_slot,t.week,t.week_slot FROM instructor natural join teaches natural join course natural join section as t,student natural join takes  as stu Where stu.ID=%s and stu.sec_id=t.sec_id'
			sql ='SELECT stu.sec_id,instructor.dept_name,department.dept_id,instructor.name,title,credits,t.semester,t.year,t.building,t.room_number,t.time_slot,t.week,t.week_slot FROM instructor natural join teaches natural join course natural join section as t natural join department,student natural join takes  as stu Where stu.ID=%s and stu.sec_id=t.sec_id'
			cursor.execute(sql,request.user.username)
			# 获取查询结果
			stu_selected_courses.append(cursor.fetchall())
			print(stu_selected_courses)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return render(request,'student.html',{'stu_selected_courses': stu_selected_courses})

	###删除
@csrf_exempt
def my_custom_sql_stu_delete_courses(request,sec_id):
	try:
	# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			sql = 'select * from section where sec_id=%s'
			cursor.execute(sql,sec_id)
			tmp=cursor.fetchone()
			year=tmp.get('year')
			sql = 'delete from takes where ID=%s and course_id=%s and sec_id=%s and year= '+str(year)+' and semester=%s';
			cursor.execute(sql,(request.user.username,tmp['course_id'],sec_id,tmp['semester']))
			# 获取查询结果
			stu_selected_courses = cursor.fetchall()
			print(stu_selected_courses)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
			return HttpResponse('失败')
	###改

	###增
@csrf_exempt
def my_custom_sql_stu_add_courses(request,sec_id):
	try:
	# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			sql = 'select * from section where sec_id=%s'
			cursor.execute(sql,sec_id)
			tmp=cursor.fetchone()
			print(tmp)
			year=tmp.get('year')
			print(year)
			sql = 'insert into takes values(%s,%s,%s,%s,'+str(year)+',%s)'
			cursor.execute(sql,(request.user.username,tmp['course_id'],sec_id,tmp['semester'],''))
			print(tmp)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
			return HttpResponse('失败')

###API
@csrf_exempt
def get_all_sel_courses_json(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			stu_selected_courses=[]
			sql = 'SELECT dept_id,dept_name FROM lab6.department order by dept_id'
			cursor.execute(sql)
			dept_list = cursor.fetchall()
			stu_selected_courses.append(dept_list)
			#sql = 'SELECT stu.sec_id,instructor.name,title,credits,t.semester,t.year,t.building,t.room_number,t.time_slot,t.week,t.week_slot FROM instructor natural join teaches natural join course natural join section as t,student natural join takes  as stu Where stu.ID=%s and stu.sec_id=t.sec_id'
			sql ='SELECT stu.sec_id,instructor.dept_name,department.dept_id,instructor.name,title,credits,t.semester,t.year,t.building,t.room_number,t.time_slot,t.week,t.week_slot FROM instructor natural join teaches natural join course natural join section as t natural join department,student natural join takes  as stu Where stu.ID=%s and stu.sec_id=t.sec_id'
			cursor.execute(sql,request.user.username)
			# 获取查询结果
			stu_selected_courses.append(cursor.fetchall())
			print(stu_selected_courses)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return HttpResponse(json.dumps({'stu_selected_courses': stu_selected_courses},default=MYdefault), content_type="application/json")


#############################################instructor.html########################################################







def instructorfsc(request,fsc):
	#函数(功能)选择
	func = {'stulist':my_custom_sql_ins_stu_list,
			'stcourses':my_custom_sql_st_courses,
			'info':my_custom_sql_ins_info,
			'allcourses':my_custom_sql_all_courses,
			'coursegrade':my_custom_sql_in_courses_grade,
			'newcourses':my_custom_sql_ins_add_new_courses,
			}  
	if request.user.is_authenticated():
		return func.get(fsc)(request)
	else:
		return HttpResponseRedirect('/login/')

def my_custom_sql_ins_stu_list(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
        	# 执行sql语句，进行查询
			sql = 'SELECT course.course_id,course.title ,student.name ,b.sec_id,b.grade,b.ID FROM instructor natural join teaches natural join course natural join section as a,student natural join takes as b where instructor.ID=%s and a.sec_id=b.sec_id order by a.sec_id'
			cursor.execute(sql,request.user.username)
			# 获取查询结果
			courses_stu_list_data = cursor.fetchall()
			print(courses_stu_list_data)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()

			title0=''
			courses_stu_list=[]
			courses_stu_list_list=[]
			for stu in courses_stu_list_data:
				if stu['title'] != title0:
					if title0=='':
						title0=stu['title']
						courses_stu_list.append({'title0': title0,'sec_id':stu['sec_id']})
					title0=stu['title']
					if len(courses_stu_list)>1:
						print(len(stu))
						courses_stu_list_list.append(courses_stu_list)
						courses_stu_list=[]
						courses_stu_list.append({'title0': title0})
						courses_stu_list.append(stu)
					else:
						courses_stu_list.append(stu)
				else:
					courses_stu_list.append(stu)
			if len(courses_stu_list)!=0:
				courses_stu_list_list.append(courses_stu_list)
			print(courses_stu_list_list)
		return render(request,'instructor.html',{'courses_stu_list_list': courses_stu_list_list})
def my_custom_sql_all_courses(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
        	# 执行sql语句，进行查询
			all_courses=[]
			sql = 'SELECT * FROM lab6.department order by dept_id'
			cursor.execute(sql)
			dept_list = cursor.fetchall()
			all_courses.append(dept_list)
			#sql = 'SELECT sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM course natural join section natural join teaches natural join instructor natural join department'#student,course natural join section natural join teaches natural join instructor Where student.ID=%s and student.dept_name=course.dept_name'
			sql = 'select department.dept_id,course.course_id,sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM department ,instructor,course natural join section natural join teaches natural join instructor as tmp where department.dept_name=instructor.dept_name and instructor.ID=tmp.ID'
			cursor.execute(sql)
			# 获取查询结果
			all_courses.append(cursor.fetchall())
			print(all_courses)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return render(request,'instructor.html',{'all_courses': all_courses})
def my_custom_sql_st_courses(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
        	# 执行sql语句，进行查询
			sql = 'SELECT * FROM instructor natural join teaches natural join course natural join section where instructor.ID=%s'
			cursor.execute(sql,request.user.username)
			# 获取查询结果
			ins_selected_courses = cursor.fetchall()
			print(ins_selected_courses)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return render(request,'instructor.html',{'ins_selected_courses': ins_selected_courses})

def my_custom_sql_ins_info(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
        	# 执行sql语句，进行查询
			sql = 'SELECT * from instructor where ID = %s'
			cursor.execute(sql,request.user.username)
			# 获取查询结果
			ins_info = cursor.fetchall()
			print(ins_info)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
		return render(request,'instructor.html',{'ins_info': ins_info})
def my_custom_sql_in_courses_grade(request):
		# 创建连接
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
        	# 执行sql语句，进行查询
			sql = 'SELECT b.semester,b.year,course.title,course.course_id,student.name ,b.sec_id,b.grade,b.ID FROM instructor natural join teaches natural join course natural join section as a,student natural join takes as b where instructor.ID=%s and a.sec_id=b.sec_id order by a.sec_id'
			cursor.execute(sql,request.user.username)
			# 获取查询结果
			courses_stu_list_data = cursor.fetchall()
			print(courses_stu_list_data)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()

			title0=''
			courses_stu_list=[]
			courses_stu_list_list=[]
			for stu in courses_stu_list_data:
				if stu['title'] != title0:
					if title0=='':
						title0=stu['title']
						courses_stu_list.append({'title0': title0,'sec_id':stu['sec_id']})
					title0=stu['title']
					if len(courses_stu_list)>1:
						print(len(stu))
						courses_stu_list_list.append(courses_stu_list)
						courses_stu_list=[]
						courses_stu_list.append({'title0': title0})
						courses_stu_list.append(stu)
					else:
						courses_stu_list.append(stu)
				else:
					courses_stu_list.append(stu)
			if len(courses_stu_list)!=0:
				courses_stu_list_list.append(courses_stu_list)
			print(courses_stu_list_list)
		return render(request,'instructor.html',{'stu_grades_list_list': courses_stu_list_list})
def my_custom_sql_ins_add_new_courses(request):
			# 创建连接
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		# 执行sql语句，进行查询
		all_courses=[]
		sql = 'SELECT * FROM lab6.department order by dept_id'
		cursor.execute(sql)
		dept_list = cursor.fetchall()
		all_courses.append(dept_list)
		#sql = 'SELECT sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM course natural join section natural join teaches natural join instructor natural join department'#student,course natural join section natural join teaches natural join instructor Where student.ID=%s and student.dept_name=course.dept_name'
		sql = 'SELECT * from section natural join course natural join department'
		cursor.execute(sql)
		# 获取查询结果
		all_courses.append(cursor.fetchall())
		print(all_courses)
		# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
		connection.close()
	return render(request,'instructor.html',{'add_new_courses': all_courses})



#############################################admin.html########################################################







def adminfsc(request,fsc):
	#函数(功能)选择
	func = {'stumanage':my_custom_sql_admin_stu_manage,
			'insmanage':my_custom_sql_admin_ins_manage,
			'allcourses':my_custom_sql_admin_all_courses,
			'newcourses':my_custom_sql_admin_add_new_courses,
			'newsections':my_custom_sql_admin_add_new_sections
			}  
	if request.user.is_authenticated():
		return func.get(fsc)(request)
	else:
		return HttpResponseRedirect('/login/')
def my_custom_sql_admin_stu_manage(request):
		# 创建连接
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		# 执行sql语句，进行查询
		all_students=[]
		sql = 'SELECT * FROM department order by dept_id'
		cursor.execute(sql)
		dept_list = cursor.fetchall()
		all_students.append(dept_list)
		#sql = 'SELECT sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM course natural join section natural join teaches natural join instructor natural join department'#student,course natural join section natural join teaches natural join instructor Where student.ID=%s and student.dept_name=course.dept_name'
		sql = 'SELECT * FROM student natural join department order by ID'
		cursor.execute(sql)
		# 获取查询结果
		all_students.append(cursor.fetchall())
		print(all_students)
		# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
		connection.close()
	return render(request,'admin.html',{'all_students': all_students})
def my_custom_sql_admin_ins_manage(request):
		# 创建连接
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		# 执行sql语句，进行查询
		all_instructors=[]
		sql = 'SELECT * FROM department order by dept_id'
		cursor.execute(sql)
		dept_list = cursor.fetchall()
		all_instructors.append(dept_list)
		#sql = 'SELECT sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM course natural join section natural join teaches natural join instructor natural join department'#student,course natural join section natural join teaches natural join instructor Where student.ID=%s and student.dept_name=course.dept_name'
		sql = 'SELECT * FROM instructor natural join department order by ID'
		cursor.execute(sql)
		# 获取查询结果
		all_instructors.append(cursor.fetchall())
		print(all_instructors)
		# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
		connection.close()
	return render(request,'admin.html',{'all_instructors': all_instructors})
def my_custom_sql_admin_all_courses(request):
		# 创建连接
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		# 执行sql语句，进行查询
		all_courses=[]
		sql = 'SELECT * FROM department order by dept_id'
		cursor.execute(sql)
		dept_list = cursor.fetchall()
		all_courses.append(dept_list)
		#sql = 'SELECT sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM course natural join section natural join teaches natural join instructor natural join department'#student,course natural join section natural join teaches natural join instructor Where student.ID=%s and student.dept_name=course.dept_name'
		sql = 'select department.dept_id,course.course_id,sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM department ,instructor,course natural join section natural join teaches natural join instructor as tmp where department.dept_name=instructor.dept_name and instructor.ID=tmp.ID'
		cursor.execute(sql)
		# 获取查询结果
		all_courses.append(cursor.fetchall())
		print(all_courses)
		# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
		connection.close()
	return render(request,'admin.html',{'all_courses': all_courses})
def my_custom_sql_admin_add_new_courses(request):
			# 创建连接
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		# 执行sql语句，进行查询
		all_courses=[]
		sql = 'SELECT * FROM lab6.department order by dept_id'
		cursor.execute(sql)
		dept_list = cursor.fetchall()
		all_courses.append(dept_list)
		#sql = 'SELECT sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM course natural join section natural join teaches natural join instructor natural join department'#student,course natural join section natural join teaches natural join instructor Where student.ID=%s and student.dept_name=course.dept_name'
		sql = 'SELECT * from course natural join department order by course_id'
		cursor.execute(sql)
		# 获取查询结果
		all_courses.append(cursor.fetchall())
		print(all_courses)
		# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
		connection.close()
	return render(request,'admin.html',{'add_new_courses': all_courses})
def my_custom_sql_admin_add_new_sections(request):
	connection = pymysql.connect(**config)
	with connection.cursor() as cursor:
		# 执行sql语句，进行查询
		all_courses=[]
		sql = 'SELECT * FROM lab6.department order by dept_id'
		cursor.execute(sql)
		dept_list = cursor.fetchall()
		all_courses.append(dept_list)
		#sql = 'SELECT sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM course natural join section natural join teaches natural join instructor natural join department'#student,course natural join section natural join teaches natural join instructor Where student.ID=%s and student.dept_name=course.dept_name'
		#sql = 'select department.dept_id,course.course_id,sec_id,instructor.name,title,credits,semester,year,building,room_number,time_slot,week,week_slot FROM department ,instructor,course natural join section natural join teaches natural join instructor as tmp where department.dept_name=instructor.dept_name and instructor.ID=tmp.ID'
		sql = 'SELECT * from section natural join course natural join department'
		cursor.execute(sql)
		# 获取查询结果
		all_courses.append(cursor.fetchall())
		sql = 'SELECT * from course'
		cursor.execute(sql)
		all_courses.append(cursor.fetchall())
		print(all_courses)
		# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
		connection.commit()
		connection.close()
	return render(request,'admin.html',{'add_new_sections': all_courses})
#############################################---API---########################################################
@csrf_exempt
def my_custom_sql_admin_upgrade_stu(request,id_name_dept_credits):
	id_name_dept_credits_split=id_name_dept_credits.rsplit('/')
	id_=id_name_dept_credits_split[0]
	name_=id_name_dept_credits_split[1]
	dept_=id_name_dept_credits_split[2]
	credits_=id_name_dept_credits_split[3]

	try:
		print(id_+name_+dept_+credits_)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			sql = 'UPDATE student set name=%s,dept_name=%s,tot_cred=%s where ID=%s'
			cursor.execute(sql,(name_,dept_,credits_,id_))
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
		traceback.print_exc()
		return HttpResponse('未知错误')
@csrf_exempt
def my_custom_sql_admin_upgrade_ins(request,id_name_dept_salary):
	id_name_dept_salary_split=id_name_dept_salary.rsplit('/')
	id_=id_name_dept_salary_split[0]
	name_=id_name_dept_salary_split[1]
	dept_=id_name_dept_salary_split[2]
	salary_=id_name_dept_salary_split[3]

	try:
		print(id_+name_+dept_+salary_)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			sql = 'UPDATE instructor set name=%s,dept_name=%s,salary=%s  where ID=%s'
			cursor.execute(sql,(name_,dept_,salary_,id_))
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
		traceback.print_exc()
		return HttpResponse('未知错误')
@csrf_exempt
def my_custom_sql_admin_add_course(request,id_title_deptname_credits):
	id_title_deptname_credits_split=id_title_deptname_credits.rsplit('/')
	id_=id_title_deptname_credits_split[0]
	title_=id_title_deptname_credits_split[1]
	dept_=id_title_deptname_credits_split[2]
	credits_=id_title_deptname_credits_split[3]
	try:
		print(id_+title_+dept_+credits_)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			sql = 'INSERT into course VALUES(%s,%s,%s,%s)'
			cursor.execute(sql,(id_,title_,dept_,credits_))
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
		traceback.print_exc()
		return HttpResponse('未知错误')
@csrf_exempt
def my_custom_sql_admin_upgrade_course(request,id_title_deptname_credits):
	id_title_deptname_credits_split=id_title_deptname_credits.rsplit('/')
	id_=id_title_deptname_credits_split[0]
	title_=id_title_deptname_credits_split[1]
	dept_=id_title_deptname_credits_split[2]
	credits_=id_title_deptname_credits_split[3]
	try:
		print(id_+title_+dept_+credits_)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			sql = 'UPDATE course SET title=%s,dept_name=%s,credits=%s WHERE course_id=%s'
			cursor.execute(sql,(title_,dept_,credits_,id_))
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
		traceback.print_exc()
		return HttpResponse('未知错误')
@csrf_exempt
def my_custom_sql_admin_delete_course(request,course_id):
	try:
		print(course_id)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			sql = 'DELETE FROM course WHERE course_id=%s'
			cursor.execute(sql,course_id)
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
		traceback.print_exc()
		return HttpResponse('未知错误') 
@csrf_exempt
def my_custom_sql_admin_add_section(request,cid_sid_semester_year_building_room_times_week_weeks):
	cid_sid_semester_year_building_room_times_week_weeks_split=cid_sid_semester_year_building_room_times_week_weeks.rsplit('/')
	course_id=cid_sid_semester_year_building_room_times_week_weeks_split[0]
	sec_id=cid_sid_semester_year_building_room_times_week_weeks_split[1]
	semester=cid_sid_semester_year_building_room_times_week_weeks_split[2]
	year=cid_sid_semester_year_building_room_times_week_weeks_split[3]
	building=cid_sid_semester_year_building_room_times_week_weeks_split[4]
	room_number=cid_sid_semester_year_building_room_times_week_weeks_split[5]
	time_slot=cid_sid_semester_year_building_room_times_week_weeks_split[6]
	week=cid_sid_semester_year_building_room_times_week_weeks_split[7]
	week_slot=cid_sid_semester_year_building_room_times_week_weeks_split[8]
	try:
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			sql = 'INSERT into section VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
			cursor.execute(sql,(course_id,sec_id,semester,year,building,room_number,time_slot,week,week_slot))
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
		traceback.print_exc()
		return HttpResponse('未知错误')
@csrf_exempt
def my_custom_sql_admin_delete_section(request,title_sid_semester_year):
	title_sid_semester_year_split=title_sid_semester_year.rsplit('/')
	title=title_sid_semester_year_split[0]
	sec_id=title_sid_semester_year_split[1]
	semester=title_sid_semester_year_split[2]
	year=title_sid_semester_year_split[3]
	try:
		print(sec_id)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			sql = 'SELECT course_id FROM course where title=%s'
			cursor.execute(sql,title)
			course_=cursor.fetchall()
			print(course_)
			sql = 'DELETE FROM section WHERE sec_id=%s and course_id=%s and semester=%s and year=%s'
			cursor.execute(sql,(sec_id,course_[0]['course_id'],semester,year))
			connection.commit()
			connection.close()
			return HttpResponse('删除成功')
	except:
		traceback.print_exc()
		return HttpResponse('未知错误') 
	###删除
@csrf_exempt
def my_custom_sql_ins_delete_courses_stu(request,sec_id_stu_id):
	try:
	# 创建连接
		sec_id_stu_id_split=sec_id_stu_id.rsplit('/')
		sec_id=sec_id_stu_id_split[0]
		stu_id=sec_id_stu_id_split[1]
		print(sec_id_stu_id_split)
		print(sec_id+stu_id)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			sql = 'SELECT * from section where sec_id=%s'
			cursor.execute(sql,sec_id)
			tmp=cursor.fetchone()
			year=tmp.get('year')
			sql = 'DELETE from takes where ID=%s and course_id=%s and sec_id=%s and year= '+str(year)+' and semester=%s';
			cursor.execute(sql,(stu_id,tmp['course_id'],sec_id,tmp['semester']))
			# 获取查询结果
			stu_selected_courses = cursor.fetchall()
			print(stu_selected_courses)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
			return HttpResponse('失败')
@csrf_exempt
def my_custom_sql_ins_add_course(request,cid_sid_semester_year):
	try:
	# 创建连接
		sec_id_split=cid_sid_semester_year.rsplit('/')
		course_id=sec_id_split[0]
		sec_id=sec_id_split[1]
		semester=sec_id_split[2]
		year=sec_id_split[3]
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			print(request.user.username+' '+course_id+' '+sec_id+' '+semester+' '+year)
			sql = 'INSERT into teaches  VALUES(%s,%s,%s,%s,%s)';
			cursor.execute(sql,(request.user.username,course_id,sec_id,semester,year))
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
			return HttpResponse('失败')
@csrf_exempt
def my_custom_sql_ins_delete_course(request,title_sid_semester_year):
	try:
	# 创建连接
		sec_id_split=title_sid_semester_year.rsplit('/')
		title=sec_id_split[0]
		sec_id=sec_id_split[1]
		semester=sec_id_split[2]
		year=sec_id_split[3]
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			sql = 'SELECT course_id FROM course where title=%s'
			cursor.execute(sql,title)
			course_=cursor.fetchall()
			sql = 'DELETE from teaches where ID=%s and course_id=%s and sec_id=%s and year= '+str(year)+' and semester=%s';
			cursor.execute(sql,(request.user.username,course_[0]['course_id'],sec_id,semester))
			sql = 'DELETE from takes where course_id=%s and sec_id=%s and year= '+str(year)+' and semester=%s';
			cursor.execute(sql,(course_[0]['course_id'],sec_id,semester))
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
			traceback.print_exc()
			return HttpResponse('失败')
	###改
@csrf_exempt
def my_custom_sql_ins_upgrade_courses_stu(request,sec_id_stu_id):
	try:
	# 创建连接
		sec_id_stu_id_split=sec_id_stu_id.rsplit('_')
		sec_id=sec_id_stu_id_split[0]
		course_id=sec_id_stu_id_split[1]
		semester=sec_id_stu_id_split[2]
		re_stu_id_split=sec_id_stu_id_split[3].rsplit('/')
		year=re_stu_id_split[0]
		stu_id=re_stu_id_split[1]
		stu_grades=re_stu_id_split[2]
		print('GG')
		print(stu_grades)
		print(sec_id+" "+course_id+" "+semester+" "+year+" "+stu_id+" "+stu_grades+" "+stu_id)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			print(year)
			sql = 'UPDATE takes set grade=%s where sec_id=%s and course_id=%s and ID=%s and year= %s and semester=%s';
			cursor.execute(sql,(stu_grades,sec_id,course_id,stu_id,year,semester))
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
			traceback.print_exc()
			return HttpResponse('失败')
	###增

@csrf_exempt
def my_custom_sql_ins_add_courses_stu(request,sec_id_stu_id):
	try:
	# 创建连接
		sec_id_stu_id_split=sec_id_stu_id.rsplit('/')
		sec_id=sec_id_stu_id_split[0]
		stu_id=sec_id_stu_id_split[1]
		stu_grades=sec_id_stu_id_split[2]
		print('sec_id_stu_id_spli')
		print(sec_id_stu_id_split)
		print(sec_id+stu_id)
		connection = pymysql.connect(**config)
		with connection.cursor() as cursor:
			# 执行sql语句，进行查询
			sql = 'SELECT * from section where sec_id=%s'
			cursor.execute(sql,sec_id)
			tmp=cursor.fetchone()
			print(tmp)
			year=tmp.get('year')
			print(year)
			sql = 'INSERT into takes values(%s,%s,%s,%s,'+str(year)+',%s)'
			cursor.execute(sql,(stu_id,tmp['course_id'],sec_id,tmp['semester'],stu_grades))
			print(tmp)
			# 没有设置默认自动提交，需要主动提交，以保存所执行的语句
			connection.commit()
			connection.close()
			return HttpResponse('成功')
	except:
			return HttpResponse('失败')
