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
    """Logging of vectors (like FFT outputs)
          fftsize - size of fft vector to log
          formetter - formatter function pointer
          filepat - pattern for beginning of filenaem
          extension - file extension
          logtime - how often to log (seconds)
          fmtstr - format string for data values
          localtime - whether to use local or UTC time
          fftshift - whether to shift FFT vector before logging
          longitude  - local longitude in decimal form
    """

    def __init__(self, fftsize=2048, formatter=None, filepat="foonly-%04d%02d%02d", extension=".csv",
        logtime=10, fmtstr="%11.9f", localtime=False, fftshift=False,longitude=-76.03):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='BAA:Vector Logger',   # will show up in GRC
            in_sig=[(np.float32,fftsize)],
            out_sig=None
        )
        
        self.formatter = formatter
        self.filepat = filepat
        self.extension = extension
        self.logtime = logtime
        self.fmtstr = fmtstr
        self.localtime = localtime
        self.vecavg = np.zeros(fftsize)
        self.now = time.time()
        self.fftshift = fftshift
        self.longitude = longitude

        

    def work(self, input_items, output_items):
        """Log a vector into a file"""
        for x in range(len(input_items[0])):
            self.vecavg = np.add(self.vecavg, input_items[0][x])
            self.vecavg = np.divide(self.vecavg, [2.0]*len(self.vecavg))
        
        #
        # If time to log
        #
        if (time.time() - self.now >= self.logtime):
            self.now = time.time()
            #
            # Decide on localtime or gmtime
            #
            if (self.localtime == True):
                ltp = time.localtime()
            else:
                ltp = time.gmtime()
            
            #
            # If they specified a formatter function call it instead
            #
            if (self.formatter != None):
                self.formatter(self.vecavg,self.filepat,self.extension)
            
            #
            # Otherwise, do it here
            #
            else:
                #
                # Open the output file, with a name according to the filepat
                #  specified
                #
                fp = open(self.filepat % (ltp.tm_year, ltp.tm_mon, ltp.tm_mday) + self.extension, "a")
                
                #
                # Write record header
                #
                fp.write ("%02d,%02d,%02d," % (ltp.tm_hour, ltp.tm_min, ltp.tm_sec))
                fp.write ("%s," % ra_funcs.cur_sidereal(self.longitude))
                
                #
                # Write each of the data items in the input vector
                #
                
                #
                # Check if they want us to  do an FFTSHIFT operation
                #  (to  normalize the ordering of FFTW3 outputs)
                #
                if (self.fftshift == True):
                    l = len(self.vecavg)
                    l1 = list(self.vecavg[int(l/2):])
                    l2 = list(self.vecavg[0:int(l/2)])
                    lout = l1 + l2
                    lout = np.array(lout)
                else:
                    lout = self.vecavg
                for x in range(len(self.vecavg)):
                    fp.write(self.fmtstr % lout[x])
                    if (x < len(self.vecavg)-1):
                        fp.write(",")
                fp.write("\n")
                fp.close()
            
            
        return len(input_items[0])
