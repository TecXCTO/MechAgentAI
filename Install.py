import subprocess

with open('requirements.txt', 'r') as f:
    for line in f:
        package = line.strip()
        if package and not package.startswith('#'):
            try:
                subprocess.check_call(['pip', 'install', package])
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}. Skipping...")
              
