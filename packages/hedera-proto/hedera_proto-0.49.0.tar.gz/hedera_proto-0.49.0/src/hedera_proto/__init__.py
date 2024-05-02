import sys
import os
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
from .network_service_pb2_grpc import NetworkService, NetworkServiceServicer, NetworkServiceStub
from .token_service_pb2_grpc import TokenService, TokenServiceServicer, TokenServiceStub
from .consensus_service_pb2_grpc import ConsensusService, ConsensusServiceServicer, ConsensusServiceStub
from .util_service_pb2_grpc import UtilService, UtilServiceServicer, UtilServiceStub
from .mirror_network_service_pb2_grpc import NetworkService, NetworkServiceServicer, NetworkServiceStub
from .file_service_pb2_grpc import FileService, FileServiceServicer, FileServiceStub
from .crypto_service_pb2_grpc import CryptoService, CryptoServiceServicer, CryptoServiceStub
from .smart_contract_service_pb2_grpc import SmartContractService, SmartContractServiceServicer, SmartContractServiceStub
from .freeze_service_pb2_grpc import FreezeService, FreezeServiceServicer, FreezeServiceStub
from .schedule_service_pb2_grpc import ScheduleService, ScheduleServiceServicer, ScheduleServiceStub
