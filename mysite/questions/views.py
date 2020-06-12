from django.shortcuts import render,redirect
from .models import *
# Create your views here.
def tests(request):
    if not request.user.is_authenticated:
        return redirect("/")

    username = request.user
    login = 1
    return render(request, 'show_tests.html', {'user': username, "login": login})


def select_test(request):
    if not request.user.is_authenticated:
        return redirect("/")
    choices = {0: 'Chapter_wise',
                1: "Subject_wise",
                2:'Part_syllabus',
                3: 'Multi_sub',
                4: 'Full_length'}
    username = request.user
    login = 1
    ttype = request.POST.get('ttype',1)
    ttype = choices[ttype]
    print(ttype)
    total_tests = test.objects.all ()
    return render(request, 'select_test.html', {'user': username, "login": login,"ttype":ttype,"tests":total_tests})