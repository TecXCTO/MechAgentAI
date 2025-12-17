import subprocess
installed_list=
un_installed_list=
with open('requirements.txt', 'r') as f:
    for line in f:
        package = line.strip()
        if package and not package.startswith('#'):
            try:
                subprocess.check_call(['pip', 'install', package])
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}. Skipping...")
              
with open('requirements_full.txt', 'r') as f:
    for line in f:
        package = line.strip()
        if package and not package.startswith('#'):
            try:
                subprocess.check_call(['pip', 'install', package])
                installed_list=package
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}. Skipping...")
                un_installed_list=package

print(f"Installed Python Packages List: {installed_list}/n Uninstalled Python Packages List: {un_installed_list}/n ")
