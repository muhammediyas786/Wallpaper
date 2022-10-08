from .models import *
import email
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models import F
from django.http import HttpResponseRedirect

# Create your views here.



# Signup,Login and Logout section start 

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(email,password)
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')
        else:
            messages.info(request,'credentials invalied !')
            return redirect('login')
    return render(request,'login.html')



def signup(request):
    if request.method == 'POST':
        
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        if password == password1:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken !')
                return redirect('signup')
            else:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already taken !')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                    upload_input = Uploadcount.objects.create(user=user)
                    upload_input.save()
                    return redirect('/')
        else:
            messages.info(request, 'password dose not match !')
            return redirect('signup')
    return render(request,'signup.html')





@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

# Signup,Login and Logout section end



@login_required(login_url='login')
def home(request, category_slug=None):
    user_profile=Profile.objects.filter(user=request.user)
    if request.method == 'POST':
        input_image=request.POST.get('image')
        input_user=request.POST.get('user')
        
        image_update =Wallpapers.objects.filter(uid=input_image)
        image = Wallpapers.objects.get(uid=input_image)
        user = User.objects.get(username=input_user)
        downloaded_count = Downloadcount.objects.filter(image=image)
        
        download = Downloaded.objects.create(user=user,image=image)
        download.save()
        
        downloaded_count.update(count_of_image_downloads = F('count_of_image_downloads') + 1)

        count=Downloadcount.objects.filter(image=image).values_list('count_of_image_downloads')
        image_update.update(download_count=count)
        return HttpResponseRedirect(request.path_info)
    else:
        
        if category_slug is not None:
            category_page = get_object_or_404(Category,category_slug=category_slug)
            images = Wallpapers.objects.filter(category=category_page)
        else:
            images = Wallpapers.objects.all()
        category_objects=Category.objects.all()
        context = {
            'profile':user_profile,
            'category':category_objects,
            'wallpapers':images,
        }
        return render(request,'index.html',context)




@login_required(login_url='login')
def details(request):
    user_profile=Profile.objects.filter(user=request.user)
    category = Category.objects.all()
    if request.method == 'POST':
        image_name = request.POST.get('image_name')
        image = request.FILES['image']
        category_slug = request.POST['category']
        category = Category.objects.filter(category_slug = category_slug)
        wallpaper = Wallpapers.objects.create(user=request.user,image=image,name=image_name)
        wallpaper.category.set(category)
        wallpaper.save()
        download_count = Downloadcount.objects.create(image=wallpaper)
        download_count.save()
        
        
        uploaded_count = Uploadcount.objects.filter(user=request.user)
        uploaded_count.update(count_of_image_uploads = F('count_of_image_uploads') + 1)


    return render(request,'details.html',{'profile':user_profile,'category':category,})






@login_required(login_url='login')
def search(request):
    user_profile=Profile.objects.filter(user=request.user)
    user_input=None
    search_keyword=None
    if 'searchKeyword' in request.GET:
        search_keyword=request.GET['searchKeyword']
        user_input=Profile.objects.all().filter(Q(firstname__contains=search_keyword)|Q(lastname__contains=search_keyword)|Q(bio__contains=search_keyword)) or User.objects.all().filter(Q(username__contains=search_keyword))
        if search_keyword == '':
            return redirect('/')
    return render(request,'search.html',{'profile':user_profile,'users':user_input})





@login_required(login_url='login')
def profile(request):
    user_profile = Profile.objects.filter(user=request.user)
    upload_count = Uploadcount.objects.filter(user=request.user)
    uploaded_wallpapers = Wallpapers.objects.filter(user=request.user)
    if request.method == 'POST':
        first_name=request.POST.get('firstname')
        sec_name=request.POST.get('secname')
        profile_image=request.FILES.get('profile_image')
        bio=request.POST.get('bio')
        user_profile.profile_image=profile_image
        print(profile_image)


        if user_profile:

            if profile_image:
                print('profile image')
                m = Profile.objects.get(user=request.user)
                m.profile_image = profile_image
                m.save()
                user_profile.update(user=request.user,firstname=first_name,lastname=sec_name,bio=bio)
                
            else:
                print('profile image nOT loded')
                user_profile.update(user=request.user,firstname=first_name,lastname=sec_name,bio=bio)

        else:
            user_profile.create(user=request.user,firstname=first_name,lastname=sec_name,profile_image=profile_image,bio=bio)
            
    context = {
        'upload_count': upload_count,
        'uploaded_wallpapers': uploaded_wallpapers,
        'profile': user_profile,
    }
    return render(request,'profile.html',context)



@login_required(login_url='login')
def streams(request):
    user_profile=Profile.objects.filter(user=request.user)

    most_downloaded_post = Downloadcount.objects.all().order_by('-count_of_image_downloads')
    latest_downloaded = Downloaded.objects.filter(user=request.user).order_by('-date')
    most_Uploaders = Uploadcount.objects.all().order_by('-count_of_image_uploads')

    context = {
        'profile':user_profile,
        'most_downloaded_post':most_downloaded_post,
        'latest_downloaded':latest_downloaded,
        'most_Uploaders':most_Uploaders,
        
    }
    return render(request,'streams.html',context)





@login_required(login_url='login')
def delete(request,pk):
    delt = Wallpapers.objects.get(uid=pk)
    delt.delete()
    uploaded_count = Uploadcount.objects.filter(user=request.user)
    uploaded_count.update(count_of_image_uploads = F('count_of_image_uploads') - 1)
    return redirect('profile')


@login_required(login_url='login')
def users_profile(request,pk):
    user_profile=Profile.objects.filter(user=request.user)
    user = User.objects.get(username=pk)
    searched_user_profile = Profile.objects.filter(user=user)
    
    upload_count = Uploadcount.objects.filter(user=user)
    uploaded_wallpapers = Wallpapers.objects.filter(user=user)

    context = {
        'profile':user_profile, 
        'searched_user':searched_user_profile,
        'upload_count': upload_count,
        'uploaded_wallpapers': uploaded_wallpapers,
    }
    return render(request,'users_profile.html',context)



