<div align="center">
  <br />
      <img src="./frontend/public/Banner.png" alt="Project Banner">
    </a>
  <br />

  <div>
    <img src="https://img.shields.io/badge/-Flask-black?style=for-the-badge&logoColor=white&logo=flask&color=000000" alt="Flask" />
    <img src="https://img.shields.io/badge/-Vue_JS-black?style=for-the-badge&logoColor=white&logo=vue.js&color=4FC08D" alt="Vue.js" />
    <img src="https://img.shields.io/badge/-SpaCy-black?style=for-the-badge&logoColor=white&logo=spacy&color=09A3D5" alt="SpaCy" />
  </div>

  <h3 align="center">Smart Inventory Management System</h3>
</div>

## <a name="introduction">🤖 Introduction</a>

The **Smart Inventory Management System** is a modern web application that leverages **Natural Language Processing (NLP)** to simplify inventory management tasks. Designed for seamless user interaction, this system enables inventory updates through intuitive text or voice commands, ensuring efficiency and user-friendliness.

## <a name="tech-stack">⚙️ Tech Stack</a>

- **Frontend**: Vue.js
- **Backend**: Flask
- **Database**: SQLite
- **NLP**: SpaCy
- **Authentication**: Flask-JWT-Extended
- **Real-time Updates**: Flask-SocketIO

## <a name="features">🔋 Features</a>

👉 **Natural Language Input**: Manage inventory with commands like:
   - *"Add 50 units of Amul butter"*
   - *"Update 4kg stock of rice"*

👉 **Intelligent Command Parsing**: Effortlessly process natural language commands.

👉 **Inventory Database**: Robust database for storing and managing inventory.

👉 **User Authentication**: Secure your data with JWT-based authentication.

👉 **Real-time Updates**: Stay synced with live inventory updates via WebSockets or SSE.

👉 **Reports & Analytics**: Gain insights with dynamic reports and trend analysis.

## <a name="quick-start">🤸 Quick Start</a>

### **Backend Setup**:

1. **Clone the repository**:

```bash
git clone https://github.com/lazycoder54/Smart-Inventory-app.git
cd smart-inventory-backend
```

2. **Create a virtual environment** and activate it:

- On **Windows**:

```bash
python -m venv venv
.\venv\Scripts\activate
```

- On **macOS/Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

4. **Run the Flask app**:

```bash
flask run
```

The backend will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

### **Frontend Setup**:

1. **Navigate to the frontend directory**:

```bash
cd smart-inventory-frontend
```

2. **Install dependencies**:

```bash
npm install
```

3. **Start the dev server**:

```bash
npm run dev
```

The frontend will be available at [http://localhost:5173](http://localhost:5173).

## <a name="usage">🎯 Usage</a>

1. Open the web application in your browser.
2. Log in with your credentials.
3. Start managing your inventory with commands like:
   - *"Add 10 units of apples"*
   - *"Update the 5kg stock of apple"*
4. Monitor real-time updates and explore analytics on the dashboard.

## <a name="contributing">🤝 Contributing</a>

We’d love your contributions! Follow these steps:

1. **Fork** the repository.
2. **Create a new branch**:

```bash
git checkout -b feature-name
```

3. **Commit** your changes and push to the branch:

```bash
git add .
git commit -m "Add feature-name"
git push origin feature-name
```

4. Open a **pull request** for review.

## <a name="license">📝 License</a>

This project is licensed under the **MIT License**.

## <a name="contact">📬 Contact</a>

Got questions or need support? Reach out to us:

- **Email**: pranjitd865@gmail.com
- **GitHub**: [lazycoder54](https://github.com/lazycoder54)

---

Happy coding! 🚀
