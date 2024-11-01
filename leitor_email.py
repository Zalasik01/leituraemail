import logging
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd

# Configuração do logging
logging.basicConfig(filename='monitoramento.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Caminho do Edge WebDriver (ajuste conforme necessário)
driver_path = r'C:\Users\nicolas.souza\Downloads\edge\msedgedriver.exe'  # Atualize com o novo caminho
service = Service(driver_path)

# Criar uma instância do WebDriver do Microsoft Edge
driver = webdriver.Edge(service=service)

try:
    logging.info("Navegando para a página de login.")
    # Navegar até a página de login
    driver.get("https://login-new.locaweb.com.br/login?service=https%3A%2F%2Fpainel-email.locaweb.com.br%2F%3F")
    
    # Encontrar os campos de usuário e senha e preenchê-los
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = driver.find_element(By.NAME, "password")
    
    # Preencher o nome de usuário e a senha
    username_input.send_keys("windi")
    logging.info("Nome de usuário preenchido.")
    time.sleep(1)

    password_input.send_keys("Nm[v'[CeK(-9/*3J.e)3=S!,%tX-F(xJ")
    logging.info("Senha preenchida.")
    time.sleep(1)

    print("Por favor, resolva o reCAPTCHA manualmente.")
    time.sleep(60)  # Aguarda 60 segundos ou ajuste conforme necessário

    # Continuar após resolver o reCAPTCHA
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
    logging.info("Clique no botão de login realizado.")

    # Aguardar a nova página carregar
    WebDriverWait(driver, 10).until(
        EC.url_contains("painel-email.locaweb.com.br")
    )

    # Navegar diretamente para a página dos domínios após o login
    logging.info("Navegando para a página dos domínios.")
    driver.get("https://painel-email.locaweb.com.br/?ticket=ST-51198-34P1MDgV9MmqY84hqHMBD0I-meHo9W2kihvt2DhMssE-prd-node1")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//li[contains(@on-finish-render-repeat, 'window.emailPanel.init()')]"))
    )

    domains_data = []
    logging.info("Coletando informações dos domínios.")
    li_elements = driver.find_elements(By.XPATH, "//li[contains(@on-finish-render-repeat, 'window.emailPanel.init()')]")

    for li in li_elements:
        domain_element = li.find_element(By.CSS_SELECTOR, "strong.ng-binding")
        domain_name = domain_element.text.strip()
        
        plan_description = li.find_element(By.CSS_SELECTOR, "p.pObs.ng-binding.ng-scope").text
        match = re.search(r'Utilizando <strong>(\d+)</strong>', plan_description)
        
        number_of_boxes = match.group(1) if match else '0'
        domains_data.append({'domain_name': domain_name, 'number_of_boxes': number_of_boxes})

    logging.info("Dados dos domínios coletados com sucesso.")

    hybrid_domains = []
    try:
        domains_list = driver.find_element(By.ID, "domains_list")
        ng_scope_elements = domains_list.find_elements(By.CLASS_NAME, "ng-scope")

        for ng_scope in ng_scope_elements:
            hybrid_domain_element = ng_scope.find_element(By.CSS_SELECTOR, "strong.ng-binding")
            hybrid_domain = hybrid_domain_element.text.strip() if hybrid_domain_element else None
            
            if hybrid_domain:
                hybrid_domains.append(hybrid_domain)
        
        logging.info("Dados hybrid_domains coletados com sucesso.")
    except Exception as e:
        logging.error("Erro ao coletar hybrid_domains: %s", e)

    # Leitura das classes ng-hide
    try:
        hidden_elements = driver.find_elements(By.CLASS_NAME, "ng-hide")
        for elem in hidden_elements:
            hidden_text = elem.text.strip()
            logging.info(f"Texto encontrado em ng-hide: {hidden_text}")
    except Exception as e:
        logging.error("Erro ao coletar informações de ng-hide: %s", e)

    # Criar um DataFrame para salvar em uma planilha
    df = pd.DataFrame(domains_data)
    df_hybrid = pd.DataFrame(hybrid_domains, columns=['domain_hybrid'])

    final_df = pd.concat([df, df_hybrid], axis=1)

    output_path = r'C:\Users\nicolas.souza\Downloads\edge\Retornos\dominios_retornos.ods'
    final_df.to_excel(output_path, index=False, engine='odf')
    logging.info('Dados salvos na planilha em: %s', output_path)

except Exception as e:
    logging.error("Ocorreu um erro durante a execução do script: %s", e)

finally:
    input("Pressione Enter para fechar o navegador...")
    driver.quit()
