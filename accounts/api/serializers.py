from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from accounts.models import Profile, Category, Transaction, Calendar, CalendarCell, BillDue


# ---------- USER -------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ---------- PROFILE ----------------------------------------------------------------
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'created_at']


# ---------- REGISTER (SIGNUP) ----------------------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ---------- LOGIN ----------------------------------------------------------------
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# ---------- CATEGORY ----------------------------------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'user']
        read_only_fields = ['user']


# ---------- TRANSACTION ----------------------------------------------------------------
class TransactionSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user',
            'amount',
            'type',
            'description',
            'date',
            'category',
            'category_id'
        ]
        read_only_fields = ['user', 'date']


# ---------- BILL DUE ----------------------------------------------------------------
class BillDueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDue
        fields = ['id', 'name', 'amount', 'due_date', 'is_paid']


# ---------- CALENDAR CELL ----------------------------------------------------------------
class CalendarCellSerializer(serializers.ModelSerializer):
    bills = serializers.SerializerMethodField()

    class Meta:
        model = CalendarCell
        fields = ['id', 'date', 'total_expenses', 'bills']

    def get_bills(self, obj):
        bills = BillDue.objects.filter(
            user=obj.calendar.user,
            due_date=obj.date
        )
        return BillDueSerializer(bills, many=True).data


# ---------- CALENDAR ----------------------------------------------------------------
class CalendarSerializer(serializers.ModelSerializer):
    cells = CalendarCellSerializer(many=True, read_only=True)

    class Meta:
        model = Calendar
        fields = ['id', 'month', 'year', 'cells']