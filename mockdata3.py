from faker import Faker
import random
import pandas as pd
from multiprocessing import Pool, cpu_count, Manager

def generate_chunk(args):
    num_entries, shared_usernames, shared_emails = args
    fake = Faker()
    data = []
    
    domains = ["gmail.com", "yahoo.com", "hotmail.com"]

    for _ in range(num_entries):
        first_name = fake.first_name()
        last_name = fake.last_name()

        # Generate username based on first and last names
        username = f"{first_name.lower()}.{last_name.lower()}"

        # Ensure username uniqueness
        while username in shared_usernames:
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}"

        shared_usernames[username] = 1

        # Custom email domain generation
        domain = random.choice(domains)
        email = f"{username}@{domain}"

        # Ensure email uniqueness
        while email in shared_emails:
            domain = random.choice(domains)
            email = f"{username}@{domain}"

        shared_emails[email] = 1

        password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

        data.append({
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
            "password": password
        })

    return data

def generate_mock_data(num_entries=5000):
    num_processors = cpu_count()
    chunk_size = num_entries // num_processors

    with Manager() as manager:
        shared_usernames = manager.dict()
        shared_emails = manager.dict()

        with Pool(processes=num_processors) as pool:
            args = [(chunk_size, shared_usernames, shared_emails) for _ in range(num_processors)]
            data_chunks = pool.map(generate_chunk, args)
    
    data = []
    for chunk in data_chunks:
        data.extend(chunk)
    
    return data

def write_to_excel(mock_data, filename='mock_data.xlsx'):
    df = pd.DataFrame(mock_data)
    df.to_excel(filename, index=False)

if __name__ == "__main__":
    mock_data = generate_mock_data()
    write_to_excel(mock_data)
    print(f"Data written to 'mock_data.xlsx'")

