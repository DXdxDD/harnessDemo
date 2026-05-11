# Harness Programming Demo

这是一份从 0 搭建的 harness 编程入门 demo。它展示一个 harness 如何把“被测对象、测试数据、执行流程、断言、报告”组织起来。

## 这个 demo 里有什么

- `src/price_engine.py`：被测业务代码，一个简单的订单价格计算器。
- `cases/price_cases.json`：数据驱动测试用例。
- `harness/runner.py`：harness 执行器，负责读取用例、运行、收集结果。
- `harness/assertions.py`：断言工具。
- `harness/report.py`：控制台和 JSON 报告。
- `run_demo.py`：一键运行入口。

## 运行

```powershell
python run_demo.py
```

运行后会看到每个用例的通过/失败状态，并在 `reports/result.json` 生成结构化报告。

## 什么是 harness

在编程里，harness 通常指一套“把目标程序跑起来并验证结果”的支撑系统。它本身不是业务逻辑，而是围绕业务逻辑做这些事：

1. 准备输入数据。
2. 调用被测对象。
3. 捕获输出、异常、耗时等信息。
4. 判断结果是否符合预期。
5. 汇总成报告，方便人或 CI 系统阅读。

## 学习路径

1. 先读 `src/price_engine.py`，理解被测对象。
2. 再读 `cases/price_cases.json`，看用例如何描述输入和预期。
3. 然后读 `harness/runner.py`，看 harness 如何把两者连接起来。
4. 修改一个 case 的 `expected.total`，观察失败报告。
5. 新增一个折扣规则，再新增对应 case。

## 可以继续扩展的方向

- 增加更多断言类型，比如近似相等、包含、正则匹配。
- 支持 YAML/CSV 用例格式。
- 接入 `pytest` 或 CI。
- 把 `src/price_engine.py` 换成 HTTP API、数据库任务、模型输出或硬件设备接口。
