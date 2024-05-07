import os
import json


class StockTransactionAnalyzer:
    def __init__(self, transaction_file):
        self.transaction_file = transaction_file
        self.scenarios = None
        self.transactions = None
        self.metadata = None
        self.input_file = os.path.join( os.getcwd(), 'input.json' )  # Standard location for input file

    def load_input(self):
        with open( self.input_file ) as f:
            input_data = json.load( f )
            self.scenarios = input_data[ 'scenarios' ]
            self.metadata = input_data[ 'metadata' ]
