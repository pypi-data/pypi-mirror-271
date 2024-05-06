import os
from pathlib import Path
import yaml
import click
import base64

def simple_encrypt(password, key):
    # Convert the key (username) into a shift value
    shift = sum(ord(c) for c in key) % 256
    
    # Modify the password using the shift value
    modified_password = ''.join(chr((ord(char) + shift) % 256) for char in password)
    
    # Encode the modified password with Base64
    encoded_password = base64.b64encode(modified_password.encode()).decode()
    
    return encoded_password

def simple_decrypt(encrypted_password, key):
    # Convert the key (username) into a shift value
    shift = sum(ord(c) for c in key) % 256
    
    # Decode the password from Base64
    decoded_password = base64.b64decode(encrypted_password).decode()
    
    # Reverse the modification using the shift value
    original_password = ''.join(chr((ord(char) - shift) % 256) for char in decoded_password)
    
    return original_password

def write_config(profiles):
    if not os.path.exists(Path.home() / '.uac'):
            os.mkdir(Path.home() / '.uac')
   
    with open(Path.home() / '.uac' / 'profiles.yml', 'w') as file:
        yaml.dump(profiles, file)
    click.echo(f"Config file written. (Path: {Path.home() / '.uac' / 'profiles.yml'})")
   
def read_config():
    if not os.path.exists(Path.home() / '.uac' / 'profiles.yml'):
        return None
    
    with open(Path.home() / '.uac' / 'profiles.yml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config
    

def read_profile(profile_name):
    if not os.path.exists(Path.home() / '.uac' / 'profiles.yml'):
        return None

    with open(Path.home() / '.uac' / 'profiles.yml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        if profile_name in config:
            profile = config[profile_name]
            if "password" in profile and len(profile.get('password')) > 0:
                profile['password'] = simple_decrypt(profile['password'], profile['username'])
        else:
            profile = None
    return profile

def write_profile(profile_name, profile):
    config = read_config()
    if config is None:
        config = {}

    config[profile_name] = profile
    write_config(config)

def ask_profile(profile):
    url = click.prompt('Please enter UAC URL', type=str, default=profile.get('url', ""))
    config = { 'url': url}
    if click.confirm('Do you use personal access token?', default=True):
        token = click.prompt('Please enter personal access token', type=str, default=profile.get('token', ""))
        config['token'] = token
    else:
        username = click.prompt('Please enter username', type=str, default=profile.get('username', ""))
        password = click.prompt('Please enter password', type=str, hide_input=True)
        config['username'] = username
        config['password'] = simple_encrypt(password, username)

    return config
