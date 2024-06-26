# EDrive

## Description
EDrive is a web application designed to manage files and folders, similar to cloud storage services.

## Technologies
- Django
- SQLite
- HTML
- CSS
- JavaScript

## Main Components
### drive
Handles file and folder operations such as creating, uploading, moving, and deleting.

### hub
Contains core settings and configurations for the Django project.

### web
Manages user authentication, main website views, and static resources.

## Key Files
- **EDrive/manage.py**: Django management script.
- **EDrive/drive/models.py**: Database models for files and folders.
- **EDrive/drive/views.py**: View functions for handling file and folder requests.
- **EDrive/drive/templates/drive.html**: HTML template for the drive interface.
- **EDrive/hub/settings.py**: Django project settings.
- **EDrive/web/views.py**: View functions for handling user-related requests.
- **EDrive/web/templates/auth/login.html**: HTML template for user login.

## Setup
1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/EDrive.git
    cd EDrive
    ```
2. **Create a virtual environment and activate it**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install the dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Apply migrations**
    ```bash
    python manage.py migrate
    ```
5. **Run the development server**
    ```bash
    python manage.py runserver
    ```

## Usage
1. **Navigate to the application in your web browser**
    ```
    http://localhost:8000/
    ```
2. **Create an account and log in**
3. **Use the interface to manage your files and folders**

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
