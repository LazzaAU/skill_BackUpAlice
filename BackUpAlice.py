import subprocess
import os
import shutil
from datetime import date, timedelta, datetime
from pathlib import Path
from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from skills.BackUpAlice import BackupConstants


class BackUpAlice(AliceSkill):
	"""
	Author: Lazza
	Description: Makes a backup copy of the projectalice folder
	"""


	def __init__(self):

		self._backupCopy = Path
		self._monthAndDate = ""
		super().__init__()


	@IntentHandler('ForceBackup')
	def forceBackUpCreation(self,session: DialogSession):
		backUpPath = f'{str(Path.home())}/{BackupConstants.PARENT_DIRECTORY}'

		shutil.rmtree(backUpPath, ignore_errors=False, onerror=None)
		Path(str(Path.home()), f'{BackupConstants.PARENT_DIRECTORY}').mkdir()
		self.preChecks()

		self.endDialog(
			sessionId=session.sessionId,
			text=self.randomTalk(text='creatingBackup'),
			siteId=session.siteId
		)
		self.logInfo(msg=f'I\'m updating your saved back up file')

		self.ThreadManager.doLater(
			interval=6,
			func=self.runCopyCommand
		)


	@staticmethod
	def mainDirChecks():
		# main path to store backup folders in
		mainPath = Path(f'{str(Path.home())}/{BackupConstants.PARENT_DIRECTORY}')

		# if there's no AliceBackUp directory then make one
		if not mainPath.exists():
			mainPath.mkdir()

		backupDirectory = os.listdir(mainPath)

		return backupDirectory


	@IntentHandler('BackUpAlice')
	def backupProjectAlice(self, session: DialogSession = None):
		backupDirectory = self.mainDirChecks()

		# Checking if the AliceBackUp directory is empty or not
		if len(backupDirectory) == 0:
			self.preChecks()
			if session:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text='firstInstall'),
					siteId=session.siteId
				)
			self.logInfo(msg=f'Just created your first BackUp file of ProjectAlice')
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
		self._backupCopy = Path(f'{str(Path.home())}/{BackupConstants.BACKUP_DIR}{self._monthAndDate}')


	def backupChecks(self, session=None):
		expiredBackup = self.datechecker()

		backUpPath = f'{str(Path.home())}/{BackupConstants.PARENT_DIRECTORY}'

		# if backup is out of date, delete the whole directory then remake the parent directory
		if expiredBackup:
			shutil.rmtree(backUpPath, ignore_errors=True, onerror=None)
			self.mainDirChecks()
			self.preChecks()

			if session:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text='creatingBackup'),
					siteId=session.siteId
				)
			self.logInfo(msg=f'I\'m updating your saved back up file')

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
			self.logInfo(msg='Current backups are up to date, no further action taken')


	# copy ProjectAlice folder to the AliceBackUp folder
	def runCopyCommand(self):
		subprocess.run(['cp', '-R', self.Commons.rootDir(), self._backupCopy])


	# Check every hour is the backup is out of date
	def onFullHour(self):
		self.backupProjectAlice()


	def datechecker(self) -> bool:
		# Get todays date and time now
		today = datetime.now()
		# Format todays date
		monthAndDate = today.strftime(BackupConstants.DATE_FORMAT)
		# Reconvert todays date to a datetime object
		now = datetime.strptime(monthAndDate, BackupConstants.DATE_FORMAT)

		# get the current file name of the backup
		fileName = os.listdir(f'{str(Path.home())}/{BackupConstants.PARENT_DIRECTORY}')
		# strip out the filename to leave just the date
		filename2 = fileName[0].strip('ProjectAlice-')

		# convert the string into a datetime object
		backupFileDate = datetime.strptime(str(filename2), BackupConstants.DATE_FORMAT)
		backupFileDate.strftime(BackupConstants.DATE_FORMAT)

		# set the date to compare against based on user setting
		comparableDate = backupFileDate + timedelta(days=self.getConfig('daysBetweenBackups'))
		# self.logWarning(f'backupFiledate is {backupFileDate} comparable date is {comparableDate}')
		# Compare two datetime objects
		if now >= comparableDate:
			return True
		else:
			return False
