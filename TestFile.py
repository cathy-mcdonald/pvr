import sys

# Return True if file is in use
def file_in_use(path):
  try:
    test_file = open(path, "a")
    test_file.close()
    return False
  except IOError:
    return True
	    

if __name__ == "__main__":
  if file_in_use(sys.argv[1]):
    print "File is in use"
  else:
    print "File is not in use"