#!/bin/bash

for i in {3..15}
do
   for j in {3..20}
   do
      python3 assignment_4.py --cost $i --duration $j --demands 200 --matrix sample.npy --sim True
   done
done