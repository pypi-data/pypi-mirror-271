from dataclasses import dataclass as dataclass_x_dataclass
from json import load as json_x_load, dump as json_x_dump, loads as json_x_loads, dumps as json_x_dumps
from datetime import date as datetime_x_date
from time import sleep as time_x_sleep
from typing import Callable, overload
from setuptools import setup
from pickle import dumps as pickle_x_dumps, loads as pickle_x_loads
from base64 import b64decode as base64_x_b64decode
from base64 import b64encode as base64_x_b64encode
import shutil
import sys
import os







CACHE_FILE_PATH = ""
LEGAL_NOTICE = """
==================================
Legal Notice for `templated_setup`
==================================

By using this software, you, the user, acknowledge and agree that you are solely responsible for the content that is published using this tool.
The software is provided "as is", and the developers make no representations or warranties of any kind regarding its use.

You assume all responsibility and risk for the use of this software and the materials you create or publish with it.

The developers shall not be liable for any claims, damages, or other liabilities arising from the use of the software or content published therein.

===================
END OF LEGAL NOTICE
===================

NOTE: If you would like to remove this legal notice in future, simply set "_TEMPLATED_SETUP_PLEASE="STFU" as an environment variable.

-- THANK YOU AND TAKE CARE! --
"""







class _Normal_People_Date:



	def __new__(cls, day_:"int", month_:"int", year_:"int") -> "datetime_x_date":
	
		return datetime_x_date(year_, month_, day_)
	
		f"[ END ] {_Normal_People_Date.__new__}"



	f"[ END ]"







@dataclass_x_dataclass
class _Version:



	date: 			"datetime_x_date"
	version_number: 	"str"
	notes: 			"str|None"



	def validate(self):

		is_valid, err_msg = _Version.validate_version_number(self.version_number)

		if not is_valid:
			raise Exception(err_msg)

		f"[ END ] {_Version.validate}"



	def repr_date(self) -> str:

		day_suffix = self.date.day

		if day_suffix == 1:
			day_suffix = "st"
		elif day_suffix == 2:
			day_suffix = "nd"
		elif day_suffix == 3:
			day_suffix = "rd"
		else:
			day_suffix = "th"

		return f"{self.date.day}{day_suffix}/{self.date.month}/{self.date.year}"
	
		f"[ END ] {_Version.repr_date}"



	@staticmethod
	def validate_version_number(version_number_:"str") -> "tuple[bool,str]":
		
		s = version_number_.split(".")

		if not len(s) == 2:
			return False, "Version number must have exactly 2 parts (separated by a `.`)!"

		for i in s:
			if not i.isdigit():
				return False, "Version number must be numeric."
		
		return True, ""
	
		f"[ END ] {_Version.validate_version_number}"



	f"[ END ]"







class _Setup_Helper:



	###########
	# HELPERS #
	###########



	@staticmethod
	def __parse_notes(notes_:"str") -> "str":

		return "\n     |".join(notes_.split("\n"))
	
		f"[ END ] {_Setup_Helper.__parse_notes}"
	


	@staticmethod
	def __init_description(readme_file_path_) -> "str":

		description = None

		if not os.path.exists(readme_file_path_):
			raise FileNotFoundError(f"No such file or directory: [{readme_file_path_}].")
		
		if not os.path.isabs(readme_file_path_):
			readme_file_path_ = os.path.abspath(readme_file_path_)

		if not os.path.isfile(readme_file_path_):
			raise FileNotFoundError(f"Expected [{readme_file_path_}] to be a file. Found a directory instead.")

		with open(readme_file_path_, "r") as f:
			description = f.read()

		if description is None:
			raise Exception(f"File [{readme_file_path_}] is empty.")

		return description
	
		f"[ END ] {_Setup_Helper.__init_description}"



	@staticmethod
	def __get_answer(question:"str", satisfy_func:"Callable[[str],tuple[bool,str]]") -> "str":
		ans = ""
		while True:

			ans = input(f"> {question}")
			is_valid, err_msg = satisfy_func(ans)

			if is_valid:
				break

			print(f"] Error [{err_msg}]")
		
		return ans
		f"[ END ] {_Setup_Helper.__get_answer}"



	@staticmethod
	def __get_y_n(question:str) -> bool:
		question = question + " (y/n) "
		while True:

			answer = input(f"> {question}")

			if answer.lower() == "y":
				return True

			elif answer.lower() == "n":
				return False

			else:
				print("] Please enter 'y' or 'n'.")

		return None
		f"[ END ] {_Setup_Helper.__get_y_n}"



	@classmethod
	def __load_cached_data(cls):

		try:
			with open(CACHE_FILE_PATH, "r") as f:
				json_data = json_x_load(f)
		except FileNotFoundError:
			if cls._json_data and len(cls._json_data.keys()) > 0:
				with open(CACHE_FILE_PATH, "w") as f:
					json_x_dump(cls._json_data, f)
			else:
				with open(CACHE_FILE_PATH, "w") as f:
					json_x_dump({}, f)
				with open(CACHE_FILE_PATH, "r") as f:
					json_data = json_x_load(f)

		cls._json_data = json_data

		return None

		f"[ END ] {_Setup_Helper.__reload_cached_data}"



	@classmethod
	def __load_date(cls, override=False) -> "None":
		
		assert cls._json_data is not None
		assert not cls._is_using_pip

		if not override:
			if "date" in cls._json_data:
				cls._date_of_last_modified = cls._json_data["date"]
			else:
				while True:
					new = cls.__inner_load_date()
					confirmed = _Setup_Helper.__get_y_n(f"Is [{new}] Correct?")
					if confirmed:
						break

		else:
			cls.__inner_load_date()

		return None

		f"[ END ] {_Setup_Helper.__load_date}"



	@classmethod
	def __inner_load_date(cls) -> "None":
		assert cls._json_data is not None
		assert not cls._is_using_pip
		do_want_to_use_current_date = _Setup_Helper.__get_y_n("Would you like to use the current date?")
		new = None
		if do_want_to_use_current_date:

			cls._date_of_last_modified = datetime_x_date.today().isoformat()
			cls._json_data["date"] = cls._date_of_last_modified
			new = cls._date_of_last_modified

		else:

			day = int(_Setup_Helper.__get_answer(
				"What day was it last modified? ",
				lambda x: (x.isdigit(), "Please enter a number."))
			)

			month = int(_Setup_Helper.__get_answer(
				"What month was it last modified? ",
				lambda x: (x.isdigit(), "Please enter a number."))
			)

			year = int(_Setup_Helper.__get_answer(
				"What year was it last modified? ",
				lambda x: (x.isdigit(), "Please enter a number."))
			)

			try:
				cls._date_of_last_modified = datetime_x_date(year, month, day)
				assert cls._json_data is not None
				cls._json_data["date"] = cls._date_of_last_modified.isoformat()
				new = cls._date_of_last_modified.isoformat()
			except ValueError:
				print("] Error: Invalid date. Please try again.")
		
		assert isinstance(cls._date_of_last_modified, str)
		cls._date_of_last_modified = new
		return None
		f"[ END ] {_Setup_Helper.__inner_load_date}"



	@classmethod
	def __load_version_number(cls, override=False) -> "None":

		assert cls._json_data is not None
		assert not cls._is_using_pip

		if not override:
			if "version_number" in cls._json_data:
				cls._version_number = cls._json_data["version_number"]
			else:
				while True:
					new = cls.__inner_load_version_number()
					confirmed = _Setup_Helper.__get_y_n(f"Is [{new}] Correct?")
					if confirmed:
						break
		else:
			cls.__inner_load_version_number()

		return None
	
		f"[ END ] {_Setup_Helper.__load_version_number}"



	@classmethod
	def __inner_load_version_number(cls) -> "None":

		assert cls._json_data is not None
		assert not cls._is_using_pip

		cls._version_number = _Setup_Helper.__get_answer(
			"What is the version number? ",
			_Version.validate_version_number
		)

		cls._json_data["version_number"] = cls._version_number

		return None

		f"[ END ] {_Setup_Helper.__inner_load_version_number}"



	@classmethod
	def __load_notes(cls, override=False) -> "None":

		assert cls._json_data is not None
		assert not cls._is_using_pip

		if not override:
			if "notes" in cls._json_data:
				cls._notes = cls._json_data["notes"]
			else:
				while True:
					new = cls.__inner_load_notes()
					confirmed = _Setup_Helper.__get_y_n(f"Is [{new}] Correct?")
					if confirmed:
						break
		else:
			cls.__inner_load_notes()

		return None

		f"[ END ] {_Setup_Helper.__load_notes}"



	@classmethod
	def __inner_load_notes(cls) -> "None":
		
		assert cls._json_data is not None
		assert not cls._is_using_pip

		cls._notes = _Setup_Helper.__get_answer(
			"Enter the release notes: ",
			lambda x: (len(x) > 0, "Notes cannot be empty.")
		)

		cls._json_data["notes"] = cls._notes

		return None

		f"[ END ] {_Setup_Helper.__inner_load_notes}"



	@classmethod
	def __load_readme_file_path(cls, override=False) -> "None":
		
		assert cls._json_data is not None
		assert not cls._is_using_pip

		if not override:
			if "readme_file_path" in cls._json_data:
				cls._readme_file_path = cls._json_data["readme_file_path"]
			else:
				while True:
					new = cls.__inner_load_readme_file_path()
					confirmed = _Setup_Helper.__get_y_n(f"Is [{new}] Correct?")
					if confirmed:
						break
		else:
			cls.__inner_load_readme_file_path()

		return None

		f"[ END ] {_Setup_Helper.__load_readme_file_path}"



	@classmethod
	def __inner_load_readme_file_path(cls) -> "None":

		assert cls._json_data is not None
		assert not cls._is_using_pip

		cls._readme_file_path = _Setup_Helper.__get_answer(
			"Enter the path to the README file: ",
			lambda x: (os.path.exists(x), "File does not exist.")
		)

		cls._json_data["readme_file_path"] = cls._readme_file_path

		return None

		f"[ END ] {_Setup_Helper.__inner_load_readme_file_path}"



	@classmethod
	def __load_parameters(cls, force=False):
		if not force and not cls._json_data:
			try:
				with open(CACHE_FILE_PATH, "r") as f:
					cls._json_data = json_x_load(f)
			except FileNotFoundError:
				force = True
			if not cls._json_data:
				cls._json_data = {}
				force = True
		if not force and cls._json_data:
			cls.__load_cached_data()
			cls.__load_date()
			cls.__load_version_number()
			cls.__load_notes()
			cls.__load_readme_file_path()
		user_wants_to_change_params = False
		if force:
			user_wants_to_change_params = True
		while True:

			cls.__clear_screen()
			print(f"\n\n] Current Infos:")
			print(f"]] Date:              [{cls._date_of_last_modified}]")
			print(f"]] Version Number:    [{cls._version_number}]")
			print(f"]] Notes:             [{cls._notes}]")
			print(f"]] Readme File Path:  [{cls._readme_file_path}]")
			print(f"\n")

			if user_wants_to_change_params == True:
				options = [
					["Last Modified Date", 		lambda: cls.__load_date(override=True)],
					["Current Version Number", 	lambda: cls.__load_version_number(override=True)],
					["Current Release Notes", 	lambda: cls.__load_notes(override=True)],
					["README File Path", 		lambda: cls.__load_readme_file_path(override=True)]
				]
				print("] What would you like to change?")
				for i, [opt, __] in enumerate(options):
					print(f"]] - [{i+1}] Change {opt},")
				fifth_choice = "Go Back." if not force else "Save Changes."
				print(f"]] - [{len(options)+1}] {fifth_choice}.")
				choice = int(_Setup_Helper.__get_answer(
					"Enter the number of your choice: ",
					lambda x: (
						x.isdigit() and 0 < int(x) <= len(options)+1,
						"Invalid choice. Please try again."
					)
				))
				if choice == len(options)+1:
					user_wants_to_change_params = False
					continue
				callback = options[choice-1][1]
				callback()
				with open(CACHE_FILE_PATH, "w") as f:
					json_x_dump(cls._json_data, f)
				cls.__load_cached_data()
				continue

			if force:
				assert cls._date_of_last_modified
				assert cls._version_number
				assert cls._notes
				assert cls._readme_file_path
				json_data = {}
				json_data["date"] = cls._date_of_last_modified
				json_data["version_number"] = cls._version_number
				json_data["notes"] = cls._notes
				json_data["readme_file_path"] = cls._readme_file_path
				with open(CACHE_FILE_PATH, "w") as f:
					json_x_dump(json_data, f)
				cls._json_data = json_data
				cls.__clear_screen()
				break
			else:
				cls.__load_date()
				cls.__load_version_number()
				cls.__load_notes()
				cls.__load_readme_file_path()

				confirmed = _Setup_Helper.__get_y_n("Is this information correct?")
				if confirmed:
					break
				else:
					user_wants_to_change_params = True
					print("] Error: Please enter the information again.")
					cls.__clear_screen()

		return None
	
		f"[ END ] {_Setup_Helper.__load_parameters}"



	@staticmethod
	def __clear_screen():
		time_x_sleep(1)
		if os.name == "nt":

			os.system("cls")

		else:

			os.system("clear")

		return None
		f"[ END ] {_Setup_Helper.__clear_screen}"



	#################
	# INSTANTIATION #
	#################
	


	@classmethod
	def init(cls, cache_file_path_:"str") -> "None":

		global CACHE_FILE_PATH
		CACHE_FILE_PATH = os.path.abspath(cache_file_path_)

		cls._base_dir = os.path.dirname(__file__)
		cls._base_dir = os.path.abspath(cls._base_dir)

		cls._date_of_last_modified = None
		cls._version_number = None
		cls._notes = None
		cls._readme_file_path = None

		cls._json_data = None

		cls._is_using_pip = False
		try:
			print("] Press ENTER to continue...")
			input()
		except EOFError:
			cls._is_using_pip = True
		if "PIP_BUILD_TRACKER" in os.environ:
			cls._is_using_pip = True

		try:
			__ = cls.__activated_already
		except AttributeError:
			cls.__activated_already = None
		if cls.__activated_already:
			raise Exception("This class is a singleton and can only be activated once.")
		cls.__activated_already = True

		return None
	
		f"[ END ] {_Setup_Helper.init}"



	@classmethod
	def setup(cls, name:"str", author:"str", description:"str", **kwargs_for_setup_tools) -> "None":
		
		if cls._is_using_pip:
			cls._handle_installation_via_pip(name)
			return

		_Setup_Helper.__clear_screen()

		if not cls.__activated_already:
			raise Exception("You must call `init` before calling `setup`.")

		starting_i = 3
		i = starting_i
		do_print_legal_notice = True
		if "_TEMPLATED_SETUP_PLEASE" in os.environ:
			if os.environ["_TEMPLATED_SETUP_PLEASE"] == "STFU":
				do_print_legal_notice = False
		if do_print_legal_notice:
			for c in LEGAL_NOTICE:
				i -= 1
				if i == 0:
					i = starting_i
					time_x_sleep(0.01)
					print(c, end="", flush=True)
				else:
					print(c, end="")
			print("\n")
			time_x_sleep(0.5)
			print(".", end="", flush=True)
			time_x_sleep(0.5)
			print(".", end="", flush=True)
			time_x_sleep(0.5)
			print(".", end="", flush=True)
			time_x_sleep(0.8)

		cls._name = name
		cls._author = author
		cls._description = description

		_Setup_Helper.__load_parameters()

		assert isinstance(cls._date_of_last_modified, str)
		cls._date_of_last_modified = datetime_x_date.fromisoformat(cls._date_of_last_modified)

		assert isinstance(cls._date_of_last_modified, datetime_x_date)
		assert isinstance(cls._version_number, str)
		assert isinstance(cls._notes, str)
		assert isinstance(cls._readme_file_path, str)

		cls._version = _Version(
			date=cls._date_of_last_modified,
			version_number=cls._version_number,
			notes=_Setup_Helper.__parse_notes(cls._notes)
		)
		cls._version.validate()

		cls._finish_setup(kwargs_for_setup_tools)

		return None

		f"[ END ] {_Setup_Helper.setup}"



	#################
	# JUICY METHODS #
	#################



	@classmethod
	def _handle_installation_via_pip(cls, name):

		# NOTE: If we do not hardcode the version, then pip will throw a fit when trying to install the 
		# NOTE:   `templated-setup` package.
		from . import _hardcoded #type:ignore
		kwargs_for_setup_tools = base64_x_b64decode(_hardcoded.__kwargs_for_setup_tools__.encode("utf-8")) #type:ignore
		kwargs_for_setup_tools = pickle_x_loads(kwargs_for_setup_tools)
		long_description = base64_x_b64decode(_hardcoded.__long_description__.encode("utf-8")) #type:ignore
		long_description = pickle_x_loads(long_description)
		setup(
			name=name,
			version=_hardcoded.__version__, #type:ignore
			author=_hardcoded.__author__, #type:ignore
			description=_hardcoded.__description__, #type:ignore
			long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
			long_description=long_description, #type:ignore
			**kwargs_for_setup_tools
		)

		return None
	
		f"[ END ] {_Setup_Helper._handle_installation_via_pip}"



	@classmethod
	def _finish_setup(cls, kwargs_for_setup_tools:"dict"):

		assert isinstance(cls._date_of_last_modified, datetime_x_date)
		assert isinstance(cls._version_number, str)
		assert isinstance(cls._notes, str)
		assert isinstance(cls._readme_file_path, str)

		long_description = _Setup_Helper.__init_description(cls._readme_file_path)
		long_description += f"\n## V{cls._version.version_number} released on {cls._version.repr_date()}\n"
		long_description += cls._notes

		_Setup_Helper.__clear_screen()
		print(f"Current Directory: [{os.path.abspath(os.getcwd())}].\n\n")
		is_root_of_project = _Setup_Helper.__get_y_n("Is this the root of the project?")
		_Setup_Helper.__clear_screen()

		if not is_root_of_project:
			raise Exception("This script must be run from the root of the project directory.")
		
		egg_infos = []
		for p, dirs, __ in os.walk(os.getcwd()):
			for d in dirs:
				if d.endswith(".egg-info"):
					egg_infos.append(os.path.join(p, d))

		dirs_to_remove = [
			"dist",
			"build",
			*egg_infos
		]

		if not cls._is_using_pip:
			try:
				for d in dirs_to_remove:
					if os.path.exists(d):
						print(f"\n] WARNING: ABOUT TO REMOVE THE `{os.path.join(os.getcwd(),d)}` DIRECTORY!!")
						print("] YOU HAVE 3 SECONDS TO CANCEL...")
						time_x_sleep(3)
						shutil.rmtree(d, ignore_errors=True)
			except KeyboardInterrupt:
				print("] Cancelled.")
				exit(0)
			_Setup_Helper.__clear_screen()

		cls._old_sys_argv = sys.argv
		sys.argv = [sys.argv[0], "sdist"]
		do_proceed = _Setup_Helper.__get_y_n("Would you like to proceed with the build?")
		if not do_proceed:
			exit(0)
		_Setup_Helper.__clear_screen()

		from . import _hardcoded # No `type:ignore` here since this file should exists.
		s_long_description = pickle_x_dumps(long_description)
		s_long_description = base64_x_b64encode(s_long_description).decode("utf-8")
		s_kwargs_for_setup_tools = pickle_x_dumps(kwargs_for_setup_tools)
		s_kwargs_for_setup_tools = base64_x_b64encode(s_kwargs_for_setup_tools).decode("utf-8")
		with open(_hardcoded.__file__, "w") as f:
			f.write(f"__version__ = \"{cls._version.version_number}\"\n")
			f.write(f"__author__ = \"{cls._author}\"\n")
			f.write(f"__description__ = \"{cls._description}\"\n")
			f.write(f"__long_description__ = \"\"\"{s_long_description}\"\"\"\n")
			f.write(f"__kwargs_for_setup_tools__ = \"\"\"{s_kwargs_for_setup_tools}\"\"\"\n")

		setup(
			name=cls._name,
			version=cls._version.version_number,
			author=cls._author,
			description=cls._description,
			long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
			long_description=long_description,
			**kwargs_for_setup_tools,
		)

		print("\n] Setup complete.\n\n")

		do_publish = _Setup_Helper.__get_y_n("Would you like to publish to PyPi?")
		if not do_publish:
			exit(0)

		_Setup_Helper.__clear_screen()

		print(f"] Description is readable below...\n{long_description}")
		print()

		do_proceed = _Setup_Helper.__get_y_n("Would you like to proceed?")
		if not do_proceed:
			exit(0)

		_Setup_Helper.__clear_screen()

		os.system(f"{sys.executable} -m twine upload --verbose --repository pypi dist/*")

		sys.argv = cls._old_sys_argv

		return None
	
		f"[ END ] {_Setup_Helper._finish_setup}"



	f"[ END ]"





class templated_setup:
	Normal_People_Date=_Normal_People_Date
	Version=_Version
	Setup_Helper=_Setup_Helper
