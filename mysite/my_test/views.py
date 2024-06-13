from django.shortcuts import render,redirect
from accounts.models import my_user as user
from .models import *
from questions.models import *
# Create your views here.
from django.http import HttpResponse


def redirect_if_not_login(request):
	if not request.user.is_authenticated:
		return redirect("/")
	
def index(request):
	login=0
	username= None
	if request.user.is_authenticated:
		username = request.user
		login = 1
		pass

	return render(request,'index.html',{'user':username,"login":login})

def add(request):
	n1 = int(request.POST['n1'])
	n2 = int(request.POST['n2'])
	n = n1+n2
	u1 = user()
	u1.name = "Vishwa"
	return render(request,'results.html',{"n":n, "user":u1})

def get_subjects_list(request):
	all_subs = subject.objects.all()
	return render(request,'subjects_list.html',{"subjects":all_subs})

def get_chapters_list(request):
	subject = request.GET['subject']
	all_subs = subject.objects.all()
	return render(request,'subjects_list.html',{"subjects":all_subs})


def get_topic(request):
	all_subs = subject.objects.all()
	return render(request,'subjects_list.html',{"subjects":all_subs})



def get_initial_topic_wise(request):
	
	return render(request,'topic_wise.html',{})


def step2(request):
	redirect_if_not_login(request)
	o1 = int(request.GET['o1'])
	ttype ="Not given"
	choices = ["Chapter_wise","Subject_wise","Part_syllabus","Multi_sub","Full_length"]
	ttype=choices[o1-1]
	if(o1 ==1):
		all_subs = subject.objects.all()
		pass
	elif(o1==2):
		all_subs = subject.objects.all()
		return render(request, 'step2.html', {"subjects": all_subs,"choice":o1})
		pass
		#display the filters and tests corresponding to them

	return render(request, 'step2.html', {"ttype":ttype})

def step3(request):
	redirect_if_not_login(request)
	username = request.user
	login = 1
	o1 = int(request.GET['o1'])
	sub = int(request.GET['sub'])
	diff = int(request.GET['diff'])
	ttype ="Not given"
	choices = ["Chapter_wise","Subject_wise","Part_syllabus","Multi_sub","Full_length"]
	#choices =select_test.objects.all()
	ttype=choices[o1-1]
	all_subs = subject.objects.all()
	diff_choices = ["Mixed","Easy", "Medium", "Hard", "VeryHard"]

	if(o1 ==1):
		all_subs = subject.objects.all()
		pass
	elif(o1==2):
		sub = all_subs[sub-1]
		diff = diff_choices[diff-1]
		my_tests = test.objects.filter(difficulty=diff,tsub=sub)
		taken = []
		for i in my_tests:
			tmp = test_result.objects.filter(test_id = i.test_id,user_id = username)
			if(len(tmp)>0):
				print(i.test_id,"taken")
				i.taken = 1
			else:
				print(i.test_id, "Not taken")
				i.taken = 0
			#
		print("Found",len(my_tests),"tests")

		return render(request, 'step3.html', {"my_tests":my_tests})
		pass
		#display the filters and tests corresponding to them

	return render(request, 'step3.html', {"my_tests":my_tests})

def tests(request):
	redirect_if_not_login(request)
	username = request.user
	login = 1
	tests = testtype.objects.all()
	#print("Test length is ",len(tests))
	#qids = test_questions.objects.find(test_id=tests[0].test_id)
	#print("Here",qids)
	return render(request, 'show_tests.html', {'user': username, "login": login,'types':tests})

def tests_v2(request):
	redirect_if_not_login(request)
	username = request.user
	login = 1
	tests = testtype.objects.all()
	return render(request, 'show_tests_v2.html', {'user': username, "login": login,'types':tests})

def start_test(request):
	redirect_if_not_login(request)
	username = request.user
	login = 1
	#id = int(request.GET['test_id'])
	id=1
	test_details = test.objects.filter(test_id=id)
	print("Found",len(test_details))
	print(len(test_details))
	test_details = test_details[0]
	return render(request,"test_page.html",{'user': username, "login": login,'test_details':test_details})
	pass

def get_question(request):
	redirect_if_not_login(request)
	username = request.user
	login = 1
	id = int(request.GET['test_id'])
	qno = int(request.GET['qno'])
	test_details = test.objects.filter(test_id=id)
	question = test_details[0].questions.all()[qno-1]
	return render(request, "question.html", {'question': question})

def store_result(request):
	redirect_if_not_login(request)
	username = request.user
	login = 1
	id = int(request.POST['test_id'])
	answers = request.POST.getlist('answers[]')
	test_details = test.objects.filter(test_id=id)
	questions = test_details[0].questions.all()
	n = len(answers)
	u = user.objects.only('email').get(email=username)
	t = test.objects.only('test_id').get(test_id=id)
	print(username)
	test_marks = 0
	for i in range(n):

		actual_sol = solution.objects.filter(q_id = questions[i].q_id)[0]
		q = question.objects.only('q_id').get(q_id=questions[i].q_id)
		tmp = test_responses(test_id=t,question_id=q,user_id = u)
		tmp.response = answers[i]
		tmp.correctness = (answers[i]==actual_sol.answer)
		print(q.attempts)
		q.attempts = q.attempts + 1
		print(q.attempts)
		if(tmp.correctness):
			tmp.mark= questions[i].marks
			test_marks += questions[i].marks
			q.correct_attempts = q.correct_attempts+1
		else:
			tmp.mark = questions[i].negative
			test_marks += questions[i].negative
		q.save()
		tmp.save()
	res = test_result(test_id = t,user_id = u)
	res.marks = test_marks
	res.save()
	return render(request, "success.html")

##The below is for the result analysis page

def view_result(request):
	redirect_if_not_login(request)
	username = request.user
	login = 1
	#id = int(request.GET['test_id'])
	#id=int(id[1:])
	id=1
	details = {}
	details["total"] = 25
	details["marks"] = 20
	details["positive"] = 22
	details["negative"] = -2
	details["total_questions"] = len(test.objects.filter(test_id=id)[0].questions.all())
	details["rank"] = test_result.objects.filter(marks__gt=1).count()+1
	details["attempted"] = details["total_questions"]-len(test_responses.objects.filter(test_id=id, user_id=username, response = "-"))
	details["correct"] = len(test_responses.objects.filter(test_id = id,user_id = username,correctness="True"))
	details["wrongly_attempted"] = len(test_responses.objects.filter(test_id=id, user_id=username, correctness="False"))
	details["accuracy"] = (100*details["correct"])/details["attempted"]
	return render(request, "view_result.html", {'user': username, "login": login, "details":details })

