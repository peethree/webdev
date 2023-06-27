from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from PIL import Image



class User(AbstractUser):
    # add more fields?
    pass


class Auction(models.Model):       
    title = models.CharField(max_length=75)    
    description = models.CharField(max_length=400)    
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)    
    date_posted = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="products")
    bid_number = models.IntegerField(default=0)   
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)    
    closed = models.BooleanField(default=False)
    winner = models.CharField(max_length=100, blank=True, default=None, null=True)
    category = models.CharField(max_length=30, default=None, null=True)   

    def __str__(self) -> str:
        return f"{self.title}, {self.description}"
        

class Bid(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()  
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return f"bid from {self.user_id} at {self.bid_time}"


class Comment(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    time_sent = models.DateTimeField()

    def __str__(self) -> str:
        return f'"{self.message}" commented by {self.user_id}'


class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)

