from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.utils import timezone
from .forms import *
from .models import *

User = get_user_model()

# index_page
def home(request):
    # 로그인 안된 상태
    if not request.user.is_authenticated:
        return redirect('login')
    # 로그인 되었을때
    else:
        if len(Friend.objects.filter(current_user=request.user)) == 0:
            Friend.objects.create(current_user=request.user)
        users = User.objects.exclude(uid=request.user.uid)
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        promises = Promise.objects.all()
        user = request.user
        arrives = Party_detail.objects.filter(user=user, success_or_fail=1)
        no_arrives = Party_detail.objects.filter(user=user, success_or_fail=0)

        # 약속 알림
        noti_promise = Notification_promise.objects.filter(receive_user=user)

        # 친구 알림
        noti_add_friend = Notification_friend.objects.filter(receive_user=user)
        noti_wait_friend = []
        for wait in Notification_friend.objects.filter(send_user=user):
            noti_wait_friend.append(wait.receive_user.uid)

        return render(request, 'home.html', {'friends':friends, 'users':users, 'promises':promises, 
                                            'user':user, 'arrives':arrives, 'no_arrives':no_arrives, 
                                            'noti_add_friend':noti_add_friend, 'noti_wait_friend':noti_wait_friend,
                                            'noti_promise':noti_promise,})

# 모든 유저 검색페이지
def search(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else: 
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
        noti_wait_friend = []
        for wait in Notification_friend.objects.filter(send_user=request.user):
            noti_wait_friend.append(wait.receive_user.uid)
        qs = User.objects.all().exclude(uid=request.user.uid).exclude(uid='admin')

        q = request.GET.get('q', '') # GET request의 인자중에 q 값이 있으면 가져오고, 없으면 빈 문자열 넣기
        if q: # q가 있으면
            qs = qs.filter(name__icontains=q) # 제목에 q가 포함되어 있는 레코드만 필터링

        return render(request, 'search.html', {
            'user_list' : qs,
            'q' : q,
            'friends': friends,
            'noti_wait_friend': noti_wait_friend,
        })


# 디테일 보여주기
def detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    else: 
        promise = get_object_or_404(Promise ,pk=pk)
        cur_user = request.user

        # 댓글
        comments = promise.comments.all()
        commentform = Promise_CommentForm()

        # 도착여부
        success = Party_detail.objects.get(promise=promise, user=request.user)

        return render(request, 'detail.html', {'promise':promise, 'comments':comments, 'commentform':commentform, 'success': success, 'cur_user':cur_user })

# 댓글작성
def new_comment(request, promise_id):
    if not request.user.is_authenticated:
        return redirect('login')
    else: 
        if request.method == 'POST':
            form = Promise_CommentForm(request.POST)
            if form.is_valid():
                promise = Promise.objects.get(id=promise_id)
                comment = form.save(commit=False)
                comment.user = request.user
                comment.promise = promise
                comment.save()

                # 댓글 알림
                user = request.user
                parties = promise.party
                if promise.user.email == user.email:
                    for party in parties:
                        noti = Notification_promise()
                        noti.send_user = request.user
                        noti.receive_user = User.objects.get(email=party)
                        noti.promise = promise
                        noti.com_or_pro = 'c'
                        noti.save()
                else:
                    noti = Notification_promise()
                    noti.send_user = request.user
                    noti.receive_user = User.objects.get(email=promise.user.email)
                    noti.promise = promise
                    noti.com_or_pro = 'c'
                    noti.save()
                    for party in parties:
                        if party is user.email:
                            pass
                        else:
                            noti = Notification_promise()
                            noti.send_user = request.user
                            noti.receive_user = User.objects.get(email=party)
                            noti.promise = promise
                            noti.com_or_pro = 'c'
                            noti.save()

                return redirect('/promise/detail/'+str(promise_id))

# 댓글 삭제
def com_del(request, promise_id, comment_id):
    promise = get_object_or_404(Promise, id=promise_id)
    comment = promise.comments.get(id=comment_id)
    comment.delete()

    return redirect('/promise/detail/'+str(promise_id))

# 글쓰기
def new(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else: 
        if request.method == "POST":
            form = PromiseForm(request.POST)
            if form.is_valid():
                parties = request.POST.getlist('party_friend[]')
                promise = form.save(commit=False)
                promise.setting_date_time = request.POST['pic_date']
                promise.user = request.user
                promise.party = parties
                promise.latitude = float(request.POST['addr_lat'])
                promise.longitud = float(request.POST['addr_lng'])
                promise.save()

                # 약속 알림 보내기
                for party in parties:
                    noti = Notification_promise()
                    noti.send_user = request.user
                    noti.receive_user = User.objects.get(uid=party)
                    noti.promise = promise
                    noti.com_or_pro = 'p'
                    noti.save()

                # 참가자들의 성공여부를 저장하는 부분
                for party in parties:
                    p = Party_detail()
                    p.promise = promise
                    p.user = User.objects.get(uid=party)
                    p.save()
                p = Party_detail()
                p.promise = promise
                p.user = request.user
                p.save()

                return redirect('home')
        else:
            form = PromiseForm()
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()

            return render(request, 'new.html', {'form':form, 'friends':friends})

# 약속 삭제
def pro_del(request, promise_id):
    promise = get_object_or_404(Promise ,id=promise_id)
    promise.delete()

    return redirect('home')

# 친구추가, 해제 버튼
def change_friend(request, operation, pk):
    friend = User.objects.get(pk=pk)
    noti = Notification_friend.objects.filter(send_user=friend, receive_user=request.user)
    if operation == 'ok':
        Friend.make_friend(request.user, friend)
        Friend.make_friend(friend, request.user)
        noti.delete()
    elif operation == 'deny':
        noti.delete()
    # 친구삭제
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
        Friend.lose_friend(friend, request.user)

    return redirect('home')

# 약속알림 버튼
def noti_promise_button(request, operation, pk):
    noti = Notification_promise.objects.get(pk=pk)
    if operation == 'delete':
        noti.delete()
        return redirect('home')
    elif operation == 'click':
        promise_id = noti.promise.id
        noti.delete()
        return redirect('/promise/detail/'+str(promise_id))

# 도착이벤트
def arrived(request, promise_id):
    if request.method == 'POST':
        promise = Promise.objects.get(id=promise_id)
        cur_lat = request.POST['current_lat']
        cur_lng = request.POST['current_lng']
        max_lat = float(promise.latitude) + 0.0006
        min_lat = float(promise.latitude) - 0.0006
        max_lng = float(promise.longitud) + 0.0006
        min_lng = float(promise.longitud) - 0.0006
        if cur_lat != '' and cur_lng != '':
            if (min_lat <= float(cur_lat) and float(cur_lat) <= max_lat) and (min_lng <= float(cur_lng) and float(cur_lng) <= max_lng):
                party = Party_detail.objects.get(promise=promise_id, user=request.user)
                party.success_or_fail = 1
                party.arrived_time = timezone.now()
                party.save()

                messages.info(request, '성공적으로 도착하셨습니다.')

                # 모두 도착했는지 확인
                party_all = promise.party_detail.all()
                arr = 0
                for party_arr in party_all:
                    if party_arr.success_or_fail == 1:
                        arr += 1
                if arr == len(party_all):
                    promise.end = 1
                    promise.save()

                return HttpResponseRedirect('/promise/detail/'+str(promise_id))
            else:
                messages.info(request, '아직 장소에 도착을 하지 못하셨습니다.')
                return HttpResponseRedirect('/promise/detail/'+str(promise_id))
        else:
            messages.info(request, '위치가 제대로 확인되지 않았습니다.')
            return HttpResponseRedirect('/promise/detail/'+str(promise_id))
    else:
        return HttpResponse('오류')

# 친구신청 이벤트
def add_friend(request, pk):
    friend = User.objects.get(pk=pk)
    me = request.user
    add_friend = Notification_friend()
    add_friend.send_user = me
    add_friend.receive_user = friend
    add_friend.save()

    return redirect('/promise/search/?q='+request.GET.get('q_2', ''))

def aboutus(request):
    return render(request, 'aboutus.html')