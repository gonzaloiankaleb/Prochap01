import os
import sys

def instalar_dependencias():
    os.system(f"{sys.executable} -m pip install -r requirements.txt")

if __name__ == "__main__":
    print("Instalando dependencias...")
    instalar_dependencias()
    print("Dependencias instaladas. Ahora puedes ejecutar la aplicación.")

