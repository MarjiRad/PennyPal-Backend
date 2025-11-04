
from django.contrib import admin
from .models import Profile, Category, Transaction, BillDue, Calendar, CalendarCell


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    search_fields = ("user__username", "user__email")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    search_fields = ("name", "user__username")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "amount", "type", "date")
    list_filter = ("type", "date")
    search_fields = ("user__username", "category__name")


@admin.register(BillDue)
class BillDueAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "amount", "due_date", "is_paid")
    list_filter = ("due_date", "is_paid")


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "month", "year")


@admin.register(CalendarCell)
class CalendarCellAdmin(admin.ModelAdmin):
    list_display = ("id", "calendar", "date", "total_expenses")