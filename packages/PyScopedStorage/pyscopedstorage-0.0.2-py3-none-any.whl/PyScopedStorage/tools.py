from __future__ import annotations

from os import fdopen as os_fdopen
from typing import TYPE_CHECKING

from plyer.utils import platform

if platform == 'android':
	from .android_objects import ContentProvider, ContentResolver, DocumentsContract

from .io import async_open
from .utils import generate_file_uri_from_access_uri, get_fd_from_android_uri, scoped_file_exists

if TYPE_CHECKING:
	from io import BufferedReader, BufferedWriter, TextIOWrapper

	from aiofiles.threadpool.binary import AsyncBufferedIOBase, AsyncBufferedReader
	from aiofiles.threadpool.text import AsyncTextIOWrapper


def scoped_file_open(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> int:
	"""Make file using access (usually directory) android uri and return the file descriptor."""
	# TODO: Optionally return file uri
	file_uri: 'android.net.Uri' = generate_file_uri_from_access_uri(access_uri, name)
	if scoped_file_exists(file_uri):
		if mode == 'x':
			del file_uri
			raise FileExistsError

	elif mode in ('r', 'rb', 'r+', 'rb+'):
		raise FileNotFoundError

	else:
		del file_uri
		# "w/wb", "a/ab", "r+/rb+"
		# "a/ab" - because usually it's makes new file if not already exists to append
		file_uri = dc_make_doc(
			access_uri,
			name, mime,
		)


	ret = get_fd_from_android_uri(file_uri, mode)
	del file_uri

	return ret


def dc_make_doc(
	access_uri: 'android.net.Uri',
	name: str,
	mime: str = '*/*',
) -> 'android.net.Uri':
	"""Make file using access (usually directory) android uri and return the file uri."""
	# TODO: Optionally return file uri
	# TODO: Raise error if file exists..
	return DocumentsContract.createDocument(
		ContentResolver,
		access_uri,
		mime, name,
	)


def dc_open_doc(
	access_uri: 'android.net.Uri',
	name: str,
) -> 'android.net.Uri':
	"""Open file using access (usually directory) android uri and return the file uri."""
	# TODO: Optionally return file uri
	# FIXME: Raise error if file exists..
	return ContentProvider.createDocument(
		ContentResolver,
		access_uri,
		mime, name,
	)


def scoped_file_open_sync(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> TextIOWrapper | BufferedReader | BufferedWriter:
	return os_fdopen(scoped_file_open(access_uri, name, mode, mime), mode)


def scoped_file_open_async(
	access_uri: 'android.net.Uri',
	name: str,
	mode: str = 'w',
	mime: str = '*/*',
) -> AsyncTextIOWrapper | AsyncBufferedReader | AsyncBufferedIOBase:
	return async_open(scoped_file_open(access_uri, name, mode, mime), mode)


sfopen_sync = scoped_file_open_sync
sfopen_async = scoped_file_open_async
