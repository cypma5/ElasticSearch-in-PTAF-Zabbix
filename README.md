# Мониторинг состояния ElasticSearch в PTAF с помощью Zabbix-Agent
# Инструкция по установке и настройке
1. Устанавливаем Zabbix-Agent
2. Настраиваем PTAF, открываем порт в Aliases
3. В архиве `zabbix_ptaf_elasticsearch.zip` лежат все необходимые ресурсы `es_zabbix.py` `elasticsearch` `urllib3`
4. В папку `/etc/zabbix/scripts/` копируем файл `es_zabbix.py` и две папки `elasticsearch` , `urllib3` с библиотеками Python для работы скрипта.
5. Даём права на скрипт 
`chmod +x es_zabbix.py`
5. Проверяем владельца скрипта, при необходимости меняем на 
`chown zabbix:zabbix /etc/zabbix/scripts/es_zabbix.py`
6. В `es_zabbix.py` меняем PASSWORD  в строке `http_auth=('root','PASSWORD')` на содержимое файла `/opt/waf/conf/master_password`
7. Прописываем в `/etc/zabbix/zabbix.conf` пользовательские диррективы
........................Добавлю позже
8. Устанавливаем Template на Zabbix Server
9. Перезапускам zabbix-agent
10. Если все сделали правильно в папке /tmp/ появятся данные за последнюю минуту

Можно вручную проверить работу скрипта 
Выполнив 
`/etc/zabbix/scripts/es_zabbix.py health status`
