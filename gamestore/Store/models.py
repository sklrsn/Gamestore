from django.db import models
from django.contrib.auth.models import User
from GameArena.models import Game
import datetime

# Purchase information


"""
@Class_Name:
@Params: Payment Ref - Payment reference field
         Order_Date - Date the order was made
         Status - Status of the order
         Checksum - Check sum value

"""
class Order(models.Model):
    paymentRef = models.IntegerField(null=True, blank=True)
    order_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    status =  models.CharField(max_length=10, null=False, default="pending")
    checksum = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = "Order"
        ordering = ['order_date']


"""
@Class_Name: Purchase
@Params: game_details - Details pertaining to the game (Foreign Key)
         Player_Details - details of the player (Foreign Key)
         Cost - Cost associated with the game(s) of purchase
         Purchase_Date - date of  purchase (Foreign Key)
         order - Order ID

"""

class Purchase(models.Model):
    game_details = models.ForeignKey(Game, related_name='purchased_games', on_delete=models.CASCADE)
    player_details = models.ForeignKey(User, related_name='purchased_players', on_delete=models.CASCADE)
    cost = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    purchase_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    order = models.ForeignKey(Order, related_name = 'order_items', null=True, blank=True)

    class Meta:
        db_table = "Purchase"
        ordering = ['purchase_date']
    def shortdesc(self):
        if(len(self.game_details.description)>100):
            return self.game_details.description[0:100]+"..."
        else:
            return self.game_details.description

    def as_json_dict(self):
        res = {
            'game': self.game_details.id,
            'buyer': self.player_details.username,
            'cost': self.cost,
            'purchase_date': str(self.purchase_date),
            'orderid': self.order.id
        }
        return res

    def __str__(self):
        return self.game_details.name

"""
@Class_Name: Cart
@Params: game_details - Details of the game purhcased - Foreign Key
         Player_details - Player details ( Foreign Key)
         cart_Date - date of the cart - cart creation date
         order - order id (Foreign key)
"""

class Cart(models.Model):
    game_details = models.ForeignKey(Game, related_name='carted_games', on_delete=models.CASCADE)
    player_details = models.ForeignKey(User, related_name='carted_players', on_delete=models.CASCADE)
    cart_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
    order = models.ForeignKey(Order, related_name = 'order_cartitems', null=True, blank=True)
    class Meta:
        db_table = "Cart"
        ordering = ['cart_date']
    def __str__(self):
        return self.game_details.name
