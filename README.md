# Financial-Data-Mining
A full-stack project based on Vue front-end and Django back-end for financial data mining, analysis and visualization.

# Tech stack
Frontend: Vue.js (Vue CLI or Vite)  
Backend: Django + Django REST Framework (DRF)  
Database: SQLite / PostgreSQL / MySQL  

# Project structure
Financial-Data-Mining/  
├── Backend/                 # Django backend  
│   ├── manage.py  
│   ├── requirements.txt     # Backend dependencies  
│   ├── backend/             # Project settings (settings.py / urls.py, etc.)  
│   └── apps/                # Business Applications (api, users, market, etc.)  
├── frontend/                # Vue frontend  
│   ├── package.json  
│   ├── vite.config.ts       # or vue.config.js  
│   ├── src/  
│   │   ├── main.ts  
│   │   ├── api/             # Front-end request encapsulation  
│   │   ├── views/           # page  
│   │   └── components/      # Components  
├── README.md  
└── LICENSE  

# Getting started
## 1. Prerequisites
    Node.js: >= 16  
    Python: >= 3.10  
    Package managers: npm or pnpm  
    Database: SQLite is the default, no additional installation is required; PostgreSQL is recommended for production   
## 2. Clone
   git clone https://github.com/lingyu-code/Financial-Data-Mining.git
   cd Financial-Data-Mining
## 3. Backend setup (Django)
   ### 3.1 Create and activate venv
        cd backend
        python -m venv venv
        # macOS/Linux
        source venv/bin/activate
        # Windows (PowerShell)
        venv\Scripts\Activate.ps1
   ### 3.2 Install dependencies
       pip install -r requirements.txt
   ### 3.3 Migrations and admin
        python manage.py makemigrations
        python manage.py migrate
## 4.frontend
  ### 4.1 Install and run
      cd ../frontend  
      npm install  
      npm run dev      # Vite 
