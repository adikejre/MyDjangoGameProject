from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import AllMyScores

from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
from django.shortcuts import redirect
# Create your views here.

def game_pg(request,*args,**kwargs):
    return render (request,'allgames.html')

def snakegame(request,*args,**kwargs):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request,"snake_game.html")

class CustomLoginView(LoginView):
    template_name='login.html'
    fields='__all__'
    redirect_authenticated_user=True
    def get_success_url(self):
        return reverse_lazy('game_list')


class RegisteringPg(FormView):
    template_name='register.html'
    form_class=UserCreationForm
    redirect_authenticated_user=True
    success_url=reverse_lazy('game_list')
    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisteringPg,self).form_valid(form)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

# def snake_score(request,*args,**kwargs):
#
#     if(request.method=='POST'):
#         #if 'final_score' in request.POST:
#         my_score=request.POST['final_score']
#         print(my_score)
#         my_score=int(my_score)
#         my_obj=AllMyScores.objects.filter(game_title='snake',user=request.user)
#         print(my_obj)
#         print(my_obj.latest_score)
#         if(my_obj):
#             print('hi')
#             my_obj.latest_score=my_score
#             if(my_score>int(my_obj.max_score)):
#                 my_obj.max_score=my_score
#             my_obj.save()
#         else:
#             AllMyScores.objects.create(
#             user=request.user,
#             game_title='snake',
#             latest_score=my_score,
#             max_score=my_score,
#             )
#
#         return HttpResponse('success')
#     return HttpResponse('failed?!?')

def snake_score(request,*args,**kwargs):

    if(request.method=='POST'):
        #if 'final_score' in request.POST:
        my_score=request.POST['final_score']
        print(my_score)
        my_score=int(my_score)
        try:
            my_obj=AllMyScores.objects.get(game_title='snake',user=request.user)
            my_obj.latest_score=my_score
            if(my_score>int(my_obj.max_score)):
                my_obj.max_score=my_score
            my_obj.save()
        except:
            AllMyScores.objects.create(
            user=request.user,
            game_title='snake',
            latest_score=my_score,
            max_score=my_score,
            )

        return HttpResponse('success')
    return HttpResponse('failed?!?')




def list_of_scores(request):
    objs=AllMyScores.objects.filter(user=request.user)
    cntxt={
    "obs":objs
    }
    return render(request,'all_my_scores.html',cntxt)
