# Library Management System

This is a **desktop application** for managing a library system built with Python and the Qt framework. It enables librarians to efficiently handle books, clients, and daily operations, offering features like statistics dashboards, reporting, and customizable themes.

---

## Key Features

- **User Authentication**: Secure login system.
- **Books Management**: Add, edit, delete, and track books.
- **Client Management**: Client registration, borrowing history, and records.
- **Daily Operations Tracking**: Monitor daily activities.
- **Dashboard**: Real-time statistics and overview.
- **History Logging**: Complete log of all operations.
- **Reporting System**: Generate reports for books, clients, and operations.
- **Settings Customization**: Multiple themes and preferences.
- **Barcode Support**: Simplifies book management.
- **Category & Publisher Management**: Organize books efficiently.
- **Branch Management**: Support for multiple locations.

---

## Tech Stack

- **Python**: Core programming language.
- **MySQL**: Relational database for persistent storage.
- **SQL**: Used for database queries.
- **PyQt5**: Python bindings for the Qt framework.
- **QSS**: Qt Style Sheets for theming.
- **Qt Designer**: GUI design tool for .ui files.

---

## Project Structure

```
├── Database.sql      # MySQL database schema
├── GUI.ui           # Qt Designer UI file
├── main.py          # Main application entry point
├── icons.qrc        # Resource file for icons
├── requirements.txt # Python dependencies
└── themes/         # QSS theme files for UI customization
```

---

## How to Run the Project

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a MySQL database named `library` and import the `Database.sql` file:
   - Open your MySQL client.
   - Import the `Database.sql` file.
   - Update MySQL credentials in the `main.py` file (username, password, host, etc.).

3. Compile the resource file (`icons.qrc`) into a Python file:
   ```bash
   pyrcc5 icons.qrc -o icons_rc.py
   ```

4. Run the project:
   ```bash
   python main.py
   ```

---

## Default Login Credentials

- **Username**: `admin`  
- **Password**: `admin`  

---

## Screenshots

### Login
![Login](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/6d84086b-135c-42be-b44f-e56bb468e28a)

### Today
![Today](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/993171e0-2613-4cda-8c87-8551b99529cd)

### Books
![Books](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/9716a562-2aac-419e-921e-c433285de22c)
![Books 2](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/34a8382c-6741-46b6-9761-f61c912a52a1)
![Books 3](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/9ccb4e6d-724c-4ab1-bb42-6f11bb3e2512)

### Clients
![Clients](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/03842df1-323c-4820-bc7f-2b266d1326d9)
![Clients 2](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/b0cb49ce-7528-4757-8181-a4cea7e51e62)
![Clients 3](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/d9612e69-35f2-480a-a6c5-d8d05177ad55)

### Dashboard
![Dashboard](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/1371892d-10da-48d3-90b2-e0e56e735b95)

### History
![History](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/1d1cf27a-0f6f-4d73-addf-651b24e1e013)

### Reports
![Reports](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/8b97ced9-7499-4dd8-a140-5c33970e7486)
![Reports 2](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/9dcdf9f2-29ca-4ef3-8f76-22276e74d164)
![Reports 3](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/b51fd2f0-0c41-4493-a850-8dce92c5b229)

### Settings
![Settings](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/8a459d79-400a-4220-aeee-16ae1482be23)
![Settings 2](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/935886ed-376b-40bd-a551-62e6a725034e)
![Settings 3](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/44f16d9c-cb81-49ae-bd83-1421e242ce5f)
![Settings 4](https://github.com/Mahmoud-A-Noor/Library-Management-System/assets/59361888/4ed37706-1ece-48ab-9a32-fa2a44203a74)

---

## Contribution

Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request with your changes.

---

## Contact

For any inquiries or support, please reach out to me at:  
📧 **Email**: mahmoudnoor917@gmail.com

