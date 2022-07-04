# Мониторинг состояния ElasticSearch в PTAF с помощью Zabbix-Agent
# Инструкция по установке и настройке
1. Устанавливаем Zabbix-Agent через af-tools 7-5,Указываем IP сервера zabbix
2. открываем порт в WEB интерфейсе ......
3 копируем архив zabbix_ptaf_elasticsearch.zip в /home/pt/
4 `unzip zabbix_ptaf_elasticsearch.zip -d /etc/zabbix/scripts/`
5 `chown zabbix:zabbix /etc/zabbix/scripts/es_zabbix/*`
`chmod +x  /etc/zabbix/scripts/es_zabbix/es_zabbix.py`
6. Настраиваем PTAF, открываем порт в Aliases
7. В `es_zabbix.py` меняем PASSWORD  в строке `http_auth=('root','PASSWORD')` на содержимое файла `/opt/waf/conf/master_password`
8. Прописываем в `/etc/zabbix/zabbix.conf` пользовательские диррективы

`cp /etc/zabbix/zabbix_agentd.conf /etc/zabbix/zabbix_agentd.conf.backup`
`echo "UserParameter=pt_elastic_zabbix[*],/etc/zabbix/scripts/es_zabbix.py $1 $2" >> /etc/zabbix/zabbix_agentd.conf`

8. Устанавливаем Template `zbx_export_templates.xml` на Zabbix Server
9. Перезапускам zabbix-agent
10. Если все сделали правильно в папке /tmp/ появятся данные за последнюю минуту

Можно вручную проверить работу скрипта 
Выполнив 
`/etc/zabbix/scripts/es_zabbix.py health status`
