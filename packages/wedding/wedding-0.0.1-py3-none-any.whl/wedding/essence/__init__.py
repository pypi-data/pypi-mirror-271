

from .seek import seek_essence
from .scan import scan_essence

def build_essence ():
	essence_path = seek_essence ()
	external_essence = scan_essence (essence_path)
	

	return;


def retrieve_essence ():
	return;