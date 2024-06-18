Этот скрипт на Python позволяет проверять состояние Elasticsearch сервера с использованием Zabbix агента.

# Установка

1. Устанавливаем Zabbix-Agent
```bash
af-tools.py 
```
`-> 7. Установка утилит`
`-> 5. zabbix-agent`

2. открываем порт в WEB интерфейсе PTAF `network aliases ->` `<<MGMT или WAN>>` -> `TCP` > `10050`
<img src="/.images/2024-06-18_07-21-31.png" alt="Описание изображения">


3. копируем архив `es_zabbix.tar.gz` в `/home/pt/`

4. Распаковываем скрипт в `/etc/zabbix/scripts/es_zabbix/`

```bash
tar -xzvf /home/pt/es_zabbix.tar.gz -C /etc/zabbix/scripts/
```

5. в конфигурационный файл `/etc/zabbix/zabbix_agentd.conf` добавляем пользовательский параметр

```bash
UserParameter=pt_elastic_zabbix[*],/opt/es_zabbix/es_zabbix.py $1 $2
```

6. Устанавливаем Template `zbx_export_templates.xml` на Zabbix Server

7. Добавляем host с PTAF3 и привязываем к нему Template `Template App PTAF ElasticSearch`

8. Перезапускам zabbix-agent

```bash
systemctl restart zabbix-agent
```

# Проверка работы
Пример алерта, который будет появлятся для standalone ноды
<img src="/.images/2024-06-18_08-54-32.png" alt="Описание изображения">



# Диагностика проблем
1. Если все сделали правильно в папке /tmp/ появятся данные за последнюю минуту
```bash
ls -lah /tmp/es_zabbix-*
```

2. Можно вручную проверить работу скрипта выполнив 

```bash
sudo -u zabbix /etc/zabbix/scripts/es_zabbix/es_zabbix.py health status`
```

3. в Latest Data zabbix
`Usage: es_zabbix.py [api|discover] key:subkey:subkey`
проверить что в пункте 5. правильно добавилась строка UserParameter
и в пункте 7. создались файлы, с содержимым состояния elasticsearch
