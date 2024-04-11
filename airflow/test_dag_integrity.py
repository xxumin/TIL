"""Test integrity of DAGs."""

import glob
import importlib.util
import os

import pytest
from airflow.models import DAG

DAG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dags/**.py")
DAG_FILES = glob.glob(DAG_PATH)
# DAG_PATH 패턴에 맞는 파일 리스트 입력

# pytest 데커레이터가 발견된 모든 파이썬 파일에 테스트 진행(DAG_FILES의 모든 구성요소)
@pytest.mark.parametrize("dag_file", DAG_FILES)
def test_dag_integrity(dag_file):
    """Import DAG files and check for DAG."""
    module_name, _ = os.path.splitext(dag_file)
    # 파일 경로에서 파일확장자를 제거하여 파일이름 추출( _ 무시하는 값)
    module_path = os.path.join(DAG_PATH, dag_file)
    # 파일 경로 생성 
    mod_spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(module)

    dag_objects = [var for var in vars(module).values() if isinstance(var, DAG)]
    # 리스트 컴프리헨션
    # 1) vars(module) : module의 속성을 딕셔너리로 가져옴 
    # 1-1) vars(module).values(): 딕셔너리의 밸류값을 가져옴
    # 2) var for var in vars(module).values(): 딕셔너리의 밸류값을 루핑 
    # 3) var for var in vars(module).values() if isinstance(var, DAG): var가 DAG의 객체인지 판단하여 ture 값만 리스트에 담음
    
    assert dag_objects
    # /dags 경로에 있는 모든 모든 파이썬파일에 DAG 객체가 적어도 하나가 포함되어있는지 유효성 검사

    for dag in dag_objects:
        # Test cycles
        dag.test_cycle()
    # 순환주기 존재여부 검사
