# python-dsa

Python 实现的数据结构与核心算法，附带 LeetCode 经典题解。

## 项目结构

```
python-dsa/
├── src/dsa/
│   ├── data_structures/    # 数据结构实现
│   │   ├── linked_list.py  # 链表（单向、双向、循环）
│   │   ├── stack.py        # 栈
│   │   ├── queue.py        # 队列（普通、双端、优先）
│   │   ├── hash_table.py   # 哈希表
│   │   ├── tree.py         # 二叉树、BST、AVL
│   │   └── graph.py        # 图（邻接表/矩阵、DFS/BFS）
│   ├── algorithms/         # 算法实现
│   │   ├── sorting.py      # 排序算法
│   │   ├── searching.py    # 搜索算法
│   │   ├── dynamic_programming.py  # 动态规划
│   │   └── greedy.py       # 贪心算法
│   └── leetcode/           # LeetCode 题解
│       └── ...
├── tests/                  # 单元测试
├── requirements.txt
├── setup.py
└── README.md
```

## 数据结构

| 模块 | 内容 |
|------|------|
| 链表 | 单向链表、双向链表、循环链表 |
| 栈 & 队列 | 基础栈、双端队列、优先级队列 |
| 哈希表 | 开放寻址、链地址法 |
| 树 | 二叉树、BST、AVL 平衡树 |
| 图 | 有向/无向图、DFS/BFS、最短路径 |

## 算法

| 模块 | 内容 |
|------|------|
| 排序 | 冒泡、选择、插入、归并、快速、堆排序、计数排序 |
| 搜索 | 二分查找、DFS/BFS 搜索 |
| 动态规划 | 背包问题、最长公共子序列、编辑距离 |
| 贪心 | 活动选择、Huffman 编码 |

## 安装

```bash
pip install -e .
```

## 运行测试

```bash
python -m pytest tests/ -v
```
