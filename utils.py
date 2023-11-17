import undetected_chromedriver
import time
from selenium.webdriver.remote.webdriver import By
import pyotp
from imap_tools import MailBox
from config import WALLETS, links, token, chain, EMAIL_LOGIN, EMAIL_2FA, OKX_2FA, CHROME_VERSION
from loguru import logger

class OKX:

    def __init__(self):
        self.okx_url_login = "https://www.okx.cab/ru/account/login"
        self.chrome_vesrion = CHROME_VERSION
        self.driver = undetected_chromedriver.Chrome(version_main = self.chrome_vesrion)
        self.AMOUNT_WALLETS = 20 # There's a maximum of 20 wallets in one pack
        self._zero = 0
        self._len_wallets = len(WALLETS)
        self.wallets_batches = [WALLETS[i:i + self.AMOUNT_WALLETS] for i in range(0, len(WALLETS), self.AMOUNT_WALLETS)]

    def manual_login(self):
        logger.info('Log in to your account and press ENTER')
        input()

    def filling_addresses(self, wallets: list):
        """Select the network and fill in the addresses in the fields"""
        self.driver.find_element(By.CLASS_NAME, 'btn-content').click()
        time.sleep(2)

        # choose a chain
        self.driver.find_element(By.XPATH, f"//input[@placeholder='Выберите...']").click()
        time.sleep(0.3)
        try:
            for i in self.driver.find_elements(By.CLASS_NAME, 'okui-select-item'):
                if chain in i.text:
                    i.click()
        except Exception as error:
            pass
        time.sleep(0.3)

        # click add wallet
        for i in range(0, len(wallets)-1):
            self.driver.find_element(By.CLASS_NAME, "add-address-form-btn").click()
            time.sleep(0.2)

        delet_acc = []
        for wallet, id, _ in zip(wallets, self.driver.find_elements(By.XPATH, f"//input[@placeholder='Введите ваш адрес {links[token]['token']}']"), range(0, self.AMOUNT_WALLETS)):
            self._zero += 1
            logger.info(f'add : {wallet} [{self._zero}/{self._len_wallets}]')
            id.send_keys(wallet)
            delet_acc.append(wallet)
            time.sleep(0.01)

        time.sleep(1)
        scroll_by = self.driver.find_element(By.ID, 'scroll-box')
        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 1500", scroll_by)
        time.sleep(0.3)

        self.driver.find_elements(By.CLASS_NAME, "okui-checkbox-input")[-1].click()
        self.driver.find_elements(By.CLASS_NAME, "btn-content")[-1].click()
        time.sleep(1)

    def confirmations(self):
        """Get the code from the mail and insert 2FA, close the window"""
        while True:
            for i in range(5):
                try:
                    time.sleep(1)
                    self.driver.find_element(By.CLASS_NAME, 'okui-input-code-btn').click()
                    logger.success('Send code to email')
                    time.sleep(15)
                    break
                except: None

            email_url = 'imap.gmail.com'
            with MailBox(email_url).login(EMAIL_LOGIN, EMAIL_2FA) as mailbox:
                for msg in mailbox.fetch(limit=1, reverse=True):
                    if 'код' in msg.html or 'code' in msg.html:
                        code_email = msg.html.split('class="code" style')[1].split('>')[1].split('</div')[0].strip()
                        logger.success(f'mail_code : {code_email}')
                        check = True
                    else:
                        logger.info('Couldnt find the code, trying again')
                        check = False
                        time.sleep(5)

            if check == True:
                break

        self.driver.find_element(By.XPATH, "//div[@data-testid='verify-input-type-email']//input[@placeholder='Ввести код']").send_keys(code_email) # вставляем код из почты
        time.sleep(0.1)
        totp = pyotp.TOTP(OKX_2FA)
        self.driver.find_element(By.XPATH, "//div[@data-testid='verify-input-type-google']//input[@placeholder='Ввести код']").send_keys(totp.now()) # вставляем 2fa код
        time.sleep(0.1)
        self.driver.find_elements(By.CLASS_NAME, 'btn-content')[-1].click()
        time.sleep(1)
        try:
            self.driver.find_element(By.CLASS_NAME, 'okui-dialog-top-r').click()
        except:
            pass
        try:
            self.driver.find_element(By.ID, 'okdDialogCloseBtn').click()
        except:
            pass

    def main(self):
        self.driver.get(self.okx_url_login)
        time.sleep(5)
        self.manual_login()

        time.sleep(5)
        self.driver.get(links[token]['link'])
        time.sleep(5)

        for wallets in self.wallets_batches:
            while True:
                try:
                    self.filling_addresses(wallets)
                    self.confirmations()
                    break
                except Exception as error:
                    logger.error(f'Try again in 30 sec., error: {error}')
                    time.sleep(30)
            logger.info('Sleep for 60 sec.')
            time.sleep(60)

        print()
