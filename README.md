# BinGraphicsExtractor
---
###Description
This script is made to extract grahpics in formats like jpg, gif, png from binary files.
It can also replace images within binaries.

###Usage
If you want to **extract** files from binary see examples below

If you want to **replace** image within binary first extract them to know indexes.

For example:

after image extracting you will have files like image0.png, image1.png and so on... This numbers are index you want to use in replacing.
 
###Examples
Extract png files from binary
```python main.py -f <path to binary> -t png```

Extract gif files from binary
```python main.py -f <path to binary> -t gif```

Replace file within binary - this file has to be smaller or equal to size of original file
```python main.py -f <path to binary> -r <path to image replacer> -i <index of original file> -t png```  