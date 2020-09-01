import subprocess
import os
import shutil
from datetime import date, timedelta
from pathlib import Path
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from skills.BackUpAlice import BackupConstants


class BackUpAlice(AliceSkill):
	"""
	Author: LazzaAU
	Description: Makes a backup copy of the projectalice folder
	"""


	def __init__(self):

		self._backupCopy = Path
		self._monthAndDate = ""
		super().__init__()


	@IntentHandler('ForceBackup')
	def forceBackUpCreation(self,session: DialogSession):
		backUpPath = f'{self.homeDir()}/{BackupConstants.PARENT_DIRECTORY}'

		shutil.rmtree(backUpPath, ignore_errors=False, onerror=None)
		Path(self.homeDir(), f'{BackupConstants.PARENT_DIRECTORY}').mkdir()
		self.preChecks()

		self.endDialog(
			sessionId=session.sessionId,
			text=self.randomTalk(text='creatingBackup'),
			siteId=session.siteId
		)
		self.logInfo(f'I\'m updating your saved back up file')

		self.ThreadManager.doLater(
			interval=6,
			func=self.runCopyCommand
		)


	@IntentHandler('BackUpAlice')
	def backupProjectAlice(self, session: DialogSession = None):
		# main path to store backup folders in
		mainPath = Path(f'{self.homeDir()}/{BackupConstants.PARENT_DIRECTORY}')

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
			self.logInfo(f'Just created your first BackUp file of ProjectAlice')
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
		self._monthAndDate = today.strftime(BackupConstants.DATE_FORMAT)
		self._backupCopy = Path(f'{self.homeDir()}/{BackupConstants.BACKUP_DIR}{self._monthAndDate}')


	def backupChecks(self, session = None):
		backupDuration = self.getConfig('daysBetweenBackups')
		# determine the date N days ago
		dateNdaysAgo = date.today() - timedelta(days=backupDuration)
		#format the date into month and day
		previous = dateNdaysAgo.strftime(BackupConstants.DATE_FORMAT)

		# Does your previous back up match your backup duration ?
		expiredPreviousBackup = Path(f'{self.homeDir()}/{BackupConstants.BACKUP_DIR}{previous}')
		backUpPath = f'{self.homeDir()}/{BackupConstants.PARENT_DIRECTORY}'

		# if backup is out of date, delete the whole directory then remake the parent directory
		if expiredPreviousBackup.exists():
			shutil.rmtree(backUpPath, ignore_errors=False, onerror=None)
			Path(self.homeDir(), f'{BackupConstants.PARENT_DIRECTORY}').mkdir()
			self.preChecks()

			if session:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text='creatingBackup'),
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

	# copy ProjectAlice folder to the AliceBackUp folder
	def runCopyCommand(self):
		subprocess.run(['cp', '-R', self.rootDir(), self._backupCopy])

	# Check every hour is the backup is out of date
	def onFullHour(self):
		self.backupProjectAlice()


	@staticmethod
	def homeDir() -> str:
		return str(Path(__file__).resolve().parent.parent.parent.parent)


	@staticmethod
	def rootDir() -> str:
		return str(Path(__file__).resolve().parent.parent.parent)
