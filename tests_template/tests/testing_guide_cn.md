# 测试框架指南

简洁的三层 TDD 工作流：**Examples → Integrations → Unittests**

## TDD 开发流程

### 步骤 1: 编写示例（可执行演示）
在 `examples/` 中创建可运行的代码来演示功能。

### 步骤 2: 集成测试（验证输出）
编写集成测试来验证示例输出是否符合预期。

### 步骤 3: 单元测试（边界情况）
提取并测试单个函数的边界条件。

---

## 命名规范

### 文件名
- 示例文件：`example_{feature}.py`
- 函数名：`{feature}_main()`
- 输入模板：`data_input/example_{feature}.json.template`
- 本地输入：`data_input_local/example_{feature}.json`
- 输出文件：`data_output/example_{feature}_{timestamp}.json`

### 测试数据
- 模板使用 `.json.template` 后缀（git 跟踪，空值）
- 本地文件使用 `.json`（git 忽略，实际值）
- 所有 JSON 使用 2 空格缩进
- 保持数据最小化和聚焦
- 模板中不含敏感数据

---

## 目录结构

```
tests/
├── data_input/              # Git 跟踪的标准输入
│   └── {module}.json        # 输入模板（使用 .template 后缀）
├── data_input_local/        # 你的本地输入覆盖（不跟踪）
│   └── {module}.json        # 你修改的输入
├── data_output/             # 自动生成的输出（不跟踪）
│   └── {module}_{timestamp}.json
├── examples/                # 可运行的演示
├── integrations/            # 集成测试
├── unittests/               # 单元测试
└── test_tools.py            # 共享工具
```

---

## 示例模板

`examples/example_feature.py` 的最小结构：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.test_tools import load, save


def feature_main():
    input_data = load()
    
    # Step 1: Process data
    result = process(input_data)
    
    # Step 2: Generate output
    output_data = {"result": result}
    
    save(output_data)


if __name__ == "__main__":
    feature_main()
```

### 输入模板

创建 `data_input/example_feature.json.template`：

```json
{
  "param1": "",
  "param2": ""
}
```

### 关键点
- **函数名匹配模块名** - `example_feature.py` → `feature_main()`
- **不需要 docstring** - 代码本身说明一切
- **使用 `load()` 和 `save()`** - 自动处理路径
- **步骤注释** - 标记逻辑部分
- **无日志** - 保持示例简单快速

---

## 测试工具 (`test_tools.py`)

### 基本函数

**`load(filename="data.json", input_data_path=None)`**
- 按优先级搜索：
  1. `data_input_local/{module}.json` （你的覆盖）
  2. `data_input/{module}.json` （标准）
  3. `--input-data` CLI 参数（JSON 字符串）

**`save(data, filename=None, save_data_path=None)`**
- 自动生成路径：`data_output/{module}_{timestamp}.json`
- 如果提供 `--output` CLI 参数则使用，否则使用模块名

### 路径优先级

```
加载优先级：
  data_input_local/{module}.json  ← 你的修改（覆盖所有）
        ↓
  data_input/{module}.json        ← 标准输入（git 跟踪）
        ↓
  --input-data                    ← CLI JSON 字符串（回退）

保存位置：
  data_output/{module}_{timestamp}.json  ← 自动生成带时间戳
```

### CLI 参数

```bash
# 使用 JSON 字符串输入
python tests/examples/example_feature.py --input-data '{"key": "value"}'

# 自定义输出文件名
python tests/examples/example_feature.py --output my_result

# 组合使用
python tests/examples/example_feature.py --input-data '{"test": 1}' --output result
```

### 设置工作流

```bash
# 1. 复制模板到本地
cp tests/data_input/example_feature.json.template tests/data_input_local/example_feature.json

# 2. 编辑本地文件填入实际值
# vim/nano/editor tests/data_input_local/example_feature.json

# 3. 运行示例
python tests/examples/example_feature.py

# 4. 检查输出
ls tests/data_output/
```

---

## 集成测试与单元测试

### 集成测试
验证示例产生预期的输出。使用 `pytest` 运行示例并比较结果。

```python
# tests/integrations/test_example_feature.py
def test_feature_output():
    # 运行示例并验证输出结构
    pass
```

### 单元测试
测试带有边界情况的单个函数。

```python
# tests/unittests/test_feature.py
def test_function_edge_case():
    # 测试边界条件
    pass
```

保持测试简单且聚焦。

---

## 核心原则

1. **KISS** - 简单代码胜过聪明代码
2. **Let it fail** - 不要过度验证，让自然错误显现
3. **Modularity** - 小函数，清晰目的
4. **Determinism** - 通过种子/模拟实现可重现结果
