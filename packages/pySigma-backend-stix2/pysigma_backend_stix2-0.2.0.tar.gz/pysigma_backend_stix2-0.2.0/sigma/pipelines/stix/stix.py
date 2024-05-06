from copy import deepcopy
from abc import ABC
import re
from typing import Union, Optional, Iterable, Tuple
from sigma.modifiers import SigmaContainsModifier, SigmaStartswithModifier, SigmaEndswithModifier
from sigma.processing.conditions import LogsourceCondition
from sigma.processing.transformations import FieldMappingTransformation, ValueTransformation, \
    DetectionItemTransformation
from sigma.processing.pipeline import ProcessingItem, ProcessingPipeline
from sigma.rule import SigmaDetectionItem, SigmaDetection
from sigma.types import SigmaString, SigmaNumber, SigmaType

stix_2_0_mapping = {
    "User": [
        "user-account:user_id"
    ],
    "USER": [
        "user-account:user_id"
    ],
    "user": [
        "user-account:user_id"
    ],
    "event_data.SubjectUserName": [
        "user-account:user_id",
        "user-account:account_login"
    ],
    "c-ip": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:src_ref.value"
    ],
    "cs-ip": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:src_ref.value"
    ],
    "destinationip": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:dst_ref.value"
    ],
    "destinationmac": [
        "mac-addr:value",
        "network-traffic:dst_ref.value"
    ],
    "destinationport": [
        "network-traffic:dst_port"
    ],
    "dst_port": [
        "network-traffic:dst_port"
    ],
    "domainname": [
        "domain-name:value"
    ],
    "dst": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:dst_ref.value"
    ],
    "dst_ip": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:dst_ref.value"
    ],
    "endtime": [
        "network-traffic:end"
    ],
    "event_data.DestinationIp": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:dst_ref.value"
    ],
    "DestinationIp": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:dst_ref.value"
    ],
    "event_data.DestinationPort": [
        "network-traffic:dst_port"
    ],
    "DestinationPort": [
        "network-traffic:dst_port"
    ],
    "destination.port": [
        "network-traffic:dst_port"
    ],
    "filehash": [
        "file:hashes.SHA-256",
        "file:hashes.MD5",
        "file:hashes.SHA-1"
    ],
    "filename": [
        "file:name"
    ],
    "filepath": [
        "file:parent_directory_ref",
        "directory:path"
    ],
    "identityip": [
        "ipv4-addr:value"
    ],
    "protocolid": [
        "network-traffic:protocols[*]"
    ],
    "sourceip": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:src_ref.value"
    ],
    "sourcemac": [
        "mac-addr:value",
        "network-traffic:src_ref.value"
    ],
    "sourceport": [
        "network-traffic:src_port"
    ],
    "SourcePort": [
        "network-traffic:src_port"
    ],
    "src": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:src_ref.value"
    ],
    "src_ip": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:src_ref.value"
    ],
    "starttime": [
        "network-traffic:start"
    ],
    "url": [
        "url:value"
    ],
    "username": [
        "user-account:user_id"
    ],
    "utf8_payload": [
        "artifact:payload_bin"
    ],
    "c-uri": [
        "network-traffic:extensions.'http-request-ext'.request_value",
        "url:value"
    ],
    "c-uri-query": [
        "network-traffic:extensions.'http-request-ext'.request_value",
        "url:value"
    ],
    "c-uri-stem": [
        "network-traffic:extensions.'http-request-ext'.request_value",
        "url:value"
    ],
    "keywords": [
        "artifact:payload_bin"
    ],
    "cs-method": [
        "network-traffic:extensions.'http-request-ext'.request_method"
    ],
    "clientip": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:src_ref.value"
    ],
    "c-useragent": [
        "network-traffic:extensions.'http-request-ext'.request_header.'User-Agent'"
    ],
    "r-dns": [
        "domain-name:value",
        "url:value"
    ],
    "cs-host": [
        "domain-name:value"
    ],
    "cs-cookie": [
        "network-traffic:extensions.'http-request-ext'.request_header.Cookie"
    ],
    "query": [
        "domain-name:value",
        "url:value"
    ],
    "host.scan.vuln_name": [
        "vulnerability:name"
    ],
    "host.scan.vuln": [
        "vulnerability:external_references[*].external_id"
    ],
    "userIdentity.type": [
        "user-account:account_login"
    ],
    "userIdentity.arn": [
        "user-account:account_login",
        "user-account:display_name"
    ],
    "responseElements.pendingModifiedValues.masterUserPassword": [
        "user-account:credential"
    ],
    "AccountDomain": [
        "user-account:x_domain"
    ],
    "AccountID": [
        "user-account:user_id"
    ],
    "AccountName": [
        "user-account:account_login",
        "user-account:display_name"
    ],
    "AccountSecurityID": [
        "user-account:x_security_id"
    ],
    "ClientIP": [
        "ipv4-addr:value",
        "ipv6-addr:value",
        "network-traffic:src_ref.value"
    ],
    "DestinationHostname": [
        "network-traffic:dst_ref.value"
    ],
    "Device": [
        "file:name"
    ],
    "FileDirectory": [
        "directory:path"
    ],
    "FileExtension": [
        "file:x_extension"
    ],
    "FileHash": [
        "file:hashes.SHA-256",
        "file:hashes.MD5",
        "file:hashes.SHA-1"
    ],
    "FilePath": [
        "file:name"
    ],
    "Filename": [
        "file:name"
    ],
    "HomeDirectory": [
        "directory:path"
    ],
    "Image": [
        "process:binary_ref.name"
    ],
    "ImageLoadedTempPath": [
        "process:extensions.'windows-service-ext'.service_dll_refs[*].x_temp_path"
    ],
    "ImageName": [
        "process:binary_ref.name"
    ],
    "ImagePath": [
        "process:binary_ref.parent_directory_ref.path"
    ],
    "SourceImage": [
        "process:binary_ref.name"
    ],
    "InitiatorUserName": [
        "user-account:user_id",
        "user-account:account_login"
    ],
    "LoadedImage": [
        "process:extensions.'windows-service-ext'.service_dll_refs[*].name"
    ],
    "LoadedImageName": [
        "process:extensions.'windows-service-ext'.service_dll_refs[*].name"
    ],
    "MD5Hash": [
        "file:hashes.MD5"
    ],
    "NewName": [
        "windows-registry-key:key"
    ],
    "ParentCommandLine": [
        "process:parent_ref.command_line"
    ],
    "ParentImage": [
        "process:parent_ref.binary_ref.name"
    ],
    "ParentImageName": [
        "process:parent_ref.binary_ref.name"
    ],
    "ParentProcessGuid": [
        "process:parent_ref.x_guid"
    ],
    "ParentProcessName": [
        "process:parent_ref.binary_ref.name"
    ],
    "ParentProcessPath": [
        "process:parent_ref.binary_ref.name"
    ],
    "ProcessCommandLine": [
        "process:command_line"
    ],
    "Command": [
        "process:command_line"
    ],
    "CommandLine": [
        "process:command_line"
    ],
    "ProcessGuid": [
        "process:x_guid"
    ],
    "ProcessId": [
        "process:pid"
    ],
    "ProcessName": [
        "process:binary_ref.name"
    ],
    "ProcessPath": [
        "process:binary_ref.parent_directory_ref.path"
    ],
    "RegistryKey": [
        "windows-registry-key:key"
    ],
    "RegistryValueData": [
        "windows-registry-key:values[*].data"
    ],
    "RegistryValueName": [
        "windows-registry-key:values[*].name"
    ],
    "SAMAccountName": [
        "user-account:account_login",
        "user-account:display_name"
    ],
    "SHA1Hash": [
        "file:hashes.SHA-1"
    ],
    "SHA256Hash": [
        "file:hashes.SHA-256"
    ],
    "ServiceFileName": [
        "process:extensions.'windows-service-ext'.service_dll_refs[*].name"
    ],
    "ServiceName": [
        "process:extensions.'windows-service-ext'.service_name"
    ],
    "Details": [
        "windows-registry-key:values[*].data"
    ],
    "TargetFilename": [
        "file:name"
    ],
    "TargetImage": [
        "process:binary_ref.name"
    ],
    "TargetObject": [
        "windows-registry-key:key"
    ],
    "UserDomain": [
        "user-account:x_domain"
    ],
    "event_data.FileName": [
        "file:name"
    ],
    "event_data.Image": [
        "process:binary_ref.name"
    ],
    "event_data.ImageLoaded": [
        "process:extensions.'windows-service-ext'.service_dll_refs[*].name"
    ],
    "ImageLoaded": [
        "process:extensions.'windows-service-ext'.service_dll_refs[*].name"
    ],
    "event_data.ImagePath": [
        "process:binary_ref.parent_directory_ref.path"
    ],
    "event_data.ParentCommandLine": [
        "process:parent_ref.command_line"
    ],
    "event_data.ParentImage": [
        "process:parent_ref.binary_ref.name"
    ],
    "event_data.ParentProcessName": [
        "process:parent_ref.binary_ref.name"
    ],
    "event_data.TargetFilename": [
        "file:name"
    ],
    "event_data.User": [
        "user-account:user_id"
    ],
    "a0": [
        "process:command_line"
    ],
    "a1": [
        "process:command_line"
    ],
    "name": [
        "file:name"
    ],
    "a3": [
        "process:command_line"
    ],
    "exe": [
        "file:name"
    ],
    "a2": [
        "process:command_line"
    ],
    "pam_user": [
        "user-account:user_id"
    ]
}
stix_shifter_mapping = {
    "action": [
        "x-oca-event:action"
    ],
    "operation": [
        "x-oca-event:action"
    ],
    "event.category": [
        "x-oca-event:category"
    ],
    "eventName": [
        "x-oca-event:action"
    ],
    "eventType": [
        "x-oca-event:category"
    ],
    "Description": [
        "x-oca-event:action",
        "x-ibm-finding:description"
    ],
    "Event-ID": [
        "x-oca-event:code"
    ],
    "EventID": [
        "x-oca-event:code"
    ],
    "Event_ID": [
        "x-oca-event:code"
    ],
    "event-id": [
        "x-oca-event:code"
    ],
    "eventId": [
        "x-oca-event:code"
    ],
    "EventType": [
        "x-oca-event:action"
    ],
    "Message": [
        "x-oca-event:original"
    ],
    "Details": [
        "windows-registry-key:values[*].data",
        "x-oca-event:original"
    ],
    "event_id": [
        "x-oca-event:code"
    ],
    "eventid": [
        "x-oca-event:code"
    ],
    "type": [
        "x-oca-event:action"
    ],
    "pam_message": [
        "x-oca-event:action"
    ],
    "PipeName": [
        "x-oca-event:pipe_name"
    ],
    "cs-host": [
        "x-oca-asset:hostname",
        "domain-name:value"
    ],
    "eventSource": [
        "x-oca-asset:hostname"
    ],
    "ComputerName": [
        "x-oca-asset:hostname"
    ],
    "pam_rhost": [
        "x-oca-asset:hostname"
    ],
    "r-dns": [
        "domain-name:value",
        "url:value",
        "network-traffic:extensions.'dns-ext'.question.domain_ref"
    ],
    "query": [
        "domain-name:value",
        "url:value",
        "network-traffic:extensions.'dns-ext'.question.domain_ref"
    ],
    "credescription": [
        "x-ibm-finding:description"
    ],
    "crename": [
        "x-ibm-finding:name"
    ],
    "rulenames": [
        "x-ibm-finding:rule_names[*]"
    ],
    "categoryid": [
        "x-qradar:category_id"
    ],
    "categoryname": [
        "x-qradar:category_name"
    ],
    "credibility": [
        "x-qradar:credibility"
    ],
    "Device": [
        "x-qradar:device_type"
    ],
    "devicetype": [
        "x-qradar:device_type"
    ],
    "direction": [
        "x-qradar:direction"
    ],
    "domainid": [
        "x-qradar:domain_id"
    ],
    "geographic": [
        "x-qradar:geographic"
    ],
    "high_level_category_id": [
        "x-qradar:high_level_category_id"
    ],
    "high_level_category_name": [
        "x-qradar:high_level_category_name"
    ],
    "identityhostname": [
        "x-qradar:identity_host_name"
    ],
    "logsourceid": [
        "x-qradar:log_source_id"
    ],
    "logsourcename": [
        "x-qradar:log_source_name"
    ],
    "logsourcetypename": [
        "x-qradar:log_source_type_name"
    ],
    "magnitude": [
        "x-qradar:magnitude"
    ],
    "qid": [
        "x-qradar:qid"
    ],
    "qidname": [
        "x-qradar:event_name"
    ],
    "relevance": [
        "x-qradar:relevance"
    ],
    "severity": [
        "x-qradar:severity"
    ]
}
keep_numeric_fields = {
    'network-traffic:dst_port',
    'network-traffic:src_port',
    'x-oca-event:code',
}


class NumericValueCastingTransformation(ValueTransformation):
    """
    By default, numeric values are converted to string, except for the certain fields.
    """
    def __post_init__(self):
        super().__post_init__()

    def apply_value(self, field: str, val: SigmaNumber) -> Union[SigmaString, SigmaNumber]:
        if field in keep_numeric_fields:
            return val
        return SigmaString(str(val))


class LinuxArgumentsCommandLineLikeTransformation(ValueTransformation):

    argument_regex_pattern = r"a[0-9]+"  # a0, a1, a2, ...

    def apply_value(self, field: str, val: SigmaString) -> Optional[Union[SigmaType, Iterable[SigmaType]]]:
        if re.match(self.argument_regex_pattern, field):
            return SigmaString(' ' + str(val) + ' ')
        return val

    def apply_detection_item(self, detection_item: SigmaDetectionItem) -> Optional[
            Union[SigmaDetection, SigmaDetectionItem]]:
        super().apply_detection_item(detection_item)
        if re.match(self.argument_regex_pattern, detection_item.field):
            if SigmaContainsModifier not in detection_item.modifiers:
                new_detection_item = SigmaDetectionItem(
                    field=detection_item.field,
                    modifiers=detection_item.modifiers + [SigmaContainsModifier],
                    value=detection_item.value,
                    value_linking=detection_item.value_linking
                )
                return new_detection_item
        return detection_item


class SplitImageFieldTransformation(DetectionItemTransformation, ABC):

    FILE_TYPE = 'file'
    DIRECTORY_TYPE = 'directory'
    WILDCARD_TOKEN = '*'

    fields_to_split_kb = {
        'file:name': {
            FILE_TYPE: 'file:name',
            DIRECTORY_TYPE: 'file:parent_directory_ref.path'
        },
        'process:binary_ref.name': {
            FILE_TYPE: 'process:binary_ref.name',
            DIRECTORY_TYPE: 'process:binary_ref.parent_directory_ref.path'
        },
        'process:parent_ref.binary_ref.name': {
            FILE_TYPE: 'process:parent_ref.binary_ref.name',
            DIRECTORY_TYPE: 'process:parent_ref.binary_ref.parent_directory_ref.path'
        }
    }
    platform: str = NotImplemented  # abstract

    @property
    def backslash_token(self):
        return '\\' if self.platform == 'windows' else '/'

    def _clean_value(self, value: str, modifiers: list) -> str:
        if (SigmaContainsModifier in modifiers or SigmaEndswithModifier in modifiers) \
                and value.startswith(self.WILDCARD_TOKEN):
            value = value[1:]
        if SigmaContainsModifier in modifiers or SigmaStartswithModifier in modifiers:
            if value.endswith(self.WILDCARD_TOKEN):
                value = value[:-1]
        return value

    def _extract_directory_path_and_filename_from_value(self, value: str) -> Optional[Tuple[Optional[str], Optional[str]]]:
        if value.endswith(self.backslash_token):
            # if the value ends with a backslash, it is a directory path
            return value, None
        value_arr = value.split(self.backslash_token)
        value_arr_dropped_empty = list(filter(lambda x: x != '', value_arr))

        if len(value_arr_dropped_empty) == 1:
            # if the value contains only one element, it is a filename
            return None, value_arr_dropped_empty[0]

        if len(value_arr_dropped_empty) > 1:
            # if the value contains more than one element, the last element is a filename,
            # and the rest is a directory path
            filename = value_arr_dropped_empty[-1]
            directory_path_arr = value_arr_dropped_empty[:-1]
            directory_path = self.backslash_token.join(directory_path_arr)
            if value.startswith(self.backslash_token):
                directory_path = self.backslash_token + directory_path
            return directory_path, filename

    def _create_detection_item(self, value: str, field: str, field_type: str, original_detection_item: SigmaDetectionItem,
                               two_parts=False) -> SigmaDetectionItem:

        modifiers = deepcopy(original_detection_item.modifiers)

        if two_parts:
            if SigmaContainsModifier in modifiers:
                if field_type == self.FILE_TYPE:
                    modifiers.remove(SigmaContainsModifier)
                    modifiers.append(SigmaStartswithModifier)
                elif field_type == self.DIRECTORY_TYPE:
                    modifiers.remove(SigmaContainsModifier)
                    modifiers.append(SigmaEndswithModifier)
            elif SigmaStartswithModifier in modifiers:
                if field_type == self.DIRECTORY_TYPE:
                    modifiers.remove(SigmaStartswithModifier)
            elif SigmaEndswithModifier in modifiers:
                if field_type == self.FILE_TYPE:
                    modifiers.remove(SigmaEndswithModifier)

        return SigmaDetectionItem(
            field=field,
            modifiers=modifiers,
            value=[SigmaString(value)],
        )

    def _produce_detection(self, value: str, detection_item: SigmaDetectionItem) -> Optional[SigmaDetection]:
        directory_path, filename = self._extract_directory_path_and_filename_from_value(value)

        if directory_path is None and filename is None:
            return None

        directory_path_detection_item = None
        filename_detection_item = None

        if directory_path is not None:
            directory_field = self.fields_to_split_kb[detection_item.field]['directory']
            directory_path_detection_item = self._create_detection_item(directory_path,
                                                                        directory_field,
                                                                        self.DIRECTORY_TYPE,
                                                                        detection_item,
                                                                        filename is not None)

        if filename is not None:
            filename_field = self.fields_to_split_kb[detection_item.field]['file']
            filename_detection_item = self._create_detection_item(filename,
                                                                  filename_field,
                                                                  self.FILE_TYPE,
                                                                  detection_item,
                                                                  directory_path is not None)

        filtered_detections = list(filter(lambda x: x is not None,
                                          [filename_detection_item, directory_path_detection_item]))
        return SigmaDetection(detection_items=filtered_detections) if len(filtered_detections) > 0 else None

    def apply_detection_item(self, detection_item: SigmaDetectionItem) -> Optional[
        Union[SigmaDetection, SigmaDetectionItem]]:

        if detection_item.field in self.fields_to_split_kb.keys():
            if isinstance(detection_item.value, list):
                aggregated_detections = []
                for value in detection_item.value:
                    value_raw = self._clean_value(str(value), detection_item.modifiers)
                    produced_detection = self._produce_detection(value_raw,
                                                                 detection_item)
                    if produced_detection is not None:
                        aggregated_detections.append(produced_detection)
                return SigmaDetection(detection_items=aggregated_detections)
            else:
                # TODO - when is this case happening?
                raise ValueError(f"Value of field {detection_item.field} is not a list")
        return detection_item


class SplitImageFieldLinuxTransformation(SplitImageFieldTransformation):
    platform = 'linux'


class SplitImageFieldWindowsTransformation(SplitImageFieldTransformation):
    platform = 'windows'


def stix_2_0() -> ProcessingPipeline:
    """This is a pipeline that maps fields to the STIX 2.0 format."""
    return ProcessingPipeline(
        name="stix 2.0",
        priority=100,
        items=[
            ProcessingItem(
                identifier="linux_arguments_command_line_like",
                transformation=LinuxArgumentsCommandLineLikeTransformation(),
                rule_conditions=[
                    LogsourceCondition(
                        product="linux",
                    )
                ]
            ),
            ProcessingItem(
                identifier="stix_2_0",
                transformation=FieldMappingTransformation(stix_2_0_mapping),
            ),
            ProcessingItem(
                identifier="numeric_value_mapping",
                transformation=NumericValueCastingTransformation(),
            ),
            ProcessingItem(
                identifier="image_split_windows",
                transformation=SplitImageFieldWindowsTransformation(),
                rule_conditions=[
                    LogsourceCondition(
                        product="windows",
                    )
                ]
            ),
            ProcessingItem(
                identifier="image_split_linux",
                transformation=SplitImageFieldLinuxTransformation(),
                rule_conditions=[
                    LogsourceCondition(
                        product="linux",
                    )
                ]
            ),
        ],
    )


def stix_shifter() -> ProcessingPipeline:
    return ProcessingPipeline(
        name="stix_shifter",
        priority=30,
        items=[
            ProcessingItem(
                identifier="stix_shifter",
                transformation=FieldMappingTransformation(stix_shifter_mapping),
            ),
            ProcessingItem(
                identifier="numeric_value_mapping",
                transformation=NumericValueCastingTransformation(),
            )
        ]
    )