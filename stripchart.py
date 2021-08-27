"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import time


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """A strip chart takes in a stream of floats and produces a 1 hour long
       strip-chart as output
       
       Params:
          decim - how much to decimate input to produce 1 SPS
          seconds - how many seconds long is the stripchart vector
    """

    def __init__(self, decim=100,seconds=3600):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='BAA:Strip Chart',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[(np.float32,seconds)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        
        #
        # How much do we need to average the input to produce a 1SPS
        #  output?
        #
        self.decim = decim
        
        #
        # The stripchart vector itself--must be persistent in the
        #  object instance
        #
        self.strip = [0.0]*seconds
        
        #
        # keeps track of decimation
        #
        self.counter = 0
        
        #
        # We continuously average the input and store it here
        #
        self.avg = 0.0

    def general_work(self, input_items, output_items):
        """take an input item(s), place appropriately in stripchart output"""
 
        #
        # Our averager hasn't been initialized with a
        #  "prime the pump" value?
        # Do it now.
        #
        if (self.avg == 0.0):
            self.avg = input_items[0][0]
            self.counter = 0
            #
            # Also init the strip-chart to this level
            #
            self.strip = [self.avg]*len(self.strip)
        #
        # For each of the input items
        #
        for x in range(len(input_items[0])):
            #
            # Effectively we get a N-point moving average
            # WHere "N" is "decim"
            #
            self.avg += input_items[0][x]
            self.counter += 1
            
            #
            # Time to output an item into the stripchart
            #
            if (self.counter >= self.decim):
                
                #
                # Reduce by decim
                #
                self.avg /= self.counter
                
                #
                # Use python array notation to effect a quick
                #  shift of items in the stripchart array
                #
                self.strip = [self.avg] + self.strip[:-1]
                self.counter = 0
                self.avg = 1.0e-15
        #
        # Stuff output items with the contents of the 
        #  possibly-updated stripchart
        #
        for y in range(len(output_items[0])):
            output_items[0][y] = self.strip
        
        #
        # Tell scheduler we consumed items
        #
        self.consume(0, len(input_items[0]))
        return len(output_items[0])
