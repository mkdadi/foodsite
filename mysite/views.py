from django.shortcuts import render
import models as md

hash="gbgfadbvm@3y77*^dnbvfh!nhbvb"

def homepage(request):
	context = {}
	return render(request,'index.html',context)


def userlogin(request):
	context = {}
	return render(request,'index.html',context)

def restaurantlogin(request):
	context = {}
	return render(request,'index.html',context)

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
