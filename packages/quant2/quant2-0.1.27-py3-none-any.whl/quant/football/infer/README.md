# Infer

## P-C-R

预测成功率`p`与赔率`c`和收益率`r`关系：

```python
p, c, r = 0.6, 1.7, 1.1

# p * c - (1 - p) * 1 >= r
# p * (c + 1) >= r + 1
# c >= (r + 1) / p - 1

c >= (r + 1) / p - 1
```

关系表`r=1.1`：

```python
for i in range(2, 10):
    p = i / 10
    c = 2.1 / p -1
    print(f"{p=:.2f}, {c=:.2f}")
# p=0.20, c=9.50
# p=0.30, c=6.00
# p=0.40, c=4.25
# p=0.50, c=3.20
# p=0.60, c=2.50
# p=0.70, c=2.00
# p=0.80, c=1.62
# p=0.90, c=1.33
```

## `infer.json`

- `bet_n_ins`: `['total', 'total_asian', ...]`
- `bet_cp_ins`: `{0: '全场', 1: '上半场', 2: '下半场'}`

```json
{
  "table": "table20240420",
  "filters": [
    {
      "name": "time_range",
      "value": [21, 45]
    }
  ],
  "preprocess": "preprocess.json",
  "model": "model.json",
  "postprocess": {
    "bet_n_ins": ["total", "total_asian"],
    "bet_cp_ins": [1],
    "ret_thr": 0.0,
    "ret_conf_thr": 0.7
  }
}
```
