
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from datetime import date


# ---------- PROFILE -------------------------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile when a new User is created."""
    if created:
        Profile.objects.create(user=instance)


# ---------- CATEGORY ------------------------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


# ---------- TRANSACTION ---------------------------------------------------------------
class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.type.capitalize()} - {self.amount} ({self.category})"


# ---------- CALENDAR ------------------------------------------------------------------
class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()  # 1–12
    year = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.month}/{self.year}"


# ---------- CALENDAR CELL -------------------------------------------------------------
class CalendarCell(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='cells')
    date = models.DateField()
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total_expenses(self):
        """Recalculate daily expenses based on related transactions."""
        from accounts.models import Transaction  # avoid circular import
        total = (
            Transaction.objects.filter(
                user=self.calendar.user,
                date=self.date,
                type='expense'
            ).aggregate(Sum('amount'))['amount__sum'] or 0
        )
        self.total_expenses = total
        self.save()

    def __str__(self):
        return f"{self.date} - {self.total_expenses}"


# ---------- BILL DUE ------------------------------------------------------------------
class BillDue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.due_date}"