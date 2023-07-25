import sys

in_file = sys.argv[1]
out_file = sys.argv[2] if len(sys.argv) > 2 else 'out.musicxml'

with open(out_file, 'w') as output:
    with open(in_file, 'r') as input:
        # whether or not we are currently in a note object
        in_note = False
        
        # whether or not this note was a tuple
        is_tuple = False
        
        # whether we are currently inside a time modification tag
        time_modification = False
        
        for line in input:
            # open a note when we see a type tag
            if '<type>' in line:
                in_note = True
                is_tuple = False
            
            # close a note when we see a stem tag
            elif '<stem>' in line:
                # if this wasn't a tuple, we need to add the dot
                if not is_tuple:
                    output.write('<dot/>')
                in_note = False
                
            # if this next tag is a tuple tag
            elif '<tuple' in line:
                continue # don't print this line
            
            # if we are in a note, let's check some stuff
            elif in_note:
                
                # time-modification tag indicates a tuple
                if '<time-modification>' in line:
                    time_modification = True
                    is_tuple = True
                    continue # don't print this line
                    
                # if we are closing the time-modification
                elif '</time-modification>' in line:
                    time_modification = False
                    continue  # don't print this line
                
                # if we are inside a time modification, don't print it
                elif time_modification:
                    continue # don't print this line
            
            # change the time signature
            elif '<beats>' in line:
                output.write('<beats>12</beats>')
                continue
            elif '<beat-type>' in line:
                output.write('<beat-type>8</beat-type>')
                continue
                
            # change the divisions
            elif '<divisions>' in line:
                divs = int(int(''.join(filter(str.isdigit, line))) * 2 / 3)
                output.write('<divisions>{divs}</divisions>'.format(divs = divs))
                continue
                        
            output.write(line)
