# Установка SSH-сервера в Ubuntu, доступ к WSL по сети и использование SSH-ключей

## Цели работы

После выполнения работы сможешь:

- Установить и запустить SSH-сервер на Ubuntu.
- Понять отличие сетевого стека WSL от обычного Linux-сервера.
- Настроить доступ к WSL по SSH с другого устройства.
- Настроить SSH-ключи и использовать их вместо паролей.
- Загружать и скачивать файлы по SSH.

---

## Часть 1. Установка SSH на Ubuntu

### 1. Обновление списка пакетов

    sudo apt update

### 2. Установка SSH-сервера

    sudo apt install ssh

Пакет ssh — это метапакет, который устанавливает:

- openssh-server
- openssh-client
- openssh-sftp-server

### 3. Проверка статуса службы

    systemctl status ssh

Ожидаемый статус:

    Active: active (running)

---

## Часть 2. Особенности SSH в WSL

WSL2 работает как виртуальная машина внутри Windows. Это означает:

- WSL получает IP вида 172.x.x.x, скрытый за NAT.
- Устройства в сети (192.168.x.x) не могут напрямую подключиться к WSL.
- Автозапуск systemd ограничен.
- Для удаленного подключения требуется проброс порта со стороны Windows.

---

## Часть 3. Запуск SSH-сервера в WSL

SSH в WSL не запускается автоматически. Запустите вручную:

    sudo systemctl start ssh

Проверка:

    ps aux | grep ssh

---

## Часть 4. Почему другие устройства не могут подключиться к WSL напрямую

Команда:

    ip addr show

показывает IP вида 172.23.101.7

Этот IP недоступен другим устройствам в сети.  
Для подключения требуется проброс порта.

---

## Часть 5. Настройка проброса порта 22 (Windows → WSL)

### Узнать IP WSL

    ip addr show eth0

### Узнать IP Windows

В PowerShell:

    ipconfig

### Создать проброс порта

PowerShell от администратора:

    netsh interface portproxy add v4tov4 listenport=22 listenaddress=0.0.0.0 connectport=22 connectaddress=172.23.101.7

### Разрешить порт в firewall Windows

    netsh advfirewall firewall add rule name="WSL SSH" dir=in action=allow protocol=TCP localport=22

Теперь можно подключаться:

    ssh <username>@192.168.1.42

---

## Часть 6. Изменение IP WSL

После перезапуска Windows WSL получает новый IP.  
Portproxy нужно перенастроить.

---

## Часть 7. SSH-ключи

### Генерация ключей

    ssh-keygen -t ed25519 -C "student-key"

Ключи создаются в:

- ~/.ssh/id_ed25519
- ~/.ssh/id_ed25519.pub

### Установка ключа на сервер

Если доступен ssh-copy-id:

    ssh-copy-id username@SERVER_IP

Иначе вручную:

    scp ~/.ssh/id_ed25519.pub username@SERVER_IP:~/

На сервере:

    mkdir -p ~/.ssh
    cat ~/id_ed25519.pub >> ~/.ssh/authorized_keys
    chmod 700 ~/.ssh
    chmod 600 ~/.ssh/authorized_keys

### Подключение без пароля

    ssh username@SERVER_IP

---

## Часть 8. Передача файлов по SSH

### SCP

Загрузка файла:

    scp file.txt username@SERVER_IP:/home/username/

Скачивание файла:

    scp username@SERVER_IP:/home/username/file.txt .

Загрузка папки:

    scp -r myfolder username@SERVER_IP:/home/username/

### SFTP

Подключение:

    sftp username@SERVER_IP

Команды:

- ls — показать файлы
- lcd — сменить локальную директорию
- cd — сменить директорию на сервере
- put file.txt — отправить файл
- get file.txt — скачать файл

---

## Контрольные вопросы

1. Что устанавливает пакет ssh в Ubuntu?
2. Почему SSH-сервер в WSL не запускается автоматически?
3. Какие сетевые ограничения WSL мешают прямому SSH?
4. Для чего используется portproxy?
5. В чем отличие приватного и публичного ключей?
6. Как передавать файлы через SSH?

