# Мониторинг состояния ElasticSearch в PTAF с помощью Zabbix-Agent
# Инструкция по установке и настройке
1. Устанавливаем Zabbix-Agent через af-tools 7-5,Указываем IP сервера zabbix

2. открываем порт в WEB интерфейсе network aliases - WAN - TCP - 10050

3. копируем архив `es_zabbix.tar` в `/home/pt/`

4. Распаковываем скрипт в /opt/es_zabbix 

`tar -C / -xvf es_zabbix.tar`

5. в конфиг  `/etc/zabbix/zabbix_agentd.conf` добавляем

`UserParameter=pt_elastic_zabbix[*],/opt/es_zabbix/es_zabbix.py $1 $2`

4.1  Выдаём права

`chown zabbix:zabbix /opt/es_zabbix/`

5. Устанавливаем Template `zbx_export_templates.xml` на Zabbix Server

6. Перезапускам zabbix-agent

`systemctl restart zabbix-agent`

7. Если все сделали правильно в папке /opt/es_zabbix/ появятся данные за последнюю минуту


8. Можно вручную проверить работу скрипта 
Выполнив 

`sudo -u zabbix /opt/es_zabbix/es_zabbix.py health status`
