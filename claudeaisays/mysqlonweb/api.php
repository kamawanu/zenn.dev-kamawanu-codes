<?php
header('Content-Type: application/json; charset=utf-8');

// エラーハンドリング
function sendError($code, $message) {
    http_response_code($code);
    echo json_encode(['error' => $message]);
    exit;
}

// 成功レスポンス
function sendSuccess($data = null) {
    if ($data !== null) {
        echo json_encode($data);
    } else {
        echo json_encode(['success' => true]);
    }
}

// PATH_INFOを解析
$pathInfo = isset($_SERVER['PATH_INFO']) ? $_SERVER['PATH_INFO'] : '';
$pathParts = array_filter(explode('/', $pathInfo));
$pathParts = array_values($pathParts); // インデックスを振り直し

if (count($pathParts) < 2) {
    sendError(400, 'Invalid path. Expected format: /database/table[/id]');
}

$database = $pathParts[0];
$table = $pathParts[1];
$id = isset($pathParts[2]) ? $pathParts[2] : null;

// db.iniから設定を読み込み
$config = parse_ini_file('db.ini', true);
if (!$config || !isset($config[$database])) {
    sendError(404, "Database configuration for '$database' not found");
}

$dbConfig = $config[$database];

// 必要な設定項目をチェック
$requiredKeys = ['host', 'username', 'password', 'dbname'];
foreach ($requiredKeys as $key) {
    if (!isset($dbConfig[$key])) {
        sendError(500, "Missing database configuration: $key");
    }
}

// MySQLに接続
try {
    $dsn = "mysql:host={$dbConfig['host']};dbname={$dbConfig['dbname']};charset=utf8mb4";
    $pdo = new PDO($dsn, $dbConfig['username'], $dbConfig['password']);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    sendError(500, 'Database connection failed');
}

// リクエストメソッドを取得
$method = $_SERVER['REQUEST_METHOD'];

// リクエストボディを取得（POST/PUT用）
$input = null;
if ($method === 'POST' || $method === 'PUT') {
    $rawInput = file_get_contents('php://input');
    if (!empty($rawInput)) {
        $input = json_decode($rawInput, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            sendError(400, 'Invalid JSON in request body');
        }
    }
}

try {
    switch ($method) {
        case 'GET':
            if ($id === null) {
                // 全件取得
                $stmt = $pdo->prepare("SELECT * FROM `$table`");
                $stmt->execute();
                $results = $stmt->fetchAll();
                sendSuccess($results);
            } else {
                // 1件取得
                $stmt = $pdo->prepare("SELECT * FROM `$table` WHERE id = ?");
                $stmt->execute([$id]);
                $result = $stmt->fetch();
                if ($result === false) {
                    sendError(404, 'Record not found');
                }
                sendSuccess($result);
            }
            break;

        case 'POST':
            if ($id !== null) {
                sendError(400, 'POST should not include ID in path');
            }
            if (empty($input)) {
                sendError(400, 'Request body required for POST');
            }

            // INSERT文を構築
            $columns = array_keys($input);
            $placeholders = array_fill(0, count($columns), '?');
            $sql = "INSERT INTO `$table` (`" . implode('`, `', $columns) . "`) VALUES (" . implode(', ', $placeholders) . ")";
            
            $stmt = $pdo->prepare($sql);
            $stmt->execute(array_values($input));
            
            $insertId = $pdo->lastInsertId();
            sendSuccess(['id' => $insertId, 'affected_rows' => $stmt->rowCount()]);
            break;

        case 'PUT':
            if ($id === null) {
                sendError(400, 'PUT requires ID in path');
            }
            if (empty($input)) {
                sendError(400, 'Request body required for PUT');
            }

            // UPDATE文を構築
            $columns = array_keys($input);
            $setParts = array_map(function($col) { return "`$col` = ?"; }, $columns);
            $sql = "UPDATE `$table` SET " . implode(', ', $setParts) . " WHERE id = ?";
            
            $values = array_values($input);
            $values[] = $id; // WHERE条件用のIDを追加
            
            $stmt = $pdo->prepare($sql);
            $stmt->execute($values);
            
            if ($stmt->rowCount() === 0) {
                sendError(404, 'Record not found or no changes made');
            }
            sendSuccess(['affected_rows' => $stmt->rowCount()]);
            break;

        case 'DELETE':
            if ($id === null) {
                sendError(400, 'DELETE requires ID in path');
            }

            $stmt = $pdo->prepare("DELETE FROM `$table` WHERE id = ?");
            $stmt->execute([$id]);
            
            if ($stmt->rowCount() === 0) {
                sendError(404, 'Record not found');
            }
            sendSuccess(['affected_rows' => $stmt->rowCount()]);
            break;

        default:
            sendError(405, 'Method not allowed');
    }

} catch (PDOException $e) {
    // SQLエラーをログに記録（本番環境では詳細を隠す）
    error_log("MySQL Error: " . $e->getMessage());
    sendError(500, 'Database operation failed');
}