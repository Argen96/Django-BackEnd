from myapp.models import User

# Retrieve all User objects from the database
all_users = User.objects.all()

# Print the data for each user
for user in all_users:
    print(f"Username: {user.username}, Email: {user.email}, Password: {user.password}")