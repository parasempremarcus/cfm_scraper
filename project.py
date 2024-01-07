import time
import pandas as pd
from alive_progress import alive_bar
from miscellaneous import estados, especialidades, inscrições, situações, usuário
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():

    pesquisa = coletar()

    while True:
        try:
            preencher(pesquisa)
            break
        except:
           print("---------------------------------------")
           print("❌ INVALID FILTER INPUT, TRY AGAIN ❌")
           print("=======================================")
           pesquisa = coletar()
           continue

    dados_cfm = scrape()

    while True:
        try:
            print("=====================================")
            formato = input("📦 CSV or Excel: ").lower()
            print(selecionar_formato(formato, dados_cfm, pesquisa))
            break
        except ValueError:
            print("-------------------------------------")
            print("❌ INVALID FORMAT, TRY AGAIN ❌")
            continue

def selecionar_formato(formato, dados_cfm, pesquisa):
    match formato:
        case "csv":
            exportar_csv(dados_cfm, pesquisa)
            print("-------------------------------------")
            return "⭐ EXPORTED TO .CSV SUCCESSFULLY ⭐"
        case "excel":
            exportar_excel(dados_cfm, pesquisa)
            print("--------------------------------------")
            return "⭐ EXPORTED TO .XLSX SUCCESSFULLY ⭐"
        case _:
            raise ValueError

def coletar():
    coleta: list = []
    try:
        coleta.append(input("➤  State: ").lower())
        coleta.append(input("➤  Specialization: ").lower())
        coleta.append(input("➤  Registration Type: ").lower())
        coleta.append(input("➤  Situation: ").lower())
        return coleta # ['são paulo', 'neurocirurgia', 'principal', 'ativo']
    except:
        raise ValueError

def preencher(arg):
    # seleciona o estado
    estado = Select(driver.find_element(By.NAME, "uf"))
    estado.select_by_value(estados[arg[0]])
    # seleciona o tipo de inscrição
    especialidade = Select(driver.find_element(By.NAME, "inscricao"))
    especialidade.select_by_value(inscrições[arg[2]])
    # seleciona a situação da inscrição
    especialidade = Select(driver.find_element(By.NAME, "tipoSituacao"))
    especialidade.select_by_value(situações[arg[3]])
    # seleciona a especialidade pelo código
    especialidade = Select(driver.find_element(By.NAME, "especialidade"))
    especialidade.select_by_value(especialidades[arg[1]])
    # clica em "ENVIAR"
    driver.find_element(By.XPATH, '//button[@class="w-100 btn-buscar btnPesquisar "]').click()
    time.sleep(2)
    anti_recaptcha(0)

def anti_recaptcha(arg):
    try:
        iframe = driver.find_element(By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')
        driver.switch_to.frame(iframe)
        time.sleep(1.5)
        driver.find_element(By.XPATH, '//*[@id="rc-imageselect"]/div[3]/div[2]/div[1]/div[1]/div[4]').click()
        driver.get_screenshot_as_file(f'click_recaptcha_p{arg}.png')
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'paginationjs-pages'))
            )
        except:
            driver.find_element(By.ID, 'recaptcha-reload-button').click()
            time.sleep(2)
            driver.find_element(By.XPATH, '//*[@id="rc-audio"]/div[8]/div[2]/div[1]/div[1]/div[4]').click()
            driver.get_screenshot_as_file(f'click_recaptcha_error_p{arg}.png')
    except:
        pass
    driver.switch_to.default_content()

def scrape():
    data: list = []
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'paginationjs-pages'))
    )
    paginação = driver.find_element(By.CLASS_NAME, 'paginationjs-pages')
    total_médicos = int(driver.find_element(By.XPATH, '//*[@id="resultados"]').text.split(' ')[0])
    print('==========================')
    print(f'💎 TOTAL DE MÉDICOS: {total_médicos}')
    print('--------------------------')

    total_páginas = int(paginação.find_elements(By.CSS_SELECTOR, 'li.paginationjs-page')[-1].text)
    página_atual: int = 1

    with alive_bar(total_médicos) as bar:
        while página_atual <= total_páginas:
            resultado = driver.find_element(By.CLASS_NAME, "busca-resultado")
            número = len(driver.find_elements(By.XPATH, '//div[contains(@class, "resultado-item resultMedico_")]')) + 1
            for x in range(1, número):
                médico = resultado.find_element(By.XPATH, f'//*[@id="content"]/div[1]/section[2]/div/div/div/div[1]/div[{x}]')
                nome = médico.find_element(By.TAG_NAME, 'h4').text
                if data != [] and nome in data[0]['Nome']:
                    página_atual -= 1
                    resolver = driver.find_element(By.CSS_SELECTOR, f'li.paginationjs-page[data-num="{página_atual}"]')
                    resolver.click()
                    WebDriverWait(driver, 4).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'li.paginationjs-page[data-num="{página_atual - 1}"'))
                    )
                    break
                else:
                    crm = médico.find_element(By.CLASS_NAME, 'col-md-4').text.replace('CRM:', '').strip()
                    inscrição = médico.find_element(By.CLASS_NAME, 'col-md-6').text.replace('Inscrição:', '').strip()
                    situação = médico.find_element(By.CLASS_NAME, 'col-md').text.replace('Situação:', '').strip()
                    data.append({
                        "CRM": crm,
                        "Nome": nome,
                        "Inscrição": inscrição,
                        "Situação": situação,
                    })
                    bar()
            if página_atual != total_páginas:
                próxima_página = driver.find_element(By.CSS_SELECTOR, f'li.paginationjs-page[data-num="{página_atual + 1}"]')
                próxima_página.click()
                página_atual += 1
                time.sleep(1)
                anti_recaptcha(página_atual)
                WebDriverWait(driver, 4).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f'li.paginationjs-page[data-num="{página_atual - 1}"'))
                )
            else:
                página_atual += 1

    return data

def exportar_csv(data, coleta):
    try:
        df = pd.DataFrame(data)
        df.to_csv(f"cfm_{coleta[1].lower()}_{estados[coleta[0]].lower()}.csv", index=False)
        return f"cfm_{coleta[1].lower()}_{estados[coleta[0]].lower()}.csv"
    except:
        raise ValueError

def exportar_excel(data, coleta):
    try:
        df = pd.DataFrame(data)
        df.to_excel(f"cfm_{coleta[1].lower()}_{estados[coleta[0]].lower()}.xlsx", sheet_name = f'{estados[coleta[0]].upper()}', index=False)
        return f"cfm_{coleta[1].lower()}_{estados[coleta[0]].lower()}.xlsx"
    except:
        raise ValueError

if __name__ == "__main__":

    link = "https://portal.cfm.org.br/busca-medicos/"

    options = Options()
    # options.add_argument("--headless")
    options.add_argument(usuário)
    options.add_argument("--start-maximized")
    options.add_extension('recaptcha.crx')
    options.add_argument('log-level=3')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options) # abre o navegador, sem acessar nenhuma página
    print("============================================================================")
    print(".:: 🧠 WELCOME TO THE BRAZILIAN FEDERAL COUNCIL OF MEDICINE DATABASE 🧠 ::.")
    print("============================================================================")
    driver.get(link)
    driver.find_element(By.XPATH, '//button[@class="button"]').click() # aceita os cookies

    main()