# 🚀 EDrive: Your Personal Cloud Storage Solution

> **EDrive** is a sleek, user-friendly web application designed to revolutionize the way you manage your files and folders. Experience the power of cloud storage right at your fingertips!

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-3.2%2B-green)](https://www.djangoproject.com/)

## ✨ Features

EDrive comes packed with an array of powerful features:

- 📁 **Intuitive File Management**: Create, upload, move, and delete files and folders with ease.
- 🔍 **Smart Search**: Quickly find your files and folders using our advanced search functionality.
- 🔒 **Secure Authentication**: Robust user authentication system to keep your data safe.
- 📥 **Drag-and-Drop Upload**: Effortlessly upload files and folders using our modern drag-and-drop interface.
- 📊 **Storage Quota**: Keep track of your storage usage with our visual quota display.
- 🌓 **Dark Mode**: Easy on the eyes with our sleek dark mode option.
- ⌨️ **Keyboard Shortcuts**: Boost your productivity with convenient keyboard shortcuts.
- 💼 **Premium Upgrades**: Unlock extra space with our premium plan.

## 🛠️ Technology Stack

- **Backend**: Django
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/get-started)
- [Python 3.12](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Mailtrap](https://mailtrap.io/)

### Option 1: Using VSCode and Dev Containers (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/maurograndaoramos/ETIC_PW2425_PROJETO_I.git
   cd EDrive
   ```

2. **Open in VSCode**
   - Install the "Dev Containers" extension in VSCode.
   - Open the project folder in VSCode.
   - When prompted, click "Reopen in Container" or use the command palette (F1) and select "Remote-Containers: Reopen in Container".

3. **Set up the project**
   - The Dev Container automatically fires poetry install & make help. Follow up with:
   ```bash
   poetry shell
   make all
   ```

### Option 2: Manual Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/EDrive.git
   cd EDrive
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Set up the project**
   ```bash
   poetry install
   poetry shell
   make all
   ```

## 📧 (Optional) Email Configuration for Password Reset

To enable the password reset feature, you need to configure the email settings. We use Mailtrap for email testing. Follow these steps to set up your email configuration:

1. **Sign up for Mailtrap**:
   - Go to [Mailtrap](https://mailtrap.io/) and create an account if you don't have one.
   - Create a new inbox or use an existing one.

2. **Get your Mailtrap credentials**:
   - In your Mailtrap inbox, go to the SMTP Settings.
   - Select 'Django' as your integration.
   - You will see a configuration similar to the one below.

3. **Set up environment variables**:
   - Create a `.env` file in the root directory of the project if it doesn't exist.
   - Add the following variables to the settings.py file, inside the hub directory, replacing the values with your Mailtrap credentials:

     ```
     DEFAULT_FROM_EMAIL=noreply@yourdomain.com
     EMAIL_HOST=live.smtp.mailtrap.io
     EMAIL_PORT=587
     EMAIL_USE_TLS=True
     EMAIL_HOST_USER=your_mailtrap_user
     EMAIL_HOST_PASSWORD=your_mailtrap_password
     ```

With these settings in place, your password reset emails will be sent through Mailtrap, allowing you to test the feature without sending real emails.

For production deployment, replace the Mailtrap settings with your actual email service provider's SMTP details.

### 🖥️ Accessing the Application

- Open your browser and navigate to `http://localhost:8000`
- If you're using a remote environment, you may need to use port forwarding. Check your terminal for the correct URL.

> **Note**: This project uses Python 3.12 and Django 5.0.6. Ensure your environment matches these versions for optimal compatibility.

### Troubleshooting

- If you encounter any issues with Docker, ensure the Docker daemon is running on your system.
- For Poetry-related problems, refer to the [official Poetry documentation](https://python-poetry.org/docs/).
- If you're new to Dev Containers, check out the [VSCode Dev Containers tutorial](https://code.visualstudio.com/docs/remote/containers-tutorial).

## 💻 Usage

After logging in, you'll be greeted with a mock-up of a standard app service landing page. The About and Premium page will also be a mock-up.

You will need to create an account by registring and then logging in with your chosen Username and Password.

Once you do, you will find an intuitive interface where you can:

- Create new folders
- Upload files and folders
- Rename, move, or delete items
- Search for specific files or folders
- Monitor your storage quota


## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

