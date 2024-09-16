from django.db import models

class product(models.Model):
    image=models.ImageField(upload_to="media")
    name=models.CharField(max_length=30)
    category=models.CharField(max_length=20)
    cost=models.IntegerField()
    description=models.CharField(max_length=200)
    class Meta:
        db_table='product'

class users(models.Model):
    name=models.CharField(max_length=40)
    email=models.EmailField(max_length=20)
    password=models.CharField(max_length=10)
    class Meta:
        db_table='User'

class cart(models.Model):
    customer=models.ForeignKey(users,on_delete=models.CASCADE)
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    totalcost=models.IntegerField()
    class Meta:
        db_table='cart'

class payment(models.Model):
    payment_id=models.CharField(max_length=150)
    user=models.ForeignKey(users,on_delete=models.CASCADE)
    amount_paid=models.CharField(max_length=150)
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.payment_id

class orders(models.Model):                                                                             
    status =(('new','new'),('pending','pending'),('deliverd','delivered'),('cancelled','cancelled'))
    states = [('AP','Andhra Pradesh'),('Gj','Gujarat'),('MH','Maharastra'),('AS','Assam'),('RJ','Rajasthan'),('MP','Madhya Pradesh')]
    user = models.ForeignKey(users,on_delete= models.SET_NULL,blank=True,null =True)
    order_number = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=100,choices=status,default='new')
    city = models.CharField(max_length=100)
    total = models.IntegerField()
    status = models.CharField(max_length=100,choices = status,default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.user.name


class Order_product(models.Model):
    user = models.ForeignKey(users,on_delete=models.CASCADE)
    payment = models.ForeignKey(payment,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    pet_price = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

