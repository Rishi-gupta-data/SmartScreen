# SmartScreen Frontend - Production Setup Guide

## 🎯 Overview

This is a production-ready React frontend for SmartScreen SaaS, featuring:
- ✅ User authentication (Login/Signup)
- ✅ Dashboard with credit balance
- ✅ Resume parsing
- ✅ Job description parsing
- ✅ Resume-to-job matching
- ✅ Billing & credit management
- ✅ Transaction history
- ✅ Protected routes
- ✅ Professional Material-UI design
- ✅ Error handling & loading states

---

## 📦 Installation

### 1. Install Dependencies

```bash
cd frontend
npm install
```

This installs:
- React 18.2
- Material-UI 5.14
- Axios for API calls
- React Router v6 for navigation
- React Testing Library

### 2. Configure Environment

Create `.env` file in `frontend/` folder:

```bash
# Development (default)
REACT_APP_API_URL=http://localhost:8000

# Production
REACT_APP_API_URL=https://api.smartscreen.com
```

---

## 🚀 Running the Frontend

### Development Mode

```bash
npm start
```

Opens at `http://localhost:3000`

### Production Build

```bash
npm run build
```

Creates optimized production build in `frontend/build/` folder.

---

## 🗂️ Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   └── ProtectedRoute.js      # Protected route wrapper
│   ├── context/
│   │   └── AuthContext.js          # Auth state management
│   ├── pages/
│   │   ├── Login.js                # Login page
│   │   ├── Signup.js               # Signup page
│   │   ├── Dashboard.js            # Main dashboard
│   │   ├── ResumeParse.js          # Resume parsing
│   │   ├── JDParse.js              # Job description parsing
│   │   ├── Match.js                # Resume-to-job matching
│   │   ├── Billing.js              # Buy credits & pricing
│   │   └── Transactions.js         # Transaction history
│   ├── services/
│   │   └── api.js                  # API client & methods
│   ├── App.js                      # Main app with routing
│   ├── index.js                    # React entry point
│   └── theme.js                    # Material-UI theme
├── .env                            # Environment variables
├── .env.example                    # Example env file
└── package.json                    # Dependencies
```

---

## 🔐 Authentication Flow

1. **Signup** - Create new account
   - Email validation
   - Password strength check
   - Auto-login after signup

2. **Login** - Authenticate with existing account
   - Email & password validation
   - JWT token storage

3. **Protected Routes** - Only logged-in users can access
   - Token auto-attached to all API requests
   - Auto-logout on token expiry
   - Redirect to login on 401 error

---

## 📄 Pages Overview

### 1. **Login** (`/login`)
- Email & password form
- Signup link
- Error handling
- Loading state

### 2. **Signup** (`/signup`)
- Email & password validation
- Password confirmation
- Error feedback
- Login link

### 3. **Dashboard** (`/dashboard`)
- Credit balance display
- Buy credits button
- Quick action cards:
  - Parse Resume
  - Parse Job Description
  - Match Candidate to Job
  - View Transactions
- Credit usage guide
- User logout

### 4. **Resume Parser** (`/resume`)
- Paste resume text
- Extract information:
  - Name, Email, Phone
  - Skills list
  - Experience
  - Education
- Credits deducted (5 per parse)
- Remaining credits displayed

### 5. **JD Parser** (`/jd`)
- Paste job description
- Extract information:
  - Job title
  - Company name
  - Salary range
  - Required skills
  - Responsibilities
- Credits deducted (3 per parse)
- Remaining credits displayed

### 6. **Matching** (`/match`)
- Compare resume with job
- Match score (0-100%)
- Recommendation (Excellent/Good/Moderate/Poor)
- Matched skills (green)
- Missing skills (red)
- Credits deducted (5 per match)

### 7. **Billing** (`/billing`)
- Current credit balance
- Quick buy packages:
  - 100 credits
  - 500 credits
  - 1000 credits
  - 5000 credits
- Transaction history table
- Credit usage pricing

### 8. **Transactions** (`/transactions`)
- Full transaction history
- Date, type, description, amount
- Credit/debit indicators
- Pagination support

---

## 🔌 API Integration

### API Client (`src/services/api.js`)

Organized by feature:

```javascript
// Auth
authAPI.signup(email, password)
authAPI.login(email, password)

// Resume
resumeAPI.parse(resumeText)

// Job Description
jdAPI.parse(jdText)

// Matching
matchAPI.match(resumeText, jdText)

// Billing
billingAPI.getCredits()
billingAPI.buyCredits(amount)
billingAPI.getTransactions(skip, limit)
```

### API Request/Response Handling

- Automatic JWT token attachment
- Error handling with user-friendly messages
- Auto-logout on 401 (unauthorized)
- Response parsing and validation

---

## 🎨 Styling & Theme

### Material-UI Theme (`src/theme.js`)

- Primary color: `#1a237e` (Dark Blue)
- Secondary color: `#667eea` (Purple)
- Responsive grid layout
- Consistent spacing & typography

### Features

- Dark theme support (extensible)
- CSS-in-JS with Emotion
- Mobile-responsive design
- Accessible components (WCAG 2.1)

---

## 🧪 Testing

### Run Tests

```bash
npm test
```

### Test Coverage

- Component rendering
- User interactions
- API integration
- Error handling

---

## 📝 State Management

### Authentication Context

Location: `src/context/AuthContext.js`

```javascript
const { user, loading, error, signup, login, logout } = useContext(AuthContext);
```

### Page-level State

- Resume/JD text input
- Loading states
- Error messages
- Results display

---

## 🚨 Error Handling

### Global Error Handling

1. **API Errors** → Display user-friendly message
2. **Auth Errors** → Redirect to login
3. **Validation Errors** → Field-level feedback
4. **Network Errors** → Retry option

### Loading States

- Skeleton loaders
- Disabled inputs during requests
- Progress indicators
- Prevent double-submission

---

## 🔐 Security Best Practices

1. **JWT Token Storage**
   - Stored in localStorage
   - Sent in Authorization header
   - Auto-removed on logout

2. **Protected Routes**
   - ProtectedRoute component
   - Checks auth context
   - Redirects unauthorized users

3. **CORS Configuration**
   - Handled by backend
   - Frontend sends credentials

4. **Input Validation**
   - Email format check
   - Password strength check
   - Text field validation

---

## 📦 Deployment

### Build for Production

```bash
npm run build
```

### Deploy Targets

1. **Vercel** (Recommended)
```bash
npm install -g vercel
vercel
```

2. **Netlify**
```bash
npm run build
# Upload build/ folder to Netlify
```

3. **Docker**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install && npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Environment Variables for Production

```
REACT_APP_API_URL=https://your-api-domain.com
```

---

## 🐛 Troubleshooting

### Issue: "Cannot find module 'react-router-dom'"

**Solution:**
```bash
npm install react-router-dom
```

### Issue: API not responding

**Solution:**
- Check backend is running
- Verify `REACT_APP_API_URL` in `.env`
- Check CORS configuration on backend

### Issue: Blank page on load

**Solution:**
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for API calls

---

## 📚 Component Reference

### ProtectedRoute

```javascript
<ProtectedRoute>
  <Dashboard />
</ProtectedRoute>
```

Wraps pages that require authentication.

### AuthContext

```javascript
const { user, loading, error, signup, login, logout } = useContext(AuthContext);
```

Provides authentication state and methods.

---

## 🎯 Next Steps

1. ✅ Install dependencies: `npm install`
2. ✅ Configure `.env` file
3. ✅ Start backend API
4. ✅ Run frontend: `npm start`
5. ✅ Test all pages
6. ✅ Deploy to production

---

## 📞 Support

For issues or questions:
1. Check error messages in browser console
2. Review API documentation
3. Check backend logs
4. Test API endpoints directly with Postman

---

**Version:** 1.0.0  
**Last Updated:** April 15, 2026  
**Status:** Production Ready ✅
