from typing import Any, Optional, Union
import time
from . import conversions

from .proto_generated import transact_pb2
from .proto_generated import transact_pb2_grpc
from .. import types
from .proto_generated import types_pb2
from . import helpers

class BaseClient(object):

    def _prepare_seeds(self, seeds) -> None:
        return helpers._prepare_seeds(seeds)
        
    def _prepare_put(self, namespace, key, record_data, set_name, logger) -> None:

        logger.debug(
            "Putting record: namespace=%s, key=%s, record_data:%s, set_name:%s",
            namespace,
            key,
            record_data,
            set_name,
        )

        key = self._get_key(namespace, set_name, key)
        bin_list = [
            types_pb2.Bin(name=k, value=conversions.toVectorDbValue(v))
            for (k, v) in record_data.items()
        ]

        transact_stub = self._get_transact_stub()
        put_request = transact_pb2.PutRequest(key=key, bins=bin_list)

        return (transact_stub, put_request)

    def _prepare_get(self, namespace, key, bin_names, set_name, logger) -> None:

        logger.debug(
            "Getting record: namespace=%s, key=%s, bin_names:%s, set_name:%s",
            namespace,
            key,
            bin_names,
            set_name,
        )


        key = self._get_key(namespace, set_name, key)
        bin_selector = self._get_bin_selector(bin_names=bin_names)

        transact_stub = self._get_transact_stub()
        get_request = transact_pb2.GetRequest(key=key, binSelector=bin_selector)

        return (transact_stub, key, get_request)

    def _prepare_exists(self, namespace, key, set_name, logger) -> None:

        logger.debug(
            "Getting record existence: namespace=%s, key=%s, set_name:%s",
            namespace,
            key,
            set_name,
        )

        key = self._get_key(namespace, set_name, key)

        transact_stub = self._get_transact_stub()

        return (transact_stub, key)

    def _prepare_is_indexed(self, namespace, key, index_name, index_namespace, set_name, logger) -> None:

        logger.debug(
            "Checking if index exists: namespace=%s, key=%s, index_name=%s, index_namespace=%s, set_name=%s",
            namespace,
            key,
            index_name,
            index_namespace,
            set_name,
        )

        if not index_namespace:
            index_namespace = namespace
        index_id = types_pb2.IndexId(namespace=index_namespace, name=index_name)
        key = self._get_key(namespace, set_name, key)

        transact_stub = self._get_transact_stub()
        is_indexed_request = transact_pb2.IsIndexedRequest(key=key, indexId=index_id)

        return (transact_stub, is_indexed_request)

    def _prepare_vector_search(self, namespace, index_name, query, limit, search_params, bin_names, logger) -> None:

        logger.debug(
            "Performing vector search: namespace=%s, index_name=%s, query=%s, limit=%s, search_params=%s, bin_names=%s",
            namespace,
            index_name,
            query,
            limit,
            search_params,
            bin_names,
        )

        if search_params != None:
            search_params = search_params._to_pb2()
        bin_selector = self._get_bin_selector(bin_names=bin_names)
        index = types_pb2.IndexId(namespace=namespace, name=index_name)
        query_vector = conversions.toVectorDbValue(query).vectorValue


        transact_stub = self._get_transact_stub()

        vector_search_request = transact_pb2.VectorSearchRequest(
            index=index,
            queryVector=query_vector,
            limit=limit,
            hnswSearchParams=search_params,
            binSelector=bin_selector,
        )
        
        return (transact_stub, vector_search_request)

    def _get_transact_stub(self):
        return transact_pb2_grpc.TransactStub(
            self._channel_provider.get_channel()
        )

    def _respond_get(self, response, key) -> None:
        return types.RecordWithKey(
            key=conversions.fromVectorDbKey(key),
            bins=conversions.fromVectorDbRecord(response),
        )

    def _respond_exists(self, response) -> None:
        return response.value

    def _respond_is_indexed(self, response) -> None:
        return response.value

    def _respond_neighbor(self, response) -> None:
        return conversions.fromVectorDbNeighbor(response)

    def _get_bin_selector(self, *, bin_names: Optional[list] = None):

        if not bin_names:
            bin_selector = transact_pb2.BinSelector(
                type=transact_pb2.BinSelectorType.ALL, binNames=bin_names
            )
        else:
            bin_selector = transact_pb2.BinSelector(
                type=transact_pb2.BinSelectorType.SPECIFIED, binNames=bin_names
            )
        return bin_selector

    def _get_key(self, namespace: str, set: str, key: Union[int, str, bytes, bytearray]):
        if isinstance(key, str):
            key = types_pb2.Key(namespace=namespace, set=set, stringValue=key)
        elif isinstance(key, int):
            key = types_pb2.Key(namespace=namespace, set=set, longValue=key)
        elif isinstance(key, (bytes, bytearray)):
            key = types_pb2.Key(namespace=namespace, set=set, bytesValue=key)
        else:
            raise Exception("Invalid key type" + type(key))
        return key

    def _prepare_wait_for_index_waiting(self, namespace, name, wait_interval):
        return helpers._prepare_wait_for_index_waiting(self, namespace, name, wait_interval)

    def _check_completion_condition(self, start_time, timeout, index_status, unmerged_record_initialized):

        if start_time + 10 < time.monotonic():
            unmerged_record_initialized = True
            
        if index_status.unmergedRecordCount > 0:
            unmerged_record_initialized = True

        if (
            index_status.unmergedRecordCount == 0
            and unmerged_record_initialized == True
        ):
            return True
        else:
            return False
