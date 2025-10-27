

# 💰 **PennyPal**

### Your Personal Finance Calendar App

---

##  **WHY?**
- See all your income, expenses, and balances clearly.  
- Understand your spending habits — how much goes to bills, food, entertainment, etc.  
- Make informed financial decisions instead of guessing.  
- Help stay on top of bills and deadlines.  
- See your expenses organized and easily spot them.  
- Track income and expenses to watch your net balance grow, set finance goals, and see progress weekly or monthly.  
- Build better habits and reduce stress.  

---

##  **MVP User Stories**
- As a new user, I want to **sign up** with name, email, password, and password confirmation so I can create an account.  
- As a registered user, I want to **sign in** so I can access my personal dashboard and calendar.  
- As a user, I want to **log out securely**.  
- As a user, I want to **create a new monthly calendar** by entering a month and year so I can track my finances.  
- As a user, I want to **view my full monthly calendar** to see daily spendings, bills, and credit dues.  
- As a user, I want to **click a day** on my calendar to see detailed spendings and due dates for that day.  
- As a user, I want to **navigate between months** to review past or upcoming spendings.  
- As a user, I want to **add a spending entry** (type, amount, note) to record expenses.  
- As a user, I want to **edit or delete** a spending entry to correct mistakes or remove items.  
- As a user, I want to **see the total amount spent** for the selected day.  
- As a user, I want to **add bills due dates** so I don’t forget payments.  
- As a user, I want to **add credit card due dates** to stay on top of payments.  
- As a user, I want to **see my due dates directly on my calendar** with color-coded markers.  
- As a user, I want to **view my monthly summary in a bar chart** to visualize total spendings, bills, and credit payments.  
- As a user, I want to **see my annual summary in a pie chart** showing yearly spending categories.  
- As a user, I want to **analyze my spending habits** through charts for better financial control.  

---

##  **Wireframes**
1. **Landing Page** – Logo + “Sign Up” / “Sign In” buttons  
2. **Sign Up Page**  
3. **Sign In Page**  
4. **Calendar Page** – Monthly grid with bills, credit, spendings  
5. **Day Details Page** – Table with spending list and add form  
6. **Monthly Summary Page** – Bar chart  
7. **Annual Summary Page** – Pie chart  

---

##  **API Endpoints**
| Endpoint | Method | Function | Description |
|-----------|--------|-----------|--------------|
| `/api/signup/` | POST | CreateUser | Register new user |
| `/api/login/` | POST | LoginUser | Authenticate user |
| `/api/logout/` | GET | LogoutUser | End session |
| `/api/calendar/` | GET | CalendarList | Get user calendars |
| `/api/calendar/create/` | POST | CalendarCreate | Add new calendar |
| `/api/calendar/<id>/` | GET | CalendarDetail | View one calendar |
| `/api/calendar/<id>/cell/<date>/` | GET | CellDetail | View spendings + dues for a date |
| `/api/entry/` | POST | EntryCreate | Add new spending |
| `/api/entry/<id>/edit/` | PUT | EntryUpdate | Edit spending |
| `/api/entry/<id>/delete/` | DELETE | EntryDelete | Delete spending |
| `/api/summary/monthly/` | GET | MonthlySummary | Return monthly totals |
| `/api/summary/annual/` | GET | AnnualSummary | Return annual totals |

---

##  **Database Schema**
###  User
| Field | Type | Relationship | Notes |
|--------|------|---------------|--------|
| id | AutoField | Primary Key | Unique user ID |
| username | CharField | — | Required, unique |
| email | EmailField | — | User’s email |
| password | CharField | — | Encrypted password |

###  Calendar
| Field | Type | Relationship | Notes |
|--------|------|---------------|--------|
| id | AutoField | Primary Key | — |
| user | ForeignKey(User) | One-to-Many | Each calendar belongs to one user |
| month | CharField | — | Example: “January” |
| year | IntegerField | — | Example: 2025 |

###  CalendarCell
| Field | Type | Relationship | Notes |
|--------|------|---------------|--------|
| id | AutoField | Primary Key | — |
| calendar | ForeignKey(Calendar) | One-to-Many | Each cell belongs to one calendar |
| date | DateField | — | Represents a single day |
| net_balance | DecimalField | — | Optional, calculated dynamically |

###  Entry
| Field | Type | Relationship | Notes |
|--------|------|---------------|--------|
| id | AutoField | Primary Key | — |
| calendar_cell | ForeignKey(CalendarCell) | One-to-Many | Each entry belongs to a day |
| category | CharField | — | Example: “Groceries”, “Transport” |
| amount | DecimalField | — | Amount spent |
| note | TextField | — | Optional |
| created_at | DateTimeField | — | Auto timestamp |

###  BillDue
| Field | Type | Relationship | Notes |
|--------|------|---------------|--------|
| id | AutoField | Primary Key | — |
| calendar_cell | ForeignKey(CalendarCell) | One-to-Many | Each bill belongs to a day |
| name | CharField | — | Example: “Rent”, “Electricity” |
| amount | DecimalField | — | Amount due |
| due_date | DateField | — | Bill due date |
| note | TextField | — | Optional |

###  CreditDue
| Field | Type | Relationship | Notes |
|--------|------|---------------|--------|
| id | AutoField | Primary Key | — |
| calendar_cell | ForeignKey(CalendarCell) | One-to-Many | Each credit belongs to a day |
| card_name | CharField | — | Example: “Amex”, “Chase” |
| amount | DecimalField | — | Amount due |
| due_date | DateField | — | Credit due date |
| note | TextField | — | Optional |

###  Summaries (Calculated)
| Summary Type | Data Source | Description |
|---------------|--------------|--------------|
| WeeklySummary | Entries + Bills + CreditDues | Aggregates totals by week |
| MonthlySummary | Entries + Bills + CreditDues | Aggregates totals by month |
| AnnualSummary | Entries grouped by category | Aggregates yearly spending |

---

##  Entity Relationships
| Entity | Description | Relationship |
|--------|--------------|---------------|
| User | Registered person | Has many Calendars |
| Calendar | Represents month/year | Belongs to one User |
| CalendarCell | Represents a day | Belongs to one Calendar |
| Entry | Spending record | Belongs to one CalendarCell |
| BillDue | Bill payment | Belongs to one CalendarCell |
| CreditDue | Credit card payment | Belongs to one CalendarCell |
| Summaries | Calculated | Generated via queries |

---

##  **Tech Stack**
| Category | Tools |
|-----------|--------|
| Frontend | React, Tailwind CSS, Recharts |
| Backend | Django REST Framework |
| Database | PostgreSQL |
| Deployment | Heroku (Backend), Netlify (Frontend) |
| Version Control | GitHub |
| Utilities | Figma, Postman, VS Code, Trello |

---


## **GITHUB**

https://github.com/MarjiRad/PennyPal-Backend.git
https://github.com/MarjiRad/PennyPal-Frontend.git


## **TRELLO**

https://trello.com/b/1yooqdM0/pennypal


