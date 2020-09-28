import sys
import math

def map(filename, fileout, new_x0, new_y0, new_x1, new_y1, \
        long0, lat0, long1, lat1, long2, lat2):
    fin = open(filename, "r")
    fout = open(fileout, "w+")
    x_col = []
    y_col = []


    for line in fin.readlines():
        converted = []
        # parsing
        point = line.split("\t")
        for i in range(len(point)):
            point[i] = point[i].strip('\n').strip(' ')

        # skip empty lines
        if (len(point) > 2):
            x_col.append(float(point[2]))
            y_col.append(float(point[3]))

    # calculating the angle
    ab = long1 - long0
    bc = lat1 - lat0
    a = math.atan2(bc,ab)

    c1 = lat2 - lat1
    b1 = c1 / math.cos(a)
    c2 = long1 - long0
    a1 = c2 / math.cos(a)
    # interpolation values
    slope_x = a1 / (new_x1 - new_x0)
    slope_y = b1 / (new_y1 - new_y0)

    # write header
    fout.write("QGC WPL 110\n")
    scaled = [] # list to hold converted coordinates

    # collect scaled coordinates
    for i in range(len(x_col)):
        converted = []
        converted.append(float(x_col[i]) * slope_x)
        converted.append(float(y_col[i]) * slope_y)
        scaled.append(converted)

    # check if rotation was made and write results to output file

    for i in range(len(scaled)):
        x_old = scaled[i][0]
        y_old = scaled[i][1]
        l = math.sqrt(x_old*x_old + y_old*y_old)
        gamma = math.atan2(y_old, x_old)
        x_new = l * math.cos(a + gamma)
        y_new = l * math.sin(a + gamma)

        # calc new coordinates

        x_new1 = x_new + long0
        y_new1 = y_new + lat0

        if i > 0:
            fout.write("{}\t0\t3\t16\t0\t5\t0\t0"
                       "\t{:.18f}\t{:.18f}\t20\t1\n"\
                       .format(i, y_new1, x_new1))
        else:
            fout.write("0\t1\t0\t16\t0\t5\t0\t0"
                       "\t{:.18f}\t{:.18f}\t0\t1\n"\
                       .format(y_new1, x_new1))

    fout.close()
## list for command line arguments casted to float
if len(sys.argv) < 12:
    print('Not enough arguments:')
    print('input_file output_file x0 y0 x1 y1 gps_long0 gps_lat0 gps_long1 gps_lat1 gps_long2 gps_lat2')
else:
    casted = []
    for i in range(3, len(sys.argv)):
        casted.append(float(sys.argv[i]))

    map(sys.argv[1], sys.argv[2], casted[0], casted[1], casted[2], casted[3], \
        casted[4], casted[5], casted[6], casted[7], casted[8], casted[9])
