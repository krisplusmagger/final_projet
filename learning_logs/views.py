from django.shortcuts import render, redirect

from .models import Topic, Entry 

from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    #topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            #form.save()
            #重定向到topics
            return redirect('learning_logs:topics')    
    
    #显示空表单或指出表单数据无效
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html',context)   
@login_required
def edit_entry(request, entry_id):
    """在特定主题中添加新条目"""      
    entry = Entry.objects.get(id=entry_id)   
    topic = entry.topic 
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)

    else:
        #表单提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    # 显示空表单或指出表单数据无效
    context = {'entry': entry, 'topic': topic, 'form': form }
    return render(request, 'learning_logs/edit_entry.html',context)            

    