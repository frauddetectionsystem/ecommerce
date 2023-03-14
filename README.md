# How to set up the project locally on your system

1. Open your code editor(either visual studio code or pycharm)

2. Open the terminal

3. Clone the project by running the following command on the terminal(ensure you are connected to the internet)
git clone https://github.com/frauddetectionsystem/ecommerce.git

4. Change directory to the project by running the following command on the terminal
cd ecommers
cd ecn

5. Create a virtual environment by running the following command:
python –m venv .myvenv

6. Activate the virtual environment using the following command
.myvenv\Scripts\activate

7. Run the following command on the terminal to install every package needed
pip install –r requirements.txt


8. Create a superuser account by running the following command:
python manage.py createsuperuser

It will ask you for a username, email, and password. Please enter the details and remember to
Save them somewhere.

9. Run the following command to makemigrations and migrate
python manage.py makemigrations
python manage.py migrate


9. Start the development server
python manage.py runserver
