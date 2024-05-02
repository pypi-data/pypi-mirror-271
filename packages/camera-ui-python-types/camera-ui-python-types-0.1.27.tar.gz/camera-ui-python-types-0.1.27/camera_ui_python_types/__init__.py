from rx.core.typing import Observable

from abc import ABC, abstractmethod

from typing import (
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    TypedDict,
    Union,
    Any,
    Protocol,
    runtime_checkable,
    Callable,
    overload,
    TypeVar,
    AsyncGenerator,
)

Callback = Callable[..., Any]


# database types
class Go2RtcFFMPEGSource(TypedDict):
    aac: str
    opus: str


class Go2RtcWSSource(TypedDict):
    webrtc: str


class Go2RtcRTSPSource(TypedDict):
    single: str
    default: str
    mp4: str


class Go2RtcEndpoint(TypedDict):
    webrtc: str
    mse: str
    lmp4: str
    mmp4: str
    mp4: str
    mp4Snapshot: str
    jpegSnapshot: str
    lHlsTs: str
    lHlsFmp4: str
    mHlsFmp4: str
    mjpeg: str
    mjpegHtml: str


class StreamUrls(TypedDict):
    ws: Go2RtcWSSource
    rtsp: Go2RtcRTSPSource
    transcoded: Go2RtcFFMPEGSource
    www: Go2RtcEndpoint


class CameraInput(TypedDict):
    _id: str
    name: str
    roles: List["CameraRoles"]
    urls: StreamUrls


CameraRoles = Literal["detect", "record", "stream", "snapshot", "none"]


class CameraZone(TypedDict):
    name: str
    regions: List["ZoneRegion"]


class ZoneRegion(TypedDict):
    _id: str
    coords: List["ZoneCoord"]


class ZoneCoord(TypedDict):
    _id: str
    points: Tuple[int, int]


class CameraInformation(TypedDict):
    model: str
    manufacturer: str
    hardware: str
    serialNumber: str
    firmwareVersion: str
    supportUrl: str


CameraType = Literal["camera", "doorbell"]


class BaseCamera(TypedDict):
    _id: str
    nativeId: Optional[str]
    pluginId: str
    name: str
    disabled: bool
    isCloud: bool
    hasLight: bool
    hasSiren: bool
    hasBinarySensor: bool
    hasBattery: bool
    info: CameraInformation
    type: CameraType
    motionZones: List[CameraZone]
    objectZones: List[CameraZone]


class Camera(BaseCamera):
    hasAudioDetector: bool
    hasMotionDetector: bool
    hasObjectDetector: bool
    hasPtz: bool
    sources: List[CameraInput]


# camera types
class BaseState(TypedDict):
    timestamp: int
    lastTriggered: int


class MotionSetEvent(TypedDict):
    state: bool


class AudioSetEvent(TypedDict):
    state: bool


class ObjectSetEvent(TypedDict):
    state: bool
    detections: List[str]


class LightSetEvent(TypedDict):
    state: bool


class DoorbellSetEvent(TypedDict):
    state: bool


class SirenSetEvent(TypedDict):
    state: bool


class BatterySetEvent(TypedDict):
    state: int


class DeviceSetEvent(TypedDict):
    pass


class LightState(BaseState, LightSetEvent):
    pass


class MotionState(BaseState, MotionSetEvent):
    pass


class AudioState(BaseState, AudioSetEvent):
    pass


class DoorbellState(BaseState, DoorbellSetEvent):
    pass


class SirenState(BaseState, SirenSetEvent):
    pass


class ObjectState(BaseState, ObjectSetEvent):
    pass


class BatteryState(BaseState, BatterySetEvent):
    pass


State = Union[
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
]

T = TypeVar(
    "T",
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
)


class StateValues(Protocol):
    light: LightState
    motion: MotionState
    audio: AudioState
    object: ObjectState
    doorbell: DoorbellState
    siren: SirenState
    battery: BatteryState


CameraStateCallbacks = Dict[str, Callable[[T], None]]

StateValue = Union[
    LightState,
    MotionState,
    AudioState,
    DoorbellState,
    SirenState,
    ObjectState,
    BatteryState,
]

OnSetEvent = Union[
    LightSetEvent,
    MotionSetEvent,
    AudioSetEvent,
    DoorbellSetEvent,
    SirenSetEvent,
    BatterySetEvent,
    ObjectSetEvent,
]

StateNames = Literal[
    "light", "motion", "audio", "doorbell", "siren", "battery", "object"
]

OnChangeCallback = Callable[[T, T], None]


class CameraSource(Protocol):
    async def is_prebuffering(self, type: str) -> bool: ...
    async def get_prebuffer_raw_url(self, type: str) -> Optional[str]: ...
    async def get_stream_info(self) -> Optional[Dict[str, Any]]: ...


class CameraDelegate(ABC):
    @abstractmethod
    async def snapshot_request(self, request_id: str) -> bytes:
        pass

    @abstractmethod
    async def prepare_stream(self, request_id: str) -> None:
        pass

    @abstractmethod
    async def on_offer(self, request_id: str, sdp: str) -> str:
        pass

    @abstractmethod
    async def on_candidates(self, request_id: str, candidates: str) -> None:
        pass

    @abstractmethod
    async def reboot(self) -> None:
        pass


class CameraPrebufferDelegate(ABC):
    @abstractmethod
    async def is_prebuffering(self, source_name: str, type: str) -> bool:
        pass

    @abstractmethod
    async def get_prebuffer_raw_url(self, source_name: str, type: str) -> Optional[str]:
        pass

    @abstractmethod
    async def get_stream_info(self, source_name: str) -> Optional[Dict[str, Any]]:
        pass


CameraExtension = Literal[
    "hub",
    "prebuffer",
    "motionDetection",
    "objectDetection",
    "audioDetection",
    "ptz",
    "intercom",
]


class BaseCameraConfig(TypedDict):
    name: str
    nativeId: Optional[str]
    isCloud: Optional[bool]
    hasLight: Optional[bool]
    hasSiren: Optional[bool]
    hasBinarySensor: Optional[bool]
    hasBattery: Optional[bool]
    disabled: Optional[bool]
    info: Optional[CameraInformation]


class CameraInputSettings(TypedDict):
    _id: str
    name: str
    roles: List[CameraRoles]
    urls: List[str]


class CameraConfigWithSources(BaseCameraConfig):
    sources: Optional[List[CameraInputSettings]]


class CameraConfigWithDelegate(BaseCameraConfig):
    delegate: Optional[CameraDelegate]


CameraConfig = Union[CameraConfigWithSources, CameraConfigWithDelegate]


# plugins types
PluginConfig = Dict[str, Union[str, int, bool]]


class JsonBaseSchema(TypedDict):
    type: Any
    key: Optional[str]
    title: Optional[str]
    description: Optional[str]
    required: Optional[bool]
    readonly: Optional[bool]
    placeholder: Optional[str]
    hidden: Optional[bool]
    group: Optional[str]
    defaultValue: Optional[Union[str, int, bool]]


class PluginJsonBaseSchema(JsonBaseSchema):
    store: Optional[bool]
    onGet: Any
    onSet: Any


class PluginJsonSchemaString(PluginJsonBaseSchema):
    type: str
    format: Optional[str]
    minLength: Optional[int]
    maxLength: Optional[int]


class PluginJsonSchemaNumber(PluginJsonBaseSchema):
    type: int
    minimum: Optional[int]
    maximum: Optional[int]


class PluginJsonSchemaBoolean(PluginJsonBaseSchema):
    type: bool


class PluginJsonSchemaEnum(PluginJsonBaseSchema):
    type: str
    enum: List[str]
    multiple: Optional[bool]


class PluginJsonSchemaObject(PluginJsonBaseSchema):
    type: Dict[str, Any]
    opened: Optional[bool]
    properties: Optional[Dict[str, "PluginJsonSchema"]]


PluginJsonSchema = Union[
    PluginJsonSchemaString,
    PluginJsonSchemaNumber,
    PluginJsonSchemaBoolean,
    PluginJsonSchemaEnum,
    PluginJsonSchemaObject,
]


PluginJsonSchemaForm = Dict[str, PluginJsonSchema]

class PluginRootSchema(TypedDict):
    schema: PluginJsonSchemaForm


# json schema types
class JsonSchemaString(JsonBaseSchema):
    type: str
    format: Optional[str]
    minLength: Optional[int]
    maxLength: Optional[int]


class JsonSchemaNumber(JsonBaseSchema):
    type: int
    minimum: Optional[int]
    maximum: Optional[int]


class JsonSchemaBoolean(JsonBaseSchema):
    type: bool


class JsonSchemaEnum(JsonBaseSchema):
    type: str
    enum: List[str]
    multiple: Optional[bool]


class JsonSchemaObject(JsonBaseSchema):
    type: Dict[str, Any]
    opened: Optional[bool]
    properties: Optional[Dict[str, "JsonSchema"]]


class JsonSchemaButton(TypedDict):
    label: str
    onSubmit: str


class JsonSchemaObjectWithButtons(JsonSchemaObject):
    buttons: Optional[Tuple[JsonSchemaButton, Optional[JsonSchemaButton]]]


class JsonSchemaAnyOf(TypedDict):
    anyOf: List["JsonSchema"]


class JsonSchemaArray(JsonBaseSchema):
    type: List[Any]
    opened: Optional[bool]
    items: Optional[Union["JsonSchema", JsonSchemaAnyOf]]


JsonSchema = Union[
    JsonSchemaString,
    JsonSchemaNumber,
    JsonSchemaBoolean,
    JsonSchemaEnum,
    JsonSchemaObject,
    JsonSchemaObjectWithButtons,
    JsonSchemaArray,
]


class JsonSchemaForm(TypedDict):
    pass


class RootSchema(TypedDict):
    schema: JsonSchemaForm


class SchemaConfig(TypedDict):
    rootSchema: PluginRootSchema
    config: Dict[str, Union[str, int, bool]]


class IceServer(TypedDict):
    urls: List[str]
    username: Optional[str]
    credential: Optional[str]


class FrameMetadata(TypedDict):
    format: str
    frameSize: int
    width: int
    height: int


class Frame(TypedDict):
    metadata: FrameMetadata
    data: bytes


# camera storage
@runtime_checkable
class CameraStorage(Protocol):
    async def initialize_storage(self) -> None: ...
    async def get_value(self, path: str, default_value: Any = None) -> Any: ...
    async def set_value(self, path: str, new_value: Any) -> None: ...
    def has_value(self, path: str) -> bool: ...
    async def get_config(self) -> SchemaConfig: ...
    async def set_config(self, new_config: Dict[str, Any]) -> None: ...
    async def add_schema(
        self,
        schema_or_path: Union[PluginJsonSchemaForm, str],
        schema: Optional[PluginJsonSchema] = None,
    ) -> None: ...
    def remove_schema(self, path: str) -> None: ...
    async def change_schema(self, path: str, new_schema: Dict[str, Any]) -> None: ...
    def get_schema(self, path: str) -> Optional[PluginJsonSchema]: ...
    def has_schema(self, path: str) -> bool: ...
    async def _resolve_on_get_functions(
        self,
        schema: Union[PluginJsonSchemaForm, PluginJsonSchema],
        base_schema_path: str = "",
    ) -> None: ...
    async def _resolve_on_get_functions_for_object(
        self,
        schema: PluginJsonSchemaForm,
        base_schema_path: str,
    ) -> None: ...
    async def _resolve_on_get_functions_for_schema(self, schema_path: str) -> None: ...
    async def _trigger_on_set_for_changes(
        self,
        old_config: Dict[str, Any],
        new_config: Dict[str, Any],
        path: str = "",
    ) -> None: ...
    def _filter_storable_values(
        self,
        schema: PluginJsonSchemaForm,
        base_schema_path: str = "",
        result: Dict[str, Any] = {},
    ) -> Dict[str, Any]: ...
    def _contains_storable_schema(
        self,
        schema: Union[PluginJsonSchemaForm, PluginJsonSchema],
    ) -> bool: ...
    def _save_db(self) -> None: ...
    def _remove_db(self) -> None: ...


# storage controller
@runtime_checkable
class StorageController(Protocol):
    async def create_camera_storage(
        self,
        instance: Any,
        camera_id: str,
        schema: Optional[PluginJsonSchemaForm] = None,
    ) -> CameraStorage: ...
    def get_camera_storage(self, camera_id: str) -> Optional[CameraStorage]: ...
    def remove_camera_storage(self, camera_id: str) -> None: ...


# logger
@runtime_checkable
class PluginLogger(Protocol):
    def log(self, *args: Any) -> None: ...
    def error(self, *args: Any) -> None: ...
    def warn(self, *args: Any) -> None: ...
    def attention(self, *args: Any) -> None: ...
    def debug(self, *args: Any) -> None: ...
    def trace(self, *args: Any) -> None: ...


# config service
@runtime_checkable
class PluginConfigService(Protocol):
    def get(
        self,
        key: str,
        default: Optional[Any] = None,
        validate: Optional[Callable[[Any], bool]] = None,
        refresh: bool = False,
        write_if_not_valid: bool = False,
    ) -> Any: ...

    def has(self, key: str, refresh: bool = False) -> bool: ...
    def ensure_exists(
        self, key: str, default: Optional[Any] = None, write: bool = False
    ) -> None: ...
    def set(self, key: str, value: Any, write: bool = False) -> None: ...
    def insert(
        self, key: str, value: Any, index: Optional[int] = None, write: bool = False
    ) -> None: ...
    def push(self, key: str, *values: Any, write: bool = False) -> None: ...
    def delete(self, key: str, write: bool = False) -> None: ...
    def all(self, refresh: bool = False) -> Dict[str, Any]: ...
    def replace(self, new_config: Dict[str, Any], write: bool = False) -> None: ...
    def update_value(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        target_key: str,
        new_value: Any,
        write: bool = False,
    ) -> None: ...
    def replace_or_add_item(
        self,
        path: str,
        search_key: str,
        search_value: Any,
        new_item: Any,
        write: bool = False,
    ) -> None: ...


# manager todo: improve typing
@runtime_checkable
class SystemManager(Protocol):
    def on(self, event: str, listener: Callback) -> "SystemManager": ...
    def once(self, event: str, listener: Callback) -> "SystemManager": ...
    def remove_listener(self, event: str, listener: Callback) -> "SystemManager": ...
    def remove_all_listeners(self, event: str) -> "SystemManager": ...


@runtime_checkable
class PluginsManager(Protocol):  # todo: add methods
    def on(self, event: str, listener: Callback) -> "PluginsManager": ...
    def once(self, event: str, listener: Callback) -> "PluginsManager": ...
    def remove_listener(self, event: str, listener: Callback) -> "PluginsManager": ...
    def remove_all_listeners(self, event: str) -> "PluginsManager": ...


@runtime_checkable
class CameraDevice(Protocol):
    id: str
    plugin_id: str
    native_id: Optional[str]
    state: bool
    disabled: bool
    name: str
    type: CameraType
    info: CameraInformation
    sources: List[CameraSource]
    motion_zones: List[CameraZone]
    object_zones: List[CameraZone]
    is_cloud: bool
    has_light: bool
    has_siren: bool
    has_binary_sensor: bool
    has_battery: bool
    has_motion_detector: bool
    has_audio_detector: bool
    has_object_detector: bool
    has_ptz: bool

    on_connected: Observable[bool]
    on_light_switched: Observable[LightState]
    on_motion_detected: Observable[MotionState]
    on_audio_detected: Observable[AudioState]
    on_object_detected: Observable[ObjectState]
    on_doorbell_pressed: Observable[DoorbellState]
    on_siren_detected: Observable[SirenState]
    on_battery_changed: Observable[BatteryState]

    stream_source: CameraSource
    snapshot_source: CameraSource
    recording_source: CameraSource
    detection_source: CameraSource
    delegate: Optional[CameraDelegate]
    prebuffer_delegate: Optional[CameraPrebufferDelegate]

    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    async def reboot(self) -> None: ...
    async def snapshot(self, force_new: Optional[bool] = None) -> bytes: ...
    async def generate_frames(self) -> AsyncGenerator[Frame, None]: ...
    async def get_ffmpeg_path(self) -> str: ...
    async def get_ice_servers(self) -> List[IceServer]: ...
    # async def create_session(self, options: Any) -> Any: ... # todo
    async def stream_video(self, source_name: str, options: Any) -> None: ...
    async def record_to_file(
        self, source_name: str, output_path: str, duration: Optional[int] = 60
    ) -> None: ...
    async def get_value(
        self, state_name: str
    ) -> Union[
        LightState,
        MotionState,
        AudioState,
        ObjectState,
        DoorbellState,
        SirenState,
        BatteryState,
    ]: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["light"],
        event_data: LightSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["motion"],
        event_data: MotionSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["audio"],
        event_data: AudioSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["object"],
        event_data: ObjectSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["doorbell"],
        event_data: DoorbellSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["siren"],
        event_data: SirenSetEvent,
    ) -> None: ...

    @overload
    async def update_state(
        self,
        state_name: Literal["battery"],
        event_data: BatterySetEvent,
    ) -> None: ...
    async def update_state(self, state_name: str, event_data: Any) -> None: ...
    def on_state_change(self, state_name: StateNames) -> Observable[Any]: ...
    def on_property_change(self, property_name: str) -> Observable[Any]: ...
    def remove_all_listeners(self) -> None: ...


# device manager
DeviceManagerEventType = Literal[
    "cameraSelected",
    "cameraDeselected",
    "cameraUpdated",
]

CameraSelectedCallback = Callable[[CameraDevice, CameraExtension], None]
CameraDeselectedCallback = Callable[[str, CameraExtension], None]
CameraAddedCallback = Callable[[CameraDevice], None]
CameraRemovedCallback = Callable[[str], None]
CameraUpdatedCallback = Callable[[str, CameraDevice], None]


@runtime_checkable
class DeviceManager(Protocol):
    async def get_camera_by_id(self, id: str) -> Optional[CameraDevice]: ...
    async def get_camera_by_name(self, name: str) -> Optional[CameraDevice]: ...
    async def create_camera(self, config: CameraConfig) -> CameraDevice: ...
    async def remove_camera_by_id(self, id: str) -> None: ...
    async def remove_camera_by_name(self, name: str) -> None: ...

    @overload
    def on(
        self, event: Literal["cameraSelected"], listener: CameraSelectedCallback
    ) -> "DeviceManager": ...
    @overload
    def on(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...
    @overload
    def on(
        self, event: Literal["cameraUpdated"], listener: CameraUpdatedCallback
    ) -> "DeviceManager": ...

    @overload
    def once(
        self, event: Literal["cameraSelected"], listener: CameraSelectedCallback
    ) -> "DeviceManager": ...
    @overload
    def once(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...
    @overload
    def once(
        self, event: Literal["cameraUpdated"], listener: CameraUpdatedCallback
    ) -> "DeviceManager": ...

    @overload
    def remove_listener(
        self, event: Literal["cameraSelected"], listener: CameraSelectedCallback
    ) -> "DeviceManager": ...
    @overload
    def remove_listener(
        self, event: Literal["cameraDeselected"], listener: CameraDeselectedCallback
    ) -> "DeviceManager": ...
    @overload
    def remove_listener(
        self, event: Literal["cameraUpdated"], listener: CameraUpdatedCallback
    ) -> "DeviceManager": ...

    def remove_all_listeners(
        self, event: Optional[DeviceManagerEventType] = None
    ) -> "DeviceManager": ...


# plugin api
APIEventType = Literal["finishLaunching", "shutdown"]


@runtime_checkable
class PluginAPI(Protocol):
    storage_path: str
    config_file: str
    config_service: PluginConfigService
    storage_controller: StorageController
    device_manager: DeviceManager
    system_manager: SystemManager
    plugins_manager: PluginsManager

    def on(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def once(self, event: APIEventType, listener: Callback) -> "PluginAPI": ...
    def remove_listener(
        self, event: APIEventType, listener: Callback
    ) -> "PluginAPI": ...
    def remove_all_listeners(
        self, event: Optional[APIEventType] = None
    ) -> "PluginAPI": ...


# base plugin
class BasePlugin(ABC):
    @abstractmethod
    async def on_form_submit(self, action_id: str, payload: Any) -> Optional[Dict[Any, Any]]:
        pass

    @abstractmethod
    def configure_cameras(self, cameras: List[CameraDevice]) -> None:
        pass
