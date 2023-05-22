from django.contrib.auth.models import User
from django.db import models


# Create your models here.
STATE_CHOICE = (
    ('Abia', 'Abia'),
    ('Adamawa', 'Adamawa'),
    ('Akwa Ibom', 'Akwa Ibom'),
    ('Anambra', 'Anambra'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Bayelsa'),
    ('Benue', 'Benue'),
    ('Borno', 'Borno'),
    ('Cross River', 'Cross River'),
    ('Delta', 'Delta'),
    ('Ebonyi', 'Ebonyi'),
    ('Edo', 'Edo'),
    ('Ekiti', 'Ekiti'),
    ('Enugu', 'Enugu'),
    ('FCT - Abuja', 'FCT - Abuja'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Imo'),
    ('Jigawa', 'Jigawa'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Katsina', 'Katsina'),
    ('Kebbi', 'Kebbi'),
    ('Kogi', 'Kogi'),
    ('Kwara', 'Kwara'),
    ('Lagos', 'Lagos'),
    ('Nasarawa', 'Nasarawa'),
    ('Niger', 'Niger'),
    ('Ogun', 'Ogun'),
    ('Ondo', 'Ondo'),
    ('Osun', 'Osun'),
    ('Oyo', 'Oyo'),
    ('Plateau', 'Plateau'),
    ('Rivers', 'Rivers'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Taraba'),
    ('Yobe', 'Yobe'),
    ('Zamfara', 'Zamfara'),
)

CATEGORY_CHOICES = (
    ('EL', 'Electronics'),
    ('CL', 'Clothes'),
    ('FW', 'Footwears'),
    ('JW', 'Jewelries'),
    ('BG', 'Bags'),
    ('PH', 'Phones'),

)

CARD_CHOICES = (
    ('Gold', 'Gold'),
    ('White', 'White'),
)

CARD_TYPE_CHOICES = (
    ('Verve', 'Verve'),
    ('Visa', 'Visa'),
    ('Other','Other'),
)

DOMAIN_CHOICES = (
    ('International', 'International'),
    ('Local', 'Local'),
)


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    # brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE, max_length=100)
    gender = models.CharField(max_length=10)
    

    def __str__(self):
        return self.firstname


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.dicounted_price


class UserPaymentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    acct_number = models.CharField(max_length=15)
    cvv = models.PositiveIntegerField(default=0)
    age = models.IntegerField(default=1)
    marital_status = models.CharField(max_length=50)
    card_color = models.CharField(choices=CARD_CHOICES, max_length=50)
    card_type = models.CharField(choices=CARD_TYPE_CHOICES, max_length=100)
    domain = models.CharField(choices=DOMAIN_CHOICES, max_length=500)
    averageincomeexp = models.DecimalField(decimal_places=2, max_digits=12)
    card_expiry_date = models.CharField(max_length=500)
    card_digit = models.CharField(max_length=20)
    
    def __str__(self):
        return self.user.username 
    

class Intending_Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    time = models.DateTimeField(auto_now_add=True)
    # city = models.CharField(max_length=500)
              
    
    def __str__(self):
        return self.user.username
    
    
class FraudCasesAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username
    
class NonFraudCasesAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
