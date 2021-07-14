export VIP=$1
#!/bin/sh
while [ 2 -le 5 ]
do
        curl -kvi --resolve www.bookinfo.com:443:$VIP https://www.bookinfo.com/productpage
        curl -kvi --resolve www.httpbin.com:443:$VIP https://www.httpbin.com
        sleep 5
done
