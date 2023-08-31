from faker import Faker
import random

def generate_mock_data(num_entries=1000000):
    fake = Faker()
    data = []
    
    emails = set()
    usernames = set()

    domains = ["gmail.com", "yahoo.com", "hotmail.com"]

    for _ in range(num_entries):
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        # Generate username based on first and last names
        username = f"{first_name.lower()}.{last_name.lower()}"
        
        # Ensure username uniqueness
        while username in usernames:
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"
        
        usernames.add(username)
        
        # Custom email domain generation
        domain = random.choice(domains)
        email = f"{username}@{domain}"
        
        # Ensure email uniqueness
        while email in emails:
            domain = random.choice(domains)
            email = f"{username}@{domain}"
        
        emails.add(email)
        
        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
        
        data.append({
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password
        })

    return data

def write_to_file(mock_data, filename='mock_data.txt'):
    with open(filename, 'w') as file:
        for entry in mock_data:
            file.write(str(entry) + '\n')

if __name__ == "__main__":
    mock_data = generate_mock_data()
    write_to_file(mock_data)
    print(f"Data written to 'mock_data.txt'")
