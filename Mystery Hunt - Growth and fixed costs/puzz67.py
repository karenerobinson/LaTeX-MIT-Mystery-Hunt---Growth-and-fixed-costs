#!/usr/bin/env python

import locale
locale.setlocale(locale.LC_ALL, 'en_US')

# format CSV into LaTeX
# this example makes a table


# reads from example.csv and writes to stuff.tex
infile = open("gafc-5.csv")

def kprint(grid,row,col,outfile):
    value = float(grid[row][col*2])
    if (value != 0): outfile.write(" & ")
    if (abs(value) == 614050): outfile.write("\\textsf{")
    if (value < 0): 
        outfile.write("(" + locale.format("%d", abs(value),grouping=True)+")")
    elif value > 0: 
        outfile.write(locale.format("%d", abs(value),grouping=True))
    if (abs(value) == 614050): outfile.write("}")
    outfile.write("\iftoggle{solution}{& \\textcolor{soln-lightblue}{" + grid[row][2*col+1] + "}}{}")


def generate(infile):
    lines = filter(lambda x: len(x) > 0, infile.read().split('\n'))
    grid = map(lambda x: x.split(','), lines)    


    rows=105

    for col in range(1, 21): # each column is a company
        filename='statement-'+str(col)+'.tex'
#        print(filename)
        # open an "outfile"; get ready to print to it
        outfile = open(filename, 'w')        
        outfile.write('\\begin{tabular}{l . l}')
        for row in range(0,rows):
            # first check the format, to see if this is a mandatory row.
 #           print str(row) + ": " + grid[row][0]
            format = grid[row][1]
            if (len(format)>1):
 #               print "len: " + format
                if (format[1]=="m"):
                    outfile.write("\\\\ \\large{\\textbf{\\textsf{%s}}} \\\\\n" % grid[row][0])

                elif (format[1]=="u"):
                    indent = float(format[0])*0.25
                    if indent > 0: outfile.write("\\hspace{%f in}" % indent)
                    outfile.write("\\underline{\\textbf{" + grid[row][0] + "}}")
                    if(len(grid[row][2*col])> 0):
                        if(float(grid[row][2*col])) > 0:
                               #outfile.write("& ")
                               kprint(grid,row,col,outfile)
                    outfile.write("\\\\\n")
                # else, if it's a heading, check to see if there's data in the upcoming sum row.
                elif (format[1]=="h"):
                    printrowq = 0
                    #print "heading: %s..." % grid[row][0]
                    if len(grid[row][2*col]) > 0:
                        if float(grid[row][2*col]) != 0:
                            printrowq = 1
                            if len(grid[row+1][2*col]) > 0:
                                if float(grid[row+1][2*col]) !=0:
                                    printrowq=2 # special printrowq, for printing only the row label
                    else:
                        for j in range (0,min(20,100-row)):
                            if(len(grid[row+j][1])>1):
                                i = j
                                printrowq=0
                                if(grid[row+i][1][1]=='s'):
                                    j = 21
                                    if (len(grid[row+i][2*col]) > 0):
                                        if float(grid[row+i][2*col]) > 0:
                                            printrowq = 1
                                    break
                                else: 
                                    if(j>1):
                                        if(grid[row+j][1][1]=='h'): 
                                            printrowq=1
                                            j = 21
                                            break
                    # end finding next s and checking for a value
                    if(printrowq >= 1):
                        # if so, print this row with appropriate indentation.
                        indent = float(format[0])*0.25
                        if indent > 0: 
                            outfile.write("\\hspace{%f in}" % indent)
                            outfile.write(grid[row][0])
                        elif indent == 0: outfile.write("\\textbf{%s} " % grid[row][0]) # bold if no indentation
                        if(len(grid[row][2*col])> 0 and printrowq==1):
                            kprint(grid,row,col,outfile)
                        outfile.write("\\\\\n")
                elif (format[1]=="s"):
                    # hline if sum
                    if(len(grid[row][2*col])> 0): 
                        if abs(float(grid[row][2*col])) > 0:
#                            outfile.write("\\rule{4in}{0.5pt}\\\\\n")
                            outfile.write("\\hline\n")
                            indent = float(format[0])*0.25
                            if indent > 0: outfile.write("\\hspace{%f in}" % indent)
                            value=int(round(float(grid[row][2*col])))
                            outfile.write("{%s} " % grid[row][0])
                            kprint(grid,row,col,outfile)
                            outfile.write("\\\\\n")
            elif(len(format)>0):
                # otherwise, check to see if there is data in this row.
                if(len(grid[row][2*col])> 0): 
#                    print "row: " + str(row) + "; company: " + str(col)
                    if abs(float(grid[row][2*col])) > 0:
                        # if so, indent appropriately and print.
                        indent = float(format[0])*0.25
                        if indent > 0: outfile.write("\\hspace{%f in}" % indent)
                        outfile.write("{%s} " % grid[row][0])
                        kprint(grid,row,col,outfile)
                        outfile.write("\\\\\n")

        outfile.write("\\vspace{0.05in}\\\\\n")
        for i in range(0,8):
            row=rows+i
#            print grid[row][0]
            if len(grid[row][0]) > 0:
                if(str(grid[row][0])!="0" and float(grid[row][2*col]) != 0):
                # make value readable .. a % or a number of days.
                    value = grid[row][col*2]
                    if len(value)>3:
                        value = str(value[0]) + value[1] + value[2] + value[3]
                    outfile.write("\\iftoggle{solution}{")
                    outfile.write("\\textcolor{soln-lightblue}{" + grid[row][0] + "}")
                    outfile.write(" & \\textcolor{soln-lightblue}{\\textsf{" + str(value) + "}}")
                    outfile.write(" & \\textcolor{soln-lightblue}{" + grid[row][1] + "}}{} \\\\\n")
        outfile.write('\\end{tabular}\n')



generate(infile)

# close the file.. maybe close a "tabular".


