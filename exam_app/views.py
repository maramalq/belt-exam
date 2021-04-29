from django.shortcuts import render, redirect
from .models import User, Wish
from django.contrib import messages
from datetime import date
import bcrypt 

def index(request):
    if 'uid' in request.session:
        return redirect('/wishes')
    context = {
        'today': date.today()
    }
    return render(request,"index.html",context)

def wishes(request):
    if 'uid' not in request.session:
        return redirect('/')

    this_user = User.objects.get(id=request.session['uid'])
    context = {
        'user' : User.objects.get(id=request.session['uid']),
        'all_users' : User.objects.all(),
        'all_wishes' : Wish.objects.all(),
        'your_wishes' : this_user.wishes_maded.all(),
        'user_wishes_granted' : Wish.objects.filter(granted=True)
    }
    return render(request, "wishes.html",context)

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()   
        print(pw_hash)
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        request.session['uid'] = new_user.id
        return redirect("/wishes")

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    
        user_list = User.objects.filter(email=request.POST['email'])
        if user_list:
            logged_user = user_list[0] 
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['uid'] = logged_user.id
                return redirect('/wishes')

    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')

def new_wish(request):
    return render(request, "new_wish.html")

def create_wishe(request):
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/new')

        this_user = User.objects.get(id=request.session['uid'])
        Wish.objects.create(
            name = request.POST['name'],
            desc = request.POST['desc'],
            made_by = this_user
        )
        return redirect('/wishes')

def delete_wish(request, wish_id):
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.delete()
    return redirect('/wishes')

def edit_wish(request, wish_id):
    this_user = User.objects.get(id=request.session['uid'])
    this_wish = Wish.objects.get(id=wish_id)
    context = {
        'the_wish' : this_wish,
        'the_user' : this_user
    }
    return render(request,"edit_wish.html",context)

def update_wish(request, wish_id):
    if request.method == "POST":
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/wishes/edit/{wish_id}')    
        
        this_wish = Wish.objects.get(id=wish_id)
        this_wish.name = request.POST['name']
        this_wish.desc = request.POST['desc']
        this_wish.save()
        return redirect('/wishes')

def granted_wish(request, wish_id):
    this_user = User.objects.get(id=request.session['uid'])
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.granted_by.add(this_user)
    this_wish.granted = True
    this_wish.save()
    return redirect('/wishes')

def liked_wish(request, wish_id):
    this_user = User.objects.get(id=request.session['uid'])
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.liked_by.add(this_user)
    this_wish.liked_count += 1
    this_wish.liked = True
    this_wish.save()
    return redirect('/wishes')

def unliked_wish(request, wish_id):
    this_user = User.objects.get(id=request.session['uid'])
    this_wish = Wish.objects.get(id=wish_id)
    this_wish.liked_by.remove(this_user)
    this_wish.liked_count -= 1
    this_wish.liked = False
    this_wish.save()
    return redirect('/wishes')

def stats(request, user_id):
    this_user = User.objects.get(id=request.session['uid'])
    pending_wishes = this_user.wishes_maded.all().count() - this_user.wishes_granted.all().count()
    context = {
        'user' : User.objects.get(id=request.session['uid']),
        'all_users' : User.objects.all(),
        'all_wishes' : Wish.objects.all(),
        'wishes_maded' : this_user.wishes_maded.all(),
        'wishes_granted' : this_user.wishes_granted.all(),
        'pending_wishes' : pending_wishes,
        'user_wishes_granted' : Wish.objects.filter(granted=True)

    }
    return render(request, "stats.html", context)
