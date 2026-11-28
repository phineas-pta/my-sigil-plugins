# -*- coding: utf-8 -*-

import re

_UNIT_MAP = {
	"không": 0,
	"linh": 0,
	"lẻ": 0,
	"một": 1,
	"mốt": 1,
	"hai": 2,
	"ba": 3,
	"bốn": 4,
	"tư": 4,
	"năm": 5,
	"nhăm": 5,
	"lăm": 5,
	"sáu": 6,
	"bảy": 7,
	"tám": 8,
	"chín": 9,
	"mười": 10,
}

_MULTIPLIER_MAP = {
	"mươi": 10,
	"trăm": 100,
	"nghìn": 1_000,
	"ngàn": 1_000,
	"vạn": 10_000,
	"triệu": 1_000_000,
	# skip anything above 10^9 for easier parsing
}

_START = ("một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười") # enforce first word
_TERMS = tuple(_UNIT_MAP.keys()) + tuple(_MULTIPLIER_MAP.keys())
_END   = tuple(i for i in _TERMS if i not in ("năm", "không", "linh", "lẻ", "triệu")) # enforce last word, other multipliers are left as-is
_SPACE = chr(32)
PATTERN = re.compile(
	r"\b"
	+ "(?:" + "|".join(_START) + ")"
	+ "(?:" + _SPACE + "(?:" + "|".join(_TERMS) + ")" + ")" + "*"
	+ _SPACE + "(?:" + "|".join(_END) + ")"
	+ r"\b"
, flags=re.IGNORECASE)
_ERROR_CODE = -1


def word2int(match: re.Match) -> str: # usage: PATTERN.sub(word2int, text)
	text = match.group(0)
	words = text.lower().split(_SPACE)

	# cases: not a number → skip
	if len(words) == 2: # pattern guarantees that words[0] in _START and words[1] in _END
		if words[0] == "mười" and words[1] in ("mươi", "tư", "mốt", "mười", "trăm"):
			return text
		if words[0] != "mười" and words[1] in _UNIT_MAP:
			return text
	if "vạn" in words and "triệu" in words: # should be unlikely but just in case
		return text

	res_start, res_mid, res_end = [], [], []
	if words[0] == "năm" and words[1] in _START and words[1] != "sáu": # year
		res_start.append(words.pop(0))
	if len(words) > 2 and words[-2] != "mười" and words[-1] == "một": # unit price, cannot be filtered with regex because special case "mười một"
		res_end.append(words.pop())

	res_int = _parse_int(_SPACE.join(words))
	if res_int == _ERROR_CODE:
		print("    cannot parse:", text)
		return text
	tmp = str(res_int)
	if 5 <= len(tmp) <= 8 and tmp.endswith("0000"):
		res_mid.extend([tmp[:-4], "vạn"])
	else:
		res_mid.append(tmp)

	res_str = _SPACE.join(res_start + res_mid + res_end)
	print(text, "->", res_str) # always print for debugging
	return res_str


def _parse_int(string: str) -> int:
	res_int = 0
	# because we skip anything above 10^9, we can tokenize by splitting string
	for mult in ("triệu", "vạn", "nghìn", "ngàn"):
		tmp_list = string.split(mult)
		match len(tmp_list):
			case 1: # not found
				pass
			case 2:
				tmp_val = _parse_sub_1000(tmp_list[0])
				if tmp_val == _ERROR_CODE:
					return _ERROR_CODE
				res_int += tmp_val * _MULTIPLIER_MAP[mult]
				string = tmp_list[1]
			case _: # duplicate
				return _ERROR_CODE
	tmp_val = _parse_sub_1000(string)
	if tmp_val == _ERROR_CODE:
		return _ERROR_CODE
	else:
		return res_int + tmp_val

def _parse_sub_1000(token: str) -> int: # only return value <1000
	if token == "": return 0
	words = token.strip(_SPACE).split(_SPACE)
	res_int, rem = 0, 0
	prev_word, prev_mult = "", ""
	while len(words) > 0:
		curr_word = words.pop(0) # parse from left to right
		if curr_word == prev_mult or (prev_word in _START[:-1] and curr_word in _START): # grammar peculiar cases
			return _ERROR_CODE

		if curr_word in _UNIT_MAP:
			rem += _UNIT_MAP[curr_word]
		else: # curr_word in _MULTIPLIER_MAP  # guaranted by pattern
			rem *= _MULTIPLIER_MAP[curr_word]
			res_int += rem
			rem = 0
			prev_mult = curr_word

		# print(curr_word, rem , res_int) # for debugging only
		prev_word = curr_word
	res_int += rem
	if res_int < 1000:
		return res_int
	else:
		return _ERROR_CODE


if __name__ == "__main__": # for debugging only
	test_cases = [
		"Chương BA Trăm tám MươI tám: Trận chiến cuối cùng",
		"đây là năm hai nghìn",
		"rộng hai mươi vạn dặm",
		"tốn một triệu năm trăm nghìn tệ",
		"tốn năm triệu một trăm tám mươi nghìn tệ",
		"mua chín ngàn chín trăm chín mươi chín đoá hồng",
		"đã qua năm trăm năm không gặp",
		"cần năm trăm sáu trăm lượng",
		"nữ hài mười tám mười chín tuổi",
		"cần bảy bảy bốn mươi chín ngày",
	]
	for i in test_cases:
		print(i)
		PATTERN.sub(word2int, i)
		print()
