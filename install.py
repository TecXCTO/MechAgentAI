import subprocess
installed_list=[[]]
un_installed_list=[[]]
with open('requirements.txt', 'r') as f:
    for line in f:
        package = line.strip()
        if package and not package.startswith('#'):
            try:
                subprocess.check_call(['pip', 'install', package])
                installed_list.extend(package)
            except subprocess.CalledProcessError:
                un_installed_list.extend(package)
                print(f"Failed to install {package}. Skipping...")
with open('requirements_all.txt', 'r') as f:
    for line in f:
        package = line.strip()
        if package and not package.startswith('#'):
            try:
                subprocess.check_call(['pip', 'install', package])
                installed_list.extend(package)
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}. Skipping...")
                un_installed_list.extend(package)
with open('installed_list.txt', 'w') as f:
    f.writelines([i + '\n' for i in installed_list])
with open('un_installed_list.txt', 'w') as f:
    f.writelines([i + '\n' for i in un_installed_list])
print(f"Installed Python Packages List: {installed_list}/n Uninstalled Python Packages List: {un_installed_list}/n ")
