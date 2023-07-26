import sys

in_file = sys.argv[1]
out_file = sys.argv[2] if len(sys.argv) > 2 else 'out.musicxml'

with open(out_file, 'w') as output:
    with open(in_file, 'r') as input:
        # whether or not we are currently in a note object
        in_note = False
        
        # whether we are currently inside a time modification tag
        time_modification = False
        
        # the pre-existing dot or accidental info. because xml is annoying.
        note_info = ''
        
        for line in input:
            # change the time signature
            if '<beats>' in line:
                output.write('<beats>12</beats>\n')
            elif '<beat-type>' in line:
                output.write('<beat-type>8</beat-type>\n')
                
            # change the divisions
            elif '<divisions>' in line:
                divs = int(int(''.join(filter(str.isdigit, line))) * 2 / 3)
                output.write('<divisions>{divs}</divisions>\n'.format(divs = divs))
            
            # change the tempo indicator to dotted quarter notes
            elif '<beat-unit>' in line:
                output.write(line)
                output.write('<beat-unit-dot/>\n')
                
            # adjust the tempo
            elif '<sound tempo' in line:
                # pls don't give a decimal tempo originally or else it will break
                tempo = int(''.join(filter(str.isdigit, line))) * 3 / 2
                output.write('<sound tempo="{tempo}"/>\n'.format(tempo = tempo))
            
            # open a note when we see a type tag
            elif '<type>' in line:
                in_note = True
                output.write(line)
                continue
            
            # if the last tag we saw was the type tag
            elif in_note:
                # there is already a dot on the note
                if '<dot/>' in line:
                    # should probably do smth special w this case but i'm lazy
                    note_info += line
                
                # if there is an accidental on the note
                elif '<accidental>' in line:
                    note_info += line
            
                # time-modification tag indicates a tuple
                elif '<time-modification>' in line:
                    time_modification = True
                
                # if we are closing the time-modification
                elif '</time-modification>' in line:
                    time_modification = False
                    output.write(note_info)
                    note_info = ''
                    in_note = False
                
                # don't print anything inside a time modification
                elif time_modification:
                    pass
                
                # we never saw a time modification so it wasn't a tuplet
                # let's add the dot and missing content
                else:
                    output.write('<dot/>\n')
                    output.write(note_info)
                    note_info = ''
                    in_note = False
                    output.write(line)
            
            # if this next tag is a tuple tag
            elif '<tuple' in line:
                pass

            # if it didn't match a case above, print the line
            else:          
                output.write(line)
