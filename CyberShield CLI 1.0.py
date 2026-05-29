# генератор трафика
import random
statuses = [200, 500, 400]
while True:
    attack_list = []
    complited_list = []
    in_work_list = []
    command = input("Введите команду: ").lower().strip()
    if command == "generate":
     with open("server_access.log", "w", encoding="utf-8") as file:
        for i in range(100):
            x1 = random.randint(1, 254)
            x2 = random.randint(1, 254)
            x3 = random.randint(1, 254)
            x4 = random.randint(1, 254)
            adres = f"{x1}.{x2}.{x3}.{x4}"
            random_status = random.choice(statuses)
            if random_status == 200:
                file.write(f"{i}. [INFO] IP: {adres} Status: in work\n")
                in_work_list.append(i)
            elif random_status == 500:
                file.write(f"{i}. [INFO] IP: {adres} Status: attack\n")
                attack_list.append(i)
            elif random_status == 400:
                file.write(f"{i}. [INFO] IP: {adres} Status: complited\n")
                complited_list.append(i)
    
    elif command == "scan":     #анализатор
        current_banned = []
        try:
            with open("ban_ips.log", "r", encoding="utf-8") as file_ban:
                for line in file_ban:
                    current_banned.append(line.strip())
        except FileNotFoundError:
            print("[-] Ошибка! Файл логов еще не создан. Сначала вызовите команду 'ban'.")
        attack_count = 0
        complited_count = 0
        in_work_count = 0
        try:
         with open("server_access.log", "r", encoding="utf-8") as file:
            for line in file:
                if "attack" in line:
                    if line in current_banned:
                        print(f"Атака с адреса {line.strip()} отражена")
                        continue    
                    attack_count += 1
                elif "in work" in line:
                    in_work_count += 1
                elif "complited" in line:
                    complited_count += 1
         print(f"Номера строк лога, которые зафиксировали атака: {attack_list}. Общее количество атак: {attack_count}")
         print(f"Номера строк лога, которые показывают статус в работе: {in_work_list}. Количество процессов в работе: {in_work_count}")
         print(f"номера строк лога, которые показывают выполненные процесс: {complited_list}. Количество выполненных процессов: {complited_count}")
        except FileNotFoundError:
            print("[-] Ошибка! Файл логов еще не создан. Сначала вызовите команду 'generate'.")

    elif command == "ban":      #бан
            ip_to_ban = input("Введите ip-адрес, который нужно заблокировать: ").strip()
            with open("ban_ips.log", "r", encoding="utf-8") as file_ban:
                banned_ips = []
                for line in file_ban:
                    banned_ips.append(line.strip())
                if ip_to_ban in banned_ips:
                    print("Данный IP уже заблокирован.")
                    continue
                else:
                    with open("ban_ips.log", "a", encoding="utf-8") as file_ban:
                        file_ban.write(f"{ip_to_ban}\n")

    elif command == "unban":        #разблокировка
        ip_to_unban = input("Введите IP адрес для разблокировки: ").strip()
        with open("ban_ips.log", "r", encoding="utf-8") as file_ban:
            banned_ips = []
            for line in file_ban:
                banned_ips.append(line.strip())
            if ip_to_unban not in banned_ips:
                print("Данный адрес не заблокирован")
                continue
            else:
                banned_ips.remove(ip_to_unban)
                with open("ban_ips.log", "w", encoding="utf-8") as file_ban:
                    for ip in banned_ips:
                        file_ban.write(f"{ip}\n")

    elif command == "exit":     #выход
        print("Выход выполнен")
        break
    else:
        print("Команда неизвестна. Доступные команды: generate, scan, ban, exit")