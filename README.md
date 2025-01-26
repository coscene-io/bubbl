
### 基于PlaywRight的界面录制与回放测试框架

```
Bubbl/
├── tests/                # 测试代码主目录
│   ├── testcases/        # 存放测试用例的目录
│   │   └── test_example.py  # 示例测试用例
│   ├── fixtures/         # 自定义 fixture 目录
│   │   └── browser.py    # 浏览器 fixture 定义
│   ├── pages/            # 页面对象模型（POM）目录
│   │   └── example_page.py # 示例页面类
│   └── conftest.py       # pytest 全局配置和 fixture
├── data/                 # 公共数据和测试资源目录
│   ├── common_data/      # 存放公共数据，如配置文件、数据库连接信息等
│   ├── test_data/        # 存放测试数据，如测试用的CSV文件、JSON数据等
│   └── images/           # 存放测试过程中使用的图片或截图
├── logs/                 # 日志文件目录
│   └── test_logs/        # 存放测试运行时的日志文件
├── reports/              # 报告生成和存放目录
│   ├── allure_report/    # Allure 测试报告生成目录
│   └── test_reports/     # 其他测试报告存放目录
├── utils/                # 辅助函数和工具类目录
│   └── helpers.py        # 辅助函数定义
├── playwright_config/    # Playwright 相关配置目录
│   └── ...               # Playwright 配置文件
├── pytest.ini            # pytest 配置文件
├── requirements.txt      # 项目依赖列表
├── .gitignore            # Git 忽略文件
├── README.md             # 项目说明文件
└── run_tests.sh          # 运行测试的脚本
```
