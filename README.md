# PCT - Django API Project

## 📌 Project Overview
This is a Django-based API project that follows best practices, including environment variable management and dependency isolation.

## 🛠️ Setup Instructions
Follow these steps to set up and run the project on your local machine.

### **1️⃣ Clone the Repository & Move to Project Root**
```sh
git clone https://github.com/Balamithran228/PCT.git
cd PCT
```

### **2️⃣ Create & Activate Virtual Environment**
For **Windows**:
```sh
python -m venv venv
venv\Scripts\activate
```
For **macOS/Linux**:
```sh
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Move into the Django Project Directory**
```sh
cd myapi
```

### **5️⃣ Configure Environment Variables**
Copy the example `.env` file and update the `SECRET_KEY`:

For **Windows (Command Prompt):**
```sh
copy .env.example .env
```
For **macOS/Linux:**
```sh
cp .env.example .env
```

Generate a new Django SECRET_KEY:
```sh
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Edit `.env` and replace `your-secret-key-here` with the generated key.

### **6️⃣ Apply Database Migrations**
```sh
python manage.py migrate
```

### **7️⃣ Create a Superuser (Optional, for Admin Panel)**
```sh
python manage.py createsuperuser
```
Follow the prompts to set up an admin account.

### **8️⃣ Run the Development Server**
```sh
python manage.py runserver
```

Now, open your browser and visit:
- **Home Page:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

---

## 📂 **Project Directory Structure**
```
PCT/
│-- myapi/      # Main Django project folder
│   │-- myapi/  # Django settings, wsgi, asgi
│   │-- api/    # Django app folder
│   │-- manage.py  # Django entry point
│-- venv/  # Virtual environment (not included in repo)
```

---

## ⚠️ **Important Notes**
✅ **Navigate to `PCT/myapi/` before running Django commands.**  
✅ **Use `.env` for storing sensitive keys (never commit it!).**  
✅ **Database:** Defaults to SQLite (change in `settings.py` if needed).  
✅ **Admin Panel:** Login at `/admin/` after creating a superuser.  

---

### 🚀 **Now You're Ready to Use the Project!**

