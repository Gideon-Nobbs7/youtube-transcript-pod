#!/bin/bash
echo "Guess a number..."
read -p "Answer: " number
echo "Your guess is $number..."

if (( number == 42 ))
then
    echo "Correct, you guessed correctly!"
elif (( number == 41 || number == 43 ))
then
    echo "So close"
else
    echo "Incorrect guess"
fi