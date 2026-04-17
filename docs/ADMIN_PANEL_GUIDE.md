# SmartScreen Admin Panel - Setup & Usage Guide

## Overview
The Admin Panel is a secure management interface for administrating the SmartScreen SaaS platform. It allows admins to:
- Create, edit, and delete other admin accounts
- View system statistics and usage metrics
- Manage users and billing
- Monitor transactions and revenue

---

## 🚀 Quick Start

### Step 1: Create the First Admin Account

Run the admin seed script to create your first admin account:

```bash
# From the project root directory
python create_admin_seed.py
```

The script will prompt you to:
1. Enter admin email address
2. Enter admin password (min 6 characters)
3. Confirm the password

**Example:**
```
Enter admin email: admin@smartscreen.com
Enter admin password (min 6 characters): YourSecurePassword123
Confirm password: YourSecurePassword123
```

### Step 2: Access the Admin Panel

1. Navigate to: `http://localhost:3000/admin-login`
2. Enter your admin email and password
3. Click "Login"

You'll be redirected to the Admin Dashboard.

---

## 📊 Admin Dashboard

The Admin Dashboard displays key system statistics:

- **Total Users**: Number of regular users in the system
- **Admin Accounts**: Number of admin users
- **Credits Sold**: Total credits purchased (in units)
- **Total Transactions**: Number of billing transactions
- **Revenue**: Calculated from credits sold (Credits × ₹0.50)

### Quick Actions
- **Manage Admins**: Create, edit, or delete admin accounts
- **View Users**: See all registered users (coming soon)
- **Transactions**: View all billing transactions (coming soon)
- **Settings**: System configuration (coming soon)

---

## 👨‍💼 Admin Management

### Create a New Admin

1. Click "Create New Admin" button
2. Enter the admin email address
3. Enter a secure password (min 6 characters)
4. Click "Create"

**Important**: New admins receive immediate access to the admin panel.

### Edit Admin Account

1. Find the admin in the list
2. Click the "Edit" (✏️) button
3. Update the email and/or password
4. Click "Update"

**Note**: Leave the password field empty if you don't want to change it.

### Delete Admin Account

1. Find the admin in the list
2. Click the "Delete" (🗑️) button
3. Confirm the deletion

**Safety Features**:
- Cannot delete your own account (self-deletion prevention)
- Requires confirmation before deletion
- Deleted accounts cannot be recovered

---

## 🔐 Security Features

### Role-Based Access Control (RBAC)
- Only users with `admin` role can access admin endpoints
- All admin operations are protected with JWT authentication
- Attempted unauthorized access returns 403 Forbidden

### Password Security
- Passwords are hashed using Argon2 algorithm
- Plaintext passwords are never stored
- Password verification happens during login

### Token-Based Authentication
- JWT tokens include user ID, email, and role
- Tokens expire after 24 hours
- Token validation happens on every admin request

---

## 📱 API Endpoints

All admin endpoints are prefixed with `/api/v1/admin` and require a valid JWT token.

### Get Statistics
```
GET /api/v1/admin/stats
Response: {
  "total_users": 150,
  "total_admins": 2,
  "total_credits_sold": 5000,
  "total_transactions": 45,
  "recent_signups": 12
}
```

### List All Admins
```
GET /api/v1/admin/list
Response: [
  {
    "id": "admin-uuid-1",
    "email": "admin@example.com",
    "created_at": "2024-01-15T10:30:00",
    "full_name": null
  }
]
```

### Get Specific Admin
```
GET /api/v1/admin/{admin_id}
Response: {
  "id": "admin-uuid",
  "email": "admin@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### Create New Admin
```
POST /api/v1/admin/create
Body: {
  "email": "newadmin@example.com",
  "password": "SecurePassword123"
}
Response: {
  "id": "new-admin-uuid",
  "email": "newadmin@example.com",
  "created_at": "2024-01-20T14:25:00"
}
```

### Update Admin
```
PUT /api/v1/admin/{admin_id}
Body: {
  "email": "updated@example.com",  // optional
  "password": "NewPassword123"      // optional
}
Response: {
  "id": "admin-uuid",
  "email": "updated@example.com",
  "created_at": "2024-01-15T10:30:00"
}
```

### Delete Admin
```
DELETE /api/v1/admin/{admin_id}
Response: {
  "message": "Admin deleted successfully"
}
```

---

## 🔧 Database Schema

### Admin Table
The `users` table in the database stores all users including admins.

**Key Fields**:
- `id` (UUID): Unique identifier for the user
- `email` (String): Email address (unique)
- `hashed_password` (String): Argon2 hashed password
- `role` (String): User role - "user" or "admin"
- `credits` (Integer): Credit balance (0 for admins)
- `created_at` (DateTime): Account creation timestamp

---

## 📝 Admin Best Practices

### Password Policy
✅ Use strong passwords (min 8 characters)
✅ Include uppercase and lowercase letters
✅ Include numbers and special characters
✅ Change passwords regularly
❌ Don't share admin passwords
❌ Don't use common/dictionary words

### Account Management
✅ Create separate admin accounts for each administrator
✅ Delete unused admin accounts
✅ Review admin list regularly
✅ Keep audit trail of changes
❌ Don't use shared admin accounts
❌ Don't reuse admin emails

### Access Control
✅ Only grant admin role to trusted users
✅ Regularly update admin credentials
✅ Monitor admin activities
✅ Implement IP whitelisting (future feature)
❌ Don't leave admin accounts logged in
❌ Don't share admin panel links

---

## 🐛 Troubleshooting

### Admin Login Issues

**Error: "Invalid credentials"**
- Verify email is correct (case-sensitive)
- Check password is correct
- Ensure admin account exists

**Error: "This account does not have admin privileges"**
- The account exists but is not an admin
- Create a new admin account using the seed script
- Or update the role in the database directly

### Admin Creation Issues

**Error: "Email already registered"**
- This email is already in use
- Use a different email address
- Delete the existing account first (if needed)

**Error: "Failed to create admin"**
- Check the backend server is running
- Verify database connection
- Check network/firewall issues

---

## 🔄 Backup & Recovery

### Backing Up Admin Credentials
1. Keep a secure record of admin emails
2. Store admin account recovery information safely
3. Never commit passwords to version control

### Recovering Lost Admin Access
1. If you lose access to all admin accounts:
   - Access the database directly
   - Query the `users` table for role='admin' accounts
   - Reset a password if needed (requires DB admin access)

---

## 📊 Monitoring & Logs

### Admin Activity Tracking
All admin operations are logged with:
- Request timestamp
- Operation type (CREATE, UPDATE, DELETE)
- Affected resource
- Response status

### Viewing Logs
Check the backend logs:
```bash
tail -f backend.log
```

Look for entries like:
```
2024-01-20 14:25:00 - INFO - POST /api/v1/admin/create | Status: 201
2024-01-20 14:26:30 - INFO - PUT /api/v1/admin/{id} | Status: 200
2024-01-20 14:27:45 - INFO - DELETE /api/v1/admin/{id} | Status: 200
```

---

## 🚨 Emergency Procedures

### Suspected Admin Compromise
1. Log out from the admin panel
2. Change your admin password immediately
3. Review recent admin activities in logs
4. Delete any unauthorized admin accounts
5. Reset other admin passwords if needed

### Database Issues
If admin system stops working:
1. Verify database is running
2. Check database connection in `.env` file
3. Verify user table exists: `sqlite3 app.db "SELECT * FROM users;"`
4. Restart the backend server

---

## 📚 Additional Resources

- **Backend API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Project README**: See main `README.md`
- **Database Setup**: See `BACKEND_SETUP.md`
- **Environment Variables**: See `.env` file template

---

## ✅ Checklist: First Time Admin Setup

- [ ] Run `create_admin_seed.py`
- [ ] Successfully created first admin account
- [ ] Navigate to `http://localhost:3000/admin-login`
- [ ] Login with admin credentials
- [ ] Access Admin Dashboard
- [ ] View system statistics
- [ ] Create a second admin account
- [ ] Logout and test login with new admin
- [ ] Review Admin Management page
- [ ] Enable notifications (if configured)

---

**Need Help?** Contact your system administrator or check the backend logs for more details.
