from typing import Dict, Optional

import requests
from prettytable import PrettyTable

from e2enetworks.cloud.tir.finetuning.constants import HUGGING_FACE, EOS_BUCKET, TEXT_MODELS_LIST
from e2enetworks.cloud.tir.helpers import get_argument_from_kwargs
from e2enetworks.cloud.tir.skus import Plans, client
from e2enetworks.cloud.tir.utils import prepare_object
from e2enetworks.constants import PIPELINE


class FinetuningClient():
    def __init__(self,
                 project: Optional[str] = None,
                 ):
        client_not_ready = (
            "Client is not ready. Please initiate client by:"
            "\n- Using e2enetworks.cloud.tir.init(...)"
        )
        if not client.Default.ready():
            raise ValueError(client_not_ready)

        if project:
            client.Default.set_project(project)

    def create_finetuning(self,
                          name,
                          model_name,
                          plan_name,
                          huggingface_integration_id,
                          wandb_integration_id=None,
                          wandb_integration_run_name="",
                          description=None,
                          training_type="Peft",
                          **kwargs
                          ):
        if not isinstance(plan_name, str):
            return ValueError("plan_name is should be string")

        if model_name in TEXT_MODELS_LIST:
            training_inputs = self._get_text_model_inputs(**kwargs)
        else:
            raise Exception(f'model_name is  invalid : {model_name}')

        payload = {"name": name,
                    "model_name": model_name,
                    "huggingface_integration_id": huggingface_integration_id,
                    "sku_item_price_id": self._get_sku_item_price_from_plan_name(plan_name),
                    "training_inputs": training_inputs,
                    "training_type": training_type,
                    "wandb_integration_id": wandb_integration_id if wandb_integration_id else None,
                    "wandb_integration_run_name": wandb_integration_run_name,
                    "description": description
                    }
        url = f"{client.Default.gpu_projects_path()}/finetuning/?"
        req = requests.Request('POST', url, json=payload)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def _get_text_model_inputs(self, **kwargs):
        return {**self._get_dataset_config(**kwargs),
                "validation_split_ratio": get_argument_from_kwargs('validation_split_ratio', kwargs, float, 0.1),
                "target_dataset_field": get_argument_from_kwargs("target_dataset_field", kwargs, str, 'text'),
                "gradient_accumulation_steps": get_argument_from_kwargs("gradient_accumulation_steps", kwargs, int, 1),
                "context_length": get_argument_from_kwargs('context_length', kwargs, int, 512),
                "learning_rate": get_argument_from_kwargs('learning_rate', kwargs, float, 0.0000141),
                "epochs": get_argument_from_kwargs('epochs', kwargs, int, 1),
                "stop_training_when": get_argument_from_kwargs('stop_training_when', kwargs, str, "epoch_count"),
                "max_steps": get_argument_from_kwargs('max_steps', kwargs, int, -1),
                "batch_size": get_argument_from_kwargs('batch_size', kwargs, int, 4),
                "peft_lora_alpha": get_argument_from_kwargs('peft_lora_alpha', kwargs, int, 16),
                "peft_lora_r": get_argument_from_kwargs('peft_lora_r', kwargs, int, 64),
                "max_grad_norm": get_argument_from_kwargs('max_grad_norm', kwargs, int, 1),
                "save_strategy": get_argument_from_kwargs('save_strategy', kwargs, str, "no"),
                "task": get_argument_from_kwargs('task', kwargs, str, "Instruction-Finetuning"),
                "prompt_configuration": get_argument_from_kwargs('prompt_configuration', kwargs, str, ""),
                "save_steps": get_argument_from_kwargs('save_steps', kwargs, int, 10),
                "limit_training_records_count": get_argument_from_kwargs('limit_training_records_count', kwargs, int, 10),
                "limit_eval_records_count": get_argument_from_kwargs('limit_training_records_count', kwargs, int, 10),
                }

    def _get_dataset_config(self, **kwargs):
        dataset_type = kwargs.get("dataset_type")
        dataset_info = kwargs.get("dataset")

        if dataset_type not in [EOS_BUCKET, HUGGING_FACE]:
            raise Exception(f"dataset_type: only {EOS_BUCKET}, {HUGGING_FACE} allowed")

        if dataset_type == HUGGING_FACE:
            return {"dataset_type": HUGGING_FACE,
                    "dataset": dataset_info}

        dataset_sub_str = dataset_info.split('/')
        if len(dataset_sub_str) <= 1:
            raise Exception("dataset invalid")
        object_name = dataset_info.replace(f"{dataset_sub_str[0]}/", '', 1)
        if not object_name:
            raise Exception("dataset invalid")
        return {"dataset_type": dataset_type,
                "dataset": f'{dataset_sub_str[0]}/{object_name}'}

    def list_finetunings(self):
        url = f"{client.Default.gpu_projects_path()}/finetuning/?"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def list_supported_models(self):
        url = f"{client.Default.gpu_projects_path()}/finetuning/model_types/?"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def show_plan_names(self):
        plans = Plans()
        plans_list = plans.list(PIPELINE, image='')
        gpu_skus = plans_list["GPU"]
        plans_table = PrettyTable()
        plans_table.field_names = ['name', 'series', 'cpu', 'gpu', 'memory',
                                   'sku_item_price_id', 'sku_type', 'committed_days', 'unit_price']
        plans.insert_plans_in_table(gpu_skus, plans_table)
        print(plans_table)

    def _get_sku_item_price_from_plan_name(self, plan_name, committed_days=0):
        plans = Plans().list(PIPELINE, image='')
        plan_name_to_sku = {}
        gpu_skus = plans["GPU"]
        for sku in gpu_skus:
            for sku_item_price in sku["plans"]:
                if not sku["is_free"]:
                    name = sku.get('name')
                    committed_days = sku_item_price.get('committed_days')
                    key = f'{name}_c{committed_days}'
                    plan_name_to_sku[key] = sku_item_price['sku_item_price_id']
        if plan_name_to_sku.get(f'{plan_name}_c{committed_days}'):
            return plan_name_to_sku.get(f'{plan_name}_c{committed_days}')
        raise Exception(f'Plan_name invalid : {plan_name}')

    def get_finetuning(self,
                       finetuning_id: str | int
                       ):
        url = f"{client.Default.gpu_projects_path()}/finetuning/{finetuning_id}/?"
        req = requests.Request('GET', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def delete_finetuning(self,
                          finetuning_id: str | int
                          ):
        url = f"{client.Default.gpu_projects_path()}/finetuning/{finetuning_id}/?"
        req = requests.Request('DELETE', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def stop_finetuning(self,
                        finetuning_id: str | int
                        ):
        url = f"{client.Default.gpu_projects_path()}/finetuning/{finetuning_id}/?&action=terminate&"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    def retry_finetuning(self,
                         finetuning_id: str | int
                         ):
        url = f"{client.Default.gpu_projects_path()}/finetuning/{finetuning_id}/?&action=retry&"
        req = requests.Request('PUT', url)
        response = client.Default.make_request(req)
        return prepare_object(response)

    @staticmethod
    def help():
        help_text = """
        FinetuningClient Class Help:

        This class provides methods for interacting with finetuning-related operations.
        Before using these methods, make sure to initialize the client using:
        - Using e2enetworks.cloud.tir.init(...)

        Available Methods:
        1. create_finetuningcreate_finetuning(self,
                          name,
                          model_name,
                          plan_name,
                          huggingface_integration_id,
                          wandb_integration_id=None,
                          wandb_integration_run_name="",
                          description="",
                          training_type="Peft",
                          **kwargs
                          )
           - Create a new finetuning.
        2. list_finetunings()
           - List existing finetunings.
        3. get_finetuning(finetuning_id)
           - Get details of a specific finetuning.
        4. delete_finetuning(finetuning_id)
           - Delete a specific finetuning.
        5. stop_finetuning(finetuning_id)
           - stop a specific finetuning.
        6. retry_finetuning(finetuning_id)
           - retry a failed/terminated finetuning.
        7. show_plan_names()
           - list currently supported skus for finetuning
        8. list_supported_models()
           - list currently supported models for finetuning
        Note: Certain methods require specific arguments. Refer to the method signatures for details.
        """
        print(help_text)
