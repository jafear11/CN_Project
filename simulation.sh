#!/bin/bash

for i in {1..10}
do
   python3 graph.py --cost $i
done