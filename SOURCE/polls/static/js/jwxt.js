/*
********************************************************************
********************************************************************
********************************************************************
*/

function bt_stu_course_delete_onclick(obj) {
	$course=$("tr[id="+obj.parentNode.parentNode.id+"]");
	if(window.confirm('你确定要退课吗？')){
		$.post("../API/stu/delcourse/"+obj.parentNode.parentNode.id,{},function(data){
			if(data=='成功'){
				$course.remove();
			}
			alert(data);
		});
		location.reload(true);	
		return true;
  	}
    else{
         return false;
    }
	}
function bt_stu_course_select_onclick(obj) {
	$course=$("tr[id="+obj.parentNode.parentNode.id+"]");
	if(window.confirm('你确定要选课吗？')){
		//location.reload(true);
		var table=$('#stu_courses');
		var c=table.find('tr');
		//alert(obj.parentNode.parentNode.id);
		$.post("../API/stu/addcourse/"+obj.parentNode.parentNode.id,{},function(data){
			if(data=='成功'){
				obj.setAttribute("class","btn btn-sm btn-default disabled");
			}else{
				//$sourse.animate({backgroundColor:"#FB6C6C"});
				//this.attr("class","btn btn-block btn-lg btn-default disabled")
			}
			alert(data);
		});

		return true;
  	}
    else{
         return false;
    }
	}
function selectChange(){
    var objS = document.getElementById("selectSId");
    //可以获取到响应的选中项
    var selected = objS.options[objS.selectedIndex].value;
	if(selected==0){//显示所有
		$("table[id=\"stu_courses\"]>tbody>tr").each(function(i,obj){  
			//alert(i+":"+attrib);  
			//attrib.setAttribute("class","btn btn-sm btn-default disabled");
			var $jobj=$(obj)
			$jobj.show();
		});  
	}
	else{//显示selected
		//alert(selected);
		$("table[id=\"stu_courses\"]>tbody>tr").each(function(i,obj){  
			//alert(i+":"+attrib);  
			//attrib.setAttribute("class","btn btn-sm btn-default disabled");
			var $jobj=$(obj);
			if($jobj.attr('tag')!=selected.toString()&&$jobj.attr('tag')!=null){
				//alert($jobj.attr('tag')+':'+selected.toString());
				$jobj.hide();
			}
			else{
				$jobj.show();
			}
		});  
	}
}
/*
$("select").select2({dropdownCssClass: 'dropdown-inverse'});
$("#select2-hidden-accessible").change(function(){
	var selected=$("#select").val();
	if(selected==0){//显示所有
		$("p").hide();
		$("table[id=\"stu_courses\"]>tbody>tr").each(function(i,obj){  
		//alert(i+":"+attrib);  
		//attrib.setAttribute("class","btn btn-sm btn-default disabled");
		var $jobj=$(obj)
		$jobj.hide();
		});  
	}
	else{//显示selected
		alert(selected);
	}
});
                 <tr id="{{course.sec_id}}" tag="{{course.dept_id}}">
                      <td>{{course.title}}</td>
                      <td>{{course.name}}</td>
                      <td>{{course.credits}}</td>
                      <td>{{course.year}}</td>
                      <td>{{course.semester}}</td>
                      <td>{{course.building}}</td>
                      <td>{{course.room_number}}</td>
                      <td>{{course.week_slot}}</td>
                      <td>星期{{course.week}} </td>
                      <td>{{course.time_slot}}节</td>
*/
//课程是否已经选中
var data={};
$(document).ready(function() { 
	$.post("../API/stu/selcourses/",data,function(data){
			//for(var i=0,l=data.length;i<l;i++){
				str='';
					for(var key1 in data.stu_selected_courses[1]){
						sec_id=data.stu_selected_courses[1][key1].sec_id;
						dept_id=data.stu_selected_courses[1][key1].dept_id;
						title=data.stu_selected_courses[1][key1].title;
						name=data.stu_selected_courses[1][key1].name;
						credits=data.stu_selected_courses[1][key1].credits;
						year=data.stu_selected_courses[1][key1].year;
						semester=data.stu_selected_courses[1][key1].semester;
						building=data.stu_selected_courses[1][key1].building;
						room_number=data.stu_selected_courses[1][key1].room_number;
						week_slot=data.stu_selected_courses[1][key1].week_slot;
						week=data.stu_selected_courses[1][key1].week;
						time_slot=data.stu_selected_courses[1][key1].time_slot;

						str=str+(key1+':'+data.stu_selected_courses[1][key1].name)+'\n';
							$("table[id=\"stu_courses\"]>tbody>tr[id=\""+sec_id+"\" ]>td>button").each(function(i,attrib){  
								//alert(i+":"+attrib);  
								//alert(attrib.parentNode.innerHTML);
								attrib.setAttribute("class","btn btn-sm btn-default disabled");
							});  
					}
				//alert(str);
			//}
			//alert(data);
		});
/*
	$button=$("table[id=\"stu_courses\"]>tr>td>button");
	$("table[id=\"stu_courses\"]>tbody>tr>td>button").each(function(i,attrib){  
		//alert(i+":"+attrib);  
		attrib.setAttribute("class","btn btn-sm btn-default disabled");
	});  */
});


/*
********************************************************************
********************************************************************
********************************************************************
*/
function bt_ins_course_delete_stu_onclick(obj) {
	$course=$("tr[id="+obj.parentNode.parentNode.id+"]");
	if(window.confirm('你确定要退  学号:'+obj.parentNode.parentNode.id+',姓名:'+obj.parentNode.parentNode.children[1].innerHTML+'   的课吗？')){
		$.post("../API/ins/delcoursestu/"+obj.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.id+"/"+obj.parentNode.parentNode.id,{},function(data){
			if(data=='成功'){
				$course.remove();
			}
			alert(data);
		});
		//location.reload(true);	
		return true;
  	}
    else{
         return false;
    }
	}
function on_id_input_change(obj){
	id=obj.value;
	if(id.match(/^[0-9]{8}$/)){
		obj.parentNode.setAttribute("class","has-success");
		obj.parentNode.parentNode.nextSibling.nextSibling.children[0].children[0].innerHTML='';
	}
	else{
		obj.parentNode.setAttribute("class","has-error");
		obj.parentNode.parentNode.nextSibling.nextSibling.children[0].children[0].innerHTML='非法输入,学号必须是八位数字！';
	}
}
function on_name_input_change(obj){
	name=obj.value;
	if(name==''){
		obj.parentNode.setAttribute("class","has-error");
		obj.parentNode.parentNode.nextSibling.nextSibling.children[1].children[0].innerHTML='姓名不能为空';
	}
	else{
		obj.parentNode.setAttribute("class","has-success");
		obj.parentNode.parentNode.nextSibling.nextSibling.children[1].children[0].innerHTML='';
	}
}
function on_grade_input_change(obj){
	grades=obj.value;
	if(grades!=''){
		if((!grades.match(/^\d{1,3}$/))){
			obj.parentNode.setAttribute("class","has-error");
			obj.parentNode.parentNode.nextSibling.nextSibling.children[2].children[0].innerHTML='非法输入';
		}
		else{
			if(Number(grades)>99||Number(grades)<0){
			obj.parentNode.setAttribute("class","has-error");
			obj.parentNode.parentNode.nextSibling.nextSibling.children[2].children[0].innerHTML='非法输入';
			}
			else{
			obj.parentNode.setAttribute("class","has-success");
			obj.parentNode.parentNode.nextSibling.nextSibling.children[2].children[0].innerHTML='';
			}
		}
	}
	else{
		obj.parentNode.setAttribute("class","has-success");
		obj.parentNode.parentNode.nextSibling.nextSibling.children[2].children[0].innerHTML='';
	}
}
function on_salary_input_change(obj){
	salary=obj.value;
	if((!salary.match(/^\d{3,10}$/))){
		obj.parentNode.setAttribute("class","has-error");
		obj.parentNode.parentNode.nextSibling.nextSibling.children[3].children[0].innerHTML='非法输入';
	}
	else{
			obj.parentNode.setAttribute("class","has-success");
			obj.parentNode.parentNode.nextSibling.nextSibling.children[3].children[0].innerHTML='';
	}
}
function on_salary_input_change_upgrade(obj){
	salary=obj.value;
	if((!salary.match(/^\d{3,10}$/))){
		obj.parentNode.setAttribute("class","has-error");
		obj.parentNode.parentNode.nextSibling.children[3].children[0].innerHTML='非法输入';
	}
	else{
			obj.parentNode.setAttribute("class","has-success");
			obj.parentNode.parentNode.nextSibling.children[3].children[0].innerHTML='';
	}
}
function on_credits_input_change(obj){
		grades=obj.value;
	if(grades!=''){
		if((!grades.match(/^\d{1,3}$/))){
			obj.parentNode.setAttribute("class","has-error");
			obj.parentNode.parentNode.nextSibling.nextSibling.children[2].children[0].innerHTML='非法输入';
		}
		else{
			if(Number(grades)>300||Number(grades)<0){
			obj.parentNode.setAttribute("class","has-error");
			obj.parentNode.parentNode.nextSibling.nextSibling.children[2].children[0].innerHTML='非法输入';
			}
			else{
			obj.parentNode.setAttribute("class","has-success");
			obj.parentNode.parentNode.nextSibling.nextSibling.children[2].children[0].innerHTML='';
			}
		}
	}
	else{
		obj.parentNode.setAttribute("class","has-success");
		obj.parentNode.parentNode.nextSibling.nextSibling.children[2].children[0].innerHTML='';
	}
}
function bt_ins_course_add_stu_onclick(obj) {
	$course=$(obj.parentNode.parentNode);
	id=obj.parentNode.parentNode.children[0].children[0].value;
	name=obj.parentNode.parentNode.children[1].children[0].value;
	grades=obj.parentNode.parentNode.children[2].children[0].value;
	//alert(obj.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute('id'));
	if(!id.match(/^[0-9]{8}$/)){
		alert('非法输入,学号必须是八位数字！');
		return true;
	}
	if(name==''){
		alert('姓名不能为空');
		return true;
	}
	if(grades!=''){
		if((!grades.match(/^\d{1,3}$/))){
			alert('非法输入！');
			return true;
		}
	}
	if(window.confirm('你确定要让  学号:'+id+',姓名:'+decodeURI(encodeURIComponent(name))+'   的同学选课吗？')){
		//location.reload(true);
		var table=$('#stu_courses');
		var c=table.find('tr');
		//alert(obj.parentNode.parentNode.id);
		tr_="<tr id=\""+id+"\"><td>"+id+"</td><td>"+name+"</td><td>"+grades+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_ins_course_delete_stu_onclick(this)\">退课</button></td></tr>";
		$.post("../API/ins/addcoursestu/"+obj.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute('id')+"/"+id+"/"+grades+"",{},function(data){
			if(data=='成功'){
				//obj.setAttribute("class","btn btn-sm btn-default disabled");
				obj.parentNode.parentNode.previousSibling.previousSibling.insertAdjacentHTML("afterend",tr_);
			}else{
				//$sourse.animate({backgroundColor:"#FB6C6C"});
				//this.attr("class","btn btn-block btn-lg btn-default disabled")
			}
			alert(data);
		});

		return true;
  	}
    else{
         return false;
    }
	}
//学生成绩录入
function on_in_id_input_change(obj){
	id=obj.value;
	if(id.match(/^[0-9]{8}$/)){
		obj.parentNode.setAttribute("class","has-success");
		obj.parentNode.parentNode.nextSibling.children[0].children[0].innerHTML='';
	}
	else{
		obj.parentNode.setAttribute("class","has-error");
		obj.parentNode.parentNode.nextSibling.children[0].children[0].innerHTML='非法输入,学号必须是八位数字！';
	}
}
function on_in_name_input_change(obj){
	name=obj.value;
	if(name==''){
		obj.parentNode.setAttribute("class","has-error");
		obj.parentNode.parentNode.nextSibling.children[1].children[0].innerHTML='姓名不能为空';
	}
	else{
		obj.parentNode.setAttribute("class","has-success");
		obj.parentNode.parentNode.nextSibling.children[1].children[0].innerHTML='';
	}
}
function on_in_grade_input_change(obj){
	grades=obj.value;
	if((!grades.match(/^\d{1,3}$/))){
		obj.parentNode.setAttribute("class","has-error");
		obj.parentNode.parentNode.nextSibling.children[2].children[0].innerHTML='非法输入';
	}
	else{
		if(Number(grades)>99||Number(grades)<0){
			obj.parentNode.setAttribute("class","has-error");
			obj.parentNode.parentNode.nextSibling.children[2].children[0].innerHTML='非法输入';
		}
		else{
			obj.parentNode.setAttribute("class","has-success");
			obj.parentNode.parentNode.nextSibling.children[2].children[0].innerHTML='';
		}
	}
}
function bt_ins_course_upgrade_stu_onclick1(obj){
	sec_id=obj.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute('id');
	id=obj.parentNode.parentNode.children[0].innerHTML;
	name=obj.parentNode.parentNode.children[1].innerHTML;
	grades=obj.parentNode.parentNode.children[2].innerHTML;
	tr_input="<tr id=\""+sec_id+"\"><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_in_id_input_change(this)\" placeholder=\"学号\" value="+id+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_in_name_input_change(this)\" placeholder=\"姓名\" value="+name+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_in_grade_input_change(this)\" placeholder=\"成绩\" value="+grades+"></td><td><button class=\"btn btn-sm btn-primary\" onclick=\"bt_ins_course_upgrade_stu_onclick2(this)\">确认</button></td></tr>"
    tr_warming="<tr><td><small class=\"text-danger\">.</small></td><td><small class=\"text-danger\">.</small></td><td><small class=\"text-danger\">.</small></td><td></td></tr>"

    obj.parentNode.parentNode.insertAdjacentHTML("afterend",tr_warming);
	obj.parentNode.parentNode.innerHTML = tr_input;
}
function bt_ins_course_upgrade_stu_onclick2(obj){
	sec_id_course_id=obj.parentNode.parentNode.parentNode.getAttribute('id');
	id=obj.parentNode.parentNode.children[0].children[0].value;
	name=obj.parentNode.parentNode.children[1].children[0].value;
	grades=obj.parentNode.parentNode.children[2].children[0].value;
	tr_="<tr id=\""+id+"\"><td>"+id+"</td><td>"+name+"</td><td>"+grades+"</td><td><button class=\"btn btn-sm btn-inverse\" onclick=\"bt_ins_course_upgrade_stu_onclick1(this)\">录入</button></td></tr>";

	$.post("../API/ins/upgradecoursestu/"+sec_id_course_id+"/"+id+"/"+grades+"",{},function(data){
	if(data=='成功'){
		//obj.setAttribute("class","btn btn-sm btn-default disabled");
			$next_del=$(obj.parentNode.parentNode.nextSibling);
			$next_del.remove();
			obj.parentNode.parentNode.innerHTML = tr_;
	}else{
		//$sourse.animate({backgroundColor:"#FB6C6C"});
		//this.attr("class","btn btn-block btn-lg btn-default disabled")
	}
	alert(data);
	});
}
//开课停课部分
function bt_ins_course_delete_onclick(obj) {
	title=obj.parentNode.parentNode.children[0].innerHTML;
	sec_id=obj.parentNode.parentNode.children[2].innerHTML;
	semester=obj.parentNode.parentNode.children[4].innerHTML;
	year=obj.parentNode.parentNode.children[3].innerHTML;
	$course=$(obj.parentNode.parentNode);
	if(window.confirm('你确定要停'+title+'课(ID：'+sec_id+' '+year+'年'+semester+'学期)吗？ 注意所有选课的学生均会被退课！')){
		$.post("../API/ins/delcourse/"+title+'/'+sec_id+'/'+semester+'/'+year+'/',{},function(data){
			if(data=='成功'){
				$course.remove();
			}
			alert(data);
		});
		//location.reload(true);	
		return true;
  	}
    else{
         return false;
    }
	}
function bt_ins_course_add_onclick(obj) {
	title=obj.parentNode.parentNode.children[0].innerHTML;
	course_id=obj.parentNode.parentNode.children[1].innerHTML;
	sec_id=obj.parentNode.parentNode.children[2].innerHTML;
	semester=obj.parentNode.parentNode.children[5].innerHTML;
	year=obj.parentNode.parentNode.children[4].innerHTML;

	//cid_sid_semester_year_building_room_times_week_weeks
	if(window.confirm('你确定要新增  课程ID:'+course_id+',课程段ID为:'+sec_id+' , 学期：'+semester+' '+year+'年的课程段吗？')){
		
		//alert(obj.parentNode.parentNode.id);
		//tr_="<tr tag=\"\"><td>"+title+"</td><td>"+sec_id+"</td><td>"+credits+"</td><td>"+year+"</td><td>"+semester+"</td><td>"+building+"</td><td>"+room+"</td><td>"+week_slot+"</td><td>"+week+"</td><td>"+time_slot+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_admin_section_del_onclick(this)\">删除</button></td></tr>";
		$.post("../API/ins/addcourse/"+course_id+"/"+sec_id+"/"+semester+"/"+year+"/",{},function(data){
			if(data=='成功'){	
				//obj.parentNode.parentNode.previousSibling.previousSibling.insertAdjacentHTML("afterend",tr_);
			}
			alert(data);
		});
		
		//return true;
	}
	else{
		return false;
	}
}
//教务员
function bt_admin_course_add_onclick(obj) {
	var objS = document.getElementById("admin_stu_course_selectSId");
    //可以获取到响应的选中项
    var dept_selected = objS.options[objS.selectedIndex].value;
    var dept_selected_name = objS.options[objS.selectedIndex].innerHTML;
	id=obj.parentNode.parentNode.children[0].children[0].value;
	title=obj.parentNode.parentNode.children[1].children[0].value;
	credits=obj.parentNode.parentNode.children[3].children[0].value;
	if(window.confirm('你确定要新增  课程ID:'+id+',课程名为:'+name+' , '+dept_selected_name+' '+credits+'学分的课程吗？')){
		
		//alert(obj.parentNode.parentNode.id);
		tr_="<tr tag=\""+dept_selected+"\"><td>"+id+"</td><td>"+title+"</td><td>"+dept_selected_name+"</td><td>"+credits+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_admin_course_del_onclick(this)\">删除</button></td><td><button class=\"btn btn-sm btn-info\" onclick=\"bt_admin_course_upgrade_onclick1(this)\">修改</button></td></tr>";
		$.post("../API/admin/addcourse/"+id+"/"+title+"/"+dept_selected_name+"/"+credits+"/",{},function(data){
			if(data=='成功'){	
				obj.parentNode.parentNode.previousSibling.previousSibling.insertAdjacentHTML("afterend",tr_);
			}
			alert(data);
		});

		return true;
	}
	else{
		return false;
	}
}
function bt_admin_course_del_onclick(obj){
	id=obj.parentNode.parentNode.children[0].innerHTML;
	title=obj.parentNode.parentNode.children[1].innerHTML;
	$course=$(obj.parentNode.parentNode);
	if(window.confirm('你确定要删除课程ID: '+id+', 名称为: '+title+'的课程吗？')){
		$.post("../API/admin/delcourse/"+id,{},function(data){
			if(data=='成功'){
				$course.remove();
			}
			alert(data);
		});
		//location.reload(true);	
		return true;
  	}
    else{
         return false;
    }
}
function bt_admin_course_upgrade_onclick1(obj) {
	dept_id=obj.parentNode.parentNode.getAttribute('tag');
	innerHTML_tmp=obj.parentNode.parentNode.innerHTML;
	id=obj.parentNode.parentNode.children[0].innerHTML;
	title=obj.parentNode.parentNode.children[1].innerHTML;
	dept_name=obj.parentNode.parentNode.children[2].innerHTML;
	credits=obj.parentNode.parentNode.children[3].innerHTML;
	tr_input="<tr tag=\""+dept_id+"\"><td><input type=\"text\" class=\"col-lg-2 form-control\" disabled=\"disabled\" oninput=\"\" placeholder=\"学号\" value="+id+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"\" placeholder=\"名称\" value="+title+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"\" placeholder=\"院系\" value="+dept_name+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"\" placeholder=\"学分\" value="+credits+"></td><td><button class=\"btn btn-sm btn-warning\" onclick=\"bt_admin_course_upgrade_ondecline(this)\">取消</button></td><td><button class=\"btn btn-sm btn-primary\" onclick=\"bt_admin_course_upgrade_onclick2(this)\">确认</button></td></tr>"
    tr_warming="<tr><td></td><td><small class=\"text-danger\">.</small></td><td></td><td><small class=\"text-danger\">.</small></td><td><small class=\"text-danger\">.</small></td><td></td></tr>"

	obj.parentNode.parentNode.innerHTML = tr_input;
}
function bt_admin_course_upgrade_ondecline(obj){
	obj.parentNode.parentNode.innerHTML=innerHTML_tmp;
}
function bt_admin_course_upgrade_onclick2(obj) {
	dept_id=obj.parentNode.parentNode.getAttribute('tag');
	id=obj.parentNode.parentNode.children[0].children[0].value;
	title=obj.parentNode.parentNode.children[1].children[0].value;
	dept_name=obj.parentNode.parentNode.children[2].children[0].value;
	credits=obj.parentNode.parentNode.children[3].children[0].value;

	tr_="<tr tag=\""+dept_id+"\"><td>"+id+"</td><td>"+title+"</td><td>"+dept_name+"</td><td>"+credits+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_admin_course_del_onclick(this)\">删除</button></td><td><button class=\"btn btn-sm btn-info\" onclick=\"bt_admin_course_upgrade_onclick1(this)\">修改</button></td></tr>";

	$.post("../API/admin/upgradecourse/"+id+"/"+name+"/"+dept_name+"/"+credits+"/",{},function(data){
	if(data=='成功'){
		//obj.setAttribute("class","btn btn-sm btn-default disabled");
			obj.parentNode.parentNode.innerHTML = tr_;
	}
	alert(data);
	});
}
//
function bt_admin_section_add_onclick(obj) {
	var objS = document.getElementById("admin_course_selectSId0");
    //可以获取到响应的选中项
    var course_selected = objS.options[objS.selectedIndex].value;
    var course_selected_name = objS.options[objS.selectedIndex].innerHTML;
	sec_id=obj.parentNode.parentNode.children[1].children[0].value;
	title=course_selected_name;
	credits=obj.parentNode.parentNode.children[2].children[0].value;
	year=obj.parentNode.parentNode.children[3].children[0].value;
	semester=obj.parentNode.parentNode.children[4].children[0].value;
	building=obj.parentNode.parentNode.children[5].children[0].value;
	room=obj.parentNode.parentNode.children[6].children[0].value;
	week_slot=obj.parentNode.parentNode.children[7].children[0].value;
	week=obj.parentNode.parentNode.children[8].children[0].value;
	time_slot=obj.parentNode.parentNode.children[9].children[0].value;

	//cid_sid_semester_year_building_room_times_week_weeks
	if(window.confirm('你确定要新增  课程ID:'+course_selected+',课程段ID为:'+sec_id+' , 学期：'+semester+' '+year+'年的课程段吗？')){
		
		//alert(obj.parentNode.parentNode.id);
		tr_="<tr tag=\"\"><td>"+title+"</td><td>"+sec_id+"</td><td>"+credits+"</td><td>"+year+"</td><td>"+semester+"</td><td>"+building+"</td><td>"+room+"</td><td>"+week_slot+"</td><td>"+week+"</td><td>"+time_slot+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_admin_section_del_onclick(this)\">删除</button></td></tr>";
		$.post("../API/admin/addsection/"+course_selected+"/"+sec_id+"/"+semester+"/"+year+"/"+building+"/"+room+"/"+time_slot+"/"+week+"/"+week_slot+"/",{},function(data){
			if(data=='成功'){	
				obj.parentNode.parentNode.previousSibling.previousSibling.insertAdjacentHTML("afterend",tr_);
			}
			alert(data);
		});
		
		//return true;
	}
	else{
		return false;
	}
}
function bt_admin_section_del_onclick(obj){
	title=obj.parentNode.parentNode.children[0].innerHTML;
	sec_id=obj.parentNode.parentNode.children[1].innerHTML;
	semester=obj.parentNode.parentNode.children[4].innerHTML;
	year=obj.parentNode.parentNode.children[3].innerHTML;

	$course=$(obj.parentNode.parentNode);
	if(window.confirm('你确定要删除课程段为: '+sec_id+',学期：'+semester+' '+year+'年的课程段:'+title+'吗？')){
		$.post("../API/admin/delsection/"+title+'/'+sec_id+'/'+semester+'/'+year+'/',{},function(data){
			if(data=='删除成功'){
				$course.remove();
			}
			alert(data);
		});
		//location.reload(true);	
		return true;
  	}
    else{
         return false;
    }
}
//
function bt_admin_add_stu_onclick(obj){
	var objS = document.getElementById("admin_stu_selectSId");
    //可以获取到响应的选中项
    var dept_selected = objS.options[objS.selectedIndex].value;
    var dept_selected_name = objS.options[objS.selectedIndex].innerHTML;
	id=obj.parentNode.parentNode.children[0].children[0].value;
	name=obj.parentNode.parentNode.children[1].children[0].value;
	credits=obj.parentNode.parentNode.children[4].children[0].value;
	//alert(obj.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute('id'));
	if(!id.match(/^[0-9]{8}$/)){
		alert('非法输入,学号必须是八位数字！');
		return true;
	}
	if(name==''){
		alert('姓名不能为空');
		return true;
	}
	if(credits!=''){
		if((!credits.match(/^\d{1,3}$/))){
			alert('非法输入！');
			return true;
		}
	}
	if(window.confirm('你确定要注册  学号:'+id+',姓名:'+name+' , '+dept_selected_name+' 的学生吗？')){
		//location.reload(true);
		var table=$('#stu_courses');
		var c=table.find('tr');
		//alert(obj.parentNode.parentNode.id);
		tr_="<tr tag=\""+dept_selected+"\"><td>"+id+"</td><td>"+name+"</td><td></td><td>"+dept_selected_name+"</td><td>"+grades+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_admin_del_stu_onclick(this)\">删除</button></td><td><button class=\"btn btn-sm btn-info\" onclick=\"bt_admin_upgrade_stu_onclick1(this)\">修改</button></td></tr>";
		$.post("../API/auth/register/stu/"+id+"/"+name+"/"+dept_selected_name+"/"+credits+"/",{},function(data){
			if(data=='注册完成'){	
				obj.parentNode.parentNode.previousSibling.previousSibling.insertAdjacentHTML("afterend",tr_);
			}
			alert(data);
		});

		return true;
  	}
    else{
         return false;
    }
}

function bt_admin_del_stu_onclick(obj){
	id=obj.parentNode.parentNode.children[0].innerHTML;
	name=obj.parentNode.parentNode.children[1].innerHTML;
	$course=$(obj.parentNode.parentNode);
	if(window.confirm('你确定要删除学号: '+id+',姓名: '+name+'的学生吗？')){
		$.post("../API/auth/unregister/stu/"+id,{},function(data){
			if(data=='删除成功'){
				$course.remove();
			}
			alert(data);
		});
		//location.reload(true);	
		return true;
  	}
    else{
         return false;
    }
}
var innerHTML_tmp;
function bt_admin_upgrade_stu_onclick1(obj){
	dept_id=obj.parentNode.parentNode.getAttribute('tag');
	innerHTML_tmp=obj.parentNode.parentNode.innerHTML;
	id=obj.parentNode.parentNode.children[0].innerHTML;
	name=obj.parentNode.parentNode.children[1].innerHTML;
	dept_name=obj.parentNode.parentNode.children[3].innerHTML;
	credits=obj.parentNode.parentNode.children[4].innerHTML;
	tr_input="<tr tag=\""+dept_id+"\"><td><input type=\"text\" class=\"col-lg-2 form-control\" disabled=\"disabled\" oninput=\"on_in_id_input_change(this)\" placeholder=\"学号\" value="+id+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_in_name_input_change(this)\" placeholder=\"姓名\" value="+name+"></td><td></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_in_id_input_change(this)\" placeholder=\"院系\" value="+dept_name+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_in_grade_input_change(this)\" placeholder=\"学分\" value="+credits+"></td><td><button class=\"btn btn-sm btn-warning\" onclick=\"bt_admin_upgrade_stu_ondecline(this)\">取消</button></td><td><button class=\"btn btn-sm btn-primary\" onclick=\"bt_admin_upgrade_stu_onclick2(this)\">确认</button></td></tr>"
    tr_warming="<tr><td></td><td><small class=\"text-danger\">.</small></td><td></td><td><small class=\"text-danger\">.</small></td><td><small class=\"text-danger\">.</small></td><td></td></tr>"

    obj.parentNode.parentNode.insertAdjacentHTML("afterend",tr_warming);
	obj.parentNode.parentNode.innerHTML = tr_input;
}
function bt_admin_upgrade_stu_ondecline(obj){
	$next_del=$(obj.parentNode.parentNode.nextSibling);
	$next_del.remove();
	obj.parentNode.parentNode.innerHTML=innerHTML_tmp;
}
function bt_admin_upgrade_stu_onclick2(obj){
	dept_id=obj.parentNode.parentNode.getAttribute('tag');
	id=obj.parentNode.parentNode.children[0].children[0].value;
	name=obj.parentNode.parentNode.children[1].children[0].value;
	dept_name=obj.parentNode.parentNode.children[3].children[0].value;
	credits=obj.parentNode.parentNode.children[4].children[0].value;

	tr_="<tr tag=\""+dept_id+"\"><td>"+id+"</td><td>"+name+"</td><td></td><td>"+dept_name+"</td><td>"+credits+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_admin_del_stu_onclick(this)\">删除</button></td><td><button class=\"btn btn-sm btn-info\" onclick=\"bt_admin_upgrade_stu_onclick1(this)\">修改</button></td></tr>";

	$.post("../API/admin/upgradestu/"+id+"/"+name+"/"+dept_name+"/"+credits+"/",{},function(data){
	if(data=='成功'){
		//obj.setAttribute("class","btn btn-sm btn-default disabled");
			$next_del=$(obj.parentNode.parentNode.nextSibling);
			$next_del.remove();
			obj.parentNode.parentNode.innerHTML = tr_;
	}
	alert(data);
	});
}

function bt_admin_upgrade_ins_onclick1(obj){
	dept_id=obj.parentNode.parentNode.getAttribute('tag');
	innerHTML_tmp=obj.parentNode.parentNode.innerHTML;
	id=obj.parentNode.parentNode.children[0].innerHTML;
	name=obj.parentNode.parentNode.children[1].innerHTML;
	dept_name=obj.parentNode.parentNode.children[2].innerHTML;
	salary=obj.parentNode.parentNode.children[3].innerHTML;
	tr_input="<tr tag=\""+dept_id+"\"><td><input type=\"text\" class=\"col-lg-2 form-control\" disabled=\"disabled\" oninput=\"on_in_id_input_change(this)\" placeholder=\"ID\" value="+id+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_in_name_input_change(this)\" placeholder=\"姓名\" value="+name+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_in_id_input_change(this)\" placeholder=\"院系\" value="+dept_name+"></td><td><input type=\"text\" class=\"col-lg-2 form-control\" oninput=\"on_salary_input_change_upgrade(this)\" placeholder=\"薪资\" value="+salary+"></td><td><button class=\"btn btn-sm btn-warning\" onclick=\"bt_admin_upgrade_ins_ondecline(this)\">取消</button></td><td><button class=\"btn btn-sm btn-primary\" onclick=\"bt_admin_upgrade_ins_onclick2(this)\">确认</button></td></tr>"
    tr_warming="<tr><td></td><td><small class=\"text-danger\">.</small></td><td><small class=\"text-danger\">.</small></td><td><small class=\"text-danger\">.</small></td><td></td></tr>"

    obj.parentNode.parentNode.insertAdjacentHTML("afterend",tr_warming);
	obj.parentNode.parentNode.innerHTML = tr_input;
}
function bt_admin_upgrade_ins_ondecline(obj){
	$next_del=$(obj.parentNode.parentNode.nextSibling);
	$next_del.remove();
	obj.parentNode.parentNode.innerHTML=innerHTML_tmp;
}
function bt_admin_upgrade_ins_onclick2(obj){
	dept_id=obj.parentNode.parentNode.getAttribute('tag');
	id=obj.parentNode.parentNode.children[0].children[0].value;
	name=obj.parentNode.parentNode.children[1].children[0].value;
	dept_name=obj.parentNode.parentNode.children[2].children[0].value;
	salary=obj.parentNode.parentNode.children[3].children[0].value;

	tr_="<tr tag=\""+dept_id+"\"><td>"+id+"</td><td>"+name+"</td><td>"+dept_name+"</td><td>"+salary+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_admin_del_ins_onclick(this)\">删除</button></td><td><button class=\"btn btn-sm btn-info\" onclick=\"bt_admin_upgrade_ins_onclick1(this)\">修改</button></td></tr>";

	$.post("../API/admin/upgradeins/"+id+"/"+name+"/"+dept_name+"/"+salary+"/",{},function(data){
	if(data=='成功'){
		//obj.setAttribute("class","btn btn-sm btn-default disabled");
			$next_del=$(obj.parentNode.parentNode.nextSibling);
			$next_del.remove();
			obj.parentNode.parentNode.innerHTML = tr_;
	}
	alert(data);
	});
}

function bt_admin_add_ins_onclick(obj){
	var objS = document.getElementById("admin_ins_selectSId");
    //可以获取到响应的选中项
    var dept_selected = objS.options[objS.selectedIndex].value;
    var dept_selected_name = objS.options[objS.selectedIndex].innerHTML;
	id=obj.parentNode.parentNode.children[0].children[0].value;
	name=obj.parentNode.parentNode.children[1].children[0].value;
	salary=obj.parentNode.parentNode.children[3].children[0].value;
	//alert(obj.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.getAttribute('id'));
	if(!id.match(/^[0-9]{8}$/)){
		alert('非法输入,ID必须是八位数字！');
		return true;
	}
	if(name==''){
		alert('姓名不能为空');
		return true;
	}
	if(salary!=''){
		if((!salary.match(/^\d{0,20}$/))){
			alert('非法输入！');
			return true;
		}
	}
	if(window.confirm('你确定要注册  ID:'+id+',姓名:'+name+' , '+dept_selected_name+' 的老师吗？')){
		//location.reload(true);
		var table=$('#stu_courses');
		var c=table.find('tr');
		//alert(obj.parentNode.parentNode.id);
		tr_="<tr tag=\""+dept_selected+"\"><td>"+id+"</td><td>"+name+"</td><td>"+dept_selected_name+"</td><td>"+salary+"</td><td><button class=\"btn btn-sm btn-danger\" onclick=\"bt_admin_del_ins_onclick(this)\">删除</button></td><td><button class=\"btn btn-sm btn-info\" onclick=\"bt_admin_upgrade_ins_onclick1(this)\">修改</button></td></tr>";
		$.post("../API/auth/register/ins/"+id+"/"+name+"/"+dept_selected_name+"/"+salary+"/",{},function(data){
			if(data=='注册完成'){	
				obj.parentNode.parentNode.previousSibling.previousSibling.insertAdjacentHTML("afterend",tr_);
			}
			alert(data);
		});

		return true;
  	}
    else{
         return false;
    }
}

function bt_admin_del_ins_onclick(obj){
	id=obj.parentNode.parentNode.children[0].innerHTML;
	name=obj.parentNode.parentNode.children[1].innerHTML;
	$course=$(obj.parentNode.parentNode);
	if(window.confirm('你确定要删除ID: '+id+',姓名: '+name+'的老师吗？')){
		$.post("../API/auth/unregister/ins/"+id,{},function(data){
			if(data=='删除成功'){
				$course.remove();
			}
			alert(data);
		});
		//location.reload(true);	
		return true;
  	}
    else{
         return false;
    }
}
//时间显示 function displayDate()
	var t = null;
	t = setTimeout(time,1000);
	function time()
	{
	clearTimeout(t);
	dt = new Date();
	var h=dt.getHours()
	var m=dt.getMinutes()
	var s=dt.getSeconds()
	var tp = document.getElementById("timePlace");
	result = dt.toLocaleDateString()+" "+dt.toLocaleTimeString()
	document.getElementById("time-display").innerHTML = "时间:"+h+"时"+m+"分"+s+"秒"
	t = setTimeout(time,1000); 
	} 
