## Building project
```
cmake .
make
```

## Generating positive dataset
```
./generate <board_size> > outputfile.txt
e.g.
./generate 3 > positive.txt
```

## Generating negative dataset
```
python3 negative.py > negative.txt
```