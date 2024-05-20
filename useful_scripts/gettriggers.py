# Original code by AKK from https://genai.stackexchange.com/questions/346/how-to-obtain-trigger-words-from-a-lora-file
# Modified by hot_laugh617 of r/sultrysyn https://www.reddit.com/r/sultrysyn
# Look I wrote a python program. *nudge nudge*, *wink wink* Get it?

# Created on: May 18, 2024
# * Outputs straight JSON from the safetensor. Could be modified to print a nice table.
# * You could also set an output file argument, but you can just redirect the output to a file if you want to.

import argparse
import json
import struct

def main():
	print("\n")
	argparser = argparse.ArgumentParser(description='Extract keywords or other metadata from a .safetensor file.', prog="Get Triggers")
	argparser.add_argument("--input", "-i", action="store", type=str, help="File to get metadata from.")
	argparser.add_argument("--triggers", action="store_true")
	argparser.add_argument("--dump", "-d", action="store_true", help="Dump all metadata. [Default]")
	args = argparser.parse_args()

	# Set a flag in case there is a failure later.
	it_worked = True

	try:
		with open(args.input, "rb") as f:
			length_of_header = struct.unpack('<Q', f.read(8))[0]
			header_data = f.read(length_of_header)
			header = json.loads(header_data)
			
			# For those interested
			type = header['__metadata__']['modelspec.architecture']
			epochs = header['__metadata__']['ss_num_epochs']
			tags = header['__metadata__']['ss_tag_frequency']
	except:
		print(f"\n[!] There was a problem opening the file '{args.input}'. Are you sure it exists? \nMay sure you use the proper file extension.")
		print("\n[!] It seems to work for some LoRA and not others. I don't know why.\n")
		it_worked = False
		return -1

	if it_worked:
		if args.dump:
			# Header is all the metadata for the file.
			print(header)
		if args.triggers:
			print(tags)
		else:
			# Pointless but can be fixed later
			print(header)

if __name__ == "__main__":
    main()
