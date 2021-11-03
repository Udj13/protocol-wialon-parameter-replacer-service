# protocol-wialon-parameter-replacer-service

Simple multithreaded socket server.

Protocol supported: Wialon IPS 1.1 (http://extapi.wialon.com/hw/cfg/Wialon%20IPS_en.pdf)

Application: Сonverts data packets “on the fly”. Moving additional parameters value to the “Analog input”, if the current GPS tracking server doesn't recognize additional parameters.

![wialon_packet_D_description](https://bitlite.ru/wp-content/uploads/2021/11/wialon-packet-D.png)

For example, additional parameter “fuel:2:45.8” can be retranslated as the first analog input.

![log screen](https://bitlite.ru/wp-content/uploads/2021/11/protocol-wialon-parameter-replacer-service.jpg)

Log:

<---- server  b'#L#8667950;NA\r\n' 

server ---->  b'#AL#1\r\n' 

tracker --->  b'#D#021121;121111;4515.8742;N;5421.1371;E;0;0;300;7;NA;0;0;777,888;NA;can32:2:111,can33:2:222,**can34:2:333**\r\n' 

<---- server  b'#D#021121;121111;4515.8742;N;5421.1371;E;0;0;300;7;NA;0;0;777,888,**333**;NA;can32:2:111,can33:2:222,can34:2:333\r\n'

server ---->  b'#AD#1\r\n'

   
   

Description in Russian (https://bitlite.ru/protocol-wialon-parameter-replacer-service-2/)
