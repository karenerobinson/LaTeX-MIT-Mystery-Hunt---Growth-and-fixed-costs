#!/usr/bin/env python

# format CSV into LaTeX
# this example makes a table


# reads from example.csv and writes to stuff.tex
infile = open('example.csv')
outfile = open('stuff.tex', 'w')

def generate(infile, outfile):
    lines = filter(lambda x: len(x) > 0, infile.read().split('\n'))
    grid = map(lambda x: x.split(','), lines)

    print "sanitycheck?"
    
    # table formatting
    outfile.write('\\begin{tabular}{|%s|}\n' % ('|'.join(['c']*len(grid[0]))))
    outfile.write('\\hline\n')

#    for row in grid:
    for i in range(0, len(grid)):
        outfile.write('%s \\\\\n' % grid[i][1])
#        outfile.write(row)
        outfile.write('\\hline\n')
    
    outfile.write('\\end{tabular}\n')


generate(infile, outfile)
