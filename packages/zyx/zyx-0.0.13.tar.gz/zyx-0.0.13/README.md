# Hammad's SupportVectors Curriculum & General Use Repository

**This repo is for internal SupportVectors use and contains multiple scripts, notebooks & resources.**

```bash
git clone https://github.com/supportvectors/hammad_curriculum
cd hammad_curriculum
```

<br>

### Cool Tools

I plan to fill the `./cool_tools` directory just with simple python libraries that i find useful or interesting. 

This repository also contains my simple `'zyx'` library that contains a few quick tools, the source code for the library is also included in the `./src` directory and sample notebooks can be found under `./zyx`. **You can install the zyx library using:**

**Install from PyPi**
```bash
pip install zyx
```

**Install from Source**
```bash
pip install .
```

<br>

### Courses

The course projects are under the `./courses` directory. Each course will be separated by folder and will contain either scripts or notebooks for each of the modules planned on being covered in the course.

<br>

### Docker

The Dockerfile inside the `./docker` directory contains the current draft SupportVectors development environment. To quickly build & run the image, run

```bash
docker build -t svlearn_image ./docker
docker run --gpus all -d -it --name svlearn svlearn_image
docker exec -it svlearn bash
```
