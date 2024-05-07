from __future__ import annotations

from typing import TYPE_CHECKING

from plyer.utils import platform

if platform == 'android':
	from jnius.jnius import JavaException

	from .android_objects import ContentResolver, DocumentsContract, Uri

PYSLET_AVAILABLE: bool = True

try:
	from pyslet.rfc2396 import URI
except ImportError:
	PYSLET_AVAILABLE = False

if TYPE_CHECKING:
	from typing import Dict, Final  # noqa: UP035

	from pyslet.rfc2396 import URI


def scoped_file_exists(file_uri: 'android.net.Uri') -> bool:
	try:
		ins = ContentResolver.openInputStream(file_uri)
	except JavaException as e:
		if 'java.io.FileNotFoundException' in e.innermessage:
			del e
			return False

		raise e

	# All's fine
	ins.close()
	del ins

	return True


# TODO: Use enums..
# NOTE: java "w" -> "wt", "rw" -> "rwt" because: https://issuetracker.google.com/issues/180526528
py_open2java_openfd: 'Final[Dict[str, str]]' = {  # noqa: UP006,UP037
	'r': 'r',
	'rb': 'r',

	# TODO: Optionally skip truncate..
	# java "w" -> "wt"
	'w': 'wt',
	'wb': 'wt',

	'x': 'wt',  # existent check is inside sfopen_{sync/async}

	'a': 'wa',
	'ab': 'wa',

	# no truncate, because
	# usually in stdlib `io.open` if file will just read, it's doesn't be overwritten
	'r+': 'rw',
	'rb+': 'rw',
}


def get_fd_from_android_uri(
	content_uri: 'android.net.Uri',
	mode: str = 'r',
) -> int:
	"""Open and detach android java file descriptor for	directly access in python.

	Note for open modes:
	https://developer.android.com/reference/android/content/ContentResolver#openFileDescriptor(android.net.Uri,%20java.lang.String,%20android.os.CancellationSignal)
	"""
	# TODO: CancellationSignal..

	# Stuff around modes to correctly use in the java descriptor
	# TODO: Raise another error..
	jp_mode = py_open2java_openfd[mode]

	fd_obj: 'android.os.ParcelFileDescriptor' = ContentResolver.openFileDescriptor(
		content_uri,
		jp_mode,
	)
	fd: int = fd_obj.detachFd()

	return fd


def get_fd_from_uri(
	uri: URI,
	mode: str = 'r',
) -> int:
	android_uri: 'android.net.Uri' = Uri.parse(str(uri))
	return get_fd_from_android_uri(android_uri, mode)


def get_fd_from_struri(
	struri: str,
	mode: str = 'r',
) -> int:
	android_uri: 'android.net.Uri' = Uri.parse(struri)
	return get_fd_from_android_uri(android_uri, mode)


# TODO: Speed check..
# Weak.. Do we really need pyslet's rfc2396?
# def _pyslet_generate_file_uri_from_access_uri(access_uri: 'android.net.Uri', name: str) -> 'android.net.Uri':
# 	py_uri: URI = URI(access_uri.toString())
# 	doc_file: str = f'{py_uri.get_file_name()}/{name}'

# 	# FIXME: Find better ways to natively use rfc2396 Uri..
# 	# py_file_uri: str = str(py_uri.resolve(doc_file))##
# 	# ret = Uri.parse(py_file_uri)

# 	ret = DocumentsContract.buildDocumentUriUsingTree(access_uri, doc_file)

# 	del py_uri, doc_file

# 	return ret


def generate_file_uri_from_access_uri(access_uri: 'android.net.Uri', name: str) -> 'android.net.Uri':
	dir_name: str = DocumentsContract.getTreeDocumentId(access_uri)
	doc_file: str = f'{dir_name}/{name}'
	del dir_name

	ret = DocumentsContract.buildDocumentUriUsingTree(access_uri, doc_file)

	del doc_file

	return ret


# TODO: Optionally allow force use java api more..
# TODO: More use `from functools import singledispatch`
# generate_file_uri_from_access_uri = _java_generate_file_uri_from_access_uri

# if PYSLET_AVAILABLE:
# 	generate_file_uri_from_access_uri = _pyslet_generate_file_uri_from_access_uri
