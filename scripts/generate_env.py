import os

if __name__ == '__main__':
    previous_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    secret_key = input(
        'Enter SECRET_KEY (or press enter to generate automatically): ')
    if not secret_key:
        from django.utils.crypto import get_random_string
        secret_key = get_random_string(50)
    debug = input('Enter DEBUG (on/off): ')
    with open(os.path.join(previous_folder, '.env'), 'w') as f:
        f.write(f'SECRET_KEY="{secret_key}"\n')
        f.write(f'DEBUG={debug}\n')
    print('.env file created in parent folder.')
