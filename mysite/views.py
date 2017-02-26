from django.shortcuts import render
import models as md

hash="gbgfadbvm@3y77*^dnbvfh!nhbvb"
def xor_strings(s):
    return "/".join(str(ord(a)^ord(b)) for a,b in zip(s,hash))

def num_to_pass(s):
	x=s.split("/")
	return "".join(chr(int(a)^ord(b)) for a,b in zip(x,hash))

def homepage(request):
    context = {}
    return render(request,'index.html',context)


def userlogin(request):
    context = {}
    users=md.User.objects.filter(username=request.POST['username'])

    if len(users) == 1:
        user=users[0]
        if xor_strings(request.POST['password']) == user.password:
            #TODO
            pass
        else:
            context['wrongupass'] = 1
    else:
        context['nouser'] = 1
    return render(request,'login.html',context)

def restaurantlogin(request):
    context = {}
    rests = md.Restaurant.objects.filter(id=request.POST['restid'])

    if len(rests) == 1:
        rest=rests[0]
        print xor_strings(request.POST['password'])
        if xor_strings(request.POST['password']) == rest.password:
            #TODO
            pass
        else:
            context['wrongrpass'] = 1
    else:
        context['norest'] = 1
    return render(request,'login.html',context)

def login(request):
    if request.POST:
        if request.POST['login'] == '2':
            return restaurantlogin(request)
        else:
            return userlogin(request)
    else:
        return render(request,'login.html')

def register(request):
    if request.POST:
        pass
    else:
        return render(request,'register.html')

def profile(request):
    pass

def viewrestaurants(request):
    pass
