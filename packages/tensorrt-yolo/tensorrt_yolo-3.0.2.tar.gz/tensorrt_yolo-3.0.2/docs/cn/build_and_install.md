[English](../en/build_and_install.md) | 简体中文

# 快速编译安装

## 安装 `tensorrt_yolo`

通过 PyPI 安装 `tensorrt_yolo` 模块，您只需执行以下命令即可：

```bash
pip install -U tensorrt_yolo
```

如果您希望获取最新的开发版本或者为项目做出贡献，可以按照以下步骤从 GitHub 克隆代码库并安装：

```bash
git clone https://github.com/laugh12321/TensorRT-YOLO  # 克隆代码库
cd TensorRT-YOLO
pip install --upgrade build
python -m build
pip install dist/tensorrt_yolo/tensorrt_yolo-3.*-py3-none-any.whl
```

在以上步骤中，您可以先克隆代码库并进行本地构建，然后再使用 `pip` 安装生成的 Wheel 包，确保安装的是最新版本并具有最新的功能和改进。

## `Deploy` 编译

### 环境要求

- Linux: gcc/g++
- Windows: MSVC
- Xmake
- CUDA
- TensorRT

为了满足部署需求，您可以使用 Xmake 进行 `Deploy` 编译。此过程支持动态库和静态库的编译：

```bash
git clone https://github.com/laugh12321/TensorRT-YOLO
cd TensorRT-YOLO
xmake f -k shared --tensorrt="C:/Program Files/NVIDIA GPU Computing Toolkit/TensorRT/v8.6.1.6"
# xmake f -k static --tensorrt="C:/Program Files/NVIDIA GPU Computing Toolkit/TensorRT/v8.6.1.6"
xmake -P . -r
```

在这个过程中，您可以使用 xmake 工具根据您的部署需求选择动态库或者静态库的编译方式，并且可以指定 TensorRT 的安装路径以确保编译过程中正确链接 TensorRT 库。Xmake 会自动识别 CUDA 的安装路径，如果您有多个版本的 CUDA，可以使用 `--cuda` 进行指定。编译后的文件将位于 `lib` 文件夹下。