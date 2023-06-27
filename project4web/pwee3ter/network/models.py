from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser): 
    pass
    

class Post(models.Model):    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add=True)     
    post_content = models.TextField()   
    image = models.ImageField(upload_to="pictures", blank=True)     
    likes = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    dislikes = models.ManyToManyField(User, blank=True, related_name='disliked_posts')
    edited = models.BooleanField(default=False)  
    likecount = models.IntegerField(default=0) 
    
    def serialize(self):
        likes = list(self.likes.values_list('username', flat=True))        

        return {
            "id": self.id,
            "post_time": self.post_time.strftime("%b %d %Y, %I:%M %p"),
            "post_content": self.post_content,            
            "likes": likes,  
            "likecount": self.likes.count(),          
            "edited": self.edited                    
        }
    

class Follow(models.Model):    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

