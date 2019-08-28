#GPL3
#Based on https://github.com/AkdM/ssncpy
#Single-file library version

import re

SERIALS ={
  "XAW1": {
    "1007900": "safe",
    "1008199": "warning",
    "1008200": "patched"
  },
  "XAW4": {
    "4001200": "safe",
    "4002999": "warning",
    "4003000": "patched"
  },
  "XAW7": {
    "7001790": "safe",
    "7002999": "warning",
    "7003000": "patched"
  },
  "XAJ1": {
    "1002100": "safe",
    "1002999": "warning",
    "1003000": "patched"
  },
  "XAJ4": {
    "4004700": "safe",
    "4005999": "warning",
    "4006000": "patched"
  },
  "XAJ7": {
    "7004100": "safe",
    "7004999": "warning",
    "7005000": "patched"
  },
  "XAW9": {
    "9999999": "warning"
  }
}

STATUSMAP = {
    "safe" : "Not patched :D",
    "warning" : "Possibly patched :|",
    "patched" : "Patched :(",
}

TESTSN = "XAW100790000" #Valid unpatched switch id for testing

def checkserial(serial_input):
    serial_input = serial_input.upper()
    digit_regex = r"\D"

    if serial_input == "": return ""
    status = "Too short" if len(serial_input) < 11 else ("Too long" if len(serial_input) > 14 else None)

    if not status:
      first_part = serial_input[0:4].upper()
      second_part = serial_input[3:10].upper()
      category_serials = SERIALS.get(first_part)

      if category_serials:
        second_part = re.sub(digit_regex, '0', second_part)
        serial_part = int(second_part)
        
        for serial in sorted(category_serials.keys()):
          if serial_part > int(serial):
              continue
          else:
              status = SERIALS.get(first_part, {}).get(serial, "Patched :(")
              break

        status = STATUSMAP.get(status, "Error :O")

      else:
          status = "incorrect"

    return status

#Call with serial number to check or leave blank for testsn
if __name__ == '__main__':
    import sys
    args = sys.argv
    
    sn = args[1] if len(args) > 1 else TESTSN

    print("{} - {}".format(sn, checkserial(sn)))