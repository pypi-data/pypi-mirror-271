# chinese-address-generator (中国地址随机生成器)
## 数据集
数据来源：国家统计局——`2023年度全国统计用区划代码和城乡划分代码`的权威数据。  
Link: ***https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html***

## 使用方法
### 通过pip安装
```bash
pip install chinese-address-generator
```
### Command Line中使用
```bash
$ cnaddrgen -h
usage: cnaddrgen [-h] --level {1,2,3,4} --num NUM [--version]

Chinese address generator

options:
  -h, --help            show this help message and exit
  --level {1,2,3,4}, -l {1,2,3,4}
                        Level of address
  --num NUM, -n NUM     Number of addresses to generate.
  --version, -v         Version of chinese-address-generator
```
#### 示例
```bash
$ cnaddrgen -l 4 -n 4            
西藏自治区拉萨市西藏文化旅游创意园区西藏文化旅游创意园区 540173
安徽省合肥市合肥新站高新技术产业开发区三十头街道 340178
重庆市璧山区河边镇 500120
广西壮族自治区南宁市江南区那洪街道 450105
```

### Project中使用
#### 导入生成器
```python
from chinese_address_generator import generator
```
#### 生成一级地址：[省、自治区、直辖市]
```python
generator.generatelevel1() #返回一级地址字符串

$ 天津市 120000
```
#### 生成二级地址：[省、自治区、直辖市]-[市、地区]
```python
generator.generatelevel2() #返回二级地址字符串

$ 江苏省南京市 320100
```
#### 生成三级地址：[省、自治区、直辖市]-[市、地区]-[区、县]
```python
generator.generatelevel3() #返回三级地址字符串

$ 陕西省西安市阎良区 610114
```
#### 生成四级地址：[省、自治区、直辖市]-[市、地区]-[区、县]-[乡、镇、街道]
```python
generator.generatelevel4() #返回四级地址字符串

$ 江西省南昌市红谷滩区龙兴街道 360113
```
## 补充说明
### 查看原始数据
```bash
import chinese_address_generator
chinese_address_generator.level3_list #三级地址原始文件
chinese_address_generator.level4_list #四级地址原始文件
```
