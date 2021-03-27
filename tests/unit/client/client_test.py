from random import randint
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from pyzeebe.errors import WorkflowNotFoundError


def test_run_workflow(zeebe_client, grpc_servicer):
    bpmn_process_id = str(uuid4())
    version = randint(0, 10)
    grpc_servicer.mock_deploy_workflow(bpmn_process_id, version, [])
    assert isinstance(zeebe_client.run_workflow(bpmn_process_id=bpmn_process_id, variables={}, version=version), int)


class TestRunWorkflowWithResult:
    @pytest.fixture
    def deployed_workflow(self, grpc_servicer):
        bpmn_process_id = str(uuid4())
        version = randint(0, 10)
        grpc_servicer.mock_deploy_workflow(bpmn_process_id, version, [])
        return bpmn_process_id, version

    def test_run_workflow_with_result_instance_key_is_int(self, zeebe_client, deployed_workflow):
        bpmn_process_id, version = deployed_workflow

        workflow_instance_key, _ = zeebe_client.run_workflow_with_result(bpmn_process_id, {}, version)

        assert isinstance(workflow_instance_key, int)

    def test_run_workflow_with_result_output_variables_are_as_expected(self, zeebe_client, deployed_workflow):
        expected = {}
        bpmn_process_id, version = deployed_workflow

        _, output_variables = zeebe_client.run_workflow_with_result(bpmn_process_id, {}, version)

        assert output_variables == expected


def test_deploy_workflow(zeebe_client):
    zeebe_client.zeebe_adapter.deploy_workflow = MagicMock()
    file_path = str(uuid4())
    zeebe_client.deploy_workflow(file_path)
    zeebe_client.zeebe_adapter.deploy_workflow.assert_called_with(file_path)


def test_run_non_existent_workflow(zeebe_client):
    with pytest.raises(WorkflowNotFoundError):
        zeebe_client.run_workflow(bpmn_process_id=str(uuid4()))


def test_run_non_existent_workflow_with_result(zeebe_client):
    with pytest.raises(WorkflowNotFoundError):
        zeebe_client.run_workflow_with_result(bpmn_process_id=str(uuid4()))


def test_cancel_workflow_instance(zeebe_client, grpc_servicer):
    bpmn_process_id = str(uuid4())
    version = randint(0, 10)
    grpc_servicer.mock_deploy_workflow(bpmn_process_id, version, [])
    workflow_instance_key = zeebe_client.run_workflow(bpmn_process_id=bpmn_process_id, variables={}, version=version)
    assert isinstance(zeebe_client.cancel_workflow_instance(workflow_instance_key=workflow_instance_key), int)


def test_publish_message(zeebe_client):
    zeebe_client.publish_message(name=str(uuid4()), correlation_key=str(uuid4()))
