# Medical Appointment System

This is a Django web application designed for managing medical appointments. The application includes three user types: Patients, Doctors, and Admins, each with their own dashboards and functionalities.

## Features

- **Patient Dashboard**: 
  - Patients can request appointments.
  - View their appointment history.
  
- **Doctor Dashboard**: 
  - Doctors can manage their schedules.
  - Access patient histories and appointment requests.
  
- **Admin Dashboard**: 
  - Admins can oversee the entire appointment process.
  - Manage users and appointments.

## Technologies Used

- Django
- HTML/CSS
- JavaScript
- Bootstrap (or any other modern UI framework)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd medical-appointment-system
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser for admin access:
   ```
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`.

## Usage

- Visit the respective dashboards for Patients, Doctors, and Admins to manage appointments and user data.
- Follow the links provided in the dashboards to navigate through the functionalities.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.