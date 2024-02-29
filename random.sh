# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    random.sh                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: tvandorm <tvandorm@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/19 11:58:22 by tvandorm          #+#    #+#              #
#    Updated: 2024/01/16 15:26:32 by tvandorm         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <n> <min> <max>"
    exit 1
fi

n=$1
min=$2
max=$3

if [ $n -le 0 ]; then
    echo "Please specify a positive integer for n."
    exit 1
fi

if ! [[ "$n" =~ ^[0-9]+$ ]]; then
    echo "Please specify a positive integer for n."
    exit 1
fi

if [ $min -ge $max ]; then
    echo "min should be less than max."
    exit 1
fi

# Check if the range is sufficient
if [ $n -gt $((max - min + 1)) ]; then
    echo "The available range of random numbers is insufficient."
    exit 1
fi

# Generate n random unique numbers and concatenate them into a single line
numbers=$(awk -v n=$n -v min=$min -v max=$max -v seed="$(date +%s%N)" 'BEGIN{srand(); while (c < n) {x = int(min + rand() * (max - min + 1)); if (!(x in arr)) {arr[x]; printf "%s ", x; c++}}}')

# Print the concatenated numbers
echo $numbers
