from ast import Delete
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import auth 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import upload,LikePost,FollowersCount,profile,saved
from itertools import chain
from django.http import Http404


@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user=user_object)

    user_following_list = []
    feed = []
    

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = upload.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))


    return render(request,"index.html",{'DP_profile':user_profile,'post':feed_list})


@login_required(login_url='signin')
def userfollowing(request):

    user_object = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user=user_object)

    user_following_list = []
    feed = []
    iduser= []
    

    user_following = FollowersCount.objects.filter(follower=request.user.username)
    for users in user_following:
        user_following_list.append(users.user)

    for user in user_following_list:
        id=User.objects.get(username=user)
        iduser.append(id)

    for usernames in iduser:
        feed_lists = profile.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    return render(request,"following.html",{'following':feed_list,'dp':user_profile})

@login_required(login_url='signin')
def follower(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user=user_object)
    
    user_following_list = []
    feed = []
    iduser= []
    

    user_following = FollowersCount.objects.filter(user=request.user.username)
    for users in user_following:
        user_following_list.append(users.follower)
        
    for user in user_following_list:
        id=User.objects.get(username=user)
        iduser.append(id)

    for usernames in iduser:
        feed_lists = profile.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    return render(request,"follower.html",{'follower':feed_list,'dp':user_profile})



@login_required(login_url='signin')
def post(request):
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        
        new_post = upload.objects.create(user=user,image=image, caption=caption,)
        new_post.save()

        return redirect('/')
        
    else:
        return redirect('/')

@login_required(login_url='signin')
def follows(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['users']
        
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

        
@login_required(login_url='signin')    
def likepost(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = upload.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')


def signup(request):

    if request.method == 'POST':

        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password == confirmpassword:

            if User.objects.filter(email=email).exists(): 
                messages.info(request,"Email Already Taken")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"Username Already Taken")
                return redirect('signup')       
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.first_name=firstname
                user.last_name=lastname
                user.save()

                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
 
                user_model=User.objects.get(username=username)
                new_profile=profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('account')
        else:
            messages.info(request,"password not matching")
            return redirect('signup')
 
    else:
        return render(request,"signup.html")


def signin(request):

    if request.method == 'POST':
                username = request.POST['username']
                password=password = request.POST['password']
                user=auth.authenticate(username=username,password=password)
                
                if user is not None:
                    auth.login(request,user)
                    return redirect('/')
                else:
                    messages.info(request,"Invalid")
                    return redirect('signin')
    else:
        return render(request,"signin.html")


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect(signin)



@login_required(login_url='signin')      
def account(request):
    user_profile=profile.objects.get(user=request.user)
    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image= user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']

            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        return redirect('account')

    return render(request,"account.html",{'user_profile':user_profile})


@login_required(login_url='signin')
def profile_account(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = profile.objects.get(user=user_object)
    user_posts = upload.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'



    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)



