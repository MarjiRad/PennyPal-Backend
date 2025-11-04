from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ProfileSerializer,
    CategorySerializer,
    CalendarSerializer,
    CalendarCellSerializer,
    BillDueSerializer,
)
from accounts.models import Profile, Category, Transaction, Calendar, CalendarCell, BillDue
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from calendar import monthrange
from datetime import date, datetime
from django.db.models.functions import TruncMonth, Coalesce
from django.db.models import Sum, F, Value as V, DecimalField
from django.db import models


# -------------------- PROFILE & USER VIEWS -----------------------------------------------------------------------
class ProfileListView(generics.ListAPIView):
    """List all user profiles (admin or debugging only)."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserProfileView(generics.RetrieveAPIView):
    """Returns the profile of the current authenticated user."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user.profile


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    """Allows the user to update their profile info."""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

# -------------------- CATEGORY --------------------------------------------------------------------
class CategoryListCreateView(generics.ListCreateAPIView):
    """Create and list user-specific categories."""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# -------------------- TRANSACTIONS ----------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def total_expenses(request):
    """Return total expense amount for the logged-in user."""
    total = Transaction.objects.filter(user=request.user, type='expense').aggregate(Sum('amount'))
    return Response({"total_expenses": total['amount__sum'] or 0})

# -------------------- MONTHLY SUMMARY --------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def monthly_summary(request):
    """Return monthly income, expenses, and balance summary."""
    user = request.user

    transactions = (
        Transaction.objects
        .filter(user_id=user.id)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(
            total_income=Coalesce(
                Sum('amount', filter=models.Q(type='income')),
                V(0),
                output_field=DecimalField()
            ),
            total_expenses=Coalesce(
                Sum('amount', filter=models.Q(type='expense')),
                V(0),
                output_field=DecimalField()
            )
        )
        .annotate(net_balance=F('total_income') - F('total_expenses'))
        .order_by('-month')
    )

    return Response(transactions)

# -------------------- DAY VIEW --------------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def day_view(request, calendar_id, date_str):
    """View details (transactions + bills) for a specific date."""
    try:
        calendar = Calendar.objects.get(id=calendar_id, user=request.user)
    except Calendar.DoesNotExist:
        return Response({"error": "Calendar not found"}, status=404)

    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format (use YYYY-MM-DD)"}, status=400)

    transactions = Transaction.objects.filter(user=request.user, date=target_date)
    bills = BillDue.objects.filter(user=request.user, due_date=target_date)

    total_expenses = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expenses

    return Response({
        "date": target_date,
        "transactions": list(transactions.values('id', 'type', 'amount', 'category__name', 'description')),
        "bills": list(bills.values('id', 'name', 'amount', 'due_date')),
        "total_expenses": total_expenses,
        "total_income": total_income,
        "net_balance": net_balance,
    })

# -------------------- ANNUAL SUMMARY ---------------------------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def annual_summary(request):
    """Return total income, expenses, and net balance for the whole year."""
    user = request.user
    year = request.query_params.get('year', datetime.now().year)

    transactions = (
        Transaction.objects
        .filter(user=user, date__year=year)
        .values('category__name')
        .annotate(
            total_expenses=Coalesce(
                Sum('amount', filter=models.Q(type='expense')),
                V(0),
                output_field=DecimalField()
            ),
            total_income=Coalesce(
                Sum('amount', filter=models.Q(type='income')),
                V(0),
                output_field=DecimalField()
            )
        )
        .annotate(net_balance=F('total_income') - F('total_expenses'))
        .order_by('-total_expenses')
    )

    total_income_all = sum(t["total_income"] for t in transactions)
    total_expenses_all = sum(t["total_expenses"] for t in transactions)
    net_balance_all = total_income_all - total_expenses_all

    return Response({
        "year": year,
        "categories": list(transactions),
        "total_income": total_income_all,
        "total_expenses": total_expenses_all,
        "net_balance": net_balance_all
    })


# -------------------- CALENDAR ---------------------------------------------------------------------
class CalendarListCreateView(generics.ListCreateAPIView):
    """List all user calendars or create a new one."""
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        calendar = serializer.save(user=self.request.user)
        _, num_days = monthrange(calendar.year, calendar.month)
        for day in range(1, num_days + 1):
            CalendarCell.objects.create(calendar=calendar, date=date(calendar.year, calendar.month, day))


# -------------------- BILLS ------------------------------------------------------------------------
class BillDueListCreateView(generics.ListCreateAPIView):
    """List or create bills due for the current user."""
    serializer_class = BillDueSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return BillDue.objects.filter(user=self.request.user).order_by('due_date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)