#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
This is an example dag for using the KubernetesPodOperator.
"""

from kubernetes.client import models as k8s

from airflow import DAG
from airflow.kubernetes.secret import Secret
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

# [START howto_operator_k8s_cluster_resources]
#secret_file = Secret('volume', '/etc/sql_conn', 'airflow-secrets', 'sql_alchemy_conn')
#secret_env = Secret('env', 'SQL_CONN', 'airflow-secrets', 'sql_alchemy_conn')
#secret_all_keys = Secret('env', None, 'airflow-secrets-2')
#volume_mount = k8s.V1VolumeMount(
#    name='test-volume', mount_path='/root/mount_file', sub_path=None, read_only=True
#)

#configmaps = [
#    k8s.V1EnvFromSource(config_map_ref=k8s.V1ConfigMapEnvSource(name='test-configmap-1')),
#    k8s.V1EnvFromSource(config_map_ref=k8s.V1ConfigMapEnvSource(name='test-configmap-2')),
#]

#volume = k8s.V1Volume(
#    name='test-volume',
#    persistent_volume_claim=k8s.V1PersistentVolumeClaimVolumeSource(claim_name='test-volume'),
#)

#port = k8s.V1ContainerPort(name='http', container_port=80)

#init_container_volume_mounts = [
#    k8s.V1VolumeMount(mount_path='/etc/foo', name='test-volume', sub_path=None, read_only=True)
#]

#init_environments = [k8s.V1EnvVar(name='key1', value='value1'), k8s.V1EnvVar(name='key2', value='value2')]

#init_container = k8s.V1Container(
#    name="init-container",
#    image="ubuntu:16.04",
#    env=init_environments,
#    volume_mounts=init_container_volume_mounts,
#    command=["bash", "-cx"],
#    args=["echo 10"],
#)

#tolerations = [k8s.V1Toleration(key="key", operator="Equal", value="value")]

# [END howto_operator_k8s_cluster_resources]

#secret_env = secret.Secret(
#    # Expose the secret as environment variable.
#    deploy_type='env',
#    # The name of the environment variable, since deploy_type is `env` rather
#    # than `volume`.
#    deploy_target='SQL_CONN',
#    # Name of the Kubernetes Secret
#    secret='airflow-secrets',
#    # Key of a secret stored in this Secret object
#    key='sql_alchemy_conn')
#secret_volume = secret.Secret(
#    deploy_type='volume',
#    # Path where we mount the secret as volume
#    deploy_target='/var/secrets/google',
#    # Name of Kubernetes Secret
#    secret='service-account',
#    # Key in the form of service account file name
#    key='service-account.json')


default_args = {
    'owner': 'airflow',
}

with DAG(
    dag_id='example_kubernetes_operator',
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
) as dag:
    k = KubernetesPodOperator(
        namespace='airflow',
        image="gcr.io/meliuz-poc-data-lake/dbt:latest",
        cmds=["bash","-cx"],
        arguments=["dbt run --target dev-airflow"],
        labels={"foo": "bar"},
        image_pull_secrets='registrykey',
        image_pull_policy='Always',
#        secrets=[secret_file, secret_env, secret_all_keys],
#        ports=[port],
#        volumes=[volume],
#        volume_mounts=[volume_mount],
#        env_from=configmaps,
        name="airflow-test-pod",
        task_id="task",
#        affinity=affinity,
        is_delete_operator_pod=True,
        hostnetwork=False,
#        tolerations=tolerations,
#        init_containers=[init_container],
    )

    # [START howto_operator_k8s_private_image]
#    quay_k8s = KubernetesPodOperator(
#        namespace='airflow',
#        image='quay.io/apache/bash',
#        image_pull_secrets=[k8s.V1LocalObjectReference('testquay')],
#        cmds=["bash", "-cx"],
#        arguments=["echo", "10", "echo pwd"],
#        labels={"foo": "bar"},
#        name="airflow-private-image-pod",
#        is_delete_operator_pod=True,
#        in_cluster=True,
#        task_id="task-two",
#        get_logs=True,
#    )
    # [END howto_operator_k8s_private_image]
