import time
import pyotp
import sys
from config import WALLETS, links, token, chain, EMAIL_LOGIN, EMAIL_2FA, OKX_2FA, IMAP_URL
from loguru import logger
from selenium.webdriver.remote.webdriver import By
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from seleniumbase import Driver
from imap_tools import MailBox


class OKX:
    def __init__(self):
        self.okx_url_login = "https://www.okx.cab/ru/account/login"
        self.driver = Driver(uc=True)
        self.AMOUNT_WALLETS = 20  # There's a maximum of 20 wallets in one pack
        self._zero = 0
        self._len_wallets = len(WALLETS)
        self.wallets_batches = [WALLETS[i:i + self.AMOUNT_WALLETS] for i in range(0, len(WALLETS), self.AMOUNT_WALLETS)]

    @staticmethod
    def manual_login():
        logger.info('Log in to your account and press ENTER')
        input()

    def scroll_window(self, x: int = 0, y: int = 50, up: bool = False):
        """
        Scrolls the window by the specified amount.

        Args:
            x (int): The horizontal scroll amount (default is 0).
            y (int): The vertical scroll amount (default is 50).
            up (bool): If True, scrolls the window upwards; if False, scrolls the window downwards (default is False).

        Returns:
            None
        """
        if up:
            y = -y
        self.driver.execute_script(f"window.scrollBy({x}, {y})")

    def filling_addresses(self, wallets: list):
        """Select the network and fill in the addresses in the fields"""
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/"
                                           "div[2]/div[4]/div[2]/button[2]/span").click()
        time.sleep(2)
        # choose a chain
        element = self.wait_an_element(By.XPATH, "//input[@placeholder='Выберите сеть']")
        if element:
            try:
                element.click()
            except (ElementClickInterceptedException, StaleElementReferenceException):
                time.sleep(3)
                element = self.wait_an_element(By.XPATH, "//input[@placeholder='Выберите сеть']")
                element.click()
        time.sleep(0.3)
        chains = self.driver.find_elements(By.CLASS_NAME, "balance_okui-select-item")
        try:
            for i in chains:
                if chain in i.text:
                    i.click()
        except Exception as error:
            logger.error(f"Error in filling_addresses function: {error}")
        time.sleep(0.3)
        # click add wallet
        for i in range(0, len(wallets)-1):
            btn = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/form/button/span")
            if btn:
                btn.click()
            else:
                self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/form/button").click()
                self.scroll_window()
            time.sleep(0.5)
        delete_acc = []
        input_forms = [i for i in self.driver.find_elements(By.CLASS_NAME, "balance_okui-input-input") if i.accessible_name == 'Адрес / домен']
        for wallet, form, _ in zip(wallets, input_forms, range(0, self.AMOUNT_WALLETS)):
            self._zero += 1
            logger.info(f'add : {wallet} [{self._zero}/{self._len_wallets}]')
            form.send_keys(wallet)
            delete_acc.append(wallet)
            time.sleep(0.01)
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]"
                                           "/div/form/div[3]/div/div/div/label/span[1]/input").click()
        self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div"
                                           "/div[2]/div/form/div[4]/div/div/div/button").click()
        time.sleep(1)

    def wait_an_element(self, by, element_selector: str, wait_time: int = 5):
        try:
            WebDriverWait(self.driver, wait_time).until(ec.presence_of_element_located((by, element_selector)))
            return self.driver.find_element(by, element_selector)
        except TimeoutException:
            logger.error(f'Error while waiting for an element: {element_selector}')
            sys.exit(-1)

    def confirmations(self):
        """Get the code from the mail and insert 2FA, close the window"""
        while True:
            for i in range(5):
                try:
                    time.sleep(1)
                    element = self.wait_an_element(By.XPATH, "//span[text()='Отправить код']")
                    if element:
                        element.click()
                    logger.success('Send code to email')
                    time.sleep(15)
                    break
                except Exception as error:
                    logger.error(f'Error in confirmations function: {error}')
            with MailBox(IMAP_URL).login(EMAIL_LOGIN, EMAIL_2FA) as mailbox:
                for msg in mailbox.fetch(limit=1, reverse=True):
                    if 'код' in msg.html or 'code' in msg.html:
                        code_email = msg.html.split('class="code" style')[1].split('>')[1].split('</div')[0].strip()
                        logger.success(f'mail_code : {code_email}')
                        check = True
                    else:
                        logger.info('Couldnt find the code, trying again')
                        check = False
                        time.sleep(5)
            if check:
                break
        code_forms = self.driver.find_elements(By.XPATH, "//input[@placeholder='Ввести код']")
        code_forms[0].send_keys(code_email)
        time.sleep(0.2)
        totp = pyotp.TOTP(OKX_2FA)
        code_forms[1].send_keys(totp.now())
        time.sleep(0.3)
        self.driver.find_elements(By.CLASS_NAME, 'btn-content')[-1].click()
        time.sleep(2)
        self.driver.get('https://www.okx.cab/ru/balance/withdrawal-address/eth/2')
        # is_closer = False
        # attempt = 0
        # while attempt < 5:
        #     try:
        #         self.driver.find_element(By.CLASS_NAME, 'okui-dialog-top-r').click()
        #         is_closer = True
        #         break
        #     except Exception as error:
        #         logger.error(f'Error in confirmations function while closing: {error}')
        #     try:
        #         self.driver.find_element(By.ID, 'okdDialogCloseBtn').click()
        #         is_closer = True
        #         break
        #     except Exception as error:
        #         logger.error(f'Error in confirmations function while closing: {error}')
        #     try:
        #         self.driver.find_element(By.CLASS_NAME, 'icon iconfont okds-close okui-dialog-c-btn').click()
        #         is_closer = True
        #         break
        #     except Exception as error:
        #         logger.error(f'Error in confirmations function while closing: {error}')
        #     attempt += 1
        #     time.sleep(0.3)
        # if not is_closer:
        #     logger.error(f"Не смог закрыть дуру, закрой сам!!!")

    def main(self):
        """
        A method to perform a series of actions, including accessing a URL, performing a manual login, accessing specific links,
         filling addresses, and handling confirmations.
        """
        self.driver.get(self.okx_url_login)
        time.sleep(5)
        self.manual_login()
        time.sleep(5)
        self.driver.get(links[token]['link'])
        time.sleep(5)
        for wallets in self.wallets_batches:
            while True:
                self.filling_addresses(wallets)
                self.confirmations()
                break
            logger.info('Sleep for 60   sec.')
            time.sleep(60)
        print()
