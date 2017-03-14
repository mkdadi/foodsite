from django.shortcuts import render,redirect
from collections import Counter
import models as md
import operator


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
            return orderhistory(request,x[1])#render(request,'order.html',context)
        else:
            return redirect(orderlist)


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

            if request.POST:
                status = int(request.POST['status'])

                if status == 1:
                    rest.status = md.Restaurant.REST_STATE_OPEN
                else:
                    rest.status = md.Restaurant.REST_STATE_CLOSED

                rest.save()

            context = {
                'login' : 2,
                'loggedin':2,
                'username':rest.id,
                'id':rest.id,
                'name' : rest.name,
                'info' : rest.info,
                'location' : rest.location,
                'approval':rest.approved,
            }

            if rest.status == md.Restaurant.REST_STATE_OPEN:
                context['open'] = 1
            else:
                context['open'] = 0

            return render(request,'profile.html',context)


def restaurants(request,restid="0"):
    z=check_login_cookie(request)
    if z == 0:
        return redirect('/login/')
    if z[0] == 2:
        return redirect('/')
    if restid != "0":
        menu = md.Menu.objects.filter(restaurant_id=restid)
        rest = md.Restaurant.objects.filter(id=restid)

        if len(rest) != 1:
            return redirect('/search/')

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
            "restname": rest[0].name,
            "restinfo": rest[0].info,
            "restlocation" : rest[0].location,
        }
        restid = "0"
        return render(request,'items-list.html',context)

    else:
        rests = md.Restaurant.objects.filter(approved=True)
        search=request.GET.get('category',0)
        placed = request.GET.get('placed',0)

        if search==0:
            context = {
                "rests" : rests,
                "loggedin" : 1,
                "username": z[1],
            }
            if placed:
                context['placed'] = 1
        else:
            items = md.Item.objects.filter(category__icontains=search)
            srests = []
            for x in items:
                menu = md.Menu.objects.filter(item_id=x.id)
                for a in menu:
                    restaurants1 = md.Restaurant.objects.filter(name=a.restaurant_id,approved=True)
                    for b in restaurants1:
                        if b not in srests:
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
    response.delete_cookie('cart')
    response.delete_cookie('rest')
    return response


def checkout(request):
    z=check_login_cookie(request)
    if z == 0:
        return redirect('/login/')
    if z[0] == 2:
        return redirect('/')
    if request.POST:
        addr = request.POST['address']
        oid = request.POST['oid']
        md.Order.objects.filter(id=int(oid)).update(delivery_addr = addr,
                                                    status=md.Order.ORDER_STATE_PLACED)

        return redirect('/search/?placed=1')

    else:
        cart = request.COOKIES['cart'].split(",")
        cart = dict(Counter(cart))
        items = []
        totalprice = 0
        uid = md.User.objects.filter(username=z[1])
        oid = md.Order()
        oid.orderedby = uid[0]
        oid.save()
        for x,y in cart.iteritems():
            item = []
            it = md.Menu.objects.filter(id=int(x))
            if len(it):
                oiid = md.OrderItems()
                oiid.item = it[0]
                oiid.quantity = int(y)
                oiid.oid = oid
                oiid.save()
                totalprice += int(y)*it[0].price
                item.append(it[0])
                it[0].quantity = it[0].quantity - y
                it[0].save()
                item.append(y)
                item.append(it[0].price*int(y))
                oid.restaurant_id = it[0].restaurant_id
            items.append(item)
        oid.total_amount = totalprice
        oid.save()
        context={
            "items" : items,
            "totalprice" : totalprice,
            "oid":oid.id,
            "loggedin":1,
            "username":z[1],
        }
        return render(request,'order.html',context)


def orderlist(request):

    z = check_login_cookie(request)

    if z==0:
        return redirect('/login/')

    if z[0] == 1:
        return redirect('/')


    if request.POST:
        oid = request.POST['orderid']
        select = request.POST['orderstatus']

        select = int(select)

        order = md.Order.objects.filter(id=oid)

        if len(order):
            x = md.Order.ORDER_STATE_WAITING
            if select == 1:
                x = md.Order.ORDER_STATE_PLACED
            elif select == 2:
                x = md.Order.ORDER_STATE_ACKNOWLEDGED
            elif select == 3:
                x = md.Order.ORDER_STATE_COMPLETED
            elif select == 4:
                x = md.Order.ORDER_STATE_DISPATCHED
            elif select == 5:
                x = md.Order.ORDER_STATE_CANCELLED
            else:
                x = md.Order.ORDER_STATE_WAITING
            order[0].status = x
            order[0].save()



    orders = md.Order.objects.filter(restaurant_id=z[1]).order_by('-timestamp')

    corders = []

    for order in orders:

        user = md.User.objects.filter(id=order.orderedby.id)

        user = user[0]
        corder = []
        corder.append(user.name)
        corder.append(user.contact)
        items_list = md.OrderItems.objects.filter(oid=order)

        items = []

        for item in items_list:
            citem = []
            citem.append(item.item)
            citem.append(item.quantity)
            menu = md.Menu.objects.filter(id=item.item.id)
            citem.append(menu[0].price*item.quantity)
            menu = 0
            items.append(citem)

        corder.append(items)
        corder.append(order.total_amount)
        corder.append(order.id)

        x = order.status

        if x == md.Order.ORDER_STATE_WAITING:
            continue
        elif x == md.Order.ORDER_STATE_PLACED:
            x = 1
        elif x == md.Order.ORDER_STATE_ACKNOWLEDGED:
            x = 2
        elif x == md.Order.ORDER_STATE_COMPLETED:
            x = 3
        elif x == md.Order.ORDER_STATE_DISPATCHED:
            x = 4
        elif x == md.Order.ORDER_STATE_CANCELLED:
            x = 5
        else:
            continue

        corder.append(x)
        corder.append(order.delivery_addr)

        corders.append(corder)

    context = {
        "loggedin":2,
        "username":z[1],
        "orders" : corders,
    }

    return render(request,"orders-list.html",context)


def edit(request):

    z = check_login_cookie(request)

    if z == 0:
        return redirect('/login/')

    if z[0] == 1:
        return redirect('/')

    rest = md.Restaurant.objects.filter(id=z[1])

    rest = rest[0]

    if request.POST:
        type = request.POST['submit']

        if type == "Modify":
            menuid = int(request.POST['menuid'])

            menu = md.Menu.objects.filter(id=menuid).\
                update(price=int(request.POST['price']),quantity=int(request.POST['quantity']))
        elif type == "Add":
            itemid = int(request.POST['item'])

            item = md.Item.objects.filter(id=itemid)
            item = item[0]

            menu = md.Menu()

            menu.item_id = item
            menu.restaurant_id = rest
            menu.price = int(request.POST['price'])
            menu.quantity = int(request.POST['quantity'])
            menu.save()
        else:
            menuid = int(request.POST['menuid'])
            menu = md.Menu.objects.filter(id=menuid)
            menu[0].delete()

    menuitems = md.Menu.objects.filter(restaurant_id=rest)

    menu = []

    for x in menuitems:
        cmenu = []

        cmenu.append(x.item_id)
        cmenu.append(x.price)
        cmenu.append(x.quantity)
        cmenu.append(x.id)

        menu.append(cmenu)

    menuitems = md.Item.objects.all()

    items = []

    for y in menuitems:
        citem = []
        citem.append(y.id)
        citem.append(y.name)

        items.append(citem)

    context = {
        "loggedin" :2,
        "username":z[1],
        "items":items,
        "menu":menu,
    }
    return render(request,'edit.html',context)


def orderhistory(request,username):

    users = md.User.objects.filter(username=username)

    context = {}

    if len(users) == 1:
        user = users[0]

        myorders = md.Order.objects.filter(orderedby=user)

        menus = []

        for myorder in myorders:

            if (myorder.status != md.Order.ORDER_STATE_WAITING
                and myorder.status != md.Order.ORDER_STATE_CANCELLED):
                items = md.OrderItems.objects.filter(oid=myorder)

                for item in items:
                    menus.append(item.item.id)


        if len(menus) > 0:

            menucount = dict(Counter(menus))
            maxmenu = max(menucount.iteritems(), key=operator.itemgetter(1))[0]

            suggestions = md.Menu.objects.filter(id=maxmenu)

            suggestion = suggestions[0]


            context["suggestionitem"] = suggestion.item_id
            context["suggestionrest"] = suggestion.restaurant_id
            context["suggestionrestid"] = suggestion.restaurant_id.id
            context["suggestion"] = 1

        else:
            context["suggestion"] = 0

        orders = md.Order.objects.filter(orderedby=user).order_by('-timestamp')

        corders = []

        for order in orders:
            rest = md.Restaurant.objects.filter(id=order.restaurant_id.id)

            rest = rest[0]
            corder = []
            corder.append(rest.name)
            items_list = md.OrderItems.objects.filter(oid=order)

            items = []

            for item in items_list:
                citem = []
                citem.append(item.item)
                citem.append(item.quantity)
                menu = md.Menu.objects.filter(id=item.item.id)
                citem.append(menu[0].price*item.quantity)
                menu = 0
                items.append(citem)

            corder.append(items)
            corder.append(order.total_amount)
            corder.append(order.id)

            x = order.status

            if x == md.Order.ORDER_STATE_WAITING:
                continue
            elif x == md.Order.ORDER_STATE_PLACED:
                x = 1
            elif x == md.Order.ORDER_STATE_ACKNOWLEDGED:
                x = 2
            elif x == md.Order.ORDER_STATE_COMPLETED:
                x = 3
            elif x == md.Order.ORDER_STATE_DISPATCHED:
                x = 4
            elif x == md.Order.ORDER_STATE_CANCELLED:
                x = 5
            else:
                continue

            corder.append(x)
            corders.append(corder)

        context["loggedin"] = 1
        context["username"] = username
        context["orders"] = corders

        return render(request,"orders-history.html",context)
