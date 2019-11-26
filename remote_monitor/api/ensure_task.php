<?php
require 'luigi_service.php';
require_once 'util.php';

$service = new LuigiService();

$now = format_datetime(new DateTime());

$input_json = file_get_contents('php://input');
$input = json_decode($input_json, TRUE);

ensure_string($input['task_name'], "input['task_name']");
ensure_string($input['task_class'], "input['task_class']");
ensure_string($input['task_params'], "input['task_params']");
ensure_integer($input['experiment_id'], "input['experiment_id']");
$task_name = SQLite3::escapeString($input['task_name']);
$task_class = SQLite3::escapeString($input['task_class']);
$task_params = SQLite3::escapeString($input['task_params']);
$experiment_id = $input['experiment_id'];

$task_id = $service->get_equivalent_task_id($experiment_id, $task_name, $task_class, $task_params);

if ($task_id === FALSE) {
    ensure_boolean($input['root_task'], "input['root_task']");
    if ($input['root_task']) {
        $task_id = $service->insert_root_task($experiment_id, $task_name, $task_class, $task_params, "pending", NULL, NULL, NULL);
    } else {
        ensure_integer($input['parent_task_id'], "input['parent_task_id']");
        $task_id = $service->insert_worker_task($input['parent_task_id'], $task_name, $task_class, $task_params, "pending", NULL, NULL, NULL);
    }
}

$data = ['task_id' => $task_id];
header('Content-Type: application/json');
echo json_encode($data);
?>
