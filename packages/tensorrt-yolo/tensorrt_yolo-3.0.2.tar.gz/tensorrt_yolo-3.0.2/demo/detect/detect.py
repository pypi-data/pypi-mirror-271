#!/usr/bin/env python
# ==============================================================================
# Copyright (c) 2024 laugh12321 Authors. All Rights Reserved.
#
# Licensed under the GNU General Public License v3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# File    :   detect.py
# Version :   4.0
# Author  :   laugh12321
# Contact :   laugh12321@vip.qq.com
# Date    :   2024/01/29 15:13:41
# Desc    :   YOLO Series Inference Script.
# ==============================================================================
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import rich_click as click
from loguru import logger
from rich.progress import track

from tensorrt_yolo.infer import TRTYOLO, ImageBatcher, generate_labels_with_colors, visualize_detections


@click.command("YOLO Series Inference Script.")
@click.option('-e', '--engine', required=True, type=str, help='The serialized TensorRT engine.')
@click.option('-i', '--input', required=True, type=str, help="Path to the image or directory to process.")
@click.option('-o', '--output', type=str, default=None, help='Directory where to save the visualization results.')
@click.option("-l", "--labels", default="./labels.txt", help="File to use for reading the class labels from, default: ./labels.txt")
def main(engine, input, output, labels):
    """
    YOLO Series Inference Script.
    """
    labels = generate_labels_with_colors(labels)
    model = TRTYOLO(engine)
    model.warmup()

    total_time = 0.0
    total_infers = 0
    total_images = 0
    logger.info(f"Infering data in {input}")
    batcher = ImageBatcher(input_path=input, batch_size=model.batch_size, imgsz=model.imgsz, dtype=model.dtype, dynamic=model.dynamic)

    for batch, images, batch_shape in track(batcher, description="[cyan]Processing batches", total=len(batcher.batches)):
        start_time_ns = time.perf_counter_ns()
        detections = model.infer(batch, batch_shape)
        end_time_ns = time.perf_counter_ns()
        elapsed_time_ms = (end_time_ns - start_time_ns) / 1e6
        total_time += elapsed_time_ms
        total_images += len(images)
        total_infers += 1
        if output:
            output_dir = Path(output)
            output_dir.mkdir(parents=True, exist_ok=True)
            with ThreadPoolExecutor() as executor:
                args_list = [(str(image), str(output_dir / image.name), detections[i], labels) for i, image in enumerate(images)]
                executor.map(visualize_detections, *zip(*args_list))

    average_latency = total_time / total_infers
    average_throughput = total_images / (total_time / 1000)
    logger.success(
        "Benchmark results include time for H2D and D2H memory copies\n"
        f"    CPU Average Latency: {average_latency:.3f} ms\n"
        f"    CPU Average Throughput: {average_throughput:.1f} ips\n"
        "    Finished Inference."
    )


if __name__ == '__main__':
    main()
