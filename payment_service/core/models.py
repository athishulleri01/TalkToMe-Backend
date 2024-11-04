from django.db import models

# Create your models here.
class Subscription(models.Model):
    user = models.IntegerField(null=False, blank=False)
    stripe_subscription_id = models.CharField(max_length=255)
    plan =  models.CharField(max_length=120, choices=[('monthly', 'Monthly'),('sixmonth', 'Sixmonth'), ('yearly', 'Yearly')])
    amount = models.IntegerField()
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    current_period_end = models.DateTimeField()
    
    