from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django import forms
import markdown2
from random import choice

from . import util


class NewPage(forms.Form):
    """class used to make a new page"""
    # the fields that the form needs to have
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)  

    # a save button
    _ = forms.CharField(widget=forms.widgets.Input(attrs={"type": "submit", "value": "Add new page"}))


class EditPage(forms.Form):
    """class used to edit pages"""     
    title = forms.CharField(label="Title")    
    content = forms.CharField(label="Content", widget=forms.Textarea) 

    # edit button
    _ = forms.CharField(widget=forms.widgets.Input(attrs={"type": "submit", "value": "Edit page"}))
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wikipage(request, title):
    """loads the page of a given entry"""

    # returns a list of all the entries so far ["CSS", "Django", etc]
    entries = util.list_entries()

    for entry in entries:
        # if lowercase value in the list matches lowercase value of title, update that title to be that occurrence in the list
        if entry.lower() == title.lower():
            # if url was wiki/css, it will now use the title "css" as "CSS" instead to find the existing entry
            title = entry
    
    # Retrieves an encyclopedia entry by its title. If no such
    # entry exists, the function returns None.    
    enc_entry = util.get_entry(title) 

    # if there is an entry, render that page --- else render page not found
    if enc_entry:        
        return render(request, "encyclopedia/wikipage.html", {
            "title": title,
            # convert the markdown to html
            "enc_entry": markdown2.markdown(enc_entry),
            "edit_link": f"/wiki/{title}/edit"
        })
    else:
        return render(request, "encyclopedia/pagenotfound.html")   
                              
# testing variables with http response:
# return HttpResponse(f"test {title} these are the entries: {entries} and what about this {enc_entry}")


def search(request):
    """searches for existing entries in the database"""
    
    if request.method == "POST":

        # get access to the "q" field from the request and save it in a variable
        query = request.POST["q"]

        entries = util.list_entries()

        # check if query matches with entries, case insensitively
        for entry in entries:            
            if entry.lower() == query.lower():                
                query = entry

        # variable for existing entries
        enc_entry = util.get_entry(query)
        
        # if there's an exact match, render the wikipedia for said match
        if enc_entry:           
            return render(request, "encyclopedia/wikipage.html", {
                "title": query,
                "enc_entry": markdown2.markdown(enc_entry)
            })
        
        # if no exact match is found, search for partial matches, add them to a list
        else:                       
            search_results = []
            for entry in entries:
                if query.lower() in entry.lower():
                    search_results.append(entry)
            
            # render the search results list as links on the page
            return render(request, "encyclopedia/search.html", {
                "query": query,
                "search_results": search_results
            })
        
         
def create_page(request):
    """allows for user to create a new entry on the encyclopedia"""

    # create a form to make a new page using the newpage class
    form = NewPage()

    # get the user's input submitted via POST and validate input
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]            

            # first check if an entry already exists
            entries = util.list_entries()

            # check if query matches with any entries, case insensitively
            for entry in entries:          
                # if so, show error message  
                if entry.lower() == title.lower():                                                      
                    return render(request, "encyclopedia/create_page.html", {
                        "form": form,
                        "error": f"Page already exists"
                    })
            else:
                # otherwise save user input to disc
                util.save_entry(title, content)

                # and redirect to the page of the newly created entry
                return redirect("wiki:wikipage", title=title)
    
    # if method is get, show form
    else:
        return render(request, "encyclopedia/create_page.html", {
            "form": NewPage()    
        })
    

def edit_page(request, title):  
    """edits a wiki page"""     

    form = EditPage()   

    content = util.get_entry(title) 

    # add some validation so the user can't edit pages that don't exist
    if not content:
        return render(request, "encyclopedia/pagenotfound.html")

    # when user fills out the form (edits the page)
    if request.method == "POST":
        form = EditPage(request.POST) 

        if form.is_valid():
            content = form.cleaned_data["content"]
            # save/update the entry
            util.save_entry(title, content)   
            # redirect to page             
            return redirect("wiki:wikipage", title=title)
    else:
        # Display the form with the currently existing content as the initial value
        form = EditPage(initial={"title": title, "content": content})

    # upon GET request, initial page load:
    return render(request, "encyclopedia/edit_page.html", { 
        "title": title,           
        "form": form        
    })


def random_page(request):
    """loads a random page"""
    
    entries = util.list_entries()

    # if the database isn't empty, get a random entry from the list of entries
    if entries:
        randomentry = choice(entries)

    title = randomentry         
                 
    return redirect("wiki:wikipage", title=title)






            

    


        
            
        







            
 


