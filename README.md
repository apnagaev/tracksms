# tracksms
tracksms - is service for route telegram messages from traccar to dedicated chat for each device. You can create chat and receive notification only for one device in this chat.
file smsconf.txt contain json with port numder and telegrambot token
file userdevice.txt contain json with device ID and telegram chatid for this device
in traccar you can configure sms notification and use notification type - sms for this service
```
<entry key='notificator.sms.manager.class'>org.traccar.sms.HttpSmsClient</entry>
<entry key='sms.http.url'>http://tracksms:8000</entry>
<entry key='sms.http.template'>userphone={phone}&amp;text={message}</entry>
```

you can dockerize it
```
docker build -t tracksms .
```

in docker compose:
```
  tracksms:
    image: tracksms
    dns:
      - 1.1.1.1
    networks:
      - traccar
    ports:
      - 8000:8000
    container_name: tracksms
    restart: unless-stopped
    environment:
      TZ: "Europe/Moscow"
    volumes:
      - ./userdevices.txt:/httpserver/userdevices.txt
      - ./smsconf.txt:/httpserver/smsconf.txt
```
