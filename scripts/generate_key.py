from django.utils.crypto import get_random_string


def generate_token():
    return get_random_string(length=50)


if __name__ == '__main__':
    print(generate_token())
