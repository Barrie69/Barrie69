i=0

while [ $i = 0]
do

echo "Wat wil je gebruiken voor je webserver apache2 of nginx?"
read opensourse

if [ $opensourse = "apache2" ]
then
zypper install apache2

elif [ $opensourse = "nginx" ]
then
zypper install nginx

fi

echo "nextcloud is bezig met installeren"
zypper install nextcloud

echo "fail2ban is bezig met installeren"
zypper install fail2ban


echo "Wil je dat het script opniew word geladen? y/n"

if [ $e = "n" ]
then
((i++))
echo "Het script is stop gezet"
else
echo "Het script word opnieuw gestart."
fi

done
