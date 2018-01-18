from django.shortcuts import render ,redirect

from user.forms import RegisterForm,LoginForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            request.session['uid'] = user.id
            return redirect('/user/info/')
        else:
            return render(request,'register.html',{'errors':form.errors})
    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user,passed = form.chk_password()
            if passed:
                request.session['uid'] = user.id
                return redirect('/user/info/')
            else:
                return render(request,'login.html',{'errors':form.errors})
    return render(request,'login.html')

def logout(request):
    request.session.flush()
    return redirect('/post/home/')

def info(request):
    user = getattr(request,'user',None)
    if user is None:
        return redirect('/user/login/')
    else:
        return render(request,'info.html',{'user':request.user})





