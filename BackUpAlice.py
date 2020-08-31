from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class BackUpAlice(AliceSkill):
	"""
	Author: LazzaAU
	Description: Makes a backup copy of the projectalice folder
	"""

	@IntentHandler('MyIntentName')
	def dummyIntent(self, session: DialogSession, **_kwargs):
		pass
