paste dtime.txt dv.txt > tv.txt
paste dtime.txt di.txt > ti.txt
/home/carol/isifilter
graph -T X  --blankout 0.0 -g 1 -x 2700 5400 -y -80 40 -h 0.35 -w 0.5 -u 0.6 -r 0.2   -C tv.txt  --reposition 0.2 0.4 1.0  -f 0.1 -h 0.175 -y 0 0.4 -u 0 -r 0 -C ti.txt  --reposition 0.2 0.0 1.0 -h 0.2 -u 0.1 -m 0 -x 0.05 0.30 -y 0 25 -S 16 0.1 fi_up.txt -S 4 0.1 fi_down.txt 
