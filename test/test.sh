#!/bin/bash

echo "Тестирование TCP"

mkdir -p tcp
rm -f tcp/*

dd if=/dev/random of=../src/tcp/file_server.txt bs=1000000 count=2 2>/dev/null
echo "Новый файл создан"

nohup python3 ../src/tcp/server.py > tcp/server.txt 2>&1 &
sleep 5
python3 ../src/tcp/client.py > tcp/client.txt 2>&1
pkill -9 -f server.py 2>/dev/null
sleep 3


if cmp -s ../src/tcp/file_server.txt  ../src/tcp/file_client.txt
then
   echo "Результат - Файлы одинаковые"
else
   echo "Результат - Файлы разные"
fi

echo ""

echo "Тестирование UDP"
mkdir -p udp
rm -f udp/*

dd if=/dev/random of=../src/udp/file_server.txt bs=1000000 count=2 2>/dev/null
echo "Новый файл создан"

nohup python3 ../src/udp/server.py > udp/server.txt 2>&1 &
sleep 5
python3 ../src/udp/client.py > udp/client.txt 2>&1
pkill -9 -f server.py 2>/dev/null
sleep 3

if cmp -s ../src/udp/file_server.txt  ../src/udp/file_client.txt 
then
   echo "Результат - Файлы одинаковые"
else
   echo "Результат - Файлы разные"
fi


