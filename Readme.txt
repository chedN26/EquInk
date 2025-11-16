Steps to Run the Project on Any Computer
----------------------------------------

1. Install Python
   - Download Python 3.10 or higher from: https://www.python.org/downloads/
   - During installation, enable "Add Python to PATH".

2. Install Required Python Libraries
   - Open Command Prompt inside the project folder.
   - Run this command:
     pip install flask python-docx pdf2image pillow opencv-python numpy docx2pdf

3. Install Poppler (Required for pdf2image)
   - Download Poppler for Windows:
     https://github.com/oschwartz10612/poppler-windows/releases/
   - Extract the ZIP to a folder, for example:
     C:\poppler-25.11.0\
   - Use the poppler 'bin' folder path in index.py:
     C:\poppler-25.11.0\bin
   - Or add this path to your Windows PATH environment variable.

4. Arrange the Project Folder
   Your project should look like this:

     project-folder/
     ├── index.py
     ├── database.py
     ├── uploads.db      (this file will auto-create when app runs)
     └── templates/
         └── index.html

   Important: index.html must be inside the "templates" folder.

5. Run the Program
   - Open Command Prompt in the project folder.
   - Run:
     python index.py
   - Open your browser and go to:
     http://127.0.0.1:5000

6. Using the Program
   - Upload a PDF or DOCX file.
   - The system will analyze the color percentage.
   - Cost will be calculated automatically.
   - Upload history will be stored in uploads.db (SQLite).

7. Optional: View Database Manually
   - Download DB Browser for SQLite:
     https://sqlitebrowser.org/
   - Open uploads.db to view all stored records.


END OF INSTRUCTIONS
