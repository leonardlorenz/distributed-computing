#!/bin/bash

i="0"

while [ $i -lt 10000 ]
do
    python client.py &
i=$[$i+1]
done
