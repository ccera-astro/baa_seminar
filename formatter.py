"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time
import ra_funcs


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """A slow data textual formatter
          inputs are expected to be science-data
             Parameters:
                formatter - pointer to a custom formatter function
                filepat - pattern used for formatting filename must provide converters for YYYY MM DD
                extension - filename extension
                logtime - how often to log, in seconds
                fmtstr - formatter for data values -- most provide converters for both values
                nchan - number of interleaved channels on input"""
                
                

    def __init__(self, formatter=None, filepat="foonly-%d%d%d", extension=".csv", 
        logtime=10,fmtstr="%11.9f",nchan=1,localtime=False,longitude=-76.03, legend=None):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='BAA:Data Logger',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        
        #
        # Formatter is a function pointer--very often 'None'
        #
        self.formatter = formatter
        
        #
        # Controls the template for filename generation
        #
        self.filepat= filepat
        
        #
        # The filename extension
        #
        self.extension=extension
        
        #
        # The logging interval
        #
        self.logtime=logtime
        
        
        #
        # The data-item formatting string
        #      
        self.fmtstr = fmtstr
        
        #
        # How many (interleaved) channels
        self.nchan = nchan
        
        #
        # Use local time, rather than UTC/GMT?
        #
        self.localtime = localtime
        
        #
        # The averaing cells
        #
        self.avg = [0.0]*nchan
        self.acnt = [0]*nchan

        
        #
        # Keep track of the next channel's averaging cell we
        #  need to update
        #
        self.cndx = 0
        
        
        #
        # This isn't strictly required, since the work function code
        #  will take care of whatever items it gets presented with.
        #
        self.set_output_multiple(nchan)
        
        self.now = time.time()
        
        self.longitude = longitude
        
        self.legend = legend
        
        self.legcount = 0
        self.fn = ""
        self.curlegend = legend

    def work(self, input_items, output_items):
        
        if (self.localtime == False):
            ltp = time.gmtime()
        else:
            ltp = time.localtime()
        
        #
        # Distribute the input items over the averaging buffer as appropriate
        #  We assume that the input is interleaved by 'nchan'
        #  We use 'self.cndx' to keep track of which channel's averaging
        #  cell we need to put the next value in.
        #
        # Because GR's scheduler has no idea what our internal "shape"
        #  is, it can hand us many, or a few, items, every time we're
        #  called.
        #
        for x in range(len(input_items[0])):
            self.avg[self.cndx % self.nchan] += input_items[0][x]
            self.acnt[self.cndx % self.nchan] += 1
            
            #
            # Increment and modularly reduce cndx
            #
            self.cndx += 1
            self.cndx %= self.nchan
            

        if ((time.time() - self.now) > self.logtime):
            self.now = time.time()
            if (self.formatter == None):
                fn = self.filepat % (ltp.tm_year, ltp.tm_mon, ltp.tm_mday) + self.extension
                fp = open(fn, "a")
                #
                # Filename has changed (new date) or
                #  legend has changed (new DEC/FREQ/BW) or
                #  legcount >= 30
                #
                wrlegend = False
                if (self.fn != fn):
                    self.fn = fn
                    wrlegend = True
                elif (self.curlegend != self.legend):
                    self.curlegend = self.legend
                    wrlegend = True
                elif (self.legcount >= 30):
                    wrlegend = True
                    self.legcount = 0
                if (wrlegend == True and self.legend != None):
                    self.legcount = 0
                    fp.write("INFO:%s\n" % self.legend)
                    
                fp.write("%02d,%02d,%02d," % (ltp.tm_hour, ltp.tm_min, ltp.tm_sec))
                fp.write("%s," % ra_funcs.cur_sidereal(self.longitude))
                for x in range(self.nchan):
                    self.avg[x] /= self.acnt[x]
                    self.acnt[x] = 1
                    fp.write (self.fmtstr  % (self.avg[x]))
                    if (x < self.nchan-1):
                        fp.write(",")
                fp.write("\n")
                self.legcount += 1
                
                    
                fp.close()
  
            else:
                self.formatter(self.filepat,self.extension,self.avg[0],self.avg[1])
            
        return len(input_items[0])
