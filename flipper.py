"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Flipper -- simply reverse the order of a vector
               fftsize - size of the (probably FFT) vector
               enabled - whether to flip or not
    """

    def __init__(self, fftsize=2048,enabled=True):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='BAA:Flipper',   # will show up in GRC
            in_sig=[(np.float32,fftsize)],
            out_sig=[(np.float32,fftsize)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.enabled = enabled

    def work(self, input_items, output_items):
        """Flip order"""
        
        #
        # For each output item
        #
        # Either stuff it with flipped input, or non-flipped input
        #
        for x in range(len(output_items[0])):
            if (self.enabled == True):
                output_items[0][x] = input_items[0][x][::-1]
            else:
                output_items[0][x] = input_items[0][x]
        return len(output_items[0])
