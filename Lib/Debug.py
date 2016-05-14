import sys, pdb, pprint

class Debug():
	def trace( self ):
		pdb.set_trace()

	def dump( self, var, abort=False ):
		pprint.pprint(var)
		sys.exit(0)

