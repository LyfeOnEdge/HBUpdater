import modules.serial_checker as sc
import modules.actionpage as actionpage

TITLE = "Serial Checker"

class serialPage(actionpage.actionPage):
	def __init__(self, parent, controller,page_name,back_command,):
		actionpage.actionPage.__init__(self, parent, controller, page_name, back_command, action = checkserial, entry_text = "Enter Switch Serial Number", on_key_do = True, title = TITLE)

def checkserial(serial):
	status = sc.checkserial(serial)
	print(status)
	return status