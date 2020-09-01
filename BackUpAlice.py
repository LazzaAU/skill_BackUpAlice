import subprocess
import os
import shutil
from datetime import date, timedelta
from pathlib import Path
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class BackUpAlice(AliceSkill):
	"""
	Author: LazzaAU
	Description: Makes a backup copy of the projectalice folder
	"""


	def __init__(self):
		self._dateFormat = "%b-%d"
		self._backupCopy = Path
		self._monthAndDate = ""
		super().__init__()


	@IntentHandler('BackUpAlice')
	def backupProjectAlice(self, session: DialogSession = None):

		mainPath = Path(f'{self.homeDir()}/AliceBackUp')

		# if ere's no AliceBackUp directory then make one
		if not mainPath.exists():
			mainPath.mkdir()

		backupDirectory = os.listdir(mainPath)

		# Checking if the AliceBackUp directory is empty or not
		if len(backupDirectory) == 0:
			self.preChecks()
			if session:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text='firstInstall'),
					siteId=session.siteId
				)

			self.ThreadManager.doLater(
				interval=6,
				func=self.runCopyCommand
			)
		else:
			if session:
				self.backupChecks(session)
			else:
				self.backupChecks()


	def preChecks(self):
		today = date.today()
		self._monthAndDate = today.strftime(self._dateFormat)
		self._backupCopy = Path(f'{self.homeDir()}/AliceBackUp/ProjectAlice-{self._monthAndDate}')


	def backupChecks(self, session = None):
		backupDuration = self.getConfig('DaysBetweenBackups')
		# determine the date N days ago
		dateNdaysAgo = date.today() - timedelta(days=backupDuration)

		previous = dateNdaysAgo.strftime(self._dateFormat)

		# Does our previous back up match our backup duration ?
		expiredPreviousBackup = Path(f'{self.homeDir()}/AliceBackUp/ProjectAlice-{previous}')
		backUpPath = f'{self.homeDir()}/AliceBackUp'

		if expiredPreviousBackup.exists():
			shutil.rmtree(backUpPath, ignore_errors=False, onerror=None)
			Path(self.homeDir(), 'AliceBackUp').mkdir()
			self.preChecks()

			if session:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text='creatingBacku'),
					siteId=session.siteId
				)
			self.logInfo(f'I\'m updating your saved back up file')
			self.ThreadManager.doLater(
				interval=6,
				func=self.runCopyCommand
			)
		else:
			if session:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text='uptoDate'),
					siteId=session.siteId
				)
			self.logInfo(f'Current backups are up to date, no further action taken')


	def runCopyCommand(self):
		subprocess.run(['cp', '-R', self.rootDir(), self._backupCopy])


	def onFullHour(self):
		self.backupProjectAlice()


	@staticmethod
	def homeDir() -> str:
		return str(Path(__file__).resolve().parent.parent.parent.parent)


	@staticmethod
	def rootDir() -> str:
		return str(Path(__file__).resolve().parent.parent.parent)
