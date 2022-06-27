from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random 

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def subPage(request, entry):
    markdowner = Markdown()
    content = util.get_entry(entry)
    if (content):
        return render(request, "encyclopedia/entrypage.html", {
        "entry": markdowner.convert(content)
    })
    else:
        return render(request, "encyclopedia/errorpage.html")

class searchForm(forms.Form):
    q = forms.CharField()
    
def search(request):
    query = request.GET.get('q')
    keyword = util.get_entry(query)

    if keyword is not None:
        return HttpResponseRedirect(reverse('entrypage', kwargs={'entry': query}))
    else:
        list = util.list_entries()
        result = []
        for l in list:
            if query.lower() in l.lower():
                result.append(l)
        return render(request, "encyclopedia/search.html", {
            "result": result
        })

class newpageForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.Textarea)
    content = forms.CharField(label='Content', widget=forms.Textarea)

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html", {
            'form':newpageForm()
        })

    elif request.method == "POST":
        form = newpageForm(request.POST)

        if form.is_valid():
            title = request.POST["title"]
            content = request.POST["content"]

            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/errorpage.html")
        
            else:
                util.save_entry(title, content)
                result = util.get_entry(title)
                return render(request, "encyclopedia/entrypage.html", {
                    "entry": result
                })


def randompage(request):
    keyword = random.choice(util.list_entries())
    result = util.get_entry(keyword)
    return render(request, "encyclopedia/entrypage.html", {
        "entry": result
    })