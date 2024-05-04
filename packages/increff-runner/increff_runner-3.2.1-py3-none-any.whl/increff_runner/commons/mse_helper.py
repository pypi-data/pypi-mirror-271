from .db_helper import *
from .constants import *
from logging_increff.function import *
import copy
from .db_service import *
from .event_helper import *
from .db_helper import *
from .graphdb_helper import *


def create_next_dag(algo_name, next_blocks, dag):
    extra_blocks = [block for block in next_blocks if block != algo_name]
    for block in extra_blocks:
        del dag[block]
    return dag


def create_algo_block_runner_data(
    client,
    task_id,
    algo_name,
    level,
    block_identifier,
    app,
    app_id,
    masterUri,
    script_info,
    webHookUri,
):
    return {
        "client": client,
        "task_id": task_id,
        "algo_name": algo_name,
        "level": level,
        "block_identifier": block_identifier,
        "app_name": app,
        "app_id": app_id,
        "masterUri": masterUri,
        "script_info": script_info,
        "webHookUri": webHookUri,
    }


def create_events_for_next_blocks(url, master_url, output, error_data, job):
    # interim_task = get_interim_tasks(
    #     INTERIM_TASK_TABLE,
    #     job["data"]["task_id"],
    #     job["data"]["algo_name"],
    #     job["data"]["level"],
    # )
    # interim_task["status"] = "SUCCESS"
    change_status_of_task_node(job["data"]["algo_name"], job["data"]["task_id"], job["data"]["level"], "SUCCESS")
    
    # persist_value(INTERIM_TASK_TABLE, interim_task["id"], interim_task)

    node = get_task_node(job["data"]["algo_name"],job["data"]["task_id"],job["data"]["level"])
    if(str(node['last_block'])=="1"):
        status = check_last_block_status(job["data"]["task_id"], job["data"]["algo_name"])
        if status:
            add_info_logs(job["id"], "All levels for the block are completed")
            send_subtask_success_callback(
                master_url, job["data"]["task_id"], node['parent_task']
            )

    next_nodes = get_next_task_nodes(job["data"]["algo_name"], job["data"]["task_id"], job["data"]["level"])
    
    # dag = copy.copy(job["data"]["dag"])
    # algo_name = job["data"]["algo_name"]
    # next_blocks = dag[algo_name]
    # del dag[algo_name]
    # if dag == {}:
    #     return

    # for block in next_blocks:
    #     new_dag = create_next_dag(
    #         copy.copy(block), copy.copy(next_blocks), copy.copy(dag)
    #     )
    #     add_info_logs(
    #         job["id"],
    #         f"Getting levels for {job['data']['task_id']} and {list(new_dag.keys())[0]}",
    #     )
    #     all_levels = get_levels_for_block(
    #         INTERIM_TASK_TABLE, job["data"]["task_id"], list(new_dag.keys())[0]
    #     )
    #     all_levels = (
    #         [job["data"]["level"]] if job["data"]["level"] in all_levels else all_levels
    #     )
    #     for level in all_levels:
    for next_node in next_nodes:
        change_edge_between_task_nodes(node,next_node)
        data = create_algo_block_runner_data(
            job["data"]["client"],
            job["data"]["task_id"],
            next_node['name'],
            next_node['level'],
            job["data"]["block_identifier"],
            job["data"]["app_name"],
            job["data"]["app_id"],
            job["data"]["masterUri"],
            job["data"]["script_info"],
            job["data"]["webHookUri"],
        )
        add_info_logs(job["id"], f"Success message -> {str(data)}")
        job["webhook_status"] = "200"
        update_job(job)
        response = create_caas_job(url, data)


def send_subtask_success_callback(url, task_id, algo_name):
    if url == "":
        return
    data = {"status": "SUCCESS", "taskId": task_id, "subtaskName": algo_name,"reason":"Success"}
    headers = {
        "Content-Type": "application/json",
        "authUsername":"caas-user@increff.com",
        "authPassword":"caasuser@123",
        "authdomainname":"celio",
        "project_name":"celio-ars",
        "Conection":"keep-alive"
    }
    add_info_logs(task_id, f"Hitting Success Callback on {url} with data {data} ")
    response = requests.put(url, headers=headers,params=data)
    if response.status_code!=200:
        add_error_logs(task_id, f"Failed to hit the callback with status code {response.text}")
