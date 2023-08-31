web development project(s)

Following are four web development projects that explore basic functionality of the web. Starting off with database manipulation in "wiki" with the use of python and django. We host a site displaying articles from inside our database. Then with the same tech. building our own database models in 'commerce'. Followed by adding javascript to get a one page application 'mail'. This then culminating in building the app "pwee3ter", which is essentially a distillation of techniques learned in the prior projects.

The final project starts off by importing cs50's source code for 'network'. In this app we shamelessly take the popular X app as inspiration in order to build a social network. To do so, we'll need models in the database to store information. Django has a user model by default, but that alone - if left untempered with - does not suffice. Hence, why I added a model for user posts and for data related to follows. This is how we keep track of who wrote what, when it was posted, if there was an image attached, likes, dislikes, whether the post is editted or not, which users one might be following and so on. The source code came with login/logout and register functionality. For every other page, we'll need to add routes to the urls.py and functions to the views.py files. With django's syntax we'll hide and show elements in our HTML depending on whether the user is authenticated or not. Concerning HTML templates: almost every page builds on top of the layout.html file, this way the navigation menu is always visible.
I'm using 4 forms to get information from the user via the POST method. Python classes inheriting from "forms.Form". There's one for new posts, follows and unfollows as well as edits. Once the user has filled out the form, the posts can be seen on the index page and can be interacted with if the user is logged in.
It was a little tricky to allow for media to be attached to the post using the django development server, but I figured out how while doing the commerce app. Inside the settings.py file I added MEDIA_ROOT and MEDIA_URL and inside urls.py. Then import the 'static' function and add it to urls patterns. This way the MEDIA_URL is mapped to the MEDIA_ROOT making it so the development server knows where to find the image when a user requests the file.
Inside my backend (views.py) I handle the database changes with several python functions. There are functions for log-in/out, register as well as an index, profile page and for keeping track which accounts the user is following.

The challenge for this project was for like/dislike, follow/unfollow as well as editting posts to be updated in real-time. To make it feel like a one page application. You can see in the video I made on 'commerce' how clunky it feels when the page isn't immediately updated and the user has to refresh in order to see what has happened since the last time the page was loaded. We solve that problem here with the use of an API. The following backend functions are written in python: 'get_post' for looking up the post in question, 'update_post' for updating it and 'like_post' and 'dislike_post' for increasing or decreasing the likecount while we press the little thumbs up or down button. All of these functions also need a route in urls.py. To interact with these functions in real-time and to store the potentially newly given information, they are fetched and manipulated with javascript code which is hosted inside the static folder of the app. In the javascript code Eventlisteners look for clicks on specific buttons. Functions exist to change the (display) values of post related fields. 

My focus with these projects lay entirely with functionality. Little to no effort was put into making the projects look pleasant. 

None of the projects are being hosted live. However, as mentioned above there are video examples of each.

## wiki

###### this application is a very basic wikipedia clone. The user can browse existing pages of encyclopedia entries. It has a very rough implementation of a search engine to look for specific articles. Users can create new pages and edit existing ones and there's an option to view a random page.


[![wiki demonstration video](https://img.youtube.com/vi/xmjftXjjxC0/default.jpg)](https://www.youtube.com/watch?v=xmjftXjjxC0)

## commerce

###### the commerce app is similar to ebay, where users can list items of various categories to be auctioned off. The app uses Django models to store information inside a database. Users can browse all the available (open) auctions and bid on items they deem desirable. The owner of the auction has the ability to close the auction, making the highest bidder the winner. It's also possible to write comments on the listing page and add items to  a watchlist.

[![commerce demonstration video](https://img.youtube.com/vi/W1ZvzmVhEsU/default.jpg)](https://www.youtube.com/watch?v=W1ZvzmVhEsU)

## mail

###### In this one-page-mail-application users can interact with their inbox, sent mails and archive. It's possible to compose emails and send them to various recipients, reply to received emails as well as archive read emails.

[![mail demonstration video](https://img.youtube.com/vi/r09U2Rb_CRQ/default.jpg)](https://www.youtube.com/watch?v=r09U2Rb_CRQ)

## pwee3ter

###### pwee3ter is a twitter clone in which each user has a profile that allows for making posts which will be visible to other users. Users can follow other users and like or dislike their posts. Only 10 posts will be displayed per page (pagination). The owner of the posts is able to edit them if he so pleases.

[![pwee3ter demonstration video](https://img.youtube.com/vi/Ovrx9iZmqio/default.jpg)](https://www.youtube.com/watch?v=Ovrx9iZmqio)
