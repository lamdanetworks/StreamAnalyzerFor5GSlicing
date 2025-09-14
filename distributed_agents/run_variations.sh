#!/bin/bash

for episode in 100; do
 for a in 0.3 0.5 0.8;do
  for chance in 0.3 0.5 0.8; do
       (python train.py $episode $a $chance)
       (python sjf.py $episode $a $chance)
   
  done
 done
done

for episode in 500; do
 for a in 0.8;do
  for chance in 0.8; do
       (python train.py $episode $a $chance)
       (python sjf.py $episode $a $chance)
   
  done
 done
done
