from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2
from django.shortcuts import redirect
from random import randint


class NewWikiPage(forms.Form):
    title = forms.CharField(label="title")
    mdtext = forms.CharField(widget=forms.Textarea, label="Add Text",
                             initial="")


def entryChecker(title):
    for entry in util.list_entries():
        if title.casefold() == entry.casefold():
            return False
    return True


def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def edit(request, title):
    if request.method == "POST":
        form = NewWikiPage(request.POST)
        if form.is_valid():
            # to not change title we do not do the form.cleaned_data["title"]
            util.save_entry(title, form.cleaned_data["mdtext"])
            return HttpResponseRedirect(reverse("encyclopedia:wiki-page", args=(title, )))
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "form": form
            })
    md_edit = util.get_entry(title)
    edit_form = NewWikiPage(initial={"title": title, "mdtext": md_edit})
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": edit_form
    })


def create(request):
    if request.method == "POST":
        form = NewWikiPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            mdtext = form.cleaned_data["mdtext"]
            if entryChecker(title) == True:
                util.save_entry(title, mdtext)
                return HttpResponseRedirect(reverse("encyclopedia:wiki-page", args=(title, )))
            else:
                return render(request, "encyclopedia/create.html", {
                    "error": f'The entry {title} already exists.',
                    "form": form
                })

        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    form = NewWikiPage()
    return render(request, "encyclopedia/create.html", {
        "form": form
    })


def random(request):
    rand = randint(0, len(util.list_entries()) - 1)
    return HttpResponseRedirect(reverse("encyclopedia:wiki-page", args=(util.list_entries()[rand],)))


def wikipage(request, name):
    entry = util.get_entry(name)
    if entry is None:
        return render(request, "encyclopedia/NoFile.html", {
            "title": name
        })
    return render(request, "encyclopedia/wikipage.html", {
        "get_entry": markdown2.markdown(util.get_entry(name)),
        "title": name
    })


def search(request):
    value = request.GET.get('q', '')
    entry = util.get_entry(value)

    if entry is not None:
        return HttpResponseRedirect(reverse("encyclopedia:wiki-page", args=(value, )))

    else:
        results = []
        for entry in util.list_entries():
            if value.casefold() in entry.casefold():
                results.append(entry)

        return render(request, "encyclopedia/search.html", {
            "entries": results,
            "value": value
        })
