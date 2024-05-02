from dataclasses import dataclass as dataclass_x_dataclass
from json import load as json_x_load, dump as json_x_dump, loads as json_x_loads, dumps as json_x_dumps
from datetime import date as datetime_x_date
from time import sleep as time_x_sleep
from typing import Callable, overload
from setuptools import setup
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

========================
THANK YOU AND TAKE CARE!
========================

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
	def __inner_reload_cached_data(cls):

		try:
			with open(CACHE_FILE_PATH, "r") as f:
				json_data = json_x_load(f)
		except FileNotFoundError:
			if cls._json_data and len(cls._json_data.keys()) == 0:
				if cls._is_using_pip:
					return
				with open(CACHE_FILE_PATH, "w") as f:
					json_x_dump({}, f)
				with open(CACHE_FILE_PATH, "r") as f:
					json_data = json_x_load(f)
			else:
				return

		cls._json_data = json_data

		return None

		f"[ END ] {_Setup_Helper.__reload_cached_data}"


	
	@classmethod
	def __reload_cached_data(cls):
		cls._load_from_hardcoded()
		return None
		f"[ END ] {_Setup_Helper.__reload_cached_data}"



	@classmethod
	def __load_date(cls, override=False):

		if cls._date_of_last_modified:
			cls.__reload_cached_data()

		if not override and cls._json_data is not None:
			assert cls._json_data
			if "date" in cls._json_data:
				cls._date_of_last_modified = datetime_x_date.fromisoformat(cls._json_data["date"])
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
	def __inner_load_date(cls) -> "str":
		do_want_to_use_current_date = _Setup_Helper.__get_y_n("Would you like to use the current date?")
		new = None
		if do_want_to_use_current_date:

			cls._date_of_last_modified = datetime_x_date.today()
			if cls._json_data:
				cls._json_data["date"] = cls._date_of_last_modified.isoformat()
			new = cls._date_of_last_modified.isoformat()

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
				assert cls._json_data
				cls._json_data["date"] = cls._date_of_last_modified.isoformat()
				new = cls._date_of_last_modified.isoformat()

			except ValueError:
				print("] Error: Invalid date. Please try again.")
		
		if cls._json_data is not None:
			with open(CACHE_FILE_PATH, "w") as f:
				json_x_dump(cls._json_data, f)
		assert isinstance(new, str)
		return new
		f"[ END ] {_Setup_Helper.__inner_load_date}"



	@classmethod
	def __load_version_number(cls, override=False):

		if cls._version_number:
			cls.__reload_cached_data()

		if not override:
			assert cls._json_data
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
	def __inner_load_version_number(cls) -> "str":
		
		cls._version_number = _Setup_Helper.__get_answer(
			"What is the version number? ",
			_Version.validate_version_number
		)

		if cls._json_data:
			cls._json_data["version_number"] = cls._version_number

		if cls._json_data is not None:
			with open(CACHE_FILE_PATH, "w") as f:
				json_x_dump(cls._json_data, f)

		return cls._version_number

		f"[ END ] {_Setup_Helper.__inner_load_version_number}"



	@classmethod
	def __load_notes(cls, override=False):


		if cls._notes:
			cls.__reload_cached_data()

		if not override:
			assert cls._json_data
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
	def __inner_load_notes(cls) -> "str":
		
		cls._notes = _Setup_Helper.__get_answer(
			"Enter the release notes: ",
			lambda x: (len(x) > 0, "Notes cannot be empty.")
		)

		if cls._json_data:
			cls._json_data["notes"] = cls._notes

		if cls._json_data is not None:
			with open(CACHE_FILE_PATH, "w") as f:
				json_x_dump(cls._json_data, f)

		return cls._notes

		f"[ END ] {_Setup_Helper.__inner_load_notes}"



	@classmethod
	def __load_readme_file_path(cls, override=False):
		
		if cls._readme_file_path:
			cls.__reload_cached_data()

		if not override:
			assert cls._json_data
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
	def __inner_load_readme_file_path(cls) -> "str":

		cls._readme_file_path = _Setup_Helper.__get_answer(
			"Enter the path to the README file: ",
			lambda x: (os.path.exists(x), "File does not exist.")
		)

		if cls._json_data:
			cls._json_data["readme_file_path"] = cls._readme_file_path

		if cls._json_data is not None:
			with open(CACHE_FILE_PATH, "w") as f:
				json_x_dump(cls._json_data, f)

		return cls._readme_file_path

		f"[ END ] {_Setup_Helper.__inner_load_readme_file_path}"



	@classmethod
	def __load_parameters(cls, force=False):
		if not force:
			cls.__inner_reload_cached_data()
			if cls._is_using_pip:
				json_data = cls._json_data_when_using_pip
				assert json_data is not None
				cls._date_of_last_modified = datetime_x_date.fromisoformat(json_data["date"])
				cls._version_number = json_data["version_number"]
				cls._notes = json_data["notes"]
				cls._readme_file_path = json_data["readme_file_path"]
				return
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
				continue

			if force:
				json_data = {}
				json_data["date"] = cls._date_of_last_modified.isoformat()
				json_data["version_number"] = cls._version_number
				json_data["notes"] = cls._notes
				json_data["readme_file_path"] = cls._readme_file_path
				with open(CACHE_FILE_PATH, "w") as f:
					json_x_dump(json_data, f)
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
					time_x_sleep(0.8)
					cls.__clear_screen()

		return None
	
		f"[ END ] {_Setup_Helper.__load_parameters}"



	@staticmethod
	def __clear_screen():
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
		CACHE_FILE_PATH = cache_file_path_

		cls._date_of_last_modified = None
		cls._version_number = None
		cls._notes = None
		cls._readme_file_path = None

		try:
			__ = cls.__activated_already
		except AttributeError:
			cls.__activated_already = None
		if cls.__activated_already:
			raise Exception("This class is a singleton and can only be activated once.")
		cls.__activated_already = True

		cls._load_from_hardcoded()

		return None
	
		f"[ END ] {_Setup_Helper.init}"



	@classmethod
	def _load_from_hardcoded(cls):

		cls._is_using_pip = False
		if "PIP_BUILD_TRACKER" in os.environ.keys():
			cls._is_using_pip = True

		try:
			__ = cls._json_data
		except AttributeError:
			cls._json_data = None
		cls.__inner_reload_cached_data()
		json_data = {} if not cls._json_data else cls._json_data
		needs_update = False

		# Before uploading to PyPi, we need to hardcode the values in a source file.
		try:
			from . import _hardcoded #type:ignore
		except ImportError:
			if not json_data:
				cls.__load_parameters(force=True)
			base_dir = os.path.dirname(__file__)
			base_dir = os.path.abspath(base_dir)
			with open(os.path.join(base_dir, "_hardcoded.py"), "w") as f:
				f.write(f"\"\"\"\n{json_x_dumps(json_data)}\n\"\"\"\n")
			from . import _hardcoded
		with open(_hardcoded.__file__, "r") as f:
			contents = f.read()
			splitted = contents.split("\n")[1:-2]
			json_str = "\n".join(splitted)
			j_data = json_x_loads(json_str)
			if j_data != json_data:
				needs_update = True
		if needs_update and len(json_data.keys()) == 4:
			with open(_hardcoded.__file__, "w") as f:
				json_str = json_x_dumps(json_data, indent=4)
				f.write(f"\"\"\"\n{json_str}\n\"\"\"\n")
		with open(_hardcoded.__file__, "r") as f:
			contents = f.read()
			splitted = contents.split("\n")[1:-2]
			json_str = "\n".join(splitted)
			print(json_str)
			json_data = json_x_loads(json_str)

		assert json_data is not None
		cls._json_data = json_data

		if cls._is_using_pip:
			cls._json_data_when_using_pip = json_data
			return None

		cls._date_of_last_modified = datetime_x_date.fromisoformat(j_data.get("date", None))
		cls._version_number = j_data.get("version_number", None)
		cls._notes = j_data.get("notes", None)
		cls._readme_file_path = j_data.get("readme_file_path", None)

		return None
	
		f"[ END ] {_Setup_Helper._load_from_hardcoded}"



	@classmethod
	def setup(cls, name:"str", author:"str", description:"str", **kwargs_for_setup_tools) -> "None":
		
		_Setup_Helper.__clear_screen()

		if not cls.__activated_already:
			raise Exception("You must call `init` before calling `setup`.")

		if not cls._is_using_pip:
			for c in LEGAL_NOTICE:
				print(c, end="", flush=True)
				time_x_sleep(0.00075)
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
	def _finish_setup(cls, kwargs_for_setup_tools:"dict"):

		assert isinstance(cls._date_of_last_modified, datetime_x_date)
		assert isinstance(cls._version_number, str)
		assert isinstance(cls._notes, str)
		assert isinstance(cls._readme_file_path, str)

		long_description = _Setup_Helper.__init_description(cls._readme_file_path)
		long_description += f"\n## V{cls._version.version_number} released on {cls._version.repr_date()}\n"
		long_description += cls._notes

		if not cls._is_using_pip:
			_Setup_Helper.__clear_screen()
			print(f"Current Directory: [{os.path.abspath(os.getcwd())}].\n\n")
			is_root_of_project = _Setup_Helper.__get_y_n("Is this the root of the project?")
			_Setup_Helper.__clear_screen()
		else:
			if not os.path.exists("setup.py"):
				raise FileNotFoundError("The `setup.py` file does not exist. Please run this script from the root of the project directory.")
			if not os.path.exists("templated_setup/_hardcoded.py"):
				raise FileNotFoundError("The `_hardcoded.py` file does not exist. Please run this script from the root of the project directory.")
			is_root_of_project = True

		if not is_root_of_project:
			raise Exception("This script must be run from the root of the project directory.")
		
		separator = "\\" if os.name == "nt" else "/"

		dirs_to_remove = [
			"dist",
			"build",
			f"{cls._name}.egg-info"
		]

		if not cls._is_using_pip:
			try:
				for d in dirs_to_remove:
					if os.path.exists(d):
						print(f"\n] WARNING: ABOUT TO REMOVE THE `{os.getcwd()}{separator}{d}` DIRECTORY!!")
						print("] YOU HAVE 3 SECONDS TO CANCEL...")
						time_x_sleep(3)
						shutil.rmtree(d, ignore_errors=True)
			except KeyboardInterrupt:
				print("] Cancelled.")
				exit(0)
			_Setup_Helper.__clear_screen()

		if not cls._is_using_pip:
			cls._old_sys_argv = sys.argv
			sys.argv = [sys.argv[0], "sdist"]
			do_proceed = _Setup_Helper.__get_y_n("Would you like to proceed with the build?")
			if not do_proceed:
				exit(0)
			_Setup_Helper.__clear_screen()

		setup(
			name=cls._name,
			version=cls._version.version_number,
			author=cls._author,
			description=cls._description,
			long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
			long_description=long_description,
			**kwargs_for_setup_tools,
		)

		if not cls._is_using_pip:
			print("\n] Setup complete.\n\n")
		else:
			return

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

		# It would be very bad if we shipped the cache file with this package.
		base_dir = os.path.dirname(__file__)
		base_dir = os.path.abspath(base_dir)
		with open(os.path.join(base_dir, "_hardcoded.py"), "w") as f:
			f.write("\"\"\"\n{}\n\"\"\"\n")

		os.system(f"{sys.executable} -m twine upload --verbose --repository pypi dist/*")

		sys.argv = cls._old_sys_argv

		return None
	
		f"[ END ] {_Setup_Helper._finish_setup}"



	f"[ END ]"





class templated_setup:
	Normal_People_Date=_Normal_People_Date
	Version=_Version
	Setup_Helper=_Setup_Helper
