# Мониторинг состояния ElasticSearch в PTAF с помощью Zabbix-Agent
# Инструкция по установке и настройке
1. Устанавливаем Zabbix-Agent через af-tools 7-5,Указываем IP сервера zabbix

2. открываем порт в WEB интерфейсе network aliases -> <<Алиас интерфейса на котрором предполагается открыть порт zabbix-agent MGMT по умолчанию>> -> TCP > 10050

3. копируем архив `es_zabbix.tar` в `/home/pt/`

4. Распаковываем скрипт в #/opt/es_zabbix 

```bash
#tar -C / -xvf es_zabbix.tar
```

5. в конфигурационный файл `/etc/zabbix/zabbix_agentd.conf` добавляем пользовательский параметр

```bash
UserParameter=pt_elastic_zabbix[*],/opt/es_zabbix/es_zabbix.py $1 $2
```


4.1  Выдаём права

#`chown zabbix:zabbix /opt/es_zabbix/`

5. Устанавливаем Template `zbx_export_templates.xml` на Zabbix Server

6. Перезапускам zabbix-agent

```bash
systemctl restart zabbix-agent
```

7. Если все сделали правильно в папке /tmp/ появятся данные за последнюю минуту
`-rw-rw-r-- 1 zabbix zabbix 2.3K Jun 18 08:17 /tmp/es_zabbix-cluster.json`
`-rw-rw-r-- 1 zabbix zabbix  338 Jun 18 08:17 /tmp/es_zabbix-health.json`
`-rw-rw-r-- 1 zabbix zabbix 7.2K Jun 18 08:16 /tmp/es_zabbix-indices.json`
`-rw-rw-r-- 1 zabbix zabbix 7.1K Jun 18 08:17 /tmp/es_zabbix-nodes.json`


8. Можно вручную проверить работу скрипта выполнив 

```bash
sudo -u zabbix /etc/zabbix/scripts/es_zabbix/es_zabbix.py health status`
```




Возможные ошибки
в Latest Data zabbix
`Usage: es_zabbix.py [api|discover] key:subkey:subkey`
проверить что в пункте 5. правильно добавилась строка UserParameter
и в пункте 7. создались файлы, с содержимым состояния elasticsearch