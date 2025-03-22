# astrbot_plugin_push_lite

> [!caution]
> token切勿泄漏，如已泄漏请尽快修改。持有token者可令Bot发送任意文本消息。

Astrbot轻量级推送插件，提供api服务。

## 调用方法

> [!note]
> 目标会话标识可用/sid查看

### **1. 发送消息**  
**Endpoint:**  
`POST /send`  

**Headers:**  
- `Authorization: Bearer <API_TOKEN>`  

**Request Body (JSON):**  
```json
{
  "content": "消息内容",
  "umo": "目标会话标识",
  "callback_url": "可选，处理结果回调URL"
}
```

**Response:**  
```json
{
  "status": "queued",
  "message_id": "生成的消息ID",
  "queue_size": 1
}
```

---

### **2. 健康检查**  
**Endpoint:**  
`GET /health`  

**Response:**  
```json
{
  "status": "ok",
  "queue_size": 1
}
```  

---

### **3. 回调通知格式（如果提供 `callback_url`）**  
**Method:** `POST`  

**Request Body (JSON):**  
```json
{
  "message_id": "原始消息ID",
  "success": true,
  "error": "可选，错误信息（仅在失败时返回）"
}
```

**成功示例:**  
```json
{
  "message_id": "123e4567-e89b-12d3-a456-426614174000",
  "success": true
}
```

**失败示例:**  
```json
{
  "message_id": "123e4567-e89b-12d3-a456-426614174000",
  "success": false,
  "error": "错误信息"
}
```

---

### **错误码**  
- **400**: 请求格式错误或缺少必要字段  
- **403**: API 令牌无效  
- **500**: 服务器内部错误