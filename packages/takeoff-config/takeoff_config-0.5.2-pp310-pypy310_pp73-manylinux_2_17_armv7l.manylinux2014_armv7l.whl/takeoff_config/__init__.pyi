from typing import Optional

class AppConfig:
    echo: bool
    port: int
    enable_metrics: bool
    heartbeat_check_interval: int
    management_port: int
    vertex_port: int
    repository_path: str
    body_size_limit_bytes: int
    allow_remote_images: bool

class ReaderConfig:
    model_name: str
    device: str
    consumer_group: str
    redis_host: Optional[str]
    backend: Optional[str]
    log_level: Optional[str]
    cuda_visible_devices: Optional[str]
    max_batch_size: Optional[int]
    batch_duration_millis: Optional[int]
    access_token: Optional[str]
    tensor_parallel: Optional[int]
    quant_type: Optional[str]
    max_sequence_length: Optional[int]
    nvlink_unavailable: Optional[int]
    disable_static: Optional[int]
    disable_cuda_graph: Optional[int]
    cuda_graph_cache_capacity: Optional[int]

    def dict_without_optionals(self) -> dict[str, str | int | bool]:
        """Creates Dictionary from ReaderConfig, with optional values removed.
        Returns:
            dict[str, Optional[str | int]]: Dict without optionals.
        """
        ...

def read_takeoff_readers_config(path: str, reader_id: str) -> ReaderConfig:
    """Fetches ReaderConfig from a yaml on the given path and reader_id.
    Returns:
        ReaderConfig: ReaderConfig object corresponding to the given reader_id.
    """
    ...
