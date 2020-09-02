import sys

filename = sys.argv[1]

with open(filename, 'rb') as bigfile:
    chunksize = 1000
    readable = ''
    while bigfile:
        start = bigfile.tell()
        print("starting at: {}".format(start))
        file_block = ''
        for _ in range(start,start + chunksize):
            line = bigfile.__next__()
            file_block = file_block + str(line)
            print('file_block' + str(type(file_block)) + file_block)
        readable = readable + file_block
        stop = bigfile.tell()
        print("readable" + str(type(readable)) + readable)
        print('reading bytes from %s to %s '%(start, stop))
        print("read bytes total:" +str(len(readable)))