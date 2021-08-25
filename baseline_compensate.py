"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Baseline compensator block
         Takes in an integrated FFT vector and either outputs that vector, or
         outputs a baseline-subtracted version of that vector
         
         fftsize - size of input vector
         collect - operate in "collect" rather than compensate mode
    """

    def __init__(self, fftsize=2048,collect=True):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='BAA:Baseline Compensator',   # will show up in GRC
            in_sig=[(np.float32,fftsize)],
            out_sig=[(np.float32,fftsize)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.collect = collect
        self.fftbuf = np.zeros(fftsize,dtype=np.float32)

    def work(self, input_items, output_items):
        """Accumulate baseline data, apply corrections when asked"""
        if (self.collect == True):
            #
            # Collect samples, and compute a moving average on them
            # They're already fairly-well smoothed, so we don't
            # need to go overboard
            #
            for x in range(len(input_items[0])):
                self.fftbuf = np.add(self.fftbuf, input_items[0][x])
                self.fftbuf = np.divide(self.fftbuf, [2.0]*len(self.fftbuf))
            self.avg = sum(self.fftbuf)/len(self.fftbuf)
            self.avg *= 1.5
            
            for x in range(len(output_items[0])):
                output_items[0][x] = input_items[0][x]
        else:
            for x in range(len(output_items[0])):
                output_items[0][x] = np.subtract(input_items[0][x], self.fftbuf)
                output_items[0][x] = np.add(output_items[0][x], self.avg)
        
        return len(output_items[0])
