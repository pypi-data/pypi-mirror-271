# SPDX-FileCopyrightText: 2024 Mass Labs
#
# SPDX-License-Identifier: MIT

OUT=massmarket_hash_event/

all: transport_pb2.py  authentication_pb2.py store_requests_pb2.py error_pb2.py

# TODO: define SRC list with replacements

transport_pb2.py: ../transport.proto
	protoc -I=.. --python_out=${OUT} ../transport.proto
	protoc -I=.. --pyi_out=${OUT} ../transport.proto
	sed -i 's#import error_pb2 as error__pb2#from massmarket_hash_event import error_pb2 as error__pb2#'  ${OUT}transport_pb2.py
	sed -i 's#import error_pb2 as _error_pb2#from massmarket_hash_event import error_pb2 as _error_pb2#'  ${OUT}transport_pb2.pyi

authentication_pb2.py: ../authentication.proto
	protoc -I=.. --python_out=${OUT} ../authentication.proto
	protoc -I=.. --pyi_out=${OUT} ../authentication.proto
	sed -i 's#import error_pb2 as error__pb2#from massmarket_hash_event import error_pb2 as error__pb2#'  ${OUT}authentication_pb2.py
	sed -i 's#import error_pb2 as _error_pb2#from massmarket_hash_event import error_pb2 as _error_pb2#'  ${OUT}authentication_pb2.pyi

store_requests_pb2.py: ../store_requests.proto
	protoc -I=.. --python_out=${OUT} ../store_requests.proto
	protoc -I=.. --pyi_out=${OUT} ../store_requests.proto
	sed -i 's#import error_pb2 as error__pb2#from massmarket_hash_event import error_pb2 as error__pb2#'  ${OUT}store_requests_pb2.py
	sed -i 's#import error_pb2 as _error_pb2#from massmarket_hash_event import error_pb2 as _error_pb2#'  ${OUT}store_requests_pb2.pyi

error_pb2.py: ../error.proto
	protoc -I=.. --python_out=${OUT} ../error.proto
	protoc -I=.. --pyi_out=${OUT} ../error.proto
