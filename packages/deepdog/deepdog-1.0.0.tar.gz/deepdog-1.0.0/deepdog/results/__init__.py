import dataclasses
import re
import typing
import logging
import deepdog.indexify
import pathlib
import csv

_logger = logging.getLogger(__name__)

FILENAME_REGEX = r"(?P<timestamp>\d{8}-\d{6})-(?P<filename_slug>.*)\.realdata\.fast_filter\.bayesrun\.csv"

MODEL_REGEXES = [
	r"geom_(?P<xmin>-?\d+)_(?P<xmax>-?\d+)_(?P<ymin>-?\d+)_(?P<ymax>-?\d+)_(?P<zmin>-?\d+)_(?P<zmax>-?\d+)-orientation_(?P<orientation>free|fixedxy|fixedz)-dipole_count_(?P<avg_filled>\d+)_(?P<field_name>\w*)"
]

FILE_SLUG_REGEXES = [
	r"mock_tarucha-(?P<job_index>\d+)",
	r"(?:(?P<mock>mock)_)?tarucha(?:_(?P<tarucha_run_id>\d+))?-(?P<job_index>\d+)",
]


@dataclasses.dataclass
class BayesrunOutputFilename:
	timestamp: str
	filename_slug: str
	path: pathlib.Path


@dataclasses.dataclass
class BayesrunColumnParsed:
	"""
	class for parsing a bayesrun while pulling certain special fields out
	"""

	def __init__(self, groupdict: typing.Dict[str, str]):
		self.column_field = groupdict["field_name"]
		self.model_field_dict = {
			k: v for k, v in groupdict.items() if k != "field_name"
		}

	def __str__(self):
		return f"BayesrunColumnParsed[{self.column_field}: {self.model_field_dict}]"


@dataclasses.dataclass
class BayesrunModelResult:
	parsed_model_keys: typing.Dict[str, str]
	success: int
	count: int


@dataclasses.dataclass
class BayesrunOutput:
	filename: BayesrunOutputFilename
	data: typing.Dict["str", typing.Any]
	results: typing.Sequence[BayesrunModelResult]


def _batch_iterable_into_chunks(iterable, n=1):
	"""
	utility for batching bayesrun files where columns appear in threes
	"""
	for ndx in range(0, len(iterable), n):
		yield iterable[ndx : min(ndx + n, len(iterable))]


def _parse_bayesrun_column(
	column: str,
) -> typing.Optional[BayesrunColumnParsed]:
	"""
	Tries one by one all of a predefined list of regexes that I might have used in the past.
	Returns the groupdict for the first match, or None if no match found.
	"""
	for pattern in MODEL_REGEXES:
		match = re.match(pattern, column)
		if match:
			return BayesrunColumnParsed(match.groupdict())
	else:
		return None


def _parse_bayesrun_row(
	row: typing.Dict[str, str],
) -> typing.Sequence[BayesrunModelResult]:

	results = []
	batched_keys = _batch_iterable_into_chunks(list(row.keys()), 3)
	for model_keys in batched_keys:
		parsed = [_parse_bayesrun_column(column) for column in model_keys]
		values = [row[column] for column in model_keys]
		if parsed[0] is None:
			raise ValueError(f"no viable success row found for keys {model_keys}")
		if parsed[1] is None:
			raise ValueError(f"no viable count row found for keys {model_keys}")
		if parsed[0].column_field != "success":
			raise ValueError(f"The column {model_keys[0]} is not a success field")
		if parsed[1].column_field != "count":
			raise ValueError(f"The column {model_keys[1]} is not a count field")
		parsed_keys = parsed[0].model_field_dict
		success = int(values[0])
		count = int(values[1])
		results.append(
			BayesrunModelResult(
				parsed_model_keys=parsed_keys,
				success=success,
				count=count,
			)
		)
	return results


def _parse_output_filename(file: pathlib.Path) -> BayesrunOutputFilename:
	filename = file.name
	match = re.match(FILENAME_REGEX, filename)
	if not match:
		raise ValueError(f"{filename} was not a valid bayesrun output")
	groups = match.groupdict()
	return BayesrunOutputFilename(
		timestamp=groups["timestamp"], filename_slug=groups["filename_slug"], path=file
	)


def _parse_file_slug(slug: str) -> typing.Optional[typing.Dict[str, str]]:
	for pattern in FILE_SLUG_REGEXES:
		match = re.match(pattern, slug)
		if match:
			return match.groupdict()
	else:
		return None


def read_output_file(
	file: pathlib.Path, indexifier: typing.Optional[deepdog.indexify.Indexifier]
) -> BayesrunOutput:

	parsed_filename = tag = _parse_output_filename(file)
	out = BayesrunOutput(filename=parsed_filename, data={}, results=[])

	out.data.update(dataclasses.asdict(tag))
	parsed_tag = _parse_file_slug(parsed_filename.filename_slug)
	if parsed_tag is None:
		_logger.warning(
			f"Could not parse {tag} against any matching regexes. Going to skip tag parsing"
		)
	else:
		out.data.update(parsed_tag)
		if indexifier is not None:
			try:
				job_index = parsed_tag["job_index"]
				indexified = indexifier.indexify(int(job_index))
				out.data.update(indexified)
			except KeyError:
				# This isn't really that important of an error, apart from the warning
				_logger.warning(
					f"Parsed tag to {parsed_tag}, and attempted to indexify but no job_index key was found. skipping and moving on"
				)

	with file.open() as input_file:
		reader = csv.DictReader(input_file)
		rows = [r for r in reader]
		if len(rows) == 1:
			row = rows[0]
		else:
			raise ValueError(f"Confused about having multiple rows in {file.name}")
	results = _parse_bayesrun_row(row)

	out.results = results

	return out
