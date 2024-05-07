from auth import Account
import pickle, os, time


def with_cookies():
    with open("temp_cookies.pkl", 'rb') as file:
        cookies = pickle.load(file)

    acc = Account(cookies)
    image_path = os.path.abspath("test.jpg")
    acc.post(image_path, "This is a test caption")

    time.sleep(100)

if __name__ == "__main__":
    with_cookies()
