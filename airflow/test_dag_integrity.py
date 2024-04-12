"""Test integrity of DAGs."""

import glob
import importlib.util
import os

import pytest
from airflow.models import DAG

DAG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dags/**.py")
# --> 현재 파일의 디렉토리에서 두단계 위의 상위 디렉토리인 dags 디렉토리 안의 모든 파이썬 파일(../../dags/**.py)
# bash_operator_no_command.py
# dag_cycle.py
# duplicated_task_ids.py
# testme.py

print(DAG_PATH)

DAG_FILES = glob.glob(DAG_PATH)
# DAG_PATH 패턴에 맞는 파일 리스트
# ['../../dags/bash_operator_no_command.py', '../../dags/dag_cycle.py', '../../dags/duplicated_task_ids.py', '../../dags/testme.py']


print(DAG_FILES)
# DAG_FILES 리스트에 정의된 DAG 파일을 dag_file이라는 파라미터변수로 입력
@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    """Import DAG files and check for DAG."""
    # dag_file의 경로 bash_operator_no_command.py -> modeule_name = bash_operator_no_command , _ = py
    module_name, _ = os.path.splitext(dag_file)

    # bash_operator_no_command.py
    module_path = os.path.join(DAG_PATH, dag_file)

    mod_spec = importlib.util.spec_from_file_location(module_name, module_path) # module_path에서 module_name을 로드하여 mod_spec 생성
    module = importlib.util.module_from_spec(mod_spec) # 모듈 스펙을 기반으로 모듈 로드
    mod_spec.loader.exec_module(module) # 해당 파일 실행

     # 리스트 컴프리헨션
    # 1) vars(module) : module의 속성을 딕셔너리로 가져옴 
    # 1-1) vars(module).values(): 딕셔너리의 밸류값을 가져옴
    # 2) var for var in vars(module).values(): 딕셔너리의 밸류값을 루핑 
    # 3) var for var in vars(module).values() if isinstance(var, DAG): var가 DAG의 객체인지 판단하여 true 값만 리스트에 담음
    
    dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]

    # moddule

    # pytest 함수
    assert dag_objects

    for dag in dag_objects:
        # Test cycles
        dag.test_cycle()
