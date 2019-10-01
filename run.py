import sys
import logging


ascii = """
#"""""""'M           dP                   oo                   
##  mmmm. `M          88                                        
#'        .M .d8888b. 88 .d8888b. 88d888b. dP .d8888b. 88d888b. 
M#  MMMb.'YM 88'  `88 88 88ooood8 88'  `88 88 88'  `88 88'  `88 
M#  MMMM'  M 88.  .88 88 88.  ... 88       88 88.  .88 88    88 
M#       .;M `88888P8 dP `88888P' dP       dP `88888P' dP    dP 
M#########M                                                    
oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"""

#  Setup initial loggers
log = logging.getLogger('Balerion')
log.setLevel(logging.DEBUG)

sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(logging.Formatter(
    fmt="[%(asctime)s] - %(levelname)s: %(message)s"
))

sh.setLevel(logging.INFO)
log.addHandler(sh)


def bye_bye(msg="Press enter to continue . . .", code=1):
    input(msg)
    sys.exit(code)


def run():
    try:
        from Balerion.balerion_main import Balerion
        b = Balerion()
        print(ascii)
        print("Connecting...\n")
        b.run()
    except Exception as e:
        log.warning(f"Closing bot : {e}")
        bye_bye()


if __name__ == "__main__":
    run()
