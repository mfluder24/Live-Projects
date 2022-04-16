# Live Project
# Introduction
During a two-week sprint, I was tasked to work on a Python live project, alongside several other students through Azure DevOps, to create an App via Django for users to store a collection of things. It was my first time working with such a large codebase, and it was thrilling to learn how to work alongside other developers, manage branches and merges, and assure that my code met established naming and style (PEP8) conventions. Creation of the App included several tasks that were new to me, which invited me to learn some new skills and techniques while continuing to practise those I had already learnt during my bootcamp. I worked on front end and back end stories, with an API, as well as web scraping via BeautifulSoup. I used Agile and Scrum methodology, with daily stand up meetings and regular virtual communication with my team and management. I found this a great introduction to working with a team from a remote workstation. 

Below are descriptions of the stories I worked on, as well as code snippets and screenshots of my finished app.

# INDEX
* [CRUD Functionality](#crud-functionality)
* [Web Scraping](#web-scraping)
* [API](#api)
* [Front End Development](#front-end-development)
* [Skills Acquired](#skills-acquired)


# CRUD Functionality
My App was created for a user to organise and manage their favourite fictional characters, including some basic information about each character. Within this App it was important to include CRUD functionality to organise and maintain the collection. 
I began by cloning the existing project repository onto my computer via PyCharm, Git, and Azure DevOps. While working on this project I used a virtual environment of Django 2.2.5, beautifulsoup4 4.8.0, and more. I began by creating a basic app, with a navbar, background, title and footer.

* **CREATE:**
In Story 2, I created the model for collecting data about each character entry, as well as a related table of what series they were from. I included several fields to give the user the ability to paint a complete picture of their character, including DND style alignments, and added a notes section for addition of anything the user felt was vital and not covered by the data fields. The Series model was used as a related table, with the series title as the foreign key. It enabled users to list the type of media the series was from (books, video games, films, etc) and list the creator of the series if they chose to. I added create pages and functions for both tables during this step.  


```
class Series(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=TYPES)
    creator = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


class Characters(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default='')
    gender = models.CharField(max_length=15, choices=GENDERS)
    species = models.CharField(max_length=50)
    skill = models.CharField(max_length=100)
    alignment = models.CharField(max_length=19, choices=ALIGNMENT, blank=True, null=True)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    notes = models.CharField(max_length=500, blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
```  


![Alt Text](https://i.imgur.com/fpNn2A1.gif)


* **READ:**
In Story 3 and Story 4 I focused on getting all of the information from the Characters model to display on a page for the user, as well as creating a page that listed all of the entries in the Characters database. For this, I created a function that displayed all of the data fields for each Character entry in an easily read format. Each Character was listed by name, and linked to the page extending their details.  


```
def list_characters(request):
    # Retrieves all entries from dB in alphabetical order by name
    char_sort = Characters.objects.order_by('name')
    return render(request,
    'FictionalCharacters/FictionalCharacters_View.html', {'chars': char_sort})
 
# Create a function to return character info based on primary key ID
def show_char(request, char_id):
    char = Characters.objects.get(pk=char_id)
    return render(request,
    'FictionalCharacters/FictionalCharacters_ShowChar.html', {'char': char}) 
```  


![Alt Text](https://i.imgur.com/XXAPZOK.gif)


* **UPDATE AND DELETE:**
In Story 5 I created an interface for users to edit Characters in the database, save those edits, or delete Characters completely. I also created a delete confirmation popup as a precaution in case the user accidentally summoned the delete function.  


```
# Create a function to allow and accept valid edits to the dB records
def edit_char(request, char_id):
    char = Characters.objects.get(pk=char_id)
    form = CharacterForm(request.POST or None, instance=char)
    if form.is_valid():
        form.save()
        return redirect('FictionalCharacters_View')
    return render(request,
    'FictionalCharacters/FictionalCharacters_Edit.html', {'char': char, 'form': form})

# Create a function to delete records from dB
def delete_char(request, char_id):
    char = Characters.objects.get(pk=char_id)
    char.delete()
    return redirect('FictionalCharacters_View')
```  


![Alt Text](https://i.imgur.com/PgLihaT.gif)  

* [Index](#index)

# Web Scraping
With Story 6 and Story 7, I set up Beautiful Soup to scrape the contents of [this article](https://www.scrolldroll.com/most-famous-fictional-characters-of-all-time/) for the names of the 'Most Famous Fictional Characters of All Time' as a fun addition to the App. The code presented an interesting challenge, as there was an issue where elements 6 & 7 in the scraped array displayed incorrectly, so I created additional code to join the two elements, delete the unneeded elements, and insert the proper one into the proper index of the array.  


```
def fc_soup(request):
    chars = []  # Character name list

    page = requests.get("https://www.scrolldroll.com/most-famous-fictional-characters-of-all-time/")
    soup = BeautifulSoup(page.content, 'html.parser')
    rankings = soup.find_all('strong')

    for i in rankings:
        rank = i.text.strip()
        chars.append(rank)
    l = chars[6], chars[7]  # Grabs the elements that need to be joined.
    fix = ' '.join(l)  # Joins the two elements and places them in a variable
    chars.insert(6, fix)  # Inserts joined elements into array at appropriate index
    del chars[8]  # Removes unnecessary element
    del chars[7]  # Removes unnecessary element

    context = {'chars': chars}
    return render(request, 'FictionalCharacters/FictionalCharacters_Soup.html', context)
```  


![Alt Text](https://i.imgur.com/G91udTU.gif)

* [Index](#index)

# API
In Story 6.5 and Story 7.5, I was tasked to connect to and utilise an API of my choice. In keeping with the theme of my App, I chose to use the [Love Calculator](https://rapidapi.com/ajith/api/love-calculator) API, so users could enter the name of two of their favourite characters into the calculator and see the results. I created a basic JSON response, and parsed through the results to assemble them into a template for the user to view.  


```
# Create a function that collects user input, uses the API, and delivers input to results page
def fc_calc(request):
    try:
        if request.method == 'POST':
            f = request.POST.get('fname')
            s = request.POST.get('sname')
            res = fc_api(f,s)
            context = {
                'fname': res['fname'],
                'sname': res['sname'],
                'percent': int(res['percentage']),
                'result': res['result'],
            }
            return render(request, 'FictionalCharacters/FictionalCharacters_Results.html', context={'data': context})
        return render(request,'FictionalCharacters/FictionalCharacters_API.html')
    except:
        return render(request, 'FictionalCharacters/FictionalCharacters_Error.html')

# Create a function to hold API code
def fc_api(f, s):
    url = "https://love-calculator.p.rapidapi.com/getPercentage"

    querystring = {"sname": s, "fname": f}

    headers = {
        "X-RapidAPI-Host": "love-calculator.p.rapidapi.com",
        "X-RapidAPI-Key": "your API key here"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    test = json.loads(response.text)
    print(response.text)

    return test
```  


 I also created three separate images to go along with the different responses determined by the percentage of compatibility from the results. I customised some styling of the pages to go along with the theme and add some extra engagement for the user.  
 
 
 ```
  {% if data.percent <= 50 %}
    <div class="FCSpace">
      <div class="FCAvatar">
          <img src="/static/FictionalCharacters/images/Characters_bad.png">
      </div>
    </div>

    It's a {{data.percent}}% match... <br/>
    {{data.result}}<br/>

    {% elif data.percent <= 75 and data.percent > 50 %}
    <div class="FCSpace">
      <div class="FCAvatar">
          <img src="/static/FictionalCharacters/images/Characters_okay.png">
      </div>
    </div>

    It's a {{data.percent}}% match! <br/>
    {{data.result}}<br/>

    {% elif data.percent <= 100 and data.percent > 75 %}
    <div class="FCSpace">
      <div class="FCAvatar">
          <img src="/static/FictionalCharacters/images/Characters_best.png">
      </div>
    </div>

    It's a {{data.percent}}% match!!! <br/>
    {{data.result}}!!!<br/>

    {% endif %}
 ```  
 
 
![Alt Text](https://i.imgur.com/nem7mNU.gif)
![Alt Text](https://i.imgur.com/uWzMb50.gif)  

* [Index](#index)

# Front End Development
With Story 8 I made some basic Front End Improvements to the overall App, including using CSS to create animated buttons and links, as well as the basic hovering image animation seen above on the API pages. I hid the scrollbars in the main content area of the pages as I felt they made it look 'clunky', and the information on the pages was cropped in a way that naturally encouraged users to attempt scrolling. On the Home page, I used some basic Javascript to display a random image from an array of four, just to add some extra visual stimulus to the page.  


```
  writeRandomQuote = function() {
    var quotes = new Array();
    quotes[0] = new Image();
    quotes[0].src = '/static/FictionalCharacters/images/Characters_hannibal.png';
    quotes[1] = new Image();
    quotes[1].src = '/static/FictionalCharacters/images/Characters_janeway.png';
    quotes[2] = new Image();
    quotes[2].src = '/static/FictionalCharacters/images/Characters_magua.png';
    quotes[3] = new Image();
    quotes[3].src = '/static/FictionalCharacters/images/Characters_scully.png';
    var rand = Math.floor(Math.random()*quotes.length);
    document.getElementById("fcquote").appendChild(quotes[rand]);
  }
  writeRandomQuote();
```  


![Alt Text](https://i.imgur.com/Ckv2M78.gif)

I also added a functioning Search bar, so users could search for a character in their collection by name, and link directly to their details page.  


```
# Create a function to list search results of Characters dB
def search_characters(request):
    if request.method == "POST":
        searched = request.POST['searched']
        chars = Characters.objects.filter(name__contains=searched)
        return render(request,
        'FictionalCharacters/FictionalCharacters_Search.html', {'searched': searched, 'chars': chars})
    else:
        return render(request,
        'FictionalCharacters/FictionalCharacters_Search.html', {})
```  


![Alt Text](https://i.imgur.com/ZbIq7Ww.gif) 

* [Index](#index)

# Skills Acquired
During this sprint, I gained a great deal of skill and appreciation for Project Management, and working on a large, established codebase with a team of several other developers. I found my understanding of Azure DevOps increased greatly, as well as my understanding of project flow, especially since I was working with people on the other side of the world in extremely different time zones. Working through stories gave me a solid understanding of working on tasks assigned to me and meeting deadlines. I found attending Daily Standups and weekly Code Retrospectives helped increase our connection as a team and gave us a good understanding of how the project was progressing. My comfort with and understanding of working with Version Control also improved during this project.  

My passion for researching new techniques and functions came in handy, as there was a lot of research to be done on this project! I found it all very beneficial and enjoyable, as it gave me a chance to really go into unknown territory on my own, build my knowledge, and come back to build my code. I developed a further sense of patience and diligence, and found that I was successfully able to debug most of my own roadblocks after doing some research and learning. When I wasn't able to figure it out on my own, I had a wonderful team there to provide assistance, and help get me moving again.  

I feel that my understanding of Django quadrupled during this project; I have a much stronger appreciation for it, and a better idea of what kind of Apps and websites can be built with Django.  

* [Index](#index)
