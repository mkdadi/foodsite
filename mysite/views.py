from django.shortcuts import render,redirect
import models as md


hash = "gbgfadbvm@3y77*^dnbvfh!nhbvb"


def xor_strings(s):
    return "/".join(str(ord(a)^ord(b)) for a,b in zip(s,hash))


def num_to_pass(s):
    x = s.split("/")
    return "".join(chr(int(a)^ord(b)) for a,b in zip(x,hash))


def check_login_cookie(request):
    if request.COOKIES.get('login',0):
        if request.COOKIES.get('id',0):
            username=num_to_pass(str(request.COOKIES.get('id')))
            return [int(request.COOKIES['login']),username]
        else:
            return 0
    else:
        return 0


def homepage(request):
    context = {}
    x = check_login_cookie(request)
    if x is 0:
        context['loggedout'] = request.GET.get('loggedout',0)
        return render(request,'index.html',context)
    else:
        context['loggedin'] = x[0]
        context['username'] = x[1]
        if x[0] == 1:
            return render(request,'order.html',context)
        else:
            return render(request,'edit.html',context)


def userlogin(request):
    context = {}
    users = md.User.objects.filter(username=request.POST['username'])

    if len(users) == 1:
        user = users[0]
        if xor_strings(request.POST['password']) == user.password:
            response = redirect('/')
            response.set_cookie('login',1,max_age=365*24*60*60)
            response.set_cookie('id',xor_strings(user.username),max_age=365*24*60*60)
            return  response
        else:
            context['wrongupass'] = 1
    else:
        context['nouser'] = 1
    return render(request,'login.html',context)


def restaurantlogin(request):
    context = {}
    rests = md.Restaurant.objects.filter(id=request.POST['restid'])

    if len(rests) == 1:
        rest = rests[0]
        if xor_strings(request.POST['password']) == rest.password:
            response = redirect('/')
            response.set_cookie('login',2,max_age=365*24*60*60)
            response.set_cookie('id',xor_strings(rest.id),max_age=365*24*60*60)
            return response
        else:
            context['wrongrpass'] = 1
    else:
        context['norest'] = 1
    return render(request,'login.html',context)


def login(request):
    if check_login_cookie(request) is 0:
        if request.POST:
            if request.POST['login'] == '2':
                return restaurantlogin(request)
            else:
                return userlogin(request)
        else:
            return render(request,'login.html')
    else:
        return redirect('/')


def userregister(request):
    context = {}
    users=md.User.objects.filter(username=request.POST['username'])

    if len(users) == 0:
        if request.POST['password'] == request.POST['cpassword']:
            user=md.User()
            user.name = request.POST['name']
            user.contact = request.POST['contact']
            user.password = xor_strings(request.POST['password'])
            user.username = request.POST['username']
            user.save()
            response = redirect('/')
            response.set_cookie('login',1,max_age=365*24*60*60)
            response.set_cookie('id',xor_strings(user.username),max_age=365*24*60*60)
            return response
        else:
            context['wrongmatch'] = 1
    else:
        context['user'] = 1
    return render(request,'register.html',context)


def restaurantregister(request):
    context = {}
    rests=md.Restaurant.objects.filter(id=request.POST['id'])

    if len(rests) == 0:
        if request.POST['password'] == request.POST['cpassword']:
            rest=md.Restaurant()
            rest.name = request.POST['name']
            rest.password = xor_strings(request.POST['password'])
            rest.id = request.POST['id']
            rest.info = request.POST['info']
            rest.location = request.POST['location']
            rest.save()
            response = redirect('/')
            response.set_cookie('login',2,max_age=365*24*60*60)
            response.set_cookie('id',xor_strings(rest.id),max_age=365*24*60*60)
            return response
        else:
            context['wrongmatch'] = 2
    else:
        context['rest'] = 1
    return render(request,'register.html',context)


def register(request):
    context={}
    if check_login_cookie(request) is 0:
        if request.POST:
            if int(request.POST['register']) == 2:
                return restaurantregister(request)
            else:
                return userregister(request)
        else:
            return render(request,'register.html',context)
    else:
        return redirect('/')


def profile(request):
    x = check_login_cookie(request)
    if x is 0:
        return redirect('/login/')
    else:
        if x[0] == 1:
            users = md.User.objects.filter(username=x[1])
            user = users[0]
            context = {
                'login' : 1,
                'loggedin':1,
                'username':user.username,
                'name' : user.name,
                'contact' : user.contact,
            }

            return render(request,'profile.html',context)
        else:
            rests = md.Restaurant.objects.filter(id=x[1])
            rest = rests[0]
            context = {
                'login' : 2,
                'loggedin':1,
                'username':rest.id,
                'id':rest.id,
                'name' : rest.name,
                'info' : rest.info,
                'location' : rest.location,
            }

            return render(request,'profile.html',context)


def restaurants(request,restid="0"):
    if restid != "0":
        menu = md.Menu.objects.filter(restaurant_id=restid)
        rest = md.Restaurant.objects.filter(id=restid)

        items = []
        for x in menu:
            item = md.Item.objects.filter(name=x.item_id)
            for a in item:
                b=[]
                b.append(a.name)
                b.append(a.category)
                b.append(x.price)
                b.append(x.quantity)
                b.append(rest[0].status)
                b.append(x.id)
                items.append(b)

        context = {
            'items' : items,
            'loggedin':1,
            "username": check_login_cookie(request)[1],
            "restid":restid,
        }
        restid = "0"
        return render(request,'orders-list.html',context)

    else:
        rests = md.Restaurant.objects.filter(approved=True)
        search=request.GET.get('category',0)
        if search==0:
            context = {
                "rests" : rests,
                "loggedin" : 1,
                "username": check_login_cookie(request)[1],
            }
        else:
            items = md.Item.objects.filter(category__icontains=search)
            sitems = []
            srests = []
            for x in items:
                sitems.append(x)
                menu = md.Menu.objects.filter(item_id=x.id)
                for a in menu:
                    restaurants1 = md.Restaurant.objects.filter(name=a.restaurant_id)
                    for b in restaurants1:
                        srests.append(b)
            context = {
                "rests" : srests,
                "loggedin":1,
                "username": check_login_cookie(request)[1],
            }
        return render(request,'popular-Restaurents.html',context)


def logout(request):
    response = redirect('/?loggedout=1')
    response.delete_cookie('login')
    response.delete_cookie('id')
    return response
