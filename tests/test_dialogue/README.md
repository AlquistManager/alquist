Alquist offline bot testing
===========================

To run offline bot testing with wit.ai, first you need to have wit installed

	pip install wit
After installing wit you can either build your own nlp base in their site, or you can use our demo.

In either case you will need to run ``run.py`` with the wit server token as a third argument and path to the folder containing your yaml files as fourth argument.

	py -3 run.py [] [] [wit-token] [yaml-path]
	
For running our demo app use 

	py -3 run.py '' '' NXOFXMBCIA6YAIXNNWYXJIJPC22AK35V [your path to alquist folder]\yaml\demo




