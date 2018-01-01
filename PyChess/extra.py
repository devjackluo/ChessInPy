count = 0
for tiles in range(64):
    if tiles < 10:
        print('0', end=str(tiles)+",")
    else:
        print('', end=str(tiles) + ",")
    count += 1
    if count == 8:
        print('', end='\n')
        count = 0
