from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Post
from .advice_form import PostForm
from django.utils import timezone
from datetime import datetime
from django.shortcuts import redirect
from .maps_form import mapsForm
from .models import Rate
from .rate_forms import RateForm
from django.db.models import Count

# Create your views here.

def index(request):
    """
    Directs to index.html page
    **Template:**

    :template:`myapp/index.html`
    """
    return render_to_response('index.html')

def time(request):
    """
    Directs to time management homepage
    **Template:**
    :template:`myapp/time.html`
    """

    now = datetime.now()
    formatedDate = now.strftime("%H:%M:%S")
    return render(request, 'time.html', {
        'myDate': now
    })

def ratings_landing_page(request):
    """
    Directs to the landing page for Rate My Class

    **Template:**

    :template:`myapp/ratings_landing_page.html`
    """
    return render_to_response('ratings_landing_page.html')


def ratings_view_class(request):
        """
        Directs to view a posted video

        **Context**

        ``rates``
        An instance of :model:`myapp.Rates`.

        **Template:**

        :template:`myapp/view_video.html`
        """
        theClassRated= request.GET.get('classChoice', None);
        context = {};
        """This def is used to get all the eecs classes even if the rating view class def filters them"""
        choiceToFilter = Rate.objects.values('class_rated').distinct()
        if theClassRated and request.method == 'GET':
            if theClassRated == 'all':
                rates = Rate.objects.all()
                context.update({'rates': rates,'choiceToFilter': choiceToFilter})
            else:
                """This def is used to filter out the class that was chosen"""
                rates = Rate.objects.filter(class_rated=theClassRated)
                context.update({'rates': rates,'choiceToFilter': choiceToFilter})
        return render(request, 'ratings_view_class.html', context)

def advice(request):
    """
    Directs to advice homepage

    **Template:**

    :template:`myapp/advice.html`
    """
    return render_to_response('advice.html')

def upload_video(request):
    """
    Directs to upload video page

    **Template:**

    :template:`myapp/upload_video.html`
    """
    return render_to_response('upload_video.html')

def view_video(request):
    """
    Directs to view a posted video

    **Template:**

    :template:`myapp/view_video.html`
    """
    return render_to_response('view_video.html')

def view_advice(request):
    """
    Directs to view a posted video

    **Context**

    ``posts``
    An instance of :model:`myapp.Post`.

    **Template:**

    :template:`myapp/view_video.html`
    """
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'view_advice.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('view_advice.html#advice')
    else:
        form = PostForm()
    return render(request, 'post_new.html', {'form': form})



def rating_form(request):
    """
    Directs to the form for class rating

    **Template:**

    :template:`myapp/rating_form.html`
    """
    if request.method == "POST":
        form = RateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            class_rated=form.cleaned_data['class_rated']
            class_difficulty_level=form.cleaned_data['class_difficulty_level']
            class_hours_spent=form.cleaned_data['class_hours_spent']
            rater_grade=form.cleaned_data['rater_grade']
            class_exams_num=form.cleaned_data['class_exams_num']
            class_hw=form.cleaned_data['class_hw']
            class_comments=form.cleaned_data['class_comments']
            class_overall=form.cleaned_data['class_overall']
            print(class_rated,class_difficulty_level,class_hours_spent,rater_grade,class_exams_num,class_hw,class_comments,class_overall);
            post.save()
            return HttpResponseRedirect("ratings_view_class.html?classChoice=all")
    else:
        form = RateForm()
    return render(request, 'rating_form.html', {'form': form})
