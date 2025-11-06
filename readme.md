### Main Function
1、Auth模块，讲解用户登录、会话保持、退出登录功能，只有登录到系统的用户，才能在后台管理知识库。

2、知识库模块，讲解知识库管理、文档管理、分段管理功能，详细拆解通过网页上传文档，添加片段等功能。

3、文本向量化，讲解用异步的方式，将文档拆分成片段，然后向量化，再存储到Milvus向量数据库的全过程。

4、知识库问答，讲解基于用户选择的知识库，进行文档片段召回，让大模型做更有针对性的回答。

5、对话历史管理，讲解历史对话信息的增删改查，巩固前面学习的前后端交互功能。

### Architecture
project
├── app.py                       # 应用程序入口
├── apps
│   └── demo                     # demo 模块
│       ├── __init__.py          # demo 应用初始化，蓝图设置
│       └── views.py             # demo 应用视图函数
├── commands
│   ├── __init__.py              # 自定义命令初始化
│   └── hello.py                 # 示例自定义命令
├── config.py                    # 配置文件
├── extensions
│   ├── ext_celery.py            # Celery 集成
│   ├── ext_database.py          # 数据库设置和集成
│   ├── ext_logger.py            # 日志配置
│   ├── ext_migrate.py           # 数据库迁移设置
│   ├── ext_milvus.py            # Milvus 集成
│   ├── ext_redis.py             # Redis 配置
│   └── ext_template_filter.py   # 自定义 Jinja 模板过滤器
├── helper.py                    # 辅助函数
├── readme.txt                   # 项目文档
├── requirements.txt             # Python 依赖
├── static                       # 静态文件 (CSS, JS, 图像)
├── storage
│   ├── files                    # 上传的文件
│   └── logs
│       └── app-20240801.log     # 应用日志文件
└── tasks
    └── demo_task.py             # 示例后台任务