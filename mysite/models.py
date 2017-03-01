from django.db import models

class User(models.Model):
	username = models.CharField(max_length=20,blank=False)
	name = models.CharField(max_length=30,blank=False)
	contact = models.CharField(max_length=15,blank=False)
	password = models.CharField(max_length=100,blank=False)

	def __unicode__(self):
		return self.username



class Restaurant(models.Model):
	id = models.CharField(max_length=20,blank=False,unique=True,primary_key=True)
	name = models.CharField(max_length=100,blank=False)
	password = models.CharField(max_length=100,blank=False)
	info = models.TextField()
	location = models.TextField()

	REST_STATE_CLOSED = "Closed"
	REST_STATE_OPEN = "Open"

	REST_STATE_CHOICES = (
		(REST_STATE_OPEN,REST_STATE_OPEN),
		(REST_STATE_CLOSED,REST_STATE_CLOSED)
	)

	status = models.CharField(max_length=50,choices=REST_STATE_CHOICES,default=REST_STATE_OPEN)
	approved = models.BooleanField(blank=False,default=False)


	def __unicode__(self):
		return self.name


class Order(models.Model):
	id = models.IntegerField(blank=False)
	id = models.AutoField(primary_key=True)
	total_amount = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now_add=True)
	delivery_addr = models.CharField(max_length=50,blank=True)
	orderedby = models.ForeignKey(User)
	restaurant_id = models.ForeignKey(Restaurant)
	ORDER_STATE_WAITING = "Waiting"
	ORDER_STATE_PLACED = "Placed"
	ORDER_STATE_ACKNOWLEDGED = "Acknowledged"
	ORDER_STATE_COMPLETED = "Completed"
	ORDER_STATE_CANCELLED = "Cancelled"
	ORDER_STATE_DISPATCHED = "Dispatched"

	ORDER_STATE_CHOICES = (
		(ORDER_STATE_WAITING,ORDER_STATE_WAITING),
	    (ORDER_STATE_PLACED, ORDER_STATE_PLACED),
	    (ORDER_STATE_ACKNOWLEDGED, ORDER_STATE_ACKNOWLEDGED),
	    (ORDER_STATE_COMPLETED, ORDER_STATE_COMPLETED),
	    (ORDER_STATE_CANCELLED, ORDER_STATE_CANCELLED),
	    (ORDER_STATE_DISPATCHED, ORDER_STATE_DISPATCHED)
	)
	status = models.CharField(max_length=50,choices=ORDER_STATE_CHOICES,default=ORDER_STATE_WAITING)

	def __unicode__(self):
		return str(self.id)+' '+self.status


class Item(models.Model):
	id = models.IntegerField(blank=False)
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100,blank=False)
	category = models.CharField(max_length=50,blank=False)

	def __unicode__(self):
		return  self.name


class Menu(models.Model):
	id = models.IntegerField(blank=False)
	id = models.AutoField(primary_key=True)

	item_id = models.ForeignKey(Item)
	restaurant_id = models.ForeignKey(Restaurant)

	price = models.IntegerField(blank=False)
	quantity = models.IntegerField(blank=False,default=0)

	def __unicode__(self):
		return self.item_id.name+' - '+str(self.price)



class OrderItems(models.Model):
	id = models.IntegerField(blank=False)
	id = models.AutoField(primary_key=True)
	item = models.ForeignKey(Menu)
	oid = models.ForeignKey(Order)
	quantity = models.IntegerField(blank=False)

	def __unicode__(self):
		return str(self.id)
