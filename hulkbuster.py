import requests
import sched
import time
import webbrowser
import json
import traceback
import random
import string
from colorama import Fore
from playsound import playsound
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3
import sys


class HulkBuster:
    def __init__(self):
        self.request = None
        # Every X seconds. In this case, 15.
        self.interval = 15
        # The sound file to play.
        self.sound_file = "wake_up.wav"
        # The base rogue fitness url.
        self.product_list = "products.txt"
        self.product_urls = []
        self.soup = None
        self.opened_urls = []
        self.opened_items = []
        self.a = Fore.LIGHTGREEN_EX
        self.b = Fore.RESET
        self.c = Fore.LIGHTYELLOW_EX
        self.d = Fore.LIGHTRED_EX
        self.e = Fore.LIGHTBLUE_EX
        self.f = Fore.LIGHTCYAN_EX
        self.banner = f"\n\nWelcome to {self.a}HULK{self.d}BUSTER{self.b}! Let's park in front of \n" \
                      f"{self.e}Rogue Fitness{self.b} until our gear is in stock!\n\n"

        self.banner += f"{self.d}  _  _ _   _ _    _  _____ _   _ ___ _____ ___ ___ \n"
        self.banner += f"{self.d} |{self.b} || | | | | |  | |/ / _ ) | | / __|_   _| __| _ {self.d}\\{self.b}\n"
        self.banner += f"{self.d} |{self.c} __ | |_| | |__| ' <| _ \ |_| \__ \ | | | _||   {self.d}/{self.b}\n"
        self.banner += f"{self.d} |_||_|\___/|____|_|\_\___/\___/|___/ |_| |___|_|_{self.d}\\{self.b}\n"
        print(self.banner)

    def start(self, scheduler):
        # Don't follow redirects. This gets us the true status code.
        with open(self.product_list, "r") as f:
            self.product_urls = f.read().splitlines()

        for url in self.product_urls:
            self.request = requests.get(url, allow_redirects=False)
            # This page is up! That means the used bars are available. Let's print.
            if self.request.status_code == 200:
                # This one is for grab bags / available options.
                self.print_availability(url)
                # This one is for everything else.
                self.check_other_quantity(url)
            # This is 301 or something else. There are no grab bag bars available.
            else:
                pass
                #print("Not in stock")
            # Repeat this same function every X seconds.
            s.enter(self.interval, 1, self.start, (scheduler,))

    def print_availability(self, url):
        self.soup = BeautifulSoup(self.request.text, "html.parser")
        title = self.soup.findAll("title")[0].text.split("|")[0].rstrip()
        #print(f"Checking {url}")
        found_something = False
        new_item = None

        # We're going to trawl through the options and ignore everything that isn't a product.
        for i in self.soup.findAll("option"):
            new_item = i.text.strip()
            if "Choose a Selection" not in new_item and "Choose an Option" not in new_item:
                if "Out of stock" not in new_item and "Coming Soon" not in new_item:
                    found_something = True
        if found_something:
            self.update_all(url, new_item, title)

    def update_all(self, url, item, title):
        alert_str = f"{self.a}IN STOCK{self.b} {self.d}[{self.c}{title}{self.d}] {self.b}" \
                    f"[{self.d}{item}{self.b}]" #- {self.e}{url}{self.b}"

        self.announce(url, item)
        self.update_urls(url, alert_str)
        self.update_items(item, alert_str)

    def check_other_quantity(self, url):
        quantity = []
        title = self.soup.findAll("title")[0].text.split("|")[0].rstrip()
        try:
            for item in self.soup.findAll("div", {"class": "grouped-item"})[1:]:
                item_name = item.findAll("div", {"class", "item-name"})[0].text
                qty = item.findAll("div", {"class", "item-qty"})

                quantity.append([item_name, qty, title.rstrip(), url])

        except IndexError:
            print(f"Unable to grab data from {url}")

        if len(quantity) > 0:
            for item in quantity:
                if len(item[1]) > 0:
                    self.update_all(url, item[0], title)

        else:
            # Maybe the options are stored in javascript on the page? If so, let's try to read that.
            # May need to change some code around if there's a problem in the future.
            # Likely the problem is the 'js' being on a different line than anticipated.
            self.read_js_json_payload(url, title)

    def read_js_json_payload(self, url, title):
        js = None
        is_in_stock = False
        try:
            js = str(self.soup.findAll("div", {"id": "product-options-wrapper"})[0].
                     findAll("script")[0]).splitlines()[5][:-1]

            if len(js) > 0:
                attributes = []
                try:
                    attributes = json.loads(js)['attributes']
                except TypeError:
                    pass
                if len(attributes) > 0:
                    for attr in attributes:
                        for i in attributes.get(attr):
                            new_list = attributes[attr][i]
                            if type(new_list) == list:
                                options = new_list[0]["additional_options"]
                                if type(options) == dict:
                                    for opt in options:
                                        in_stock = options[opt].get("isInStock")
                                        option_label = options[opt].get("label")
                                        if in_stock:
                                            is_in_stock = True
                                            self.update_all(url, option_label, title)
            if not is_in_stock:
                attributes = []
                try:
                    js = json.loads(str(self.soup.findAll("div", {"class": "default-swatches"})[0].
                                        findAll("script")[0]).splitlines()[2][:-1])
                except IndexError:
                    # Doesn't exist, just ignore it.
                    pass
                except Exception:
                    try:
                        raise Exception(f"You're on {url}. Title is {title}.\n Send me this stack trace")
                    except:
                        pass
                    traceback.print_exc()

                #  For color swatches.
                if len(js) > 0:
                    for attr in attributes:
                        new_dict = attributes[attr]
                        if type(new_dict) == dict:
                            for item in new_dict:
                                new_list = new_dict.get(item)
                                if type(new_list) == list:
                                    for prod in new_list:
                                        label = prod.get("label")
                                        if not "Out of Stock".lower() in label.lower() and not "Coming Soon".lower() in label.lower():
                                            self.update_all(url, label, title)
                else:
                    # This might be something like the "OSO" mini bar page.
                    self.read_additional_options(url, title)
        except TypeError:
            pass
        except IndexError:
            pass
        except Exception as e:
            print(f"=======\nSend this to me: \nURL: {url}\nTitle: {title}\njs: {js}\nError: {str(e)}\n=======")
            raise

    def read_additional_options(self, url, title):
        add_to_cart_button = self.soup.findAll("div", {"class": "add-to-cart"})[0].text.rstrip()
        if len(add_to_cart_button) > 0:
            # Until this comes in stock, I can't reliably test it. We'll use the "title" as the product item name.
            # So, no options. e.g: Purple, Red, Blue, Green.
            new_title = self.soup.findAll("title")[0].text.split("|")[0].rstrip()
            self.update_all(url, new_title, new_title)
        pass

    def get_time(self):
        now = datetime.now()
        return now.strftime(f"{self.d}[{self.b}%Y{self.d}-{self.b}%m{self.d}-{self.b}%d{self.d} @ "
                            f"{self.b}%H{self.d}:{self.b}%M{self.d}:{self.b}%S{self.d}]{self.b}")

    def update_urls(self, url, alert_str):
        if not self.item_used(url, self.opened_urls):
            self.opened_urls.append(url)

    def update_items(self, item, alert_str):
        if not self.item_used(item, self.opened_items):
            print(f"{self.get_time()} {alert_str}")
            self.opened_items.append(item)

    @staticmethod
    def item_used(item, list_obj):
        for new_item in list_obj:
            if item == new_item:
                return True
        return False

    def announce(self, url, item):
        # We haven't already opened this browser. Let's do it
        if not self.item_used(url, self.opened_urls):
            self.play_sound(url)
        # We already opened the browser...
        else:
            # No need to open it again unless a new item comes in stock...
            if not self.item_used(item, self.opened_items):
                self.play_sound(url)

    def play_sound(self, url):
        try:
            rnd_string = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(7))
            webbrowser.open(f"{url}?={rnd_string}")
        except Exception:
            print("Couldn't open web browser. This is all your fault")
        try:
            playsound(self.sound_file, False)
        except Exception:
            print("Couldn't play alarm. This is all your fault.")


if __name__ == "__main__":
    hb = HulkBuster()
    s = sched.scheduler(time.time, time.sleep)
    try:
        s.enter(1, 1, hb.start, (s,))
        s.run()
    except urllib3.exceptions.ProtocolError:
        pass
    except requests.exceptions.ConnectionError:
        pass
    # When you switch VPNs.
    except requests.exceptions.ChunkedEncodingError:
        pass
    # When your computer goes to sleep.
    except OSError:
        pass
    except KeyboardInterrupt:
        sys.exit(1)

