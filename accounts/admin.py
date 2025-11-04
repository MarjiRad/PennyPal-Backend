
from django.contrib import admin
from .models import Profile, Category, Transaction


# ---------- PROFILE ----------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("created_at",)


# ---------- CATEGORY ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user")
    search_fields = ("name", "user__username")


# ---------- TRANSACTION ----------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "amount", "category", "date")
    search_fields = ("user__username", "category__name", "description")
    list_filter = ("type", "date")


# ---------- CALENDAR ----------
@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "month", "year")
    list_filter = ("year", "month")


# ---------- CALENDAR CELL ----------
@admin.register(CalendarCell)
class CalendarCellAdmin(admin.ModelAdmin):
    list_display = ("id", "calendar", "date", "total_expenses")
    list_filter = ("date",)


# ---------- BILL DUE ----------
@admin.register(BillDue)
class BillDueAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "amount", "due_date", "is_paid")
    search_fields = ("name", "user__username")
    list_filter = ("due_date", "is_paid")from
