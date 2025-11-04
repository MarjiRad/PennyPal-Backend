

from django.urls import path
from accounts.api.auth_views import RegisterView, SignInView
from accounts.api.views import (
    UserProfileView,
    ProfileListView,
    ProfileUpdateView,
    total_expenses,
    monthly_summary,
    annual_summary,
    day_view,
    CalendarListCreateView,
    BillDueListCreateView
)
from accounts.api.transaction_views import (
    CategoryListCreateView,
    TransactionListCreateView
)


urlpatterns = [
    # -------- AUTH --------
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),

    # -------- PROFILE --------
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),

    # -------- CATEGORIES & TRANSACTIONS --------
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/total-expenses/', total_expenses, name='total-expenses'),

    # -------- CALENDAR & BILLS --------
    path('calendar/', CalendarListCreateView.as_view(), name='calendar-list-create'),
    path('calendar/<int:calendar_id>/day/<str:date_str>/', day_view, name='day-view'),
    path('bills/', BillDueListCreateView.as_view(), name='bills-list-create'),

    # -------- SUMMARIES --------
    path('summary/monthly/', monthly_summary, name='monthly-summary'),
    path('summary/annual/', annual_summary, name='annual-summary'),
]
