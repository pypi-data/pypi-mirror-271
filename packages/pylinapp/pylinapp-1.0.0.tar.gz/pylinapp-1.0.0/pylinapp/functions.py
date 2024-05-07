import os
import shutil
import subprocess
from .variables import version, repository_options, app

url_repository = ""

def print_version():
    print(f'Version: {version}')

def install_dependencies():
    current_dir = os.getcwd()
    app_dir = os.path.join(current_dir, app)
    os.chdir(app_dir)
    print('Instalando dependencias...')
    subprocess.run('npm install', shell=True)
    subprocess.run('npm install -g allure-commandline', shell=True)

    try:
        subprocess.run('allure --version', shell=True, check=True)
    except subprocess.CalledProcessError:
        print('Allure no está correctamente instalado. Cambiando la política de ejecución...')
        subprocess.run('Set-ExecutionPolicy RemoteSigned -Scope CurrentUser', shell=True)
        subprocess.run('npm install -g allure-commandline', shell=True)
        subprocess.run('allure --version', shell=True)

    print('Dependencias instaladas exitosamente.')

def execute_tests():
    print('Ejecutando pruebas...')
    subprocess.run('behave --no-skipped', shell=True)

def generate_report_html():
    print('Generando reporte...')
    subprocess.run('allure generate', shell=True)
    subprocess.run('allure open', shell=True)

def generate_report_word():
    subprocess.run('python ./src/test/config/generate_word_web.py', shell=True)

def reset_files():
    folders = ["allure-report", "allure-results", "screenshots", "Evidencias"]
    current_dir = os.getcwd()

    for folder in folders:
        folder_path = os.path.join(current_dir, folder)
        try:
            shutil.rmtree(folder_path)
            print(f"La carpeta '{folder}' ha sido eliminada exitosamente.")
        except FileNotFoundError:
            print(f"La carpeta '{folder}' no existe.")

def clone_repository():
    print('¡Vamos a descargar el repositorio del framework web!') #replicar para mobile
    
    repository_type = select_repository_type()
    if repository_type == "Github":
        repository_name = select_repository_name()
        branch_name = select_brach_name()
        url_repository = f"https://github.com/aariverar/{repository_name}.git"
    elif repository_type == "Azure Repos":
        repository_name = select_repository_name()
        branch_name = select_brach_name()
        url_repository = f"https://mibanco-devops@dev.azure.com/mibanco-devops/DevOps/_git/{repository_name}"
    else: 
        url_repository = None

    if url_repository is not None:
        # Verificar si la rama existe en el repositorio remoto
        result = subprocess.run(f'git ls-remote --heads {url_repository} {branch_name}', shell=True, capture_output=True, text=True)
        if branch_name in result.stdout:
            if os.path.isdir(app):
                print(f'El directorio {app} ya existe. Actualizando...')
                subprocess.run(f'git pull', shell=True)
                subprocess.run(f'git -C {app} checkout {branch_name}', shell=True)
                subprocess.run(f'git -C {app} pull origin {branch_name}', shell=True)
            else:
                print('Clonando repositorio...')
                subprocess.run(f'git clone {url_repository} {app}', shell=True)
                print(f'Cambiando a la rama {branch_name}...')
                subprocess.run(f'git -C {app} checkout {branch_name}', shell=True)
        else:
            print(f"La rama {branch_name} no existe en el repositorio {url_repository}.")

def select_repository_type():
    print('Selecciona el repositorio que deseas clonar:')
    for index, key in enumerate(repository_options):
        print(f'{index + 1}. {key}')

    option = int(input('Opción: '))

    if option > len(repository_options):
        print('Opción inválida. Inténtalo de nuevo.')
        select_repository_type()

    repository_type = repository_options[option - 1]
    print(repository_type)
    return repository_type

def select_repository_name():
    repository_name = input("Escribe el nombre del repositorio:")
    return repository_name

def select_brach_name():
    branch_name = input('Escribe el nombre de la rama (La rama debe existir en el repositorio): ')
    return branch_name

def open_application():
    subprocess.run('python ./src/test/config/app_run.py', shell=True)
