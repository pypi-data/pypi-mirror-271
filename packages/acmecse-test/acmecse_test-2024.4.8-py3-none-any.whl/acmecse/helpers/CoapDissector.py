#
#	CoapDissector.py
#
#	(c) 2024 by Andreas Kraft, Yann Garcia 
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#
#	This module contains various utilty functions that are used from various
#	modules and entities of the CSE.
#

from __future__ import annotations
from typing import Any, Dict, Tuple, Union

from .CoAP.Types import CoAPCodes, CodeItem, CoAPTypes
from .CoAP.CoAPMessage import CoAPMessage


import collections
import array
import struct
import ctypes
import random
import string

import ACMEIntEnum


class CoAPDissector(object):

	@staticmethod
	def get_option_flags(option_num):
		"""
		Get Critical, UnSafe, NoCacheKey flags from the option number (see RFC 7252, section 5.4.6)
		:param option_num: option number
		:return: option flags
		:rtype: 3-tuple (critical, unsafe, no-cache)
		"""
		opt_bytes = array.array('B', [0, 0])
		if option_num < 256:
			s = struct.Struct("!B")
			s.pack_into(opt_bytes, 0, option_num)
		else:
			s = struct.Struct("H")
			s.pack_into(opt_bytes, 0, option_num)
		critical = (opt_bytes[0] & 0x01) > 0
		unsafe = (opt_bytes[0] & 0x02) > 0
		nocache = ((opt_bytes[0] & 0x1e) == 0x1c)
		return (critical, unsafe, nocache)


	@staticmethod
	def decode(data:bytes, source:Any) -> CoapMessage:
		try:
			fmt = "!BBH"
			pos = struct.calcsize(fmt)
			s = struct.Struct(fmt)
			values = s.unpack_from(p_data)
			first = values[0]
			code = values[1]
			mid = values[2]
			version = (first & 0xC0) >> 6
			message_type = (first & 0x30) >> 4
			token_length = (first & 0x0F)
			message = None
			if CoapDissector.is_response(code):
				message = CoapMessageResponse()
				message.code = code
			elif CoapDissector.is_request(code):
				message = CoapMessageRequest()
				message.code = code
			else:
				message = CoapMessage()
				message.code = code
			message.source = p_source
			message.destination = None
			message.version = version
			message.type = message_type
			message.mid = mid
			if token_length > 0:
				fmt = "%ss" % token_length
				s = struct.Struct(fmt)
				token_value = s.unpack_from(p_data[pos:])[0]
				message.token = token_value.decode("utf-8")
			else:
				message.token = None

			pos += token_length
			current_option = 0
			values = p_data[pos:]
			length_packet = len(values)
			pos = 0
			while pos < length_packet:
				next_byte = struct.unpack("B", values[pos].to_bytes(1, "big"))[0]
				pos += 1
				if next_byte != int(CoapDissector.PAYLOAD_MARKER):
					# The first 4 bits of the byte represent the option delta
					num, option_length, pos = CoapDissector.read_option_value_len_from_byte(next_byte, pos, values)
					current_option += num
					# Read option
					try:
						option_item = CoapDissector.LIST_OPTIONS[current_option]
					except KeyError:
						(opt_critical, _, _) = CoapDissector.get_option_flags(current_option)
						if opt_critical:
							raise AttributeError("Critical option %s unknown" % current_option)
						else:
							# If the non-critical option is unknown
							# (vendor-specific, proprietary) - just skip it
							#log.err("unrecognized option %d" % current_option)
							pass
					else:
						if option_length == 0:
							value = None
						elif option_item.value_type == CoapDissector.INTEGER:
							tmp = values[pos: pos + option_length]
							value = 0
							for b in tmp:
								value = (value << 8) | struct.unpack("B", b.to_bytes(1, "big"))[0]
						elif option_item.value_type == CoapDissector.OPAQUE:
							tmp = values[pos: pos + option_length]
							value = tmp
						else:
							value = values[pos: pos + option_length]

						option = CoapOption()
						option.number = current_option
						option.value = CoapDissector.convert_to_raw(current_option, value, option_length)

						message.add_option(option)
						if option.number == CoapDissector.CONTENT_TYPE.number:
							message.payload_type = option.value
					finally:
						pos += option_length
				else:

					if length_packet <= pos:
						# log.err("Payload Marker with no payload")
						raise AttributeError("Packet length %s, pos %s" % (length_packet, pos))
					message.payload = ""
					payload = values[pos:]
					try:
						if message.payload_type == CoapDissector.Content_types["application/octet-stream"]:
							message.payload = payload
						else:
							message.payload = payload.decode("utf-8")
					except AttributeError:
						message.payload = payload.decode("utf-8")
					pos += len(payload)

			return message
		except AttributeError:
			return CoapDissector.BAD_REQUEST.number
		except struct.error:
			return CoapDissector.BAD_REQUEST.number
		# End of method decode

	@staticmethod
	def encode(p_coap_message:CoapMessage):
		fmt = "!BBH"

		if p_coap_message.token is None or p_coap_message.token == "":
			tkl = 0
		else:
			tkl = len(p_coap_message.token)
		tmp = (CoapDissector.VERSION << 2)
		tmp |= p_coap_message.type
		tmp <<= 4
		tmp |= tkl

		values = [tmp, p_coap_message.code, p_coap_message.mid]

		if p_coap_message.token is not None and tkl > 0:

			for b in str(p_coap_message.token):
				fmt += "c"
				values.append(bytes(b, "utf-8"))

		options = CoapDissector.as_sorted_list(p_coap_message.options)  # already sorted
		lastoptionnumber = 0
		for option in options:

			# write 4-bit option delta
			optiondelta = option.number - lastoptionnumber
			optiondeltanibble = CoapDissector.get_option_nibble(optiondelta)
			tmp = (optiondeltanibble << CoapDissector.OPTION_DELTA_BITS)

			# write 4-bit option length
			optionlength = option.length
			optionlengthnibble = CoapDissector.get_option_nibble(optionlength)
			tmp |= optionlengthnibble
			fmt += "B"
			values.append(tmp)

			# write extended option delta field (0 - 2 bytes)
			if optiondeltanibble == 13:
				fmt += "B"
				values.append(optiondelta - 13)
			elif optiondeltanibble == 14:
				fmt += "H"
				values.append(optiondelta - 269)

			# write extended option length field (0 - 2 bytes)
			if optionlengthnibble == 13:
				fmt += "B"
				values.append(optionlength - 13)
			elif optionlengthnibble == 14:
				fmt += "H"
				values.append(optionlength - 269)

			# write option value
			if optionlength > 0:
				opt_type = CoapDissector.LIST_OPTIONS[option.number].value_type
				if opt_type == CoapDissector.INTEGER:
					words = CoapDissector.int_to_words(option.value, optionlength, 8)
					for num in range(0, optionlength):
						fmt += "B"
						values.append(words[num])
				elif opt_type == CoapDissector.STRING:
					fmt += str(len(bytes(option.value, "utf-8"))) + "s"
					values.append(bytes(option.value, "utf-8"))

				else:  # OPAQUE
					for b in option.value:
						fmt += "B"
						values.append(b)

			# update last option number
			lastoptionnumber = option.number

		payload = p_coap_message.payload

		if payload is not None and len(payload) > 0:
			# if payload is present and of non-zero length, it is prefixed by
			# an one-byte Payload Marker (0xFF) which indicates the end of
			# options and the start of the payload

			fmt += "B"
			values.append(CoapDissector.PAYLOAD_MARKER)

			if isinstance(payload, bytes):
				fmt += str(len(payload)) + "s"
				values.append(payload)
			else:
				fmt += str(len(bytes(payload, "utf-8"))) + "s"
				values.append(bytes(payload, "utf-8"))
			# for b in str(payload):
			#	 fmt += "c"
			#	 values.append(bytes(b, "utf-8"))

		datagram = None
		if values[1] is None:
			values[1] = 0
		if values[2] is None:
			values[2] = 0
		try:
			s = struct.Struct(fmt)
			datagram = ctypes.create_string_buffer(s.size)
			s.pack_into(datagram, 0, *values)
		except struct.error:
			# The .exception method will report on the exception encountered
			# and provide a traceback.
			Logging.logDebug(fmt)
			Logging.logDebug(values)
			Logging.logErr('Failed to pack structure')

		return datagram
		# End of method encode

	@staticmethod
	def is_request(code):
		"""
		Checks if it is a request.

		:return: True, if is request
		"""
		return CoapDissector.REQUEST_CODE_LOWER_BOUND <= code <= CoapDissector.REQUEST_CODE_UPPER_BOUND

	@staticmethod
	def is_response(code):
		"""
		Checks if it is a response.
		:return: True, if is response
		"""
		return CoapDissector.RESPONSE_CODE_LOWER_BOUND <= code <= CoapDissector.RESPONSE_CODE_UPPER_BOUND

	@staticmethod
	def read_option_value_len_from_byte(byte, pos, values):
		"""
		Calculates the value and length used in the extended option fields.

		:param byte: 1-byte option header value.
		:return: the value and length, calculated from the header including the extended fields.
		"""
		h_nibble = (byte & 0xF0) >> 4
		l_nibble = byte & 0x0F
		value = 0
		length = 0
		if h_nibble <= 12:
			value = h_nibble
		elif h_nibble == 13:
			value = struct.unpack("!B", values[pos].to_bytes(1, "big"))[0] + 13
			pos += 1
		elif h_nibble == 14:
			s = struct.Struct("!H")
			value = s.unpack_from(values[pos:].to_bytes(2, "big"))[0] + 269
			pos += 2
		else:
			raise AttributeError("Unsupported option number nibble " + str(h_nibble))

		if l_nibble <= 12:
			length = l_nibble
		elif l_nibble == 13:
			length = struct.unpack("!B", values[pos].to_bytes(1, "big"))[0] + 13
			pos += 1
		elif l_nibble == 14:
			length = s.unpack_from(values[pos:].to_bytes(2, "big"))[0] + 269
			pos += 2
		else:
			raise AttributeError("Unsupported option length nibble " + str(l_nibble))
		return value, length, pos

	@staticmethod
	def convert_to_raw(number, value, length):
		"""
		Get the value of an option as a ByteArray.

		:param number: the option number
		:param value: the option value
		:param length: the option length
		:return: the value of an option as a BitArray
		"""

		opt_type = CoapDissector.LIST_OPTIONS[number].value_type

		if length == 0 and opt_type != CoapDissector.INTEGER:
			return bytes()
		elif length == 0 and opt_type == CoapDissector.INTEGER:
			return 0
		elif opt_type == CoapDissector.STRING:
			if isinstance(value, bytes):
				return value.decode("utf-8")
		elif opt_type == CoapDissector.OPAQUE:
			if isinstance(value, bytes):
				return value
			else:
				return bytes(value, "utf-8")
		if isinstance(value, tuple):
			value = value[0]
		if isinstance(value, str):
			value = str(value)
		if isinstance(value, str):
			return bytearray(value, "utf-8")
		elif isinstance(value, int):
			return value
		else:
			return bytearray(value)

	@staticmethod
	def as_sorted_list(options):
		"""
		Returns all options in a list sorted according to their option numbers.

		:return: the sorted list
		"""
		if len(options) > 0:
			options = sorted(options, key=lambda o: o.number)
		return options

	@staticmethod
	def get_option_nibble(optionvalue):
		"""
		Returns the 4-bit option header value.

		:param optionvalue: the option value (delta or length) to be encoded.
		:return: the 4-bit option header value.
		 """
		if optionvalue <= 12:
			return optionvalue
		elif optionvalue <= 255 + 13:
			return 13
		elif optionvalue <= 65535 + 269:
			return 14
		else:
			raise AttributeError("Unsupported option delta " + optionvalue)

	@staticmethod
	def int_to_words(int_val, num_words=4, word_size=32):
		"""
		Convert a int value to bytes.

		:param int_val: an arbitrary length Python integer to be split up.
			Network byte order is assumed. Raises an IndexError if width of
			integer (in bits) exceeds word_size * num_words.

		:param num_words: number of words expected in return value tuple.

		:param word_size: size/width of individual words (in bits).

		:return: a list of fixed width words based on provided parameters.
		"""
		max_int = 2 ** (word_size*num_words) - 1
		max_word_size = 2 ** word_size - 1

		if not 0 <= int_val <= max_int:
			raise AttributeError('integer %r is out of bounds!' % hex(int_val))

		words = []
		for _ in range(num_words):
			word = int_val & max_word_size
			words.append(int(word))
			int_val >>= word_size
		words.reverse()

		return words

	#Message Format

	# Length of the CoAP headers in bbits
	VERSION_BITS = 2
	"""	Number of bits used for the encoding of the CoAP version field. """
	TYPE_BITS = 2
	"""	Number of bits used for the encoding of the message type field. """
	TOKEN_LENGTH_BITS = 4
	"""	Number of bits used for the encoding of the token length field. """
	CODE_BITS = 8
	"""	Number of bits used for the encoding of the request method/response code field. """
	MESSAGE_ID_BITS = 16
	"""	Number of bits used for the encoding of the message ID. """
	OPTION_DELTA_BITS = 4
	"""	Number of bits used for the encoding of the option delta field. """
	OPTION_LENGTH_BITS = 4
	"""	Number of bits used for the encoding of the option length field. """


	PAYLOAD_MARKER = 0xFF
	"""	One byte which indicates indicates the end of options and the start of the payload. """

	VERSION = 1
	"""	The version of the CoAP protocol supported by this version of the library. """

	REQUEST_CODE_LOWER_BOUND = 1
	"""	The lowest value of a request code. """
	REQUEST_CODE_UPPER_BOUND = 31
	"""	The highest value of a request code. """

	# The lowest value of a response code.
	RESPONSE_CODE_LOWER_BOUND = 64
	"""	The lowest value of a response code. """

	RESPONSE_CODE_UPPER_BOUND = 191
	"""	The highest value of a response code. """

	# Type codes
	# The integer.





	# End of class CoapDissector

