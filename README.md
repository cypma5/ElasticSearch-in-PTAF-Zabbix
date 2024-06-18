# Мониторинг состояния ElasticSearch в PTAF 3 с помощью Zabbix-Agent
# Инструкция по установке и настройке

1. Устанавливаем Zabbix-Agent
```bash
af-tools.py 
```
`-> 7. Установка утилит`
`-> 5. zabbix-agent`

2. открываем порт в WEB интерфейсе PTAF `network aliases ->` `<<MGMT или WAN>>` -> `TCP` > `10050`

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

7. Перезапускам zabbix-agent

```bash
systemctl restart zabbix-agent
```

7. Если все сделали правильно в папке /tmp/ появятся данные за последнюю минуту
-rw-rw-r-- 1 zabbix zabbix 2.3K Jun 18 08:17 /tmp/es_zabbix-cluster.json
-rw-rw-r-- 1 zabbix zabbix  338 Jun 18 08:17 /tmp/es_zabbix-health.json
-rw-rw-r-- 1 zabbix zabbix 7.2K Jun 18 08:16 /tmp/es_zabbix-indices.json
-rw-rw-r-- 1 zabbix zabbix 7.1K Jun 18 08:17 /tmp/es_zabbix-nodes.json


8. Можно вручную проверить работу скрипта выполнив 

```bash
sudo -u zabbix /etc/zabbix/scripts/es_zabbix/es_zabbix.py health status`
```




Возможные ошибки
в Latest Data zabbix
`Usage: es_zabbix.py [api|discover] key:subkey:subkey`
проверить что в пункте 5. правильно добавилась строка UserParameter
и в пункте 7. создались файлы, с содержимым состояния elasticsearch