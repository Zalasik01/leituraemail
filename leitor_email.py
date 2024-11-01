from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Caminho do Edge WebDriver (ajuste conforme necessário)
driver_path = r'C:\Users\nicolas.souza\Downloads\edge\msedgedriver.exe'  # Atualize com o novo caminho
service = Service(driver_path)

# Criar uma instância do WebDriver do Microsoft Edge
driver = webdriver.Edge(service=service)

# Navegar até a página de login
driver.get("https://login-new.locaweb.com.br/login?service=https%3A%2F%2Fpainel-email.locaweb.com.br%2F%3F")

# Encontrar os campos de usuário e senha e preenchê-los com pausas
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

# Preencher o nome de usuário lentamente
username_input.send_keys("windi")
time.sleep(1)  # Pausa de 1 segundo

# Preencher a senha lentamente
password_input.send_keys("Nm[v'[CeK(-9/*3J.e)3=S!,%tX-F(xJ")
time.sleep(1)  # Pausa de 1 segundo

# Encontrar e marcar o checkbox "Não sou um robô" (ou similar)
checkbox = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']")  # Ajuste o seletor conforme necessário
if not checkbox.is_selected():
    checkbox.click()
time.sleep(1)  # Pausa de 1 segundo

# Enviar o formulário
password_input.send_keys(Keys.RETURN)

# Esperar alguns segundos para visualizar o resultado
time.sleep(5)

# Esperar até que o usuário pressione Enter
input("Pressione Enter para fechar o navegador...")

# Fechar o navegador
driver.quit()
