# 상위 디렉토리 참조 오류
```bash
python main_dir/main.py
  File "main_dir/main.py", line 1, in <module>
    from subdir1 import module1
ModuleNotFoundError: No module named 'subdir1'
```

# PYTHONPATH 로 최상위 디렉토리 지정

## 리눅스 기준
```bash
cd /path/to/your/project
export PYTHONPATH=$(pwd)
python main_dir/main.py
```

### 쉘 스크립트 만들기
```bash
#!/bin/bash
export PYTHONPATH=$(pwd)
python main_dir/main.py
```

```bash
chmod +x run.sh
./run.sh
```

## 윈도우 기준
```bash
(py38_64_flask) project_root> set PYTHONPATH=%cd%

(py38_64_flask) project_root> python main_dir/main.py
Greetings from module1!
Hello from module2!
```
### 자동 배치파일 만들기
```bash
@echo off
set PYTHONPATH=%cd%
python main_dir\main.py
```

```bash
run.bat
```
