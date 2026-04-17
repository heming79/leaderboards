# AI Provider Leaderboards

一个复刻 [Artificial Analysis](https://artificialanalysis.ai/leaderboards/providers) 的AI模型提供商排行榜网站，用于比较不同AI模型提供商的性能、价格和速度。

## 功能特性

- 📊 **提供商排行榜**：展示AI模型提供商的综合排名
- 📈 **多维度比较**：智能指数、编码能力、代理能力、价格、延迟、吞吐量
- 🔍 **灵活排序**：支持按任意指标升序/降序排序
- 📄 **分页浏览**：支持分页查看大量数据
- 🔄 **数据刷新**：一键刷新最新数据
- 🗄️ **SQLite存储**：轻量级本地数据库存储
- 🕷️ **数据爬取**：支持从目标网站爬取最新数据
- ✅ **自动化测试**：完整的测试套件确保代码质量

## 技术栈

### 后端
- **Python 3.8+**：核心编程语言
- **Flask 3.0+**：轻量级Web框架
- **Flask-SQLAlchemy**：ORM数据库操作
- **SQLite**：本地数据库存储

### 前端
- **HTML5**：页面结构
- **CSS3**：样式设计
- **JavaScript (ES6+)**：交互逻辑

### 工具
- **Requests**：HTTP请求库
- **BeautifulSoup4**：HTML解析库
- **pytest**：测试框架
- **pytest-flask**：Flask测试扩展

## 项目结构

```
leaderboards/
├── app/                          # 应用主目录
│   ├── __init__.py              # 应用初始化
│   ├── models/                   # 数据模型
│   │   ├── __init__.py
│   │   └── provider.py          # 提供商模型
│   ├── routes/                   # 路由定义
│   │   ├── __init__.py
│   │   ├── main.py              # 主页面路由
│   │   └── api.py               # RESTful API路由
│   ├── static/                   # 静态文件
│   │   ├── css/
│   │   │   └── style.css        # 样式文件
│   │   └── js/
│   │       └── main.js          # 前端交互逻辑
│   ├── templates/                # HTML模板
│   │   └── index.html           # 主页面模板
│   └── utils/                    # 工具模块
│       ├── __init__.py
│       ├── database.py          # 数据库操作工具
│       └── scraper.py           # 数据爬取工具
├── data/                         # 数据目录
├── tests/                        # 测试目录
│   ├── __init__.py
│   ├── conftest.py              # 测试配置
│   ├── test_api.py              # API测试
│   ├── test_models.py           # 模型测试
│   └── test_database.py         # 数据库测试
├── config.py                     # 配置文件
├── requirements.txt              # 依赖列表
├── run.py                        # 应用入口
└── README.md                     # 项目文档
```

## 安装说明

### 环境要求
- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd leaderboards
   ```

2. **创建虚拟环境（推荐）**
   ```bash
   python -m venv venv
   ```

3. **激活虚拟环境**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/macOS:
     ```bash
     source venv/bin/activate
     ```

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

5. **初始化数据库**
   ```bash
   python -c "from app.utils.database import init_db, add_sample_data; init_db(); add_sample_data()"
   ```

## 使用方法

### 启动应用

```bash
python run.py
```

应用将在 `http://localhost:5000` 启动。

### 访问界面

打开浏览器访问：`http://localhost:5000`

### 数据爬取

如果需要从目标网站爬取最新数据：

```bash
python -c "from app.utils.scraper import scrape_and_save; scrape_and_save()"
```

**注意**：由于目标网站可能有反爬机制，如果爬取失败，系统会自动使用预设的示例数据。

## API 文档

### 基础URL
`http://localhost:5000/api`

### 端点列表

#### 1. 获取提供商列表
```
GET /providers
```

**查询参数**：
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| per_page | int | 20 | 每页数量 |
| sort_by | string | intelligence_index | 排序字段 |
| sort_order | string | desc | 排序方向 (asc/desc) |

**排序字段可选值**：
- `intelligence_index` - 智能指数
- `coding_index` - 编码指数
- `agentic_index` - 代理指数
- `price_per_1k_input` - 输入价格
- `price_per_1k_output` - 输出价格
- `latency_ms` - 延迟
- `throughput_tokens_per_sec` - 吞吐量

**响应示例**：
```json
{
  "providers": [
    {
      "id": 1,
      "name": "Anthropic",
      "intelligence_index": 95.2,
      "coding_index": 92.8,
      "agentic_index": 94.1,
      "price_per_1k_input": 0.008,
      "price_per_1k_output": 0.024,
      "latency_ms": 120.5,
      "throughput_tokens_per_sec": 45.2,
      "models_count": 5,
      "last_updated": "2024-01-01T00:00:00"
    }
  ],
  "total": 5,
  "pages": 1,
  "current_page": 1,
  "per_page": 20
}
```

#### 2. 获取单个提供商
```
GET /providers/<provider_id>
```

**响应示例**：
```json
{
  "id": 1,
  "name": "Anthropic",
  "intelligence_index": 95.2,
  "coding_index": 92.8,
  "agentic_index": 94.1,
  "price_per_1k_input": 0.008,
  "price_per_1k_output": 0.024,
  "latency_ms": 120.5,
  "throughput_tokens_per_sec": 45.2,
  "models_count": 5,
  "last_updated": "2024-01-01T00:00:00"
}
```

#### 3. 创建提供商
```
POST /providers
```

**请求体**：
```json
{
  "name": "NewProvider",
  "intelligence_index": 90.0,
  "coding_index": 85.0,
  "agentic_index": 88.0,
  "price_per_1k_input": 0.005,
  "price_per_1k_output": 0.015,
  "latency_ms": 100.0,
  "throughput_tokens_per_sec": 40.0,
  "models_count": 3
}
```

**响应**：201 Created，返回创建的提供商数据

#### 4. 更新提供商
```
PUT /providers/<provider_id>
```

**请求体**：
```json
{
  "intelligence_index": 95.0,
  "coding_index": 92.0
}
```

**响应**：200 OK，返回更新后的提供商数据

#### 5. 删除提供商
```
DELETE /providers/<provider_id>
```

**响应**：200 OK
```json
{
  "message": "Provider deleted successfully"
}
```

## 数据模型

### Provider 模型

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| name | String(100) | 提供商名称，唯一 |
| intelligence_index | Float | 智能指数 |
| coding_index | Float | 编码指数 |
| agentic_index | Float | 代理指数 |
| price_per_1k_input | Float | 每1000输入token价格 |
| price_per_1k_output | Float | 每1000输出token价格 |
| latency_ms | Float | 延迟（毫秒） |
| throughput_tokens_per_sec | Float | 吞吐量（token/秒） |
| models_count | Integer | 模型数量 |
| last_updated | DateTime | 最后更新时间 |

## 测试

### 运行测试

```bash
pytest
```

### 运行测试并显示详细信息

```bash
pytest -v
```

### 运行测试并生成覆盖率报告

```bash
pytest --cov=app
```

### 测试覆盖范围

- **API测试**：所有RESTful API端点的增删改查操作
- **模型测试**：数据模型的创建、更新、删除、序列化
- **数据库测试**：数据库操作、事务、分页、查询

## 配置说明

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| SECRET_KEY | Flask密钥 | 'leaderboards-secret-key' |
| DATABASE_URL | 数据库连接URL | SQLite本地文件 |

### 配置文件

配置位于 `config.py`，可以根据需要修改：

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'leaderboards-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data', 'leaderboards.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## 开发指南

### 添加新的排序字段

1. 在 `app/models/provider.py` 中添加新字段
2. 在 `app/routes/api.py` 中确保排序逻辑支持新字段
3. 在 `app/static/js/main.js` 中添加排序选项
4. 在 `app/templates/index.html` 中更新下拉菜单

### 扩展API功能

1. 在 `app/routes/api.py` 中添加新的路由
2. 确保遵循RESTful设计原则
3. 添加对应的测试用例

### 自定义样式

修改 `app/static/css/style.css` 文件来自定义界面样式。

## 部署

### 生产环境部署

1. **设置生产环境变量**
   ```bash
   export SECRET_KEY='your-secret-key'
   export DATABASE_URL='your-database-url'
   ```

2. **使用生产级WSGI服务器**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```

3. **使用Nginx反向代理**（推荐）
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## 常见问题

### Q: 为什么爬取数据失败？
A: 目标网站可能有反爬机制。系统会自动使用预设的示例数据。你也可以手动添加数据或修改爬虫逻辑。

### Q: 如何添加更多示例数据？
A: 编辑 `app/utils/database.py` 中的 `sample_providers` 列表，添加更多提供商数据。

### Q: 如何切换到Redis存储？
A: 目前项目使用SQLite。如果需要切换到Redis，可以：
1. 安装 `redis` 和 `flask-redis` 包
2. 修改配置文件添加Redis连接
3. 重写数据访问层使用Redis

### Q: 测试失败怎么办？
A: 确保：
1. 已安装所有依赖
2. Python版本 >= 3.8
3. 没有其他进程占用测试端口

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交GitHub Issue
- 发送邮件

---

**注意**：本项目仅供学习和研究使用。请遵守目标网站的使用条款和robots.txt规则。
