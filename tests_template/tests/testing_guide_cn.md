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

## 目录结构

```
tests/
├── data_input/         # Git 跟踪的标准输入
├── data_input_local/   # 你的本地输入覆盖（不跟踪）
├── data_output/        # 自动生成的输出（不跟踪）
├── examples/           # 可运行的演示
├── integrations/       # 集成测试
├── unittests/          # 单元测试
└── test_tools.py       # 共享工具
```

---

## 示例模板

`examples/01_my_feature.py` 的最小结构：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.test_tools import load, save


def my_feature_main():
    input_data = load()
    
    # Step 1: Process data
    result = process(input_data)
    
    # Step 2: Generate output
    output_data = {"result": result, "status": "ok"}
    
    save(output_data)


if __name__ == "__main__":
    my_feature_main()
```

### 关键点
- **函数名匹配模块名** - `01_my_feature.py` → `my_feature_main()`
- **不需要 docstring** - 代码本身说明一切
- **使用 `load()` 和 `save()`** - 自动处理路径
- **步骤注释** - 标记逻辑部分

---

## 测试工具 (`test_tools.py`)

### 基本函数

**`load(filename="data.json", input_data_path=None)`**
- 按优先级搜索：
  1. `data_input_local/{package}/{module}/{filename}` （你的覆盖）
  2. `data_input/{package}/{module}/{filename}` （标准）
  3. `--input-data` CLI 参数（JSON 字符串）

**`save(data, filename=None, save_data_path=None)`**
- 自动生成路径：`data_output/{package}_{module}_{timestamp}.json`
- 如果提供 `--output` CLI 参数则使用，否则使用模块名

### 路径优先级

```
加载优先级：
  data_input_local/  ← 你的修改（覆盖所有）
        ↓
  data_input/        ← 标准输入（git 跟踪）
        ↓
  --input-data       ← CLI JSON 字符串（回退）

保存位置：
  data_output/       ← 自动生成带时间戳
```

### CLI 参数

```bash
# 使用 JSON 字符串输入
python example.py --input-data '{"key": "value"}'

# 自定义输出文件名
python example.py --output my_result

# 组合使用
python example.py --input-data '{"test": 1}' --output result
```

---

## 集成测试与单元测试

### 集成测试
验证示例产生预期的输出。使用 `pytest` 运行示例并比较结果。

```python
# tests/integrations/test_example_01.py
def test_example_output():
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

保持测试简单且聚焦。详细模式参见代码示例。

---

## 核心原则

1. **KISS** - 简单代码胜过聪明代码
2. **Let it fail** - 不要过度验证，让自然错误显现
3. **Modularity** - 小函数，清晰目的
4. **Determinism** - 通过种子/模拟实现可重现结果
