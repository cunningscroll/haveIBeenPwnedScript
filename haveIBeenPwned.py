import hashlib
import requests
import sys


def check_password(password):
    
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    request_url = f"https://api.pwnedpasswords.com/range/{first5_char}"
    response = requests.get(request_url)

    if response.status_code != 200:
        raise RuntimeError(f"Error fetching: {response.status_code}, check the api and try again")
    
    hashes = (line.split(':') for line in response.text.splitlines())
    for hash_suffix, count in hashes:
        if hash_suffix == tail:
            return int(count)
    return 0 



def main():
    if(len(sys.argv) < 2):
        print("Usage: python3 haveIBeenPwned.py {file path}")
        return 
    path = sys.argv[1]

    try:
        with open(path, 'r') as file:
            passwords = [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {path}")
        return

    for password in passwords:
        count = check_password(password)
        if count:
            print(f"Password: {password} was found {count} times. You should probably change your password")
        else:
            print(f"Password: {password} was not found. Carry on")
        
if __name__ == "__main__":
    main()