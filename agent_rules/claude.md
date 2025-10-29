# Claude 编程规范

## 核心原则

### 最高优先级原则
1. 可读性优先：生成的代码需要简单易读，初学者也能理解，复杂优化留给人类
2. 模块独立性：保持各模块独立功能，逻辑简单清晰
3. 契约式设计：设计函数时，明确输入输出契约，通过合理的放缩范围避免处理的职责过大

### 核心设计原则
1. KISS (Keep It Simple, Stupid) - 最优先的原则，代码要简单易懂并且易于维护，像Linus Torvalds一样
2. Let it fail - 让它失败，不要过度添加异常代码，异常处理留给调用者或者更高层
3. DRY (Don't Repeat Yourself) - 避免重复代码
4. YAGNI (You Ain't Gonna Need It) - 不要实现不需要的功能
5. POLA (Principle of Least Astonishment) - 最小惊讶原则
6. LoD (Law of Demeter) - 最少知识原则
7. SoC (Separation of Concerns) - 关注点分离原则
8. High Cohesion, Loose Coupling - 高内聚，低耦合

### 开发原则
- 最小化测试：除非明确要求，否则不创建测试文件
- 函数优先：默认使用函数实现逻辑，避免不必要的类设计
- 分层实现：简单函数构建基础模块，复杂函数构建业务模块
- 依赖管理：函数按依赖关系排序，最小依赖在前，整合功能在后
TODO

### 实现原则
1. 最小代码量：用最少的代码实现需求，不加冗余代码
2. 自然约束：利用程序本身的约束实现验证，而非额外验证逻辑
3. 简洁优雅：一行能实现的不写多行，避免复杂验证代码

示例：接收 URL 的函数不需要验证输入是否为整数类型

## 代码规范

### 模块结构
大部分 Python 模块遵循以下结构：

```python
# 0. 模块级注释 - 模块简要说明 (可使用 Sphinx 格式)
"""
Module description

Example:
    >>>"Example code"
    
"""

# 1. Import 部分 - 所有外部依赖
import os
import sys
from typing import List, Dict

# 2. 模块级配置
_INNER_VARIABLE = "inner_variable"
COMMON_CONFIG = {
    'debug': False
}

# 3. 函数实现 - 按依赖关系排序，最小单元在前
def helper_function():
    """Helper function description"""
    pass

def main_function():
    """Main function using helper"""
    pass

# 4. 可选的入口代码 - 简洁的测试和运行入口
if __name__ == '__main__':
    main_function()
```

### 命名规范
#### 变量命名
- 格式：使用 snake_case 格式
- 字典取值：直接使用键名命名变量

```python
# 正确
item_data = result_dict['item_data']
user_info = user_data['user_info']

# 错误
data = result_dict['item_data']
info = user_data['user_info']
```

#### 重复命名处理
出现命名冲突时，使用下划线和后缀区分：

```python
item_info = get_item_info()
item_info_mapper = map_item_info(item_info)
item_info_mapper_iter = iter(item_info_mapper)
item_info_mapper_iter_copy = list(item_info_mapper_iter)
```

### 函数设计
#### 单一职责原则
函数应该只做一件事，避免在函数中进行无关的数据处理操作。

错误示例：
```python
external_data_info = get_data()

def func(data_info):
    user_info = [item.get('user_info') for item in data_info]
    # do something with user_info

func(external_data_info)
```

正确示例：
```python
external_data_info = get_data()

def func(user_info):
    # do something with user_info

func([item.get('user_info') for item in external_data_info])
```

## 文档规范

### 注释规则
- 语言：使用英文注释，代码按逻辑流程用空格分割
- 模块文档：符合 Sphinx 规范，包含服务介绍和示例（高度封装模块需要）
- 函数文档：简单介绍参数和返回值，缺失则留空

模块文档示例：
```python
"""
Module for data processing utilities.

This module provides common functions for data transformation and validation.

Example:
    >>> from data_processor import process_data
    >>> result = process_data(raw_data)
    >>> print(result)
"""
```

函数文档示例：
```python
def process_data(data: Dict) -> List:
    """Process raw data and return cleaned list."""
    # implementation
    pass
```

## 工作流程

### 协作规范
1. 代码可读性：避免过长复杂的代码，保持简洁明了
2. 注释语言：英文注释代码，中文回复消息
3. 平台差异：程序运行在 Linux，开发在 Windows 平台

### 质量保证
- 可读性检查：确保代码对初学者友好
- 逻辑简洁性：保持代码逻辑简单直接
- 模块独立性：确保各模块功能独立，耦合度低

---

说明：本规范按优先级排序，从核心原则到具体实现细节，确保代码质量和开发效率。所有规则都为项目服务，可根据实际情况灵活调整。
