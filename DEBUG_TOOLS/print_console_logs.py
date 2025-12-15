import user_settings
import os

logs = os.listdir(f"../{user_settings.DIRECTORY_FOR_CONSOLE_LOGS}")

for log in logs[-1:]:
    with open(os.path.join(f"../{user_settings.DIRECTORY_FOR_CONSOLE_LOGS}", log), 'r') as f:
        print(f.read())
        print("\n"*5)

